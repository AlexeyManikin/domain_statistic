# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'alexeyymanikin'

import sys
import os

PROGRAM_NAME = 'update_as_info'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, CURRENT_DIR)
logfile = os.path.join(CURRENT_DIR, '%s.debug' % PROGRAM_NAME)

import traceback
from classes.asInet import AsInet


if __name__ == "__main__":
    try:
        as_parser = AsInet()
        as_parser.parsing_as(show_log=False)
    except Exception as e:
        print "Got an exception: %s" % e.message
        print traceback.format_exc()
