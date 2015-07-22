# -*- coding: utf-8 -*-
# Project server.pyportal
from __future__ import unicode_literals

__author__ = 'alexeyymnaikin'

import os

# Default logger
CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))+'/../')
MAX_AS_NUMBER = 300000

PREFIX_LIST = ['ru', 'su', 'rf']
DEFAULT_TIMEOUT = 5.0

MYSQL_HOST = 'db'
MYSQL_PORT = 3306
MYSQL_USER = 'domain_statistic'
MYSQL_PASSWD = 'domain_statisticdomain_statistic'
MYSQL_DATABASE = 'domain_statistic'

COUNT_THREAD = 200
