# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'alexeyymanikin'

import os
import types

class Downloader(object):

    def __init__(self):
        pass

    def create_data_dir(self):
        """
        Создает директорию с текущей датой в download
        :rtype: unicode
        """
        pass

    def download_file(self, url, data_dir):
        """
        Скачивает файл в указанную директорию
        :type url: unicode
        :type data_dir: unicode
        :rtype: bool
        """
        pass
