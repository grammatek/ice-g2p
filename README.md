# Ice-g2p : Phonetic transcription (grapheme-to-phoneme) for Icelandic

Ice-g2p is a module for automatic phonetic transcription of Icelandic.

## Setup

Clone the repository and create a virtual environment in the project root directory. Install the requirements:

    git clone git@github.com:grammatek/ice-g2p.git
	cd ice-g2p
	python -m venv g2p-venv
	source g2p-venv/bin/activate
	pip install -r requirements.txt



## Command line interface

**The input strings/texts need to be normalized. The module only handles lowercase characters from the Icelandic alphabet, no punctuation or other characters**

Characters allowed: _[aábcðdeéfghiíjklmnoóprstuúvxyýzþæö]_. If other characters are found in the input, the transcription of the respective token is skipped and a notice written to stdout.

To transcribe text, currently two main options are available, direct from stdin to stdout or from file or a collection of files (directory) 

    %python src/main.py -i 'hljóðrita þetta takk'
	l_0 j ou D r I t a T E h t a t_h a h k

	%python src/main.py -if file_to_transcribe.txt

If the input comes from stdin, the output is written to stdout. Input from file(s) is written to file(s) with the same name with the suffix '_transcribed.tsv'. The files are transcribed line by line and written out correspondingly. 

### Flags

The options available:

    --infile INFILE, -if INFILE
                        inputfile or directory
  	--inputstr INPUTSTR, -i INPUTSTR
                          input string
  	--keep, -k            keep original
  	--sep, -s             use word separator
	--dict, -d            use pronunciation dictionary

Using the `-k` flag keeps the original grapheme strings and for file input/output writes the original strings in the first column of the tab separated output file, and the phonetic transcription in the second one.
The `-s`flag adds a word separator to the transcription, necessary if the output is to be processed further e.g. through syllabification and stress labeling. With the `-d` flag all tokens are first looked up in an existing pronunciation dictionary, the automatic g2p is then only a fallback for words not contained in the dictionary.:

    %python src/main.py -i 'hljóðrita þetta takk' -k -s
	hljóðrita þetta takk : l_0 j ou D r I t a-T E h t a-t_h a h k


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
