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
MYSQL_USER = 'domain_statistic'
MYSQL_PASSWD = '12345678'
MYSQL_DATABASE = 'domain_statistic'

PRKI_JSON_URL = 'http://rpki:8080/export.json'

COUNT_THREAD = 450
MAX_DOMAIN_COUNT = 10000000

START_YEAR = 2020
START_MONTH = 4
START_DAY = 3
