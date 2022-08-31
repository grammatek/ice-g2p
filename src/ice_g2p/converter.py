"""
Converts phonetic transcriptions in one alphabet to transcriptions in another alphabet
"""
import os

package_path = os.path.dirname(os.path.abspath(__file__))
ALPHABETS_FILE = os.path.join(package_path, 'data/sampa_ipa_single_flite.csv')


class Converter:

    def __init__(self):
        self.alphabet_dictionary = self.init_dict()

    def init_dict(self):
        """
        Initialize a symbol dictionary where we can look up mappings between all alphabets in ALPHABETS_FILE.
        The result is a dictionary of dictionaries, where the top-level keys are the names of the alphabets
        and the sub-dictionaries the mappings from a top-level dictionary to all other dictionaries.

        Example:
        {'SAMPA' : {'a' : {'IPA' : 'a', 'SINGLE' : 'a', 'FLITE' : 'a'},
                   {'a:' : {'IPA' : 'aː', 'SINGLE' : 'A', 'FLITE' : 'aa'},
                   { ... }}
        'IPA'   : { ... },
        }

        """
        alphabet_dictionary = {}
        lines = self.read_mapping_file()
        headers = lines[0].split('\t')
        for ind, header in enumerate(headers):
            alphabet_dictionary[header] = {}
            for line in lines[1:]:
                symbols = line.split('\t')
                key_symbol = symbols[ind]
                symbol_dict = {}
                for i, h in enumerate(headers):
                    if i == ind:
                        continue
                    else:
                       symbol_dict[h] = symbols[i]
                alphabet_dictionary[header][key_symbol] = symbol_dict
        return alphabet_dictionary

    def read_mapping_file(self):
        with open(ALPHABETS_FILE) as f:
            lines = f.read().splitlines()
        return lines

    def get_valid_alphabets(self):
        return list(self.alphabet_dictionary.keys())

    def convert(self, input: str, from_alphabet: str, to_alphabet: str):
        """
        Converts a transcription in one alphabet to another alphabet.
        Raises a ValueError if either from or to alphabet is not available for conversion.
        If a symbol in the input string is not found in the respective from alphabet, the symbol is
        kept as is and not converted. A message is written to stdout if this happens.

        :param input: a transcribed string, the symbols have to be separated by a space character
        :param from_alphabet: the alphabet of the input string
        :param to_alphabet: the alphabet to convert the input string into
        :return: a converted transcription
        """

        valid = self.get_valid_alphabets()
        if from_alphabet not in valid or to_alphabet not in valid:
            raise ValueError(f"{from_alphabet} or {to_alphabet} is not contained in the converter's dictionary."
                             f" Valid alphabets: {valid}")

        if from_alphabet == to_alphabet:
            return input

        converted_str = ''
        current_dict = self.alphabet_dictionary[from_alphabet]
        for symbol in input.split():
            if symbol not in current_dict:
                print(f'"{symbol}" seems not to be a valid symbol in {from_alphabet} alphabet. Skipping conversion.')
                converted_str += symbol + ' '
            else:
                converted_symbol = current_dict[symbol][to_alphabet]
                converted_str += converted_symbol + ' '

        return converted_str.strip()


def main():
    converter = Converter()
    print(converter.get_valid_alphabets())
    print(converter.convert('p_h au f Y k l_0', 'SAMPA', 'IPA'))


if __name__ == '__main__':
    main()