# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Alexey Y Manikin'

from helpers.helpers import get_mysql_connection
from config.main import START_YEAR, START_MONTH, START_DAY, PREFIX_LIST, MINIMUM_DOMAIN_COUNT
import datetime
import MySQLdb
import pprint
import traceback
import multiprocessing
from config.main import *


class WorkerProvaderArray(multiprocessing.Process):

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


class Statistic(object):

    # cname_count_statistic
    # a_count_statistic
    # registrant_count_statistic
    # ns_count_statistic
    # mx_count_statistic
    # as_count_statistic
    # domain_count_statistic
    # as_domain_old_count_statistic
    # ns_domain_old_count_statistic
    # a_domain_old_count_statistic
    # ns_domain_group_count_statistic

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
            sql_insert = ''
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

            sql = 'INSERT INTO domain_count_statistic(`date`, `tld`, `count`) VALUE ' + sql_insert
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

        if date is not None:
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
            sql_insert = ''
            as_array = {}

            for i in range(1, 5):
                sql = """SELECT asn%s as as_number, count(*) as count FROM domain_history
    WHERE delegated = 'Y' AND tld = '%s' AND date_start <= '%s' AND date_end >= '%s'
    GROUP BY asn%s
    HAVING count(*) > %s
    ORDER BY count(*) desc""" % (i, zone, date, date, i, MINIMUM_DOMAIN_COUNT)

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
                    sql_insert += ', ' + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            sql = 'INSERT INTO as_count_statistic(`date`, `tld`, `asn`, `count`) VALUE ' + sql_insert
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

        if date is not None:
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
            sql_insert = ''
            mx_array = {}

            for i in range(1, 5):
                sql = """SELECT mx%s as mx, count(*) as count FROM domain_history
    WHERE delegated = 'Y' AND tld = '%s' AND date_start <= '%s' AND date_end >= '%s'
    GROUP BY mx%s
    HAVING count(*) > %s
    ORDER BY count(*) desc""" % (i, zone, date, date, i, MINIMUM_DOMAIN_COUNT)

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

            sql = 'INSERT INTO mx_count_statistic(`date`, `tld`, `mx`, `count`) VALUE ' + sql_insert
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

        if date is not None:
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
            sql_insert = ''
            ns_array = {}

            for i in range(1, 5):
                sql = """SELECT ns%s as ns, count(*) as count FROM domain_history
    WHERE delegated = 'Y' AND tld = '%s' AND date_start <= '%s' AND date_end >= '%s'
    GROUP BY ns%s
    HAVING count(*) > %s
    ORDER BY count(*) desc""" % (i, zone, date, date, i, MINIMUM_DOMAIN_COUNT)

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
                    sql_insert += ', ' + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            sql = 'INSERT INTO ns_count_statistic(`date`, `tld`, `ns`, `count`) VALUE ' + sql_insert
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

        if date is not None:
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
            sql_insert = ''
            sql = """SELECT registrant as registrant, count(*) as count FROM domain_history
WHERE tld = '%s' AND date_start <= '%s' AND date_end >= '%s'
GROUP BY registrant
HAVING count(*) > %s
ORDER BY count(*) desc""" % (zone, date, date, MINIMUM_DOMAIN_COUNT)

            cursor.execute(sql)
            data = cursor.fetchall()

            for row in data:
                sql_insert_date = " ('%s','%s','%s','%s')" % (date, row['registrant'], zone, row['count'])
                if len(sql_insert) > 5:
                    sql_insert += ", " + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            sql = 'INSERT INTO registrant_count_statistic(`date`, `registrant`, `tld`, `count`) VALUE ' + sql_insert
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

        if date is not None:
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
            self.connection.commit()
            date += datetime.timedelta(days=1)

    def update_a_count_statistic(self):
        """
        Обновлене статистики по A записям
        :return:
        """
        today = datetime.date.today()
        date = self.get_date_after_without_statistic('a')

        if date is not None:
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
HAVING count(*) > %s
ORDER BY count(*) desc""" % (zone, date, date, MINIMUM_DOMAIN_COUNT)

            cursor.execute(sql)
            data = cursor.fetchall()

            for row in data:
                sql_insert_date = " ('%s','%s','%s','%s')" % (date, row['cname'], zone, row['count'])
                if len(sql_insert) > 5:
                    sql_insert += ', ' + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            sql = 'INSERT INTO cname_count_statistic(`date`, `cname`, `tld`, `count`) VALUE ' + sql_insert
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

        if date is not None:
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
    HAVING count(*) > %s
    ORDER BY count(*) desc""" % (zone, date, date, MINIMUM_DOMAIN_COUNT)

                cursor.execute(sql)
                data = cursor.fetchall()

                for row in data:

                    if row['asn'] is None or row['asn'] == 'None':
                        row['asn'] = 0

                    sql_insert_date = " ('%s','%s','%s','%s')" % (date, row['asn'], zone, row['old'])
                    if len(sql_insert) > 5:
                        sql_insert += ', ' + sql_insert_date
                    else:
                        sql_insert += sql_insert_date

                sql = 'INSERT INTO as_domain_old_count_statistic(`date`, `asn`, `tld`, `old`) VALUE ' + sql_insert
                cursor.execute(sql)
                self.connection.commit()
                date += datetime.timedelta(days=1)

    def update_as_domain_old_count_statistic(self):
        """
        Обновлене статистики по среднему возрасту доменов на автономной системе
        :return:
        """
        today = datetime.date.today()
        date = self.get_date_after_without_statistic('as_domain_old')

        if date is not None:
            for prefix in PREFIX_LIST:
                self._update_as_domain_old_count_per_zone(date, today, prefix)

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
            self.connection.commit()
            date += datetime.timedelta(days=1)

    def update_ns_domain_old_count_statistic(self):
        """
        Обновлене статистики по среднему возрасту доменов на NS серверах
        :return:
        """
        today = datetime.date.today()
        date = self.get_date_after_without_statistic('ns_domain_old')

        if date is not None:
            for prefix in PREFIX_LIST:
                self._update_ns_domain_old_count_per_zone(date, today, prefix)

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
            self.connection.commit()
            date += datetime.timedelta(days=1)

    def update_a_domain_old_count_statistic(self):
        """
        Обновлене статистики по среднему возрасту доменов на IP адресах
        :return:
        """
        today = datetime.date.today()
        date = self.get_date_after_without_statistic('a_domain_old')

        if date is not None:
            for prefix in PREFIX_LIST:
                self._update_a_domain_old_count_per_zone(date, today, prefix)

    def _update_ns_domain_group_count_statistic_mysql(self, date, today, zone):
        """
        Отрабатывает очень долго, индексы не проставит, размер таблицы расрастается,
        функцию ставил на случай чуда в БД
        :type date: date
        :type today: date
        :type zone: unicode
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            ns_array = {}
            provider_array = {}

            # Вариант когда записей нет в БД
            for i in range(1, 5):
                sql = """SELECT ns%s as ns, count(*) as count FROM domain_history
                        WHERE delegated = 'Y' AND tld = '%s' AND date_start <= '%s' AND date_end >= '%s'
                        GROUP BY ns%s
                        HAVING count(*) > %s
                        ORDER BY count(*) desc""" % (i, zone, date, date, i, MINIMUM_DOMAIN_COUNT)

                cursor.execute(sql)
                data = cursor.fetchall()

                for row in data:
                    if row['ns'] in ns_array:
                        ns_array[row['ns']] += row['count']
                    else:
                        ns_array[row['ns']] = row['count']

            for key in ns_array:
                try:
                    if '.net.ru.' in key or '.com.ua.' in key:
                        provider = key.split('.')[-4]
                    else:
                        provider = key.split('.')[-3]

                    if provider in provider_array:
                        provider_array[provider] += ns_array[key]
                    else:
                        provider_array[provider] = ns_array[key]

                except Exception as e:
                    # ну что бывает, не запоминаем это значение
                    print("\n\n\nGot an exception: %s\n\n\n" % e.message)

            sql_insert = ''
            for key in provider_array:
                like = '%.' + key + '.%'

                sql = """SELECT count(*) as count FROM domain_history
                        WHERE delegated = 'Y' AND tld = '%s' AND date_start <= '%s' AND date_end >= '%s' AND
                              (ns1 like '%s' OR ns2 like '%s' OR ns3 like '%s' OR ns4 like '%s')
                """ % (zone, date, date, like, like, like, like)

                cursor.execute(sql)
                data = cursor.fetchone()

                sql_insert_date = " ('%s','%s','%s','%s')" % (date, key, zone, data['count'])
                if len(sql_insert) > 5:
                    sql_insert += ', ' + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            sql = 'INSERT INTO ns_domain_group_count_statistic(`date`, `ns_group`, `tld`, `count`) VALUE ' \
                  + sql_insert

            cursor.execute(sql)
            self.connection.commit()

            date += datetime.timedelta(days=1)

    def _update_ns_domain_group_count_statistic_python(self, date, today, zone, count=COUNT_THREAD):
        """
        Реализация на питоне с использованием процессов
        :type date: date
        :type today: date
        :type zone: unicode
        :return:
        """
        self.connection.close()

        while date <= today:
            connection = get_mysql_connection()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            print("date is %s" % date)

            ns_array = {}
            provider_array = {}

            sql_has_data = """SELECT count(*) as count FROM ns_count_statistic
                              WHERE tld = '%s' AND date = '%s'""" % (zone, date)
            cursor.execute(sql_has_data)
            data = cursor.fetchone()

            if data['count'] == 0:
                # Вариант когда записей нет в статистикие по NS серверам
                for i in range(1, 5):
                    sql = """SELECT ns%s as ns, count(*) as count FROM domain_history
                            WHERE delegated = 'Y' AND tld = '%s' AND date_start <= '%s' AND date_end >= '%s'
                            GROUP BY ns%s
                            HAVING count(*) > %s
                            ORDER BY count(*) desc""" % (i, zone, date, date, i, MINIMUM_DOMAIN_COUNT)

                    cursor.execute(sql)
                    data = cursor.fetchall()

                    for row in data:
                        if row['ns'] in ns_array:
                            ns_array[row['ns']] += row['count']
                        else:
                            ns_array[row['ns']] = row['count']
            else:
                # вариант с использованием уже подготовленных данных
                sql = """SELECT ns, count FROM ns_count_statistic
                        WHERE tld = '%s' AND date= '%s'""" % (zone, date)
                cursor.execute(sql)
                data = cursor.fetchall()
                for row in data:
                    ns_array[row['ns']] = row['count']

            for key in ns_array:
                try:
                    if key is not None:
                        split_ns = key.split('.')
                        if len(split_ns) > 2:

                            if '.net.ru.' in key or '.com.ua.' in key:
                                provider = split_ns[-4]
                            else:
                                provider = split_ns[-3]

                            if provider in provider_array:
                                provider_array[provider] += ns_array[key]
                            else:
                                provider_array[provider] = ns_array[key]

                except Exception as e:
                    # ну что бывает, не запоминаем это значение
                    print("Got an exception: %s" % e.message)
                    print(traceback.format_exc())

            sql = """SELECT ns1, ns2, ns3, ns4 FROM domain_history
                    WHERE delegated = 'Y' AND tld = '%s' AND date_start <= '%s' AND date_end >= '%s'
            """ % (zone, date, date)
            cursor.execute(sql)
            data = cursor.fetchall()

            connection.close()

            process_list = []
            i = 0

            for key in provider_array:
                search_string = key
                print("%s Search key is %s" % (i, search_string))

                worker = WorkerProvaderArray(i, search_string, data, zone, date)
                worker.daemon = True
                process_list.append(worker)
                worker.start()

                i += 1

                if i != 0 and i % count == 0:
                    for process in process_list:
                        try:
                            # timeout 2 days
                            process.join(1728000)
                        except KeyboardInterrupt:
                            return
                    process_list = []

            for process in process_list:
                try:
                    # timeout 2 days
                    process.join(1728000)
                except KeyboardInterrupt:
                    return

            date += datetime.timedelta(days=1)

        self.connection = get_mysql_connection()

    def update_ns_domain_group_count_statistic(self):
        """
        Обновлене статистики по груперованным провайдерам
        :return:
        """
        today = datetime.date.today()
        date = self.get_date_after_without_statistic('ns_domain_group')

        if date is not None:
            for prefix in PREFIX_LIST:
                self._update_ns_domain_group_count_statistic_python(date, today, prefix, 16)

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
        self.update_ns_domain_old_count_statistic()
        self.update_a_domain_old_count_statistic()
        self.update_ns_domain_group_count_statistic()
