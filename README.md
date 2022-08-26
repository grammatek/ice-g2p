# Ice-g2p : Phonetic transcription (grapheme-to-phoneme) for Icelandic

Ice-g2p is a module for automatic phonetic transcription of Icelandic. Ice-g2p can be used as a stand-alone
command line tool or as a library, and can e.g. be used for the final text processing step in a frontend
pipeline for speech synthesis (TTS).

Ice-g2p uses a manually curated [pronunciation dictionary](https://github.com/grammatek/iceprondict)
and LSTM-based [g2p-models](https://github.com/grammatek/g2p-lstm) for unknown words. It can be used
to transcribe Icelandic in four pronunciation variations and also uses a special model to transcribe
English words that might occur in Icelandic texts, using the Icelandic phone set.

## Setup

Clone the repository and create a virtual environment in the project root directory. Install the requirements:

    git clone git@github.com:grammatek/ice-g2p.git
	cd ice-g2p
	python -m venv g2p-venv
	source g2p-venv/bin/activate
	pip install -r requirements.txt



## Command line interface

**The input strings/texts need to be normalized. The module only handles lowercase characters from the Icelandic alphabet, no punctuation or other characters, unless language detection is enabled (see Flags)**

Characters allowed: _[aábcðdeéfghiíjklmnoóprstuúvxyýzþæö]_. If other characters are found in the input, the transcription of the respective token is skipped and a notice written to stdout.

To transcribe text, currently two main options are available, direct from stdin to stdout or from file or a collection of files (directory) 

    $ python3 src/ice-g2p/main.py -i 'hljóðrita þetta takk'
	l_0 j ou D r I t a T E h t a t_h a h k

    $ python3 src/ice-g2p/main.py -i 'þetta war fürir þig'
    war contains non valid character(s) {'w'}, skipping transcription.
    fürir contains non valid character(s) {'ü'}, skipping transcription.
    T E h t a   T I: G

	%python src/ice-g2p/main.py -if file_to_transcribe.txt

If the input comes from stdin, the output is written to stdout. Input from file(s) is written to file(s) with the same name with the suffix '_transcribed.tsv'. The files are transcribed line by line and written out correspondingly. 

### Flags

The options available:

    --infile INFILE, -if INFILE
                        inputfile or directory
  	--inputstr INPUTSTR, -i INPUTSTR
                          input string
    --sep SEP_STR, -s SEP_STR  word separator to use, if not present, no word separators are used
    --syll SYLL_STR -y SYLL_STR syllable separator to use, if not present, no syllabification will be performed
    # boolean arguments
    --stress, -t          perform stress labeling, ONLY APPLICABLE IN COMBINATION WITH --syll ARGUMENT!
  	--keep, -k            keep original
  	--sep, -s             use word separator
	--dict, -d            use pronunciation dictionary
	--langdetect, -l      use word-based language detection
    --phoneticalpha, -p   return the output in a specific alphabet (default: SAMPA)

Using the `-k` flag keeps the original grapheme strings and for file input/output writes the original strings in the first column of the tab separated output file, and the phonetic transcription in the second one.
The `-s`flag adds the defined word separator to the transcription and with the `-y` flag syllabification is added to 
the transcription with the chosen separator. The word and syllable separators may be the same or different symbols.
Common symbol for syllable separation is a dot `.` In combination with syllabification, stress labels can be added
using the `-t` flag.
With the `-d` flag all tokens are first looked up in an existing pronunciation dictionary, the automatic g2p is then 
only a fallback for words not contained in the dictionary. 

    %python src/ice-g2p/main.py -i 'hljóðrita þetta takk' -k -s '-'
	hljóðrita þetta takk : l_0 j ou D r I t a - T E h t a - t_h a h k

	%python src/ice-g2p/main.py -i 'hljóðrita þetta takk' -k -y '.' -s '.' -t
	hljóðrita þetta takk : l_0 j ou1 D . r I0 . t a0 . T E1 h . t a0 . t_h a1 h k

Using the `-l` flag allows for word-based language detection, where words considered foreign are transcribed by an LSTM trained on English words instead of Icelandic. If this flag is used, the module can handle common non-Icelandic characters, including all of the English alphabet:

    %python src/ice-g2p/main.py -i 'hljóðrita þetta please'
	l_0 j ou D r I t a T E h t a t_h a p_h l E: a s E
	
	%python src/ice-g2p/main.py -i 'hljóðrita þetta please' -l
	l_0 j ou D r I t a T E h t a p_h l i: s


## Data

The file [sampa_ipa_single_flite.tsv](https://github.com/grammatek/ice-g2p/tree/master/src/ice_g2p/data/sampa_ipa_single_flite.tsv) contains all the phonetic alphabets that have been used in Icelandic speech technology projects 
with in the language technology program. 

* [X-SAMPA](https://en.wikipedia.org/wiki/X-SAMPA)
* [IPA](https://www.internationalphoneticassociation.org/content/ipa-chart)
* Single: A custom alphabet designed to only contain one character per phone
* Flite: A custom alphabet for Festival/Flite that only contains ascii alphabetic characters (no ':', '_', or digits)


## Trouble shooting & inquiries

This application is still in development. If you encounter any errors, feel free to open an issue inside the
[issue tracker](https://github.com/grammatek/ice-g2p/issues). You can also [contact us](mailto:info@grammatek.com) via email.

## Contributing

You can contribute to this project by forking it, creating a private branch and opening a new [pull request](https://github.com/grammatek/ice-g2p/pulls).  

## License

[![Grammatek](grammatek-logo-small.png)](https://www.grammatek.com)

Copyright © 2020, 2021 Grammatek ehf.

This software is developed under the auspices of the Icelandic Government 5-Year Language Technology Program, described
[here](https://www.stjornarradid.is/lisalib/getfile.aspx?itemid=56f6368e-54f0-11e7-941a-005056bc530c) and
[here](https://clarin.is/media/uploads/mlt-en.pdf) (English).

This software is licensed under the [Apache License](LICENSE)
