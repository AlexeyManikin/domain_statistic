# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'alexeyymanikin'


import sys
import os

PROGRAM_NAME = 'update_as_info'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, CURRENT_DIR)
logfile = os.path.join(CURRENT_DIR, '%s.debug' % (PROGRAM_NAME))

import traceback
from classes.asInet import AsInet
from config.main import MAX_AS_NUMBER


if __name__ == "__main__":
    try:
        asparcer = AsInet()
        for i in range(1, MAX_AS_NUMBER):
            asparcer.update_as(i, show_log=True)
    except Exception as e:
        print "Got an exception: %s" % e.message
        print traceback.format_exc()
# EOF