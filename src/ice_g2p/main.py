#
# A complete grapheme-to-phoneme module for Icelandic.
# Transcribes graphemes (alphabetic text) to phonemes with or without the help of a pronunciation dictionary.
# Output is according to input: a wordlist as input produces a dictionary formatted output word\ttranscription,
# text as input produces a line by line transcription text\ttranscription.
#
# Syllabification and stress labeling is optional.
#
# Examples:
#
#

import os
import sys
import logging
import argparse
from pathlib import Path

from ice_g2p.converter import Converter
from ice_g2p.transcriber import Transcriber
from ice_g2p.transcriber import G2P_METHOD

AVAILABLE_DIALECTS = ['standard', 'north']


def write_transcribed(transcribed: dict, filename: Path, suffix: str, keep_original: bool) -> None:
    """
    Writes the transcriptions with the original grapheme strings to a file
    named 'filename' extended by 'suffix', for example:
    original filename: path/to/textfile.txt
    output filename: path/to/textfile_transcribed.tsv

    :param transcribed: a map with grapheme strings as keys and phonetic transcr. as values
    :param filename: the original filename containing the grapheme strings
    :param suffix: the suffix to label the output file with
    :param keep_original: write the original grapheme string in the first column
    :return:
    """
    filename_stem = filename.stem
    extended_filename = str(filename.parent) + '/' + filename_stem + suffix + '.tsv'
    with open(extended_filename, 'w') as f:
        for key in transcribed:
            if keep_original:
                f.write(key + '\t')
            f.write(transcribed[key] + '\n')


def process_string(input_str: str, dialect='standard', use_dict=False, syllab_symbol='', word_sep='',
                   stress_label=False, lang_detect=False) -> str:
    print('processing: "' + input_str + '"')
    g2p = Transcriber(G2P_METHOD.FAIRSEQ, dialect=dialect, lang_detect=lang_detect, syllab_symbol=syllab_symbol, word_sep=word_sep,
                      stress_label=stress_label, use_dict=use_dict)
    return g2p.transcribe(input_str)


def process_file(filename: Path, dialect='standard', use_dict=False, syllab_symbol='', word_sep='',
                   stress_label=False, lang_detect=False) -> dict:
    """
    Transcribes the content of 'filename' line by line
    :param filename: input file to transcribe
    :param word_sep: if the transcription should contain word separators
    :return: a map of grapheme strings and their phonetic transcriptions
    """
    print("processing: " + str(filename))
    with open(filename) as f:
        file_content = f.read().splitlines()

    g2p = Transcriber(G2P_METHOD.FAIRSEQ, dialect=dialect, use_dict=use_dict, syllab_symbol=syllab_symbol, word_sep=word_sep,
                   stress_label=stress_label, lang_detect=lang_detect)
    transcribed = {}
    for line in file_content:
        transcribed[line] = g2p.transcribe(line)

    return transcribed


def process_file_or_dir(file_or_dir: Path, out_suffix: str, dialect='standard', use_dict=False, syllab_symbol='', word_sep='',
                   stress_label=False, lang_detect=False, keep_original=False) -> None:
    print("processing: " + str(file_or_dir))
    if os.path.isdir(file_or_dir):
        for root, dirs, files in os.walk(file_or_dir):
            for filename in files:
                if filename.startswith('.'):
                    continue
                file_path = Path(os.path.join(root, filename))
                transcribed_content = process_file(file_path, dialect=dialect, use_dict=use_dict, syllab_symbol=syllab_symbol, word_sep=word_sep,
                   stress_label=stress_label, lang_detect=lang_detect)
                write_transcribed(transcribed_content, file_path, out_suffix, keep_original)
    elif os.path.isfile(file_or_dir):
        transcribed_content = process_file(file_or_dir, dialect=dialect, use_dict=use_dict, syllab_symbol=syllab_symbol, word_sep=word_sep,
                   stress_label=stress_label, lang_detect=lang_detect)
        write_transcribed(transcribed_content, file_or_dir, out_suffix, keep_original)


def convert(transcription: str, from_alpha: str, to_alpha):
    converter = Converter()
    converted = converter.convert(transcription, from_alpha, to_alpha)
    return converted


def get_alphabets():
    converter = Converter()
    return converter.get_valid_alphabets()


def get_arguments():
    parser = argparse.ArgumentParser(description='Transcribe text input to phonetic representation. Provide '
                                                 'an input file or directory, or a string on stdin to transcribe.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--infile', '-if', type=Path, help='inputfile or directory')
    group.add_argument('--inputstr', '-i', help='input string')
    parser.add_argument('--dialect', '-a', default='standard',
                        help='dialect to transcribe by, available: "standard" and "north"')
    parser.add_argument('--sep', '-s', type=str, help='word separator to use')
    parser.add_argument('--syll', '-y', type=str, help='syllable separator to use')
    parser.add_argument('--stress', '-t', action='store_true', help='use stress labels')
    parser.add_argument('--dict', '-d', action='store_true', help='use pronunciation dictionary')
    parser.add_argument('--keep', '-k', action='store_true', help='keep original')
    parser.add_argument('--langdetect', '-l', action='store_true', help='use word-based language detection')
    parser.add_argument('--phoneticalpha', '-p', type=str, help='output in a specific phonetic alphabet')
    return parser.parse_args()


def main():
    args = get_arguments()
    keep_original = args.keep
    dialect = args.dialect
    word_sep = args.sep
    use_dict = args.dict
    syllab = args.syll
    stress = args.stress
    lang_detect = args.langdetect
    alphabet = args.phoneticalpha

    if dialect not in AVAILABLE_DIALECTS:
        logging.error(f'Transcription is not available for dialect "{dialect}". Available dialects: {AVAILABLE_DIALECTS}')
        sys.exit(1)

    available_alphabets = get_alphabets()
    if alphabet and not alphabet in available_alphabets:
        logging.error(f'{alphabet} is not available. Available phonetic alphabets: {available_alphabets}')
        sys.exit(1)

    # we need either an input file or directory, or a string from stdin
    if args.infile is not None:
        if not args.infile.exists():
            logging.error(str(args.infile) + ' does not exist.')
            sys.exit(1)
        else:
            process_file_or_dir(args.infile, '_transcribed', dialect=dialect, use_dict=use_dict, syllab_symbol=syllab, word_sep=word_sep,
                                stress_label=stress, lang_detect=lang_detect, keep_original=keep_original)

    if args.inputstr is not None:
        transcribed = process_string(args.inputstr, dialect=dialect, use_dict=use_dict, syllab_symbol=syllab, word_sep=word_sep,
                                stress_label=stress, lang_detect=lang_detect)

        if alphabet:
            transcribed = convert(transcribed, 'SAMPA', alphabet)
        if keep_original:
            print(args.inputstr + ' : ' + transcribed)
        else:
            print(transcribed)


if __name__ == '__main__':
    main()
