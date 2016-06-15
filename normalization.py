# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Alexey Y Manikin'

import sys
import os

PROGRAM_NAME = 'normalizate'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, CURRENT_DIR)
logfile = os.path.join(CURRENT_DIR, '%s.debug' % PROGRAM_NAME)

import traceback
from classes.normalizate import DbNormalizate


if __name__ == "__main__":
    try:
        norm = DbNormalizate(show_log=True)
        norm.normalization_db()
    except Exception as e:
        print("Got an exception: %s" % e.message)
        print(traceback.format_exc())