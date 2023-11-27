"""
Fetch the models at MODELS_URL and store them in MODELS_DIR, where the g2p-transcriber finds them.
"""

import os
import urllib.error
import zipfile
from io import BytesIO
from urllib.request import urlopen
from logging import getLogger

log = getLogger(__name__)
MODELS_URL = "https://github.com/grammatek/ice-g2p/releases/download/v1.2.0/ice-g2p-models.zip"
MODELS_DIR = 'fairseq_models'


def load_models():
    log.info(f'Downloading models from {MODELS_URL} ...')
    general_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), MODELS_DIR)
    try:
        with urlopen(MODELS_URL) as downl_file:
            zip_file = zipfile.ZipFile(BytesIO(downl_file.read()))
            log.debug("Extracting model ...")
            zip_file.extractall(general_model_path)
            log.debug("models extracted")
    except urllib.error.HTTPError:
        log.error(f'Could not download models from {MODELS_URL}')
        raise
    except urllib.error.URLError:
        log.error(f'Could not download models from {MODELS_URL}')
        raise


def main():
    load_models()


if __name__ == '__main__':
    main()