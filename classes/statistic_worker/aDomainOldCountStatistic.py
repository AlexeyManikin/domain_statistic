# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Alexey Y Manikin'

from helpers.helpers import get_mysql_connection
import MySQLdb
import multiprocessing
import datetime
from config.main import MINIMUM_DOMAIN_COUNT


class ADomainOldCountStatistic(multiprocessing.Process):

    def __init__(self, number, data, today, zone):
        """
        :param number:
        """
        multiprocessing.Process.__init__(self, name="a_domain_old_count_%s" % number)
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

    def _update_a_domain_old_count_per_zone(self, date, today, zone):
        """
        Особого смысла смотреть по всем 4 а записям не вижу, только лишняя нагрузка на базу. На данные
        статистики почти не влияет.
        :type date: date
        :type today: date
        :type zone: unicode
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            sql_insert = ""
            sql = """SELECT a1 as a, AVG(DATEDIFF(NOW(), register_date)) as old, count(*) as count
FROM domain_history
WHERE tld = '%s' AND date_start <= '%s' AND date_end >= '%s' AND delegated = 'Y'
GROUP BY a1
HAVING count(*) > %s
ORDER BY count(*) desc""" % (zone, date, date, MINIMUM_DOMAIN_COUNT)

            cursor.execute(sql)
            data = cursor.fetchall()

            for row in data:
                sql_insert_date = " ('%s','%s','%s','%s')" % (date, row['a'], zone, row['old'])
                if len(sql_insert) > 5:
                    sql_insert += ', ' + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            sql = 'INSERT INTO a_domain_old_count_statistic(`date`, `a`, `tld`, `old`) VALUE ' + sql_insert
            cursor.execute(sql)
            date += datetime.timedelta(days=1)

    def run(self):
        """
        Обрабатываем массив записываем в БД
        :return:
        """
        self._connect_mysql()
        self._update_a_domain_old_count_per_zone(self.data, self.today, self.zone)
        self.connection.commit()
        self.connection.close()
