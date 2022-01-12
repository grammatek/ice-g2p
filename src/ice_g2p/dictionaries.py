import os, sys
DICTIONARY_FILE = os.path.join(sys.prefix, 'dictionaries/ice_pron_dict_standard_clear.csv')
HEAD_FILE = os.path.join(sys.prefix, 'data/head_map.csv')
MODIFIER_FILE = os.path.join(sys.prefix, 'data/modifier_map.csv')
VOWELS_FILE = os.path.join(sys.prefix, 'data/vowels_sampa.txt')
CONS_CLUSTERS_FILE = os.path.join(sys.prefix, 'data/cons_clusters_sampa.txt')


def read_map(filename):
    with open(filename) as f:
        file_content = f.read().splitlines()
    dict_map = {}
    for line in file_content:
        arr = line.split('\t')
        if len(arr) > 1:
            values = arr[1:]
        else:
            values = []
        key = arr[0]
        dict_map[key] = values
    return dict_map


def read_dictionary(filename):
    with open(filename) as f:
        file_content = f.read().splitlines()
    pronDict = {}
    for line in file_content:
        word, transcr = line.split('\t')
        pronDict[word] = transcr
    return pronDict


def read_list(filename):
    with open(filename) as f:
        file_content = f.read().splitlines()
    return file_content


def get_head_map():
    return read_map(HEAD_FILE)


def get_modifier_map():
    return read_map(MODIFIER_FILE)


def get_dictionary():
    return read_dictionary(DICTIONARY_FILE)


def get_vowels():
    return read_list(VOWELS_FILE)


def get_cons_clusters():
    return read_list(CONS_CLUSTERS_FILE)
