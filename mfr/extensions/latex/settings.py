import os

try:
    from mfr import settings
except ImportError:
    settings = {}

config = settings.get('LATEX_EXTENSION_CONFIG', {})

PDFLATEX_BIN = config.get('PDFLATEX_BIN', 'pdflatex')
RERUN_STRING = b'Rerun to get cross-references right.'
MAX_RUN_TIMES = 2

RENDERER = '.pdf'
FORMAT = 'pdf'
