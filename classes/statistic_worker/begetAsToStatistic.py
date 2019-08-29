# -*- coding: utf-8 -*-
__author__ = 'Alexey Y Manikin'

from helpers.helpers import get_mysql_connection
import MySQLdb
import multiprocessing
import datetime
from config.main import PREFIX_LIST_ZONE


class BegetAsToStatistic(multiprocessing.Process):

    def __init__(self, number, data, today, zone):
        """
        :param number:
        """
        multiprocessing.Process.__init__(self, name="beget_as_to_%s" % number)
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

    def _update(self, date, today, zone):
        """
        :type date: date
        :type today: date
        :type zone: unicode
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            sql_insert = ''
            sql = """SELECT 
            dh1.domain_id,
            dh1.domain_name, 
            dh1.tld, 
            dh1.asn1
        FROM
            domain_history AS dh1
        WHERE
            dh1.asn1 != 198610
                AND dh1.date_start <= '%s'
                AND dh1.date_end > '%s'
                AND dh1.delegated = 'Y'
                AND dh1.domain_id IN (SELECT 
                    dh.domain_id
                FROM
                    domain_history AS dh
                WHERE
                    dh.date_start <= DATE_SUB('%s', INTERVAL 1 DAY)
                        AND dh.date_end > DATE_SUB('%s', INTERVAL 1 DAY)
                        AND dh.delegated = 'Y'
                        AND dh.asn1 = 198610
                        AND dh.tld = %s)""" % (date, date, date, date, zone)

            cursor.execute(sql)
            data = cursor.fetchall()

            for row in data:
                sql_insert_date = " ('%s','%s','%s','%s',%s)" % (date, row['domain_id'], row['domain_name'], row['asn1'], zone)
                if len(sql_insert) > 5:
                    sql_insert += ", " + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            if len(sql_insert) > 1:
                sql = """INSERT INTO beget_domain_as_to_count_statistic(`date`, 
                            `domain_id`, 
                            `domain_name`, 
                            `as_to`, 
                            `tld`) VALUE """ + sql_insert
                cursor.execute(sql)
                self.connection.commit()
            date += datetime.timedelta(days=1)

    def run(self):
        """
        Обрабатываем массив записываем в БД
        :return:
        """
        self._connect_mysql()
        self._update(self.data, self.today, self.zone)
        self.connection.commit()
        self.connection.close()
