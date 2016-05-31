# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'alexeyymanikin'

import re
import dns.resolver
import MySQLdb
import pprint
import urllib2
import traceback
import time

from helpers.helperUnicode import as_default_string
from helpers.helpers import get_mysql_connection
from config.main import MAX_AS_NUMBER


class AsInet(object):

    URL_AS_INFO = 'http://www.cidr-report.org/as2.0/autnums.html'

    def __init__(self):
        """
        :return:
        """
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 1
        self.resolver.lifetime = 1

        self.re_plus = re.compile('\s+')
        self.re_all = re.compile('\s*')

        self.connection = get_mysql_connection()

    def __del__(self):
        """
        Подчисщаем за собой все
        :return:
        """
        self.connection.close()

    @staticmethod
    def download_data():
        """
        Скачивает данные http
        :rtype: unicode|bool
        """
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'}
        try:
            req = urllib2.Request(AsInet.URL_AS_INFO, None, headers)
            response = urllib2.urlopen(req)
            if int(response.getcode()) == 200:
                return response.read()
            else:
                return False
        except urllib2.URLError:
            return False

    def _get_all_as_info(self):
        """
        Получаем список всех AS с их описанием с сайта
        http://www.cidr-report.org/as2.0/autnums.html
        https://github.com/AlexeyManikin/domain_statistic/issues/1
        пример строки <a href="/cgi-bin/as-report?as=AS0&view=2.0">AS0    </a> -Reserved AS-, ZZ
        :rtype: dict
        """

        re_domain_table = re.compile(r'<PRE>(.*)</PRE>', re.IGNORECASE | re.DOTALL | re.UNICODE)
        re_parce_data = re.compile(r'>(.*)</a> (.*), (.*)', re.IGNORECASE | re.DOTALL | re.UNICODE)
        re_parce_as = re.compile(r'AS([0-9]*)', re.IGNORECASE | re.DOTALL | re.UNICODE)

        return_array = {}
        data = AsInet.download_data()

        try:
            tag_pre = re.findall(re_domain_table, data)
            strings = as_default_string(tag_pre[0]).split(as_default_string("\n"))

            for string in strings:
                try:
                    result = re.findall(re_parce_data, string)
                    as_num = re.findall(re_parce_as, result[0][0])

                    as_desc = "%s" % result[0][1]
                    as_country = "%s" % result[0][2]

                    return_array[int(as_num[0])] = {'as': as_num[0],
                                                    'descriptions': as_desc,
                                                    'country': as_country}
                except:
                    # Ошибка UnicodeDecodeError - ну и ладно
                    pass

            return return_array
        except Exception:
            print(traceback.format_exc())
            return []

    def parsing_as(self, show_log=False, max_as=MAX_AS_NUMBER):
        """
        парсим названия AS
        :type show_log:  bool
        :type max_as: int
        :return:
        """

        as_data = self._get_all_as_info()
        for i in range(1, max_as):
            self.update_as(i, as_data,  show_log=show_log)

    def _get_asn_description(self, number):
        """
        :type number: int
        :return:
        """
        answers = self.resolver.query('AS' + str(number) + '.asn.cymru.com', 'TXT')
        asn_name = re.sub(r'"', '', answers[0].to_text())
        list_as_info = asn_name.split('|')

        try:
            description = re.sub(self.re_plus, ' ', list_as_info[4])
        except IndexError:
            description = ''

        try:
            date_register = re.sub(self.re_all, '', list_as_info[3])
        except IndexError:
            date_register = ''

        try:
            country = re.sub(self.re_plus, '', list_as_info[1])
        except IndexError:
            country = ''

        return {'AS': re.sub(self.re_plus, ' ', list_as_info[0]),
                'COUNTRY': country,
                'ORGANIZATION': re.sub(self.re_plus, ' ', list_as_info[2]),
                'DATE_REGISTER': date_register,
                'DESCRIPTION': description,
                'USE_FAST': 0}

    def update_as(self, number, as_data, show_log=False):
        """
        Обновляем информацию об AS в базе данных
        :type number: int
        :type as_data: dict
        :return:
        """

        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute("SELECT COUNT(*) as count FROM as_list WHERE id = %s" % str(number))
        except:
            self.connection = get_mysql_connection()
            cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT COUNT(*) as count FROM as_list WHERE id = %s" % str(number))

        count = cursor.fetchone()

        if number in as_data and count['count'] != 0:
            as_info = {'AS': number,
                       'COUNTRY': as_data[number]['country'],
                       'ORGANIZATION': '',
                       'DATE_REGISTER': '',
                       'DESCRIPTION': as_data[number]['descriptions'],
                       'USE_FAST': 1}
        else:
            try:
                time.sleep(1)
                as_info = self._get_asn_description(number)
            except:
                as_info = {'AS': number,
                           'COUNTRY': '',
                           'ORGANIZATION': '',
                           'DATE_REGISTER': '',
                           'DESCRIPTION': '',
                           'USE_FAST': 0}

        if show_log:
            print("AS Number %s" % number)
            pprint.pprint(as_info)

        if as_info['DATE_REGISTER'] == '':
            as_info['DATE_REGISTER'] = '2001-01-01'

        if as_info['COUNTRY'] == '':
            as_info['COUNTRY'] = 'undef'

        if as_info['ORGANIZATION'] == '':
            as_info['ORGANIZATION'] = 'undef'

        if count['count'] == 0:
            cursor.execute(
                """INSERT INTO as_list(id,
                                       descriptions,
                                       country,
                                       date_register,
                                       organization_register)
                   VALUE(%s, %s, %s, %s, %s)""", (str(number),
                                                  as_info['DESCRIPTION'],
                                                  as_info['COUNTRY'],
                                                  as_info['DATE_REGISTER'],
                                                  as_info['ORGANIZATION']))
        else:
            if as_info['USE_FAST'] == 0:
                cursor.execute(
                    """UPDATE  as_list SET
                                          descriptions = %s,
                                          country = %s,
                                          date_register = %s,
                                          organization_register = %s
                       WHERE id = %s""", (as_info['DESCRIPTION'],
                                          as_info['COUNTRY'],
                                          as_info['DATE_REGISTER'],
                                          as_info['ORGANIZATION'],
                                          str(number)))
            else:
                cursor.execute(
                    """UPDATE  as_list SET
                                          descriptions = %s,
                                          country = %s
                       WHERE id = %s""", (as_info['DESCRIPTION'],
                                          as_info['COUNTRY'],
                                          str(number)))
        self.connection.commit()
        return True
