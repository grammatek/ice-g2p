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

from g2p_lstm import FairseqG2P


def process_string(input_str: str, word_sep=False) -> str:
    print('processing: "' + input_str + '"')
    g2p = FairseqG2P()
    if word_sep:
        transcribed = g2p.transcribe(input_str, True)
    else:
        transcribed = g2p.transcribe(input_str)

    return transcribed


def process_file_or_dir(file_or_dir: Path) -> None:
    print("processing: " + str(file_or_dir))


def validate_file_input(file_or_directory: Path) -> bool:
    """
    Ensure file_or_directory is a valid path
    :param file_or_directory:
    :return: True if path to file_or_directory is valid, False otherwise
    """
    is_dir = False
    is_file = False
    if os.path.isdir(file_or_directory):
        is_dir = True
    elif os.path.isfile(file_or_directory):
        is_file = True

    return is_dir or is_file


def get_arguments():
    parser = argparse.ArgumentParser(description='Transcribe text input to phonetic representation. Provide '
                                                 'an input file or directory, or a string on stdin to transcribe.')
    parser.add_argument('--infile', '-if', type=Path, help='inputfile or directory')
    parser.add_argument('--inputstr', '-i', help='input string')
    return parser.parse_args()


def main():
    args = get_arguments()

    # we need either an input file or directory, or a string from stdin
    if args.infile is not None:
        valid = validate_file_input(args.infile)
        if not valid:
            logging.error(str(args.infile) + ' does not exist.')
            sys.exit(1)
        else:
            process_file_or_dir(args.infile)

    if args.inputstr is not None:
        print(process_string(args.inputstr, True))


if __name__ == '__main__':
    main()


