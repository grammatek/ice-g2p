#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ice_g2p.syllabification import VOWELS


class PronDictEntry:
    """
    Contains information on a pronunciation dict entry and methods to manipulate it

    The initialisation of a PronDictEntry object takes a word string and its transcription as parameters.
    """

    def __init__(self, word='', transcription='', reference='', alphabet='SAMPA', syllab_symbol='.'):
        """

        :param word: a dictionary entry (ex: 'dag')
        :param transcription: transcription of 'word', with the phones space separated (ex: 't a: G')

        """
        self.word = word
        self.transcript = transcription.strip()
        self.transcription_arr = self.transcript.split()
        self.transcript_variants = set()
        self.transcript_variants.add(self.transcript)
        self.gpos = 'nil'  # guessed part-of-speech
        # transcript, syllabification or stress labeled reference string for testing
        self.reference_transcr = reference
        self.syllables = []
        self.compound_elements = []
        self.entailing_compounds = [] # compounds where this word is one part
        self.frequency = 0
        self.set_phon_symbols(alphabet)
        self.syllab_symbol = syllab_symbol

    def __str__(self):
        return self.word + '\t' + self.gpos + '\t' + self.transcript + '\t' + str(self.syllables)

    def __repr__(self):
        return self.__str__()

    def set_phon_symbols(self, alphabet):
        if alphabet == 'IPA':
            self.length_symbol = 'ː'
            self.post_aspir = '\u02B0'
        else:
            self.length_symbol = ':'
            self.post_aspir = '_h'


    def simplify_compound_variants(self):
        tmp_variants = self.transcript_variants
        self.transcript_variants = set()
        orig_transcript = self.transcript
        no_postaspir = orig_transcript.replace(self.post_aspir, '')
        self.transcript_variants.add(orig_transcript)
        for t in tmp_variants:
            if t.replace(self.length_symbol, '') == orig_transcript or orig_transcript.replace(self.length_symbol, '') == t:
                continue
            elif t == no_postaspir:
                continue
            elif t.replace(self.length_symbol, '') == no_postaspir or no_postaspir.replace(self.length_symbol, '') == t:
                continue
            else:
                self.transcript_variants.add(t)

    def update_syllables(self, ind, prev_syll, syll):
        self.syllables[ind - 1] = prev_syll
        self.syllables[ind] = syll

    def cmu_format_syllables(self):
        formatted_string = '('
        for syll in self.syllables:
            formatted_string += '((' + syll.content + ') ' + str(syll.stress) + ') '

        return formatted_string.strip() + ')'

    def cmu_format(self):
        return '("' + self.word + '" ' + self.gpos + ' ' + self.cmu_format_syllables() + ')'

    def dot_format_syllables(self):
        sylls = ''
        for syll in self.syllables:
            sylls += syll.content.strip() + f" {self.syllab_symbol} "
        if len(sylls) > 3:
            # strip the last syllab_symbol with spaces from the word
            sylls = sylls[0:-3]
        return sylls

    def syllable_format(self):
        return self.word + ' - ' + self.dot_format_syllables()

    def stress_format(self):
        sylls = ''
        for syll in self.syllables:
            stressed_phones = []
            phones = syll.content.strip().split()
            for p in phones:
                if p in VOWELS:
                    p = p + str(syll.stress)
                stressed_phones.append(p)

            sylls += ' '.join(stressed_phones) + f" {self.syllab_symbol} "

        return sylls.strip()[:-2]

    def simple_stress_format(self):
        return self.stress_format()