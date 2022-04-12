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
        g2p = Transcriber(use_dict=True, word_sep='-')
        transcribed = g2p.transcribe(test_string)
        self.assertEqual('l_0 9i: p a - i: - p Y r_0 t Y - i: - t a: G', transcribed)


    def test_syllabification(self):
        print("Current working dir: " + os.getcwd())
        test_string = 'hlaupa í burtu í dag'
        g2p = Transcriber(use_dict=True, syllab_symbol='.')
        transcribed = g2p.transcribe(test_string)
        self.assertEqual('l_0 9i: . p a i: p Y r_0 . t Y i: t a: G', transcribed)

    def test_word_sep(self):
        print("Current working dir: " + os.getcwd())
        test_string = 'hlaupa í burtu í dag'
        g2p = Transcriber(use_dict=True, syllab_symbol='-', word_sep='-', stress_label=True)
        transcribed = g2p.transcribe(test_string)
        self.assertEqual('l_0 9i:1 - p a0 - i:1 - p Y1 r_0 - t Y0 - i:1 - t a:1 G', transcribed)

    def test_dialect(self):
        # 'hlaupa' in dict, 'hlaupastrákur' not in dict
        test_string = 'hlaupa í burtu hlaupastrákur'
        g2p = Transcriber(dialect='north', use_dict=True, syllab_symbol='-', word_sep='-', stress_label=True)
        transcribed = g2p.transcribe(test_string)
        self.assertEqual('l_0 9i:1 - p_h a0 - i:1 - p Y1 r_0 - t Y0 - l_0 9i:1 - p_h a0 - s t r au0 - k_h Y0 r', transcribed)

    def test_english(self):
        test_string = 'what ertu crazy'
        g2p = Transcriber(dialect='north', use_dict=True, lang_detect=True, syllab_symbol='-', word_sep='-', stress_label=True)
        transcribed = g2p.transcribe(test_string)
        self.assertEqual('v a1 h t - E1 r_0 - t Y0 - k_h r ei:1 - s i0', transcribed)


    def test_cmu_format(self):
        print("Current working dir: " + os.getcwd())
        test_string = 'hljóðritaður texti'
        g2p = Transcriber(use_dict=True, syllab_symbol='.')
        # input_str: str, icelandic=True, syllab=False, use_dict=False, word_sep: str=None, cmu=False
        transcribed = g2p.transcribe(test_string, cmu=True)
        print(transcribed)
        self.assertEqual('("hljóðritaður" nil (((l_0 j ou D ) 1) ((r I ) 0) ((t a ) 0) ((D Y r ) 0))) ("texti" nil (((t_h E k s ) 1) ((t I ) 0)))', transcribed)

    def test_custom_dict(self):
        custom_dict = self.get_custom_dict()
        test_string = 'þessi texti en engir aukvisar'
        g2p = Transcriber(use_dict=True)
        g2p.set_custom_dict(custom_dict)
        transcribed = g2p.transcribe(test_string)
        self.assertEqual('T E s I t_h E x s t I E n 9 N k v I r 9i: k v I s a r', transcribed)


    def get_custom_dict(self):
        custom = {'texti': 't_h E x s t I', 'engir': '9 N k v I r'}
        return custom

if __name__ == '__main__':
    unittest.main()