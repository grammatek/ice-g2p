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


def write_transcribed(transcribed: dict, filename: Path, suffix: str) -> None:
    """
    Writes the transcriptions with the original grapheme strings to a file
    named 'filename' extended by 'suffix', for example:
    original filename: path/to/textfile.txt
    output filename: path/to/textfile_transcribed.tsv

    :param transcribed: a map with grapheme strings as keys and phonetic transcr. as values
    :param filename: the original filename containing the grapheme strings
    :param suffix: the suffix to label the output file with
    :return:
    """
    filename_stem = filename.stem
    extended_filename = str(filename.parent) + '/' + filename_stem + suffix + '.tsv'
    with open(extended_filename, 'w') as f:
        for key in transcribed:
            f.write(key + '\t')
            f.write(transcribed[key] + '\n')


def process_string(input_str: str, word_sep=False) -> str:
    print('processing: "' + input_str + '"')
    g2p = FairseqG2P()
    transcribed = g2p.transcribe(input_str.strip(), word_sep)

    return transcribed


def process_file(filename: Path, word_sep=False) -> dict:
    """
    Transcribes the content of 'filename' line by line
    :param filename: input file to transcribe
    :param word_sep: if the transcription should contain word separators
    :return: a map of grapheme strings and their phonetic transcriptions
    """
    print("processing: " + str(filename))
    g2p = FairseqG2P()
    with open(filename) as f:
        file_content = f.read().splitlines()

    transcribed = {}
    for line in file_content:
        transcribed[line] = g2p.transcribe(line.strip(), word_sep)

    return transcribed


def process_file_or_dir(file_or_dir: Path, out_suffix: str, word_sep=False) -> None:
    print("processing: " + str(file_or_dir))
    if os.path.isdir(file_or_dir):
        for root, dirs, files in os.walk(file_or_dir):
            for filename in files:
                file_path = Path(os.path.join(root, filename))
                transcribed_content = process_file(file_path, word_sep)
                write_transcribed(transcribed_content, file_path, out_suffix)
    elif os.path.isfile(file_or_dir):
        transcribed_content = process_file(file_or_dir, word_sep)
        write_transcribed(transcribed_content, file_or_dir, out_suffix)


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
        if not args.infile.exists():
            logging.error(str(args.infile) + ' does not exist.')
            sys.exit(1)
        else:
            process_file_or_dir(args.infile, '_transcribed')

    if args.inputstr is not None:
        print(process_string(args.inputstr, False))


if __name__ == '__main__':
    main()
