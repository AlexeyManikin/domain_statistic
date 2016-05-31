# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Alexey Y Manikin'

from helpers.helpers import get_mysql_connection
import datetime
import MySQLdb

# https://habrahabr.ru/post/95148/
# https://github.com/adamn/python-webkit2png

class Screenshoter(object):
    def __init__(self):
        pass