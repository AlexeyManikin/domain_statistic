__author__ = 'Alexey Y Manikin'

import sys
import os

PROGRAM_NAME = 'update_rpki_history'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, CURRENT_DIR)
logfile = os.path.join(CURRENT_DIR, '%s.debug' % PROGRAM_NAME)

import traceback
from classes.rpkiCheker import RpkiChecker


if __name__ == "__main__":
    try:
        checker = RpkiChecker()
        checker.update_base()
    except Exception as e:
        print(("Got an exception: %s" % e))
        print((traceback.format_exc()))
