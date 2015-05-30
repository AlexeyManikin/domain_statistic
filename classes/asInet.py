# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'alexeyymanikin'

import re
import dns.resolver
import MySQLdb
import pprint
from helpers.helpers import get_mysql_connection
from config.main import MAX_AS_NUMBER


class AsInet(object):

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

    def parsing_as(self, show_log=False, max_as=MAX_AS_NUMBER):
        """
        парсим названия AS
        :type show_log:  bool
        :type max_as: int
        :return:
        """
        for i in range(1, max_as):
            self.update_as(i, show_log=show_log)

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
                'DESCRIPTION': description}

    def update_as(self, number, show_log=False):
        """
        Обновляем информацию об AS в базе данных
        :type number: int
        :return:
        """

        try:
            as_info = self._get_asn_description(number)
        except:
            as_info = {'AS': number,
                       'COUNTRY': '',
                       'ORGANIZATION': '',
                       'DATE_REGISTER': '',
                       'DESCRIPTION': ''}

        if show_log:
            print "AS Number %s" % number
            pprint.pprint(as_info)

        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute("SELECT COUNT(*) as count FROM as_list WHERE id = %s" % str(number))
        except:
            self.connection = get_mysql_connection()
            cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT COUNT(*) as count FROM as_list WHERE id = %s" % str(number))

        count = cursor.fetchone()

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
        self.connection.commit()
        return True
