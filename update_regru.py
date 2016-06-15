# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Alexey Y Manikin'

import sys
from config.main import *

PROGRAM_NAME = 'update_regru'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, CURRENT_DIR)
logfile = os.path.join(CURRENT_DIR, '%s.debug' % PROGRAM_NAME)

import traceback
from helpers.helpersCollor import BColor
from classes.regru_parcer import RegruParcer
from helpers.helperUnicode import as_default_string


def save(data, file_name):
    """
    :param data:
    :param file_name:
    :return:
    """
    saved_file = open(file_name, 'w')
    saved_file.write(as_default_string(data))
    saved_file.close()


def load(file_name):
    """
    :param file_name:
    :return:
    """
    as_list_file = open(file_name, 'r')
    return_data = as_list_file.read()
    return return_data

if __name__ == "__main__":
    try:
        regru = RegruParcer()
        regru.run()
    except Exception as e:
        BColor.error("Got an exception: %s" % e.message)
        print(traceback.format_exc())
