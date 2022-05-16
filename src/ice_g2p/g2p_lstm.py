"""
    Converts grapheme strings (texts) to phonetic transcriptions using a
    Fairseq transformer model.
"""

import os
from fairseq.models.transformer import TransformerModel

# if word separation is required in transcribed output
# use this separator
WORD_SEP = '-'
ALPHABET = '[aábcðdeéfghiíjklmnoóprstuúvxyýzþæö]'
DICT_PREFIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dictionaries/ice_pron_dict_')


class FairseqG2P:

    def __init__(self, model_path=f'{os.path.dirname(os.path.abspath(__file__))}/fairseq_models/',
                 model_file='model-256-.3-s-s.pt', dialect='standard', alphabet=ALPHABET):
        """
        Initializes a Fairseq lstm g2p model according to model_path
        and model_file. If use_cwd=False, be sure to set model_path to
        an absolute path.
        :param model_path: a relative or an absolute path to the model-dir
        :param model_file: the g2p model file
        :param dialect: the pronunciation variant to use
        :param use_cwd: if set to False, model_path has to be absolute
        """
        self.model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fairseq_models", dialect)
        self.model_file = model_file
        print(self.model_path)
        print(self.model_file)
        self.g2p_model = TransformerModel.from_pretrained(self.model_path, self.model_file)
        self.alphabet = alphabet
        self.pron_dict = self.read_prondict(dialect)
        self.custom_dict = None

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
            transcr = ''
            if use_dict and self.custom_dict:
                transcr = self.custom_dict.get(wrd)
            if use_dict and not transcr:
                transcr = self.pron_dict.get(wrd, '')
            if transcr:
                transcribed_arr.append(transcr)
                continue
            if set(wrd).difference(self.alphabet):
                print(wrd + ' contains non valid character(s) ' + str(set(wrd).difference(self.alphabet)) + ', skipping transcription.')
                continue
            transcribed_arr.append(self.g2p_model.translate(' '.join(wrd)))
        if sep:
            transcribed = WORD_SEP.join(transcribed_arr)
        else:
            transcribed = ' '.join(transcribed_arr)

        return transcribed

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

