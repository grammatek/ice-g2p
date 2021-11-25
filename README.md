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

To transcribe text, currently two main options are available, direct from stdin to stdout or from file or a collection of files (directory) 

    %python src/main.py -i 'hljóðrita þetta takk'
	l_0 j ou D r I t a T E h t a t_h a h k

	%python src/main.py -if file_to_transcribe.txt

If the input comes from stdin, the output is written to stdout. Input from file(s) is written to file(s) with the same name with the suffix '_transcribed.tsv' in a two-column format. The files are transcribed line by line and written out with the original string (line) in the first column and the phonetic transcription in the second column. This approach is thus applicable both to word lists where a pronunciation dictionary would be the output, and e.g. TTS training data.

## Coming up
This is a repository in development and more options will be added step by step, e.g. the option to use a pronunciation dictionary for the transcription and/or to add syllabification and stress labeling to the output.

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
