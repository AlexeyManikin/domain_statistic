# -*- coding: utf-8 -*-
# Project server.pyportal
from __future__ import unicode_literals

__author__ = 'alexeyymnaikin'

import os
import getpass

# Default logger
CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))+'/../')
MAX_AS_NUMBER = 500000

MYSQL_HOST = '192.168.2.201'
MYSQL_USER = 'root'
MYSQL_PASSWD = '258da5c71b7d854456a7c89402f48593'
MYSQL_DATABASE = 'domain_statistic'

COUNT_THREAD = 50
