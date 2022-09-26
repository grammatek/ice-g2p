"""G2P for Icelandic

Copyright (C) 2022 Grammatek ehf.

License: Apache 2.0 (see: LICENSE)
This package uses 3rd party submodules that might be published under other comparable open licenses.

This module is a grapheme-to-phoneme (g2p) program for Icelandic.
The _post_install() only gets called when installing from repository via setup.py install.
If installing from pip, it is necessary to run `fetch_models` before running g2p.

"""
import os
import urllib.error
import zipfile
from io import BytesIO
from urllib.request import urlopen
from logging import getLogger
from setuptools import setup

MODEL_URL = "https://github.com/grammatek/ice-g2p/releases/download/v1.1/ice-g2p-models.zip"

log = getLogger(__name__)


def _post_install():
    log.info(f'Downloading models from {MODEL_URL} ...')
    general_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fairseq_models')
    try:
        with urlopen(MODEL_URL) as downl_file:
            zip_file = zipfile.ZipFile(BytesIO(downl_file.read()))
            log.debug("Extracting model ...")
            zip_file.extractall(general_model_path)
            log.debug("models extracted")
    except urllib.error.HTTPError:
        log.error(f'Could not download models from {MODEL_URL}')
        raise
    except urllib.error.URLError:
        log.error(f'Could not download models from {MODEL_URL}')
        raise


setup()

_post_install()