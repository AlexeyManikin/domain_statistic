# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Alexey Y Manikin'

from helpers.helpers import get_mysql_connection
import MySQLdb
import multiprocessing
import datetime
from config.main import MINIMUM_DOMAIN_COUNT


class NsDomainOldCountStatistic(multiprocessing.Process):

    def __init__(self, number, data, today, zone):
        """
        :param number:
        """
        multiprocessing.Process.__init__(self, name="ns_domain_old_count_%s" % number)
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

    def _update_ns_domain_old_count_per_zone(self, date, today, zone):
        """
        :type date: date
        :type today: date
        :type zone: unicode
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            ns_list = {}

            for i in [1, 2, 3, 4]:
                sql = """SELECT ns%s as ns, AVG(DATEDIFF(NOW(), register_date)) as old, count(*) as count
    FROM domain_history
    WHERE tld = '%s' AND date_start <= '%s' AND date_end >= '%s' AND delegated = 'Y'
    GROUP BY ns%i
    HAVING count(*) > %s
    ORDER BY count(*) desc""" % (i, zone, date, date, i, MINIMUM_DOMAIN_COUNT)
                cursor.execute(sql)
                data = cursor.fetchall()
                for row in data:
                    if row['ns'] not in ns_list:
                        ns_list[row['ns']] = []
                    ns_list[row['ns']].append({'i': i,
                                               'old': row['old'],
                                               'count': row['count']})

            sql_insert = ""

            for key in ns_list:
                summary_value = 0
                summary_count = 0
                for item in ns_list[key]:
                    summary_value = summary_value + item['old'] * item['count']
                    summary_count = summary_count + item['count']

                if summary_count == 0:
                    summary_count = 1

                old = round((summary_value / summary_count), 2)

                sql_insert_date = " ('%s','%s','%s','%s')" % (date, key, zone, old)
                if len(sql_insert) > 5:
                    sql_insert += ', ' + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            sql = 'INSERT INTO ns_domain_old_count_statistic(`date`, `ns`, `tld`, `old`) VALUE ' + sql_insert
            cursor.execute(sql)
            date += datetime.timedelta(days=1)

    def run(self):
        """
        Обрабатываем массив записываем в БД
        :return:
        """
        self._connect_mysql()
        self._update_ns_domain_old_count_per_zone(self.data, self.today, self.zone)
        self.connection.commit()
        self.connection.close()
