# -*- coding: utf-8 -*-


__author__ = 'Alexey Y Manikin'

from helpers.helpers import get_mysql_connection
import MySQLdb
import multiprocessing
import datetime
from config.main import MINIMUM_DOMAIN_COUNT, PREFIX_LIST_ZONE


class AsCountStatistic(multiprocessing.Process):

    def __init__(self, number, data, today, zone):
        """

        :param number:
        """
        multiprocessing.Process.__init__(self, name="as_count_%s" % number)
        self.number = number
        self.connection = None

        self.today = today
        self.data = data
        self.zone = PREFIX_LIST_ZONE[zone]

    def _connect_mysql(self):
        """
        :return:
        """
        self.connection = get_mysql_connection()

    def _update_as_count_per_zone(self, date, today, zone):
        """
        :type date: date
        :type today: date
        :type zone: unicode
        :return:
        """

        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            sql_insert = ''
            as_array = {}

            sql = """SELECT asn1 as as_number, count(*) as count FROM domain_history
   WHERE delegated = 'Y' AND tld = %s AND date_start <= '%s' AND date_end > '%s'
   GROUP BY asn1
   HAVING count(*) > %s
   ORDER BY count(*) desc""" % (zone, date, date, MINIMUM_DOMAIN_COUNT)

            print(sql)

            cursor.execute(sql)
            data = cursor.fetchall()

            for row in data:
                if row['as_number'] is None:
                    asn = 0
                else:
                    asn = row['as_number']

                as_array[asn] = row['count']

            for key in as_array:
                sql_insert_date = " ('%s', %s,'%s', '%s')" % (date, zone, key, as_array[key])
                if len(sql_insert) > 5:
                    sql_insert += ', ' + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            sql = 'INSERT INTO as_count_statistic(`date`, `tld`, `asn`, `count`) VALUE ' + sql_insert
            print(sql)
            cursor.execute(sql)
            self.connection.commit()
            date += datetime.timedelta(days=1)

    def run(self):
        """
        Обрабатываем массив записываем в БД
        :return:
        """

        self._connect_mysql()
        self._update_as_count_per_zone(self.data, self.today, self.zone)
        self.connection.commit()
        self.connection.close()
