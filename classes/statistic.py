# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Alexey Y Manikin'

from helpers.helpers import get_mysql_connection
from config.main import START_YEAR, START_MONTH, START_DAY, PREFIX_LIST
import datetime
import MySQLdb


class Statistic(object):

    # cname_count_statistic
    # a_count_statistic
    # registrant_count_statistic
    # ns_count_statistic
    # mx_count_statistic
    # as_count_statistic
    # domain_count_statistic
    # as_domain_old_count_statistic

    def __init__(self):
        """
        :return:
        """
        self.connection = get_mysql_connection()

    def get_date_after_without_statistic(self, table_prefix):
        """
        получить последнию дату без агригации данных
        :type table_prefix: unicode
        :rtype: date
        """
        today = datetime.date.today()
        date = datetime.date(START_YEAR, START_MONTH, START_DAY)
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            sql = "SELECT count(*) as count FROM %s_count_statistic WHERE date = '%s'" % (table_prefix, date)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result['count'] == 0:
                return date

            date += datetime.timedelta(days=1)

    def _update_domain_count_per_zone(self, date, today, zone):
        """
        :type date: date
        :type today: date
        :type zone: unicode
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            sql_insert = ""
            sql = """SELECT count(*) as count FROM domain_history
WHERE tld = '%s' AND date_start <= '%s' AND date_end >= '%s'
ORDER BY count(*) desc""" % (zone, date, date)

            cursor.execute(sql)
            data = cursor.fetchall()

            for row in data:
                sql_insert_date = " ('%s','%s','%s')" % (date, zone, row['count'])
                if len(sql_insert) > 5:
                    sql_insert += ", " + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            sql = "INSERT INTO domain_count_statistic(`date`, `tld`, `count`) VALUE " + sql_insert
            cursor.execute(sql)
            self.connection.commit()
            date += datetime.timedelta(days=1)

    def update_domain_count_statistic(self):
        """
        Обновление статистики по количеству доменов системам
        :return:
        """
        today = datetime.date.today()
        date = self.get_date_after_without_statistic('domain')

        for prefix in PREFIX_LIST:
            self._update_domain_count_per_zone(date, today, prefix)

    def _update_as_count_per_zone(self, date, today, zone):
        """
        :type date: date
        :type today: date
        :type zone: unicode
        :return:
        """

        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            sql_insert = ""
            as_array = {}

            for i in range(1, 5):
                sql = """SELECT asn%s as as_number, count(*) as count FROM domain_history
    WHERE delegated = 'Y' AND tld = '%s' AND date_start <= '%s' AND date_end >= '%s'
    GROUP BY asn%s
    HAVING count(*) > 50
    ORDER BY count(*) desc""" % (i, zone, date, date, i)

                cursor.execute(sql)
                data = cursor.fetchall()

                for row in data:
                    if row['as_number'] == None:
                        asn = 0
                    else:
                        asn = row['as_number']

                    if asn in as_array:
                        as_array[asn] += row['count']
                    else:
                        as_array[asn] = row['count']

            for key in as_array:
                sql_insert_date = " ('%s','%s','%s', '%s')" % (date, zone, key, as_array[key])
                if len(sql_insert) > 5:
                    sql_insert += ", " + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            sql = "INSERT INTO as_count_statistic(`date`, `tld`, `asn`, `count`) VALUE " + sql_insert
            cursor.execute(sql)
            self.connection.commit()
            date += datetime.timedelta(days=1)

    def update_as_count_statistic(self):
        """
        Обновление статистики по автономным системам
        :return:
        """
        today = datetime.date.today()
        date = self.get_date_after_without_statistic('as')

        for prefix in PREFIX_LIST:
            self._update_as_count_per_zone(date, today, prefix)

    def _update_mx_count_per_zone(self, date, today, zone):
        """
        :type date: date
        :type today: date
        :type zone: unicode
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            sql_insert = ""
            mx_array = {}

            for i in range(1, 5):
                sql = """SELECT mx%s as mx, count(*) as count FROM domain_history
    WHERE delegated = 'Y' AND tld = '%s' AND date_start <= '%s' AND date_end >= '%s'
    GROUP BY mx%s
    HAVING count(*) > 50
    ORDER BY count(*) desc""" % (i, zone, date, date, i)

                cursor.execute(sql)
                data = cursor.fetchall()

                for row in data:
                    if row['mx'] in mx_array:
                        mx_array[row['mx']] += row['count']
                    else:
                        mx_array[row['mx']] = row['count']

            for key in mx_array:
                sql_insert_date = " ('%s','%s','%s', '%s')" % (date, zone, key, mx_array[key])
                if len(sql_insert) > 5:
                    sql_insert += ", " + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            sql = "INSERT INTO mx_count_statistic(`date`, `tld`, `mx`, `count`) VALUE " + sql_insert
            cursor.execute(sql)
            self.connection.commit()
            date += datetime.timedelta(days=1)

    def update_mx_count_statistic(self):
        """
        Обновлене статистики по MX серверам
        :return:
        """
        today = datetime.date.today()
        date = self.get_date_after_without_statistic('mx')

        for prefix in PREFIX_LIST:
            self._update_mx_count_per_zone(date, today, prefix)

    def _update_ns_count_per_zone(self, date, today, zone):
        """
        :type date: date
        :type today: date
        :type zone: unicode
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            sql_insert = ""
            ns_array = {}

            for i in range(1, 5):
                sql = """SELECT ns%s as ns, count(*) as count FROM domain_history
    WHERE delegated = 'Y' AND tld = '%s' AND date_start <= '%s' AND date_end >= '%s'
    GROUP BY ns%s
    HAVING count(*) > 50
    ORDER BY count(*) desc""" % (i, zone, date, date, i)

                cursor.execute(sql)
                data = cursor.fetchall()

                for row in data:
                    if row['ns'] in ns_array:
                        ns_array[row['ns']] += row['count']
                    else:
                        ns_array[row['ns']] = row['count']

            for key in ns_array:
                sql_insert_date = " ('%s','%s','%s', '%s')" % (date, zone, key, ns_array[key])
                if len(sql_insert) > 5:
                    sql_insert += ", " + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            sql = "INSERT INTO ns_count_statistic(`date`, `tld`, `ns`, `count`) VALUE " + sql_insert
            cursor.execute(sql)
            self.connection.commit()
            date += datetime.timedelta(days=1)

    def update_ns_count_statistic(self):
        """
        Обновлене статистики по NS серверам
        :return:
        """
        today = datetime.date.today()
        date = self.get_date_after_without_statistic('ns')

        for prefix in PREFIX_LIST:
            self._update_ns_count_per_zone(date, today, prefix)

    def _update_registrant_count_per_zone(self, date, today, zone):
        """
        :type date: date
        :type today: date
        :type zone: unicode
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            sql_insert = ""
            sql = """SELECT registrant as registrant, count(*) as count FROM domain_history
WHERE tld = '%s' AND date_start <= '%s' AND date_end >= '%s'
GROUP BY registrant
HAVING count(*) > 50
ORDER BY count(*) desc""" % (zone, date, date)

            cursor.execute(sql)
            data = cursor.fetchall()

            for row in data:
                sql_insert_date = " ('%s','%s','%s','%s')" % (date, row['registrant'], zone, row['count'])
                if len(sql_insert) > 5:
                    sql_insert += ", " + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            sql = "INSERT INTO registrant_count_statistic(`date`, `registrant`, `tld`, `count`) VALUE " + sql_insert
            cursor.execute(sql)
            self.connection.commit()
            date += datetime.timedelta(days=1)

    def update_registrant_count_statistic(self):
        """
        Обновлене статистики по Регистраторам
        :return:
        """
        today = datetime.date.today()
        date = self.get_date_after_without_statistic('registrant')

        for prefix in PREFIX_LIST:
            self._update_registrant_count_per_zone(date, today, prefix)

    def _update_a_count_per_zone(self, date, today, zone):
        """
        :type date: date
        :type today: date
        :type zone: unicode
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            sql_insert = ""
            a_array = {}
            asn_array = {}

            for i in range(1, 5):
                sql = """SELECT a%s as a, asn%s as asn, count(*) as count FROM domain_history
