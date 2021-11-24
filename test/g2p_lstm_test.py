import unittest
import os
from src.g2p_lstm import FairseqG2P

class TestG2P_LSTM(unittest.TestCase):

    os.chdir(os.path.split(os.getcwd())[0])

    def test_simple_transcribe(self):
        test_string = 'hlaupa'
        g2p = FairseqG2P()
        transcribed = g2p.transcribe(test_string)
        self.assertEqual('l_0 9i: p a', transcribed)

    def test_word_sep_transcribe(self):
        test_string = 'hlaupa í burtu'
        g2p = FairseqG2P()
        transcribed = g2p.transcribe(test_string, True)
        self.assertEqual('l_0 9i: p a-i:-p Y r_0 t Y', transcribed)


if __name__ == '__main__':
    unittest.main()