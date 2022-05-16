import math
from nltk import trigrams
from enum import Enum
import ice_g2p.syllab_stress_processing as syllabify
from ice_g2p.g2p_lstm import FairseqG2P
from ice_g2p.trigrams import ice_grams, eng_grams
from ice_g2p.stress import set_stress


class G2P_METHOD(Enum):
    FAIRSEQ = 1
    # THRAX = 2 TODO: implement!


class Transcriber:

    def __init__(self, g2p_method=G2P_METHOD.FAIRSEQ, dialect='standard', lang_detect=False, use_dict=False,
                 stress_label=False, syllab_symbol='', word_sep=''):

        self.g2p = self.init_g2p(g2p_method, dialect)
        self.use_dict = use_dict
        self.syllab_symbol = syllab_symbol
        self.word_separator = word_sep
        self.add_stress_label = stress_label
        if lang_detect:
            self.g2p_foreign = self.init_g2p(g2p_method, dialect=dialect, use_english=True)
            self.lang_detect = True
        else:
            self.g2p_foreign = None
            self.lang_detect = False
        if use_dict:
            from ice_g2p.dictionaries import get_dictionary
            self.dictionary = get_dictionary()
        else:
            self.dictionary = None

    def init_g2p(self, g2p_method: G2P_METHOD, dialect: str='standard', use_english=False) -> FairseqG2P:
        if g2p_method == G2P_METHOD.FAIRSEQ:
                return FairseqG2P(dialect=dialect, use_english=use_english)
        else:
            raise ValueError('Model ' + str(g2p_method) + ' does not exist!')

    def override_core_dict(self, pron_dict: dict):
        """
        Override the default pronunciation dictionary
        :param pron_dict:
        :return:
        """
        self.g2p.override_pron_dict(pron_dict)

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
        self.g2p.set_custom_dict(custom_dict)

    def transcribe(self, input_str: str, icelandic=True, cmu=False) -> str:
        transcr_arr = []
        for wrd in input_str.split(' '):
            if icelandic:
                # a word labelled as Icelandic will be sent to automatic lang detection
                transcr_arr.append(self.transcribe_lang(wrd.strip(), icelandic=self.is_icelandic(wrd.strip())))
            else:
                # word labelled as not Icelandic, will be sent directly to foreign transcription model
                transcr_arr.append(
                    self.transcribe_lang(wrd.strip(), icelandic=False))
        if self.syllab_symbol:
            entries = syllabify.init_pron_dict_from_tuples(list(zip(input_str.split(' '), transcr_arr)), self.syllab_symbol)
            syllabified_dict = syllabify.syllabify_and_label(entries)
            transcribed_utt = set_stress([syllabified_dict[wrd] for wrd in input_str.split(' ')])
            transcribed = self.extract_transcript(transcribed_utt, cmu)
        elif self.word_separator:
            transcribed = f' {self.word_separator} '.join(transcr_arr)
        else:
            transcribed = ' '.join(transcr_arr)

        return transcribed

    def extract_transcript(self, syllabified: list, cmu=False) -> str:
        if cmu:
            return self.extract_cmu_transcript(syllabified)
        result = ''
        for entr in syllabified:
            if self.add_stress_label:
                string_repr = entr.simple_stress_format()
            else:
                string_repr = entr.dot_format_syllables()
            if not result:
                result += string_repr
            elif self.word_separator:
                result += f" {self.word_separator} " + string_repr
            else:
                result += " " + string_repr

        return result

    def extract_cmu_transcript(self, syllabified: list) -> str:
        result = ''
        for entr in syllabified:
            if not result:
                result += entr.cmu_format()
            elif self.word_separator:
                result += f" {self.word_separator} " + entr.cmu_format()
            else:
                result += " " + entr.cmu_format()

        return result

    def transcribe_lang(self, input_str: str, icelandic=True) -> str:
        if icelandic or self.g2p_foreign is None:
            return self.g2p.transcribe(input_str.strip(), self.use_dict, self.word_separator)
        else:
            return self.g2p_foreign.transcribe(input_str.strip(), self.use_dict, self.word_separator)

    # Use trigrams to estimate the probability of a word being Icelandic or not
    def is_icelandic(self, word: str) -> bool:
        # if we don't have a foreign g2p, all words are processed as Icelandic
        if not self.lang_detect or not self.g2p_foreign:
            return True

        # If word contains non-valid characters for either of the models, it can't be transcribed by
        # the corresponding model. We use the Icelandic one as fallback, so just check for non-valid
        # English characters. Important check because of loanwords that might contain Icelandic characters
        # like: 'absúrd', 'dnépr', 'penélope' that have higher combined trigram probs for English despite
        # the non-valid trigrams containing Icelandic characters.
        if set(word).difference(self.g2p_foreign.alphabet):
            return True
        # Special case for spelling
        if len(word) == 1:
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
