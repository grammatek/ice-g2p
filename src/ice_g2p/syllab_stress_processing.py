#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The pron_dict module processes an ASR pronunciation dictionary, containing entries of the form 'word     transcription',
computes the necessary additional information for TTS (part-of-speech, syllabification and stress marks) and
outputs the results in the CMU format or plain syllable format.

Example:
    Input entry:

    adolfsdóttir     a: t O l f s t ou h t I r

    CMU output entry:

    ("adolfsdóttir" n (((a:) 1) ((t O l f s) 3) ((t ou h) 1) ((t I r) 3))))

    Plain syllable output entry:

    adolfsdóttir - a:.t O l f s.t ou h.t I r


"""

__license__ = 'Apache 2.0 (see: LICENSE)'

from .syllabification import syllabify_tree_dict
from .stress import set_stress
from .tree_builder import build_compound_tree

from .entry import PronDictEntry


def init_pron_dict(dict_file):
    with open(dict_file) as f:
        dict_list = f.read().splitlines()

    pron_dict = []
    for line in dict_list:
        word, transcr = line.split('\t')
        entry = PronDictEntry(word, transcr)
        pron_dict.append(entry)
    return pron_dict


def init_pron_dict_from_dict(dict_pairs):
    pron_dict = []
    for word in dict_pairs:
        entry = PronDictEntry(word, dict_pairs[word])
        pron_dict.append(entry)
    return pron_dict


def create_tree_list(pron_dict):
    tree_list = []
    for entry in pron_dict:
        t = build_compound_tree(entry)
        tree_list.append(t)
    return tree_list

def syllabify_and_label(pron_dict):
    tree_dict = create_tree_list(pron_dict)

    syllabified = syllabify_tree_dict(tree_dict)
    syllab_with_stress = set_stress(syllabified)
    return syllab_with_stress


def syllabify_and_label_dict(dictfile):
    pron_dict = init_pron_dict(dictfile)
    return syllabify_and_label(pron_dict)


def syllabify_and_label_from_lists(word_list, transcr_list):
    pron_dict_pairs = dict(zip(word_list, transcr_list))
    pron_dict = init_pron_dict_from_dict(pron_dict_pairs)
    return syllabify_and_label(pron_dict)


def main():
    # add syllabification and stress labeling to a transcription
    # we need both the transcription and the original word string, the user has to make sure the indices
    # in the lists match, i.e. that a word at index n has its transcription at index n
    # returns a list of transcripts, syllabified only or syllabified and stress labeled
    #word_list = ['öskjuhlíð', 'yndislega', 'víetnam']
    #transcr_list = ['9 s c Y l_0 i D', 'I n t I s t l E G a','v i: j E t n a m']
    word_list = ['ferðast', 'sjö', 'komma', 'fimm', 'kílómetrar', 'í', 'tíu', 'gráður', 'hita']
    transcr_list = ['f E r D a s t', 's j 9:', 'k_h O m a', 'f I m', 'c_h i: l ou m E t r a r', 'i:', 't_h i: j Y',
                    'k r au: D Y r', 'h I: t a']
    syllab_with_stress = syllabify_and_label_from_lists(word_list, transcr_list)

    for entry in syllab_with_stress:
        print(entry.dot_format_syllables())

    for entry in syllab_with_stress:
        print(entry.stress_format())

    for entry in syllab_with_stress:
        print(entry.cmu_format())


    """
    # create a syllabified/stress labelled pronunciation dictionary from a plain transcribed dict
    dictfile = '../data/ice_pron_dict_standard_clear.csv'
    syllab_with_stress = syllabify_and_label_dict(dictfile)
    # print in cmu or in plain syllable format (syllable format not containin stress info):
    with open('../data/ice_pron_dict_standard_clear_cmu.txt', 'w') as f:
        for entry in syllab_with_stress:
            f.write(entry.cmu_format())
            f.write('\n')

    with open('../data/ice_pron_dict_standard_clear_syllab.txt', 'w') as f:
        for entry in syllab_with_stress:
            f.write(entry.syllable_format())
            f.write('\n')
    """



if __name__ == '__main__':
    main()
