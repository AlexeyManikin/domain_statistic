# -*- coding: utf-8 -*-
__author__ = 'Alexey Y Manikin'

import sys
import os

PROGRAM_NAME = 'normalizate'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, CURRENT_DIR)
logfile = os.path.join(CURRENT_DIR, '%s.debug' % PROGRAM_NAME)

import traceback
from classes.normalizate import DbNormalization


if __name__ == "__main__":
    try:
        norm = DbNormalization(show_log=True)
        norm.normalization_db()
    except Exception as e:
        print((traceback.format_exc()))