WHERE delegated = 'Y' AND tld = '%s' AND date_start <= '%s' AND date_end >= '%s'
GROUP BY a%s
HAVING count(*) > 50
ORDER BY count(*) desc""" % (i, i, zone, date, date, i)

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
                    sql_insert += ", " + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            sql = "INSERT INTO a_count_statistic(`date`, `tld`, `a`, `count`, `asn`) VALUE " + sql_insert
            cursor.execute(sql)
            self.connection.commit()
            date += datetime.timedelta(days=1)

    def update_a_count_statistic(self):
        """
        Обновлене статистики по A записям
        :return:
        """
        today = datetime.date.today()
        date = self.get_date_after_without_statistic('a')

        for prefix in PREFIX_LIST:
            self._update_a_count_per_zone(date, today, prefix)

    def _update_cname_count_per_zone(self, date, today, zone):
        """
        :type date: date
        :type today: date
        :type zone: unicode
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            sql_insert = ""
            sql = """SELECT cname as cname, count(*) as count FROM domain_history
WHERE tld = '%s' AND date_start <= '%s' AND date_end >= '%s'
GROUP BY cname
HAVING count(*) > 50
ORDER BY count(*) desc""" % (zone, date, date)

            cursor.execute(sql)
            data = cursor.fetchall()

            for row in data:
                sql_insert_date = " ('%s','%s','%s','%s')" % (date, row['cname'], zone, row['count'])
                if len(sql_insert) > 5:
                    sql_insert += ", " + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            sql = "INSERT INTO cname_count_statistic(`date`, `cname`, `tld`, `count`) VALUE " + sql_insert
            cursor.execute(sql)
            self.connection.commit()
            date += datetime.timedelta(days=1)

    def update_cname_count_statistic(self):
        """
        Обновлене статистики по CNAME записям
        :return:
        """
        today = datetime.date.today()
        date = self.get_date_after_without_statistic('cname')

        for prefix in PREFIX_LIST:
            self._update_cname_count_per_zone(date, today, prefix)

    def _update_as_domain_old_count_per_zone(self, date, today, zone):
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
                sql = """SELECT asn1 as asn, AVG(DATEDIFF(NOW(), register_date)) as old, count(*) as count
    FROM domain_history
    WHERE tld = '%s' AND date_start <= '%s' AND date_end >= '%s' AND delegated = 'Y'
    GROUP BY asn1
    HAVING count(*) > 50
    ORDER BY count(*) desc""" % (zone, date, date)

                cursor.execute(sql)
                data = cursor.fetchall()

                for row in data:
                    sql_insert_date = " ('%s','%s','%s','%s')" % (date, row['asn'], zone, row['old'])
                    if len(sql_insert) > 5:
                        sql_insert += ", " + sql_insert_date
                    else:
                        sql_insert += sql_insert_date

                sql = "INSERT INTO as_domain_old_count_statistic(`date`, `asn`, `tld`, `old`) VALUE " + sql_insert
                cursor.execute(sql)
                self.connection.commit()
                date += datetime.timedelta(days=1)

    def update_as_domain_old_count_statistic(self):
        """
        Обновлене статистики по среднему возрасту доменов
        :return:
        """
        today = datetime.date.today()
        date = self.get_date_after_without_statistic('as_domain_old')

        for prefix in PREFIX_LIST:
            self._update_as_domain_old_count_per_zone(date, today, prefix)

    def update_all_statistic(self):
        """
        Обновление всех статистик
        :return:
        """
        self.update_a_count_statistic()
        self.update_as_count_statistic()
        self.update_domain_count_statistic()
        self.update_mx_count_statistic()
        self.update_ns_count_statistic()
        self.update_registrant_count_statistic()
        self.update_cname_count_statistic()
        self.update_as_domain_old_count_statistic()
