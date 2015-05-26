# -*- coding: utf-8 -*-
# Project server.pyportal
from __future__ import unicode_literals

__author__ = 'alexeyymnaikin'

import os
import getpass

# Default logger
CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))+'/../')
MAX_AS_NUMBER = 500000

MYSQL_HOST = '192.168.2.240'
MYSQL_PORT = '13307'
MYSQL_USER = 'domain_statistic'
MYSQL_PASSWD = 'domain_statisticdomain_statistic'
MYSQL_DATABASE = 'domain_statistic'

COUNT_THREAD = 150
