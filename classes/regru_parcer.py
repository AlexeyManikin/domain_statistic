# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Alexey Y Manikin'

import urllib2
import re
from helpers.helpers import get_mysql_connection
import MySQLdb
import traceback


# Данный медот очень устарелый - скопипастил его для проверки результатов
# и совместимости со старой версией


class RegruParcer(object):

    URL_REG_RU = 'http://statonline.ru/dns?tld=ru&sort_field=domains_count&page=1&order=' \
                 'DESC&rows_per_page=200&dns_by_prov=1'

    def __init__(self):
        self.connection = get_mysql_connection()
        pass

    @staticmethod
    def download_data():
        """
        Скачивает данные с statonline.ru
        :rtype: unicode|bool
        """
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'}
        try:
            req = urllib2.Request(RegruParcer.URL_REG_RU, None, headers)
            response = urllib2.urlopen(req)
            if int(response.getcode()) == 200:
                return response.read()
            else:
                return False
        except urllib2.URLError:
            return False

    @staticmethod
    def get_array_info(data):
        """
        Переписываем с PHP и стараемся не думать, что тут делается
        :type data: unicode
        :rtype: list
        """
        re_domain_table = re.compile(r'for_expander.*?>(.*)</table>', re.IGNORECASE | re.DOTALL | re.UNICODE)
        re_tag_value = re.compile(r'<TAG>(.*?)</TAG>', re.IGNORECASE | re.DOTALL | re.UNICODE)

        re_td_open = re.compile(r'<tdclass=".*?">', re.IGNORECASE | re.DOTALL | re.UNICODE)
        re_td_close = re.compile(r'</td>', re.IGNORECASE | re.DOTALL | re.UNICODE)
        re_span_open = re.compile(r'<spanclass=".*?">', re.IGNORECASE | re.DOTALL | re.UNICODE)
        re_span_close = re.compile(r'</span>', re.IGNORECASE | re.DOTALL | re.UNICODE)

        dns_provider = []

        try:
            title = re.findall(re_domain_table, data)[0]
            title = re.sub(r' ', '', title)
            title = re.sub("\n", '', title)
            title = re.sub(r'<trclass="">', '', title)
            title = re.sub(r'</tr>', "\n", title)

            title = re.sub(re_td_open, "<TAG>", title)
            title = re.sub(re_td_close, "</TAG>", title)
            title = re.sub(re_span_open, "", title)
            title = re.sub(re_span_close, "", title)
            title = re.sub(r'&nbsp;', '', title)

            strings = title.split("\n")
            for string in strings:
                try:
                    list = re.findall(re_tag_value, string)
                    provider = {'position': int(list[1]),
                                'name': list[2],
                                'domain': int(list[3]),
                                'diff': int(list[4]),
                                'percent': float(list[5])}
                    dns_provider.append(provider)
                except Exception:
                    continue

            return dns_provider
        except Exception:
            return []

    def insert_array_in_base(self, array):
        """
        Запись в БД новых значений
        :type array: list
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        for provider in array:
            try:
                cursor.execute("SELECT id FROM regru_providers WHERE name = LOWER('%s')" % provider['name'])
                provider_id = cursor.fetchone()
                if not provider_id:
                    cursor.execute("INSERT INTO regru_providers (date_create, name, link)"\
                                    " VALUE (CURDATE(), LOWER('%s'), LOWER('%s'))" % (provider['name'], provider['name']))
                    self.connection.commit()
                    cursor.execute("SELECT id FROM regru_providers WHERE name = LOWER('%s')" % provider['name'])
                    provider_id = cursor.fetchone()

                if provider_id:
                    provider_id = provider_id['id']
                    cursor.execute("INSERT INTO regru_stat_data (date, provider_id, value)"\
                                   " VALUE (CURDATE(), '%s', '%s')" % (provider_id, provider['domain']))
                    self.connection.commit()
                else:
                    print "Error"

            except Exception:
                print traceback.format_exc()
                continue

    def run(self):
        """
        Функция обновления данных
        :rtype: bool
        """

        site_data = self.download_data()
        if not site_data:
            print "Not site data"
            return False

        array_info = self.get_array_info(site_data)
        if not array_info:
            print "Not array info"
            return False

        self.insert_array_in_base(array_info)
        return True
