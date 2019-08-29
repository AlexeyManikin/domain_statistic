# -*- coding: utf-8 -*-
__author__ = 'Alexey Y Manikin'

import sys
from config.main import *
import traceback

PROGRAM_NAME = 'update_statistic'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, CURRENT_DIR)
logfile = os.path.join(CURRENT_DIR, '%s.debug' % PROGRAM_NAME)

from classes.statistic import Statistic


if __name__ == "__main__":
    try:
        statistic = Statistic()
        statistic.update_all_statistic()
    except Exception as e:
        print((traceback.format_exc()))
