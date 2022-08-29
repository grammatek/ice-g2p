"""G2P for Icelandic

Copyright (C) 2022 Grammatek ehf.

License: Apache 2.0 (see: LICENSE)
This package uses 3rd party submodules that might be published under other comparable open licenses.

This module is a grapheme-to-phoneme (g2p) program for Icelandic.
"""
import pathlib

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='ice-g2p',
    version='0.1.0',

    description='A grapheme-to-phoneme (g2p) converter for Icelandic',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/grammatek/ice-g2p',
    author='Grammatek ehf.',
    author_email='info@grammatek.com',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Topic :: Text Processing :: Linguistic',
        'Natural Language :: Icelandic',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='g2p, grapheme-to-phoneme, text-processing, asr, tts',

    include_package_data=True,
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',

    entry_points={
        'console_scripts': [
            'transcribe=ice_g2p.main:main',
        ],
    },
)
