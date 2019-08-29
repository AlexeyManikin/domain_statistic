# -*- coding: utf-8 -*-
__author__ = 'alexeyymnaikin'

import os

# Default logger
CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))+'/../')
MAX_AS_NUMBER = 450000
MINIMUM_DOMAIN_COUNT = 50

PREFIX_LIST_ZONE = {'ru': 0, 'su': 1, 'rf': 2}

DEFAULT_TIMEOUT = 3.0


MYSQL_HOST = 'db'
MYSQL_PORT = 3306
MYSQL_USER = 'DBUSER'
MYSQL_PASSWD = 'DBPASSWD'
MYSQL_DATABASE = 'domain_statistic'

PRKI_JSON_URL = 'http://rpki:8080/export.json'

COUNT_THREAD = 120

START_YEAR = 2019
START_MONTH = 8
START_DAY = 17
