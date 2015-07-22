# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'alexeyymanikin'

import sys
from config.main import *

PROGRAM_NAME = 'delete_domain'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, CURRENT_DIR)
logfile = os.path.join(CURRENT_DIR, '%s.debug' % PROGRAM_NAME)

import traceback
from helpers.helpers import check_prog_run
from classes.resolver import Resolver


def print_log(log_flag, text):
    """
    Выводим сообщение в консоль или лог
    :type log_flag: bool
    :type text: unicode
    :return:
    """
    if log_flag:
        print text

if __name__ == "__main__":
    show_log = True
    try:
        if check_prog_run(PROGRAM_NAME):
            print "Program %s already running" % PROGRAM_NAME
            sys.exit(1)

        Resolver.delete_not_updated_today()

    except Exception as e:
        print "Got an exception: %s" % e.message
        print traceback.format_exc()
