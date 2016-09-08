# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Alexey Y Manikin'

from helpers.helpers import get_mysql_connection
import MySQLdb
import multiprocessing


class GroupProviderStatistic(multiprocessing.Process):

    def __init__(self, number, key, data, zone, date):
        """
        :param number:
        """
        multiprocessing.Process.__init__(self, name="resolver_%s" % number)
        self.number = number
        self.connection = None
        self.key = key
        self.data = data
        self.date = date
        self.zone = zone

    def _connect_mysql(self):
        """
        :return:
        """
        self.connection = get_mysql_connection()

    def run(self):
        """
        Обрабатываем массив записываем в БД
        :return:
        """
        search_string = '.' + self.key + '.'
        count = 0

        for row in self.data:

            if 'ns1' in row and row['ns1'] is not None and search_string in row['ns1']:
                count += 1
            elif 'ns2' in row and row['ns2'] is not None and search_string in row['ns2']:
                count += 1
            elif 'ns3' in row and row['ns3'] is not None and search_string in row['ns3']:
                count += 1
            elif 'ns4' in row and row['ns4'] is not None and search_string in row['ns4']:
                count += 1

        sql_insert_date = " ('%s','%s','%s','%s')" % (self.date, self.key, self.zone, count)
        sql = 'INSERT INTO ns_domain_group_count_statistic(`date`, `ns_group`, `tld`, `count`) VALUE ' \
              + sql_insert_date

        print("process %s - sql %s" % (self.number, sql))

        self._connect_mysql()
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)
        self.connection.commit()
        self.connection.close()
