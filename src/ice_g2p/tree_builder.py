#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ice_g2p import dictionaries
from ice_g2p import entry


VOWELS = ['a', 'á', 'e', 'é', 'i', 'í', 'o', 'ó', 'u', 'ú', 'y', 'ý', 'ö']
MODIFIER_MAP = dictionaries.get_modifier_map()
HEAD_MAP = dictionaries.get_head_map()
TRANSCR_MAP = dictionaries.get_dictionary()
MIN_COMP_LEN = 4
MIN_INDEX = 2       # the position from which to start searching for a head word


class CompoundTree:
    def __init__(self, pron_dict_entry):
        self.elem = pron_dict_entry
        self.left = None
        self.right = None

    def preorder(self):
        if not self.left:
            print(self.elem)
        if self.left:
            self.left.preorder()
        if self.right:
            self.right.preorder()


def contains_vowel(word):
    for c in word:
        if c in VOWELS:
            return True

    return False


def compare_transcripts(comp_transcript, head_transcript):
    """
    If a transcript differs only in a length mark or in voiced/voiceless or having post aspriation or not,
    it should be recognized as the same transcript (since we have already matched the corresponding word strings)
    """
    if not comp_transcript:
        return -1

    head_ind = len(head_transcript) - 1
    comp_ind = len(comp_transcript) - 1

    while head_ind >= 0:
        head_char = head_transcript[head_ind]
        comp_char = comp_transcript[comp_ind]
        if head_char == comp_char:
            head_ind -= 1
            comp_ind -= 1
        elif head_char == ':':
            head_ind -= 1
        elif comp_char == ':':
            comp_ind -= 1
        elif head_char == '0' or head_char == 'h':
            head_ind -= 2
        elif comp_char == '0' or comp_char == 'h':
            comp_ind -= 2
        else:
            return -1

    return comp_ind + 1 # make up for the last iteration where head_ind went below 0


def extract_transcription(entry, comp_head):
    """
    Get the transcript of comp_head from the pron. dictionary and try to match it with the transcript of
    the whole entry. We are somewhat flexible here: length symbol, voicelessness or postaspiration do not
    cause the matching to fail (a: == a, r_0 == r, t_h == t), since transcriptions might not always match 100%.

    Other variations could be added, like 'r t n' == 't n' like in barn: 'b a t n' vs. 'b a r t n', but we are
    not there yet.

    :param entry: PronDictEntry of the compound being analysed
    :param comp_head: the head of the compound as string
    :return:
    """

    head_transcr = TRANSCR_MAP[comp_head] if comp_head in TRANSCR_MAP else 'NO_TRANSCRIPT'
    head_syllable_index = entry.transcript.rfind(head_transcr)

    if head_syllable_index <= 0:
       head_syllable_index = compare_transcripts(entry.transcript, head_transcr)
    if head_syllable_index <= 0:
        #print("did not find transcription of " + comp_head + "!")
        #print("transcription in db: " + head_transcr + ", compound transcr: " + entry.transcript)
        return '', ''

    else:
        modifier_transcr = entry.transcript[0:head_syllable_index]
        head_transcr = entry.transcript[head_syllable_index:]
        return modifier_transcr, head_transcr


def lookup_compound_components(word):
    """
    Divides the word based on if its components are found in the compound database. The rule of thumb is that
    the longest possible head word shows the correct division, but if a modifier is found for a shorter
    head word, this one is chosen. If no modifier is found but a valid head word, the longest valid head word is
    returned, with the assumption that the modifier will also be valid, even if it is not in the dictionary.

    :param word:
    :return: extracted modifier and head if found, returns empty strings if no components are found
    """
    if len(word) <= MIN_COMP_LEN:
        return '', ''

    n = MIN_INDEX
    longest_valid_head = ''
    mod = ''
    while n < len(word) - 2:
        head = word[n:]
        if head in HEAD_MAP:
            if word[:n] in MODIFIER_MAP:
                return word[:n], head
            elif longest_valid_head == '':
                longest_valid_head = head
        n += 1

    if len(mod) == 0 and len(longest_valid_head) > 0:
        # assume we have a valid modifier anyway
        mod = word[:word.index(longest_valid_head)]
        # but only as long as it contains a vowel!
        if not contains_vowel(mod):
            mod = ''

    return mod, longest_valid_head


def extract_compound_components(comp_tree):
    """
    As long as compound components can be extracted, extract compound components and their transcripts recursively.

    :param comp_tree: a tree containing one root element. If compound components are found, they are added
    as children of the root.
    :return:
    """
    mod, head = lookup_compound_components(comp_tree.elem.word)
    if len(mod) > 0 and len(head) > 0:
        mod_transcr, head_transcr = extract_transcription(comp_tree.elem, head)
        if len(mod_transcr) > 0 and len(head_transcr) > 0:
            left_elem = entry.PronDictEntry(mod, mod_transcr)
            left_tree = CompoundTree(left_elem)
            comp_tree.left = left_tree
            right_elem = entry.PronDictEntry(head, head_transcr)
            right_tree = CompoundTree(right_elem)
            comp_tree.right = right_tree
            extract_compound_components(left_tree)
            extract_compound_components(right_tree)


def build_compound_tree(entry):
    """
    :param entry: a PronDictEntry
    :return: a binary tree based on compound division
    """

    comp_tree = CompoundTree(entry)
    extract_compound_components(comp_tree)
    return comp_tree

