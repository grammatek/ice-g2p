"""
    Converts grapheme strings (texts) to phonetic transcriptions using a
    Fairseq transformer model.
"""

import os
import logging
from fairseq.models.transformer import TransformerModel

from ice_g2p import compound_analysis

logging.getLogger('fairseq').setLevel(logging.WARNING)

# if word separation is required in transcribed output
# use this separator
WORD_SEP = '-'
ALPHABET = '[aábcðdeéfghiíjklmnoóprstuúvxyýzþæö]'
ENGLISH_ALPHABET = '[aåäbcdefghijklmnoöpqrstuüvwxyz]'
DICT_PREFIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dictionaries/ice_pron_dict_')


class FairseqG2P:

    def __init__(self, model_file='model-256-.3-s-s.pt', dialect='standard', use_english=False):
        """
        Initializes a Fairseq lstm g2p model according to model_path
        and model_file.
        :param model_file: the g2p model file
        :param dialect: the pronunciation variant to use
        :param use_cwd: if set to False, model_path has to be absolute
        """
        self.model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fairseq_models/ice-g2p-models', dialect)
        self.model_file = model_file
        if use_english:
            model_path_english = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fairseq_models/ice-g2p-models', 'english')
            self.g2p_model = TransformerModel.from_pretrained(model_path_english, self.model_file)
            self.alphabet = ENGLISH_ALPHABET
        else:
            self.g2p_model = TransformerModel.from_pretrained(self.model_path, self.model_file)
            self.alphabet = ALPHABET
        self.pron_dict = self.read_prondict(dialect)
        self.custom_dict = None
        self.automatic_g2p_dict = {}

    def override_pron_dict(self, pron_dict: dict):
        """
        Override the core pronunciation dictionary initialized in init
        :param pron_dict: new pronunciation dictionary
        :return:
        """
        self.pron_dict = pron_dict

    def set_custom_dict(self, custom_dict: dict):
        """
        A custom dictionary will be used additionally to the built in dictionary.
        The custom dictionary, if present, is checked first and thus has priority over the built-in dictionary
        in the cases where the include the same words.
        Be careful when using a custom dictionary that it follows the same dialect as selected for the g2p and
        thus the built-in dictionary.

        :param custom_dict: a dictionary with custom vocabulary and/or transcriptions. Has priority over the
        built-in dicionary
        """
        self.custom_dict = custom_dict

    def transcribe(self, text, use_dict=False, sep=False) -> str:
        """
        Transcribes text according to the initialized transformer model.
        Text can be a single word or longer text.
        :param text: the text to transcribe
        :param sep: if True, inserts a separator between each transcribed word in text
        :return: transcribed version of text as string
        """
        transcribed_arr = []
        for wrd in text.split(' '):
            if not wrd:
                continue
            # start with lookup
            transcr = self.dict_lookup(wrd, use_dict)
            if not transcr:
                # if transcription not yet found, perform automatic g2p
                if set(wrd).difference(self.alphabet):
                    print(text + ' contains non valid character(s) ' + str(
                        set(wrd).difference(self.alphabet)) + ', skipping transcription.')
                    continue
                # use the current g2p model to transcribe the word automatically
                transcr = self.model_transcribe(wrd, use_dict)
                # add to automatic_g2p_dict so that each word only gets transcribed once in batch processing.
                self.automatic_g2p_dict[wrd] = transcr

            # add transcription regardless of origin
            transcribed_arr.append(transcr)

        if sep:
            transcribed = WORD_SEP.join(transcribed_arr)
        else:
            transcribed = ' '.join(transcribed_arr)

        return transcribed

    def dict_lookup(self, wrd, use_dict):
        """ Look up the transcription of wrd in the available dictionaries if use_dict==True and return the
        transcription.
        If use_dict==False or if no transcription is found, return an empty string. """
        if not use_dict:
            return ''
        transcr = self.automatic_g2p_dict.get(wrd)
        if self.custom_dict and not transcr:
            transcr = self.custom_dict.get(wrd)
        if not transcr:
            transcr = self.pron_dict.get(wrd, '')
        return transcr

    def model_transcribe(self, wrd, use_dict):
        """ Transcribe 'wrd', if the compound analysis detects compound parts, transcribe each part
        separately and join the transcripts into one string. Return the transcript of 'wrd'. """
        transcr = ''
        # if wrd is a compound, transcribe each compound part separately
        comp_parts = compound_analysis.get_compound_parts(wrd)
        for i, part in enumerate(comp_parts):
            t = self.dict_lookup(part, use_dict)
            if not t:
                t = self.g2p_model.translate(' '.join(part))
            if i > 0:
                # currently we only transcribe long vowels in the first syllable
                # this is not entirely correct, but as long as the pronunciation dictionary
                # follows this rule, we follow it here as well
                t = t.replace(':', '')
            transcr += t + ' '
        transcr = transcr.strip()
        return transcr

    @staticmethod
    def read_prondict(dialect: str) -> dict:
        dictfile = DICT_PREFIX + dialect + '_clear.csv'
        prondict = {}
        with open(dictfile) as f:
            content = f.read().splitlines()
        for line in content:
            wrd, transcr = line.split('\t')
            prondict[wrd] = transcr

        return prondict

