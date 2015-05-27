# -*- coding: utf-8 -*-
# Project server.pyportal
from __future__ import unicode_literals

__author__ = 'alexeyymnaikin'

import os
import getpass

# Default logger
CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))+'/../')
MAX_AS_NUMBER = 500000

PREFIX_LIST = ['ru', 'su', 'rf']

MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = 'passwd'
MYSQL_DATABASE = 'domain_statistic'

COUNT_THREAD = 120
