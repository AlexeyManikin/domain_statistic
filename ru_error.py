# -*- coding: utf-8 -*-
__author__ = 'Alexey Y Manikin'

import sys
from config.main import *
from classes.ruErrorMove2 import RuErrorMove2
import traceback

PROGRAM_NAME = 'ru_error'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, CURRENT_DIR)
logfile = os.path.join(CURRENT_DIR, '%s.debug' % PROGRAM_NAME)


if __name__ == "__main__":
    try:
        ru_errors = RuErrorMove2()
        ru_errors.run()
    except Exception as e:
        print((traceback.format_exc()))
