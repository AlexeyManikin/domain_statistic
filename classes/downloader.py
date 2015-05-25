# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'alexeyymanikin'

import datetime
from config.main import *
from classes.command.wget import Wget
from helpers.helpers import *
import shutil


class Downloader(object):

    def __init__(self):
        pass

    @staticmethod
    def create_data_dir():
        """
        Создает директорию с текущей датой в download
        :rtype: unicode
        """
        download_path = os.path.abspath(os.path.join(CURRENT_PATH, 'download'))
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        date_string = datetime.date.fromtimestamp(time.time()).isoformat()
        date_path = os.path.abspath(os.path.join(download_path, date_string))
        if not os.path.exists(date_path):
            os.makedirs(date_path)

        return date_path

    @staticmethod
    def download_file(url, data_dir):
        """
        Скачивает файл в указанную директорию
        :type url: unicode
        :type data_dir: unicode
        :rtype: bool
        """

        rsync = Wget(url, data_dir)
        command = rsync.get_command()

        p = SubprocessRunner(command=command)
        p.run()
        p.wait(write_output_in_log=False)
        if p.process.returncode != 0:
            return False

        return True

    def download_data_for_current_date(self):
        """
        Скачивает все необходимы файлы для парсинга

        С R01 данные по локальным зонам
        https://partner.r01.ru/zones/ru_domains.gz
        https://partner.r01.ru/zones/su_domains.gz
        https://partner.r01.ru/zones/rf_domains.gz

        С http://archive.routeviews.org информацию по fullview, подробно описывает Павел в своем блоге
        http://phpsuxx.blogspot.com/2011/12/full-bgp.html
        http://phpsuxx.blogspot.com/2011/12/libbgpdump-debian-6-squeeze.html
        :rtype: unicode
        """
        now_date = datetime.date.today()
        delta = datetime.timedelta(days=1)
        now_date = now_date - delta

        files_list = [{'url': 'https://partner.r01.ru/zones/ru_domains.gz', 'file_name': 'ru_domains.gz'},
                      {'url': 'https://partner.r01.ru/zones/su_domains.gz', 'file_name': 'su_domains.gz'},
                      {'url': 'https://partner.r01.ru/zones/rf_domains.gz', 'file_name': 'rf_domains.gz'},
                      {'url': 'http://archive.routeviews.org/bgpdata/%s/RIBS/rib.%s.0600.bz2'
                               % (now_date.strftime("%Y.%m"), now_date.strftime("%Y%m%d")), 'file_name': 'rib.bz2'}]

        path = self.create_data_dir()

        for item in files_list:
            path_file = os.path.abspath(os.path.join(path, item['file_name']))
            print "Download %s to %s " % (item['url'], path_file)
            shutil.rmtree(path_file, ignore_errors=True)
            self.download_file(item['url'], path_file)
            if os.path.getsize(path_file) == 0:
                raise Exception("Can`t download file %s to %s" % (item['url'], path_file))

        return path
