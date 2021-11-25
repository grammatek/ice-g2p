"""
    Converts grapheme strings (texts) to phonetic transcriptions using a
    Fairseq transformer model.
"""

import os
from pathlib import Path
from fairseq.models.transformer import TransformerModel

# if word separation is required in transcribed output
# use this separator
WORD_SEP = '-'


class FairseqG2P:

    def __init__(self, model_path='/fairseq_models/standard/',
                 model_file='model-256-.3-s-s.pt', use_cwd=True):
        """
        Initializes a Fairseq lstm g2p model according to model_path
        and model_file. If use_cwd=False, be sure to set model_path to
        an absolute path.
        :param model_path: a relative or an absolute path to the model-dir
        :param model_file: the g2p model file
        :param use_cwd: if set to False, model_path has to be absolute
        """
        if use_cwd:
            self.model_path = Path(os.getcwd() + model_path)
        else:
            self.model_path = model_path
        self.model_file = model_file
        self.g2p_model = TransformerModel.from_pretrained(self.model_path, self.model_file)

    def transcribe(self, text, sep=False) -> str:
        """
            Transcribes text according to the initialized transformer model.
        Text can be a single word or longer text.
        :param text: the text to transcribe
        :param sep: if True, inserts a separator between each transcribed word in text
        :return: transcribed version of text as string
        """
        transcribed_arr = []
        for wrd in text.split(' '):
            transcribed_arr.append(self.g2p_model.translate(' '.join(wrd)))
        if sep:
            transcribed = '-'.join(transcribed_arr)
        else:
            transcribed = ' '.join(transcribed_arr)
        print(transcribed)
        return transcribed
