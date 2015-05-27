# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'alexeyymanikin'

import re
import dns.resolver
import MySQLdb
import pprint
from helpers.helpers import get_mysql_connection


class AsInet(object):

    def __init__(self, mysql_connection=False):
        """
        :param mysql_connection:
        :return:
        """
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 1
        self.resolver.lifetime = 1

        self._connect_mysql(mysql_connection)

    def _connect_mysql(self, connection=False):
        """
        :param connection:
        :return:
        """
        if connection:
            self.connection = connection
        else:
            self.connection = get_mysql_connection()

    def _get_asn_descrption(self, number):
        """
        :type number: int
        :return:
        """
        answers = self.resolver.query('AS' + str(number) + '.asn.cymru.com', 'TXT')
        asn_name = re.sub(r'"', '', answers[0].to_text())
        list = asn_name.split('|')

        try:
            description = re.sub(r'\s+', ' ', list[4])
        except IndexError:
            description = ''

        try:
            date_registry = re.sub(r'\s*', '', list[3])
        except IndexError:
            date_registry = ''

        try:
            contry = re.sub(r'\s+', '', list[1])
        except IndexError:
            contry = ''

        return {'AS': re.sub(r'\s+', ' ', list[0]),
                'CONTRY': contry,
                'ORGANIZATION': re.sub(r'\s+', ' ', list[2]),
                'DATEREGISTER': date_registry,
                'DESCRIPTION': description}

    def update_as(self, number, show_log=False):
        """
        Обновляем информацию об AS в базе данных
        :type number: int
        :return:
        """

        try:
            as_info = self._get_asn_descrption(number)
        except:
            as_info = {'AS': number,
                       'CONTRY': '',
                       'ORGANIZATION': '',
                       'DATEREGISTER': '',
                       'DESCRIPTION': ''}

        if show_log:
            print "AS Number %s" % number
            pprint.pprint(as_info)

        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute("SELECT COUNT(*) as count FROM as_list WHERE id = %s" % str(number))
        except:
            self._connect_mysql()
            cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT COUNT(*) as count FROM as_list WHERE id = %s" % str(number))

        count = cursor.fetchone()

        if as_info['DATEREGISTER'] == '':
            as_info['DATEREGISTER'] = '2001-01-01'

        if as_info['CONTRY'] == '':
            as_info['CONTRY'] = 'undef'

        if as_info['ORGANIZATION'] == '':
            as_info['ORGANIZATION'] = 'undef'

        if count['count'] == 0:
            cursor.execute(
                """INSERT INTO as_list(id,
                                       descriptions,
                                       contry,
                                       date_register,
                                       organization_register)
                   VALUE(%s, %s, %s, %s, %s)""", (str(number),
                                                  as_info['DESCRIPTION'],
                                                  as_info['CONTRY'],
                                                  as_info['DATEREGISTER'],
                                                  as_info['ORGANIZATION']))
            self.connection.commit()

        else:
            cursor.execute(
                """UPDATE  as_list SET
                                      descriptions = %s,
                                      contry = %s,
                                      date_register = %s,
                                      organization_register = %s
                   WHERE id = %s""", (as_info['DESCRIPTION'],
                                      as_info['CONTRY'],
                                      as_info['DATEREGISTER'],
                                      as_info['ORGANIZATION'],
                                      str(number)))
            self.connection.commit()

        return True



