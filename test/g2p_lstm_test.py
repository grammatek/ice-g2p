import unittest
import os
from src.ice_g2p.g2p_lstm import FairseqG2P
from src.ice_g2p.transcriber import Transcriber

class TestG2P_LSTM(unittest.TestCase):

    os.chdir(os.path.split(os.getcwd())[0])


    def test_simple_transcribe(self):
        test_string = 'hlaupa'
        g2p = FairseqG2P()
        transcribed = g2p.transcribe(test_string)
        self.assertEqual('l_0 9i: p a', transcribed)


    def test_word_sep_transcribe(self):
        test_string = 'hlaupa í burtu í dag'
        g2p = FairseqG2P()
        transcribed = g2p.transcribe(test_string, True, True)
        self.assertEqual('l_0 9i: p a-i:-p Y r_0 t Y-i:-t a: G', transcribed)


    def test_syllabification(self):
        print("Current working dir: " + os.getcwd())
        test_string = 'hlaupa í burtu í dag'
        g2p = Transcriber()
        transcribed = g2p.transcribe(test_string, True, True, True)
        self.assertEqual('l_0 9i:1 . p a0 . i:1 . p Y1 r_0 . t Y0 . i:1 . t a:1 G', transcribed)


    def test_cmu_format(self):
        print("Current working dir: " + os.getcwd())
        test_string = 'hljóðritaður texti'
        g2p = Transcriber()
        # input_str: str, icelandic=True, syllab=False, use_dict=False, word_sep: str=None, cmu=False
        transcribed = g2p.transcribe(test_string, True, True, True, '', True)
        print(transcribed)
        self.assertEqual('("hljóðritaður" nil (((l_0 j ou D ) 1) ((r I ) 0) ((t a ) 0) ((D Y r ) 0))) ("texti" nil (((t_h E k s ) 1) ((t I ) 0)))', transcribed)

    def test_custom_dict(self):
        custom_dict = self.get_custom_dict()
        test_string = 'þessi texti en engir aukvisar'
        g2p = Transcriber()
        g2p.set_custom_dict(custom_dict)
        transcribed = g2p.transcribe(test_string, True, True, True, '')
        print(transcribed)


    def get_custom_dict(self):
        custom = {'texti': 't_h E x s t I', 'engir': '9 N k v I r'}
        return custom

if __name__ == '__main__':
    unittest.main()