# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Alexey Y Manikin'

from helpers.helpers import get_mysql_connection
import MySQLdb
import multiprocessing
import datetime
from config.main import MINIMUM_DOMAIN_COUNT


class ACountStatistic(multiprocessing.Process):

    def __init__(self, number, data, today, zone):
        """

        :param number:
        """
        multiprocessing.Process.__init__(self, name="a_count_%s" % number)
        self.number = number
        self.connection = None

        self.today = today
        self.data = data
        self.zone = zone

    def _connect_mysql(self):
        """
        :return:
        """
        self.connection = get_mysql_connection()

    def _update_a_count_per_zone(self, date, today, zone):
        """
        :type date: date
        :type today: date
        :type zone: unicode
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            sql_insert = ''
            a_array = {}
            asn_array = {}

            for i in range(1, 5):
                sql = """SELECT a%s as a, asn%s as asn, count(*) as count FROM domain_history
WHERE delegated = 'Y' AND tld = '%s' AND date_start <= '%s' AND date_end >= '%s'
GROUP BY a%s
HAVING count(*) > %s
ORDER BY count(*) desc""" % (i, i, zone, date, date, i, MINIMUM_DOMAIN_COUNT)

                cursor.execute(sql)
                data = cursor.fetchall()

                for row in data:
                    if row['a'] in a_array:
                        a_array[row['a']] += row['count']
                    else:
                        a_array[row['a']] = row['count']

                for row in data:
                    if row['asn'] is None:
                        asn = 0
                    else:
                        asn = row['asn']

                    asn_array[row['a']] = asn

            for key in a_array:
                if key in asn_array:
                    asn = asn_array[key]
                else:
                    asn = 0

                sql_insert_date = " ('%s','%s','%s', '%s', '%s')" % (date, zone, key, a_array[key], asn)
                if len(sql_insert) > 5:
                    sql_insert += ', ' + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            sql = 'INSERT INTO a_count_statistic(`date`, `tld`, `a`, `count`, `asn`) VALUE ' + sql_insert
            cursor.execute(sql)
            date += datetime.timedelta(days=1)

    def run(self):
        """
        Обрабатываем массив записываем в БД
        :return:
        """

        self._connect_mysql()
        self._update_a_count_per_zone(self.data, self.today, self.zone)
        self.connection.commit()
        self.connection.close()
