import math
from nltk import trigrams
from enum import Enum
import ice_g2p.syllab_stress_processing as syllabify
from ice_g2p.g2p_lstm import FairseqG2P
from ice_g2p.trigrams import ice_grams, eng_grams
from ice_g2p.stress import set_stress


class G2P_METHOD(Enum):
    FAIRSEQ = 1
    THRAX = 2


class Transcriber:

    def __init__(self, g2p_method=G2P_METHOD.FAIRSEQ, lang_detect=False, use_dict=False, use_syll=False):
        self.g2p = self.init_g2p(g2p_method)
        self.use_dict = use_dict
        self.use_syll = use_syll
        if lang_detect:
            self.g2p_foreign = self.init_g2p(g2p_method, lang_detect)
            self.lang_detect = True
        else:
            self.lang_detect = False
        if use_dict:
            from ice_g2p.dictionaries import get_dictionary
            self.dictionary = get_dictionary()
        else:
            self.dictionary = None

    def init_g2p(self, g2p_method: G2P_METHOD, lang_detect: bool=False):
        if g2p_method == G2P_METHOD.FAIRSEQ:
            if lang_detect:
                return FairseqG2P(dialect='english', alphabet='[aåäbcdefghijklmnoöpqrstuüvwxyz]')
            else:
                return FairseqG2P()
        else:
            raise ValueError('Model ' + str(g2p_method) + ' does not exist!')

    def transcribe(self, input_str: str, icelandic=True, syllab=False, use_dict=False, word_sep=False) -> str:
        # TODO: manage word_sep
        transcr_arr = []
        for wrd in input_str.split(' '):
            if icelandic:
                # a word labelled as Icelandic will be sent to automatic lang detection
                transcr_arr.append(self.transcribe_lang(wrd.strip(), use_dict, word_sep, self.is_icelandic(wrd.strip())))
            else:
                # word labelled as not Icelandic, will be sent directly to foreign transcription model
                transcr_arr.append(
                    self.transcribe_lang(wrd.strip(), use_dict, word_sep, False))
        if syllab:
            entries = syllabify.init_pron_dict_from_tuples(list(zip(input_str.split(' '), transcr_arr)))
            syllabified_dict = syllabify.syllabify_and_label(entries)
            transcribed_utt = set_stress([syllabified_dict[wrd] for wrd in input_str.split(' ')])
            transcribed = self.extract_transcript(transcribed_utt, word_sep=word_sep)
        else:
            if word_sep:
                if type(word_sep) == str:
                    transcribed = f' {word_sep} '.join(transcr_arr)
                else:
                    transcribed = "-".join(transcr_arr)
            else:
                transcribed = ' '.join(transcr_arr)

        return transcribed

    def extract_transcript(self, syllabified: list, word_sep: str=None) -> str:
        result = ''
        for entr in syllabified:
            if not result:
                result += entr.simple_stress_format()
            else:
                if word_sep:
                    result += f" {word_sep} " + entr.simple_stress_format()
                else:
                    result += ' . ' + entr.simple_stress_format()

        return result

    def transcribe_lang(self, input_str: str, use_dict=False, word_sep=False, icelandic=True) -> str:
        if icelandic:
            return self.g2p.transcribe(input_str.strip(), use_dict, word_sep)
        else:
            return self.g2p_foreign.transcribe(input_str.strip(), use_dict, word_sep)

    # Use trigrams to estimate the probability of a word being Icelandic or not
    def is_icelandic(self, word: str) -> bool:
        # if we don't have a foreign g2p, all words are processed as Icelandic
        if not self.lang_detect:
            return True

        ice_probs = []
        eng_probs = []
        for c1, c2, c3 in trigrams(word.lower(), pad_right=True, pad_left=True):
            if (c1, c2) in ice_grams and c3 in ice_grams[(c1, c2)]:
                ice_probs.append(ice_grams[(c1, c2)][c3])
            else:
                ice_probs.append(0.001)
            if (c1, c2) in eng_grams and c3 in eng_grams[(c1, c2)]:
                eng_probs.append(eng_grams[(c1, c2)][c3])
            else:
                eng_probs.append(0.001)
        if math.prod(ice_probs) >= math.prod(eng_probs):
            return True
        return False
