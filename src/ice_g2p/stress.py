#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ice_g2p import entry

# max number of syllables for a word only having primary stress on first syllable, other syllables without stress
ONE_STRESS_SYLL_COUNT = 4

PRIMARY_STRESS = 1
NO_STRESS = 3

# grammatical and other endings containing a vowel and thus constituting a syllable of their own
ENDING_SYLLABLES = ['a', 'i', 'u', 'ar', 'ir', 'ur', 'is', 'um', 'na', 'ni', 'nu', 'ið', 'ins', 'sins', 'in', 'inn',
                    'unum', 'num', 'nna', 'nni', 'nnar', 'innar', 'nar', 'inum', 'nir', 'irnir', 'ina', 'va', 'var', 'vum',
                    'ngur', 'inu', 'stu', 'ra', 'ndi', 'da', 'di', 'un', 'uð', 'ri', 'gur', 'ga', 'gðar', 'gðir', 'gður',
                    'nga', 'leg', 'lega', 'nlegt', 'legt', 'semi', 'ning', 'arinnar', 'ði', 'tha', 'ðar', 'ðir', 'sti',
                    'nda', 'ba', 'ngu', 'inni', 'ður', 'ngum', 'ann', 'anna', 'anni', 'ara', 'ari', 'as', 'að', 'enn', 'í', 'ía']


def last_stress(pron_dict_entry):
    if len(pron_dict_entry.syllables) > 0:
        return pron_dict_entry.syllables[-1].stress
    else:
        return NO_STRESS


def same_word_with_ending(short_word, long_word):
    """

    :param short_word:
    :param long_word:
    :return: True if long_word is the same word as short_word, but with another grammatical ending, False otherwise
    """

    ending = long_word.word[len(short_word.word):].strip()
    if ending in ENDING_SYLLABLES:
        return True
    return False


def synchronize_stress(short_word, long_word):
    """
    Synchronizes the stress marks between the two words, whereas the longer word has to start
    with the shorter word. The stress marks of the shorter words are transferred to the beginning
    of the longer word.
    :param short_word: syllabified word with stress marks
    :param long_word: syllabified word with stress mark only on first syllable or none
    :return:
    """

    # dative of 'te' has two syllables, whereas longer words like 'teig' only have one syllable
    if short_word.word == 'tei':
        return

    for i, elem in enumerate(short_word.syllables):
        if i >= len(long_word.syllables) or i >= len(short_word.syllables):
            print('i: ' + str(i) + ' long: ' + str(long_word.syllables) + ' short: ' + str(short_word.syllables))
        else:
            long_word.syllables[i].stress = short_word.syllables[i].stress


def should_add_primary_stress(current_word, modifier):
    """
    Tests for plausibility of a primary stress on the first syllable after the common syllables of current word
    and its modifier. If the current word has more syllables, if the last syllable of the modifier does not
    have a primary stress and if current word is not simply the modifier with a grammatical ending, then this
    method returns True, False otherwise
    :param current_word: word starting with modifier
    :param modifier: the beginning of current word (possible compound modifier)
    :return: True if it is plausible that the syllable in current word that comes right after the common
    syllables of both words should have primary stress, False otherwise
    """
    if len(current_word.syllables) > len(modifier.syllables) and \
        last_stress(modifier) != PRIMARY_STRESS and not \
        same_word_with_ending(modifier, current_word):
            return True

    return False


def set_stress(syllabified_words):
    """
    Performs a simple stress-setting algorithm:
    - for every word with less than ONE_STRESS_SYLL_COUNT syllables, set primary stress on first syllable
    - for every longer word, check if it starts with a previous word, use the previous syllabification and
        add primary stress on the first syllable after the common syllables if it is not a flective ending:

        verslunar -> ve'rslunar
        verslunareigandi -> ve'rslunarei'gandi  (compound: primary stress on head word)
        verslunarinnar -> ve'rslunarinnar   (ending: no stress)

    :param syllabified_words: alphabetical sorted list of syllabified words
    :return: a list of syllabified words with stress marks on each syllable
    """
    result_list = []
    modifiers = []
    last_word = entry.PronDictEntry('')
    for current in syllabified_words:
        current.syllables[0].stress = PRIMARY_STRESS
        if current.word.startswith(last_word.word):
            synchronize_stress(last_word, current)
            if len(last_word.word) > 1:
                modifiers.append(last_word)
            if should_add_primary_stress(current, last_word):
                current.syllables[len(last_word.syllables)].stress = PRIMARY_STRESS
        else:
            mod_len = len(modifiers)
            while mod_len > 0:
                mod_len -= 1
                if current.word.startswith(modifiers[mod_len].word):
                    synchronize_stress(modifiers[mod_len], current)
                    if should_add_primary_stress(current, modifiers[mod_len]):
                        current.syllables[len(modifiers[mod_len].syllables)].stress = PRIMARY_STRESS
                    break
                else:
                    modifiers.pop()
                    mod_len = len(modifiers)

        result_list.append(current)
        last_word = current

    return result_list
