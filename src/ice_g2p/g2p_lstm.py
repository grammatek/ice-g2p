"""
    Converts grapheme strings (texts) to phonetic transcriptions using a
    Fairseq transformer model.
"""

import os, sys
from pathlib import Path
from fairseq.models.transformer import TransformerModel

# if word separation is required in transcribed output
# use this separator
WORD_SEP = '-'
ALPHABET = '[aábcðdeéfghiíjklmnoóprstuúvxyýzþæö]'
DICT_PREFIX = 'dictionaries/ice_pron_dict_'


class FairseqG2P:

    def __init__(self, model_path='./fairseq_models/',
                 model_file='model-256-.3-s-s.pt', dialect='standard', packaged=False):
        """
        Initializes a Fairseq lstm g2p model according to model_path
        and model_file. If use_cwd=False, be sure to set model_path to
        an absolute path.
        :param model_path: a relative or an absolute path to the model-dir
        :param model_file: the g2p model file
        :param dialect: the pronunciation variant to use
        :param use_cwd: if set to False, model_path has to be absolute
        """
        if packaged:
            self.model_path = os.path.join(sys.prefix, "models")
        else:
            self.model_path = model_path + dialect
        self.model_file = model_file
        print(self.model_path)
        print(self.model_file)
        self.g2p_model = TransformerModel.from_pretrained(self.model_path, self.model_file)
        self.pron_dict = self.read_prondict(dialect)

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
            if use_dict:
                transcr = self.pron_dict.get(wrd, '')
                if transcr:
                    transcribed_arr.append(transcr)
                    continue
            if set(wrd).difference(ALPHABET):
                print(wrd + ' contains non valid character(s) ' + str(set(wrd).difference(ALPHABET)) + ', skipping transcription.')
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

