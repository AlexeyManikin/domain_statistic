# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Alexey Y Manikin'

from helpers.helpers import get_mysql_connection
import datetime
import MySQLdb
import traceback
from config.main import *

from classes.statistic_worker.groupProviderStatistic import GroupProviderStatistic

from classes.statistic_worker.cnameCountStatistic import CnameCountStatistic
from classes.statistic_worker.aCountStatistic import ACountStatistic
from classes.statistic_worker.asCountStatistic import AsCountStatistic
from classes.statistic_worker.domainCountStatistic import DomainCountStatistic
from classes.statistic_worker.mxCountStatistic import MxCountStatistic
from classes.statistic_worker.nsCountStatistic import NsCountStatistic
from classes.statistic_worker.registrantCountStatistic import RegistrantCountStatistic
from classes.statistic_worker.asDomainOldCountStatistic import AsDomainOldCountStatistic
from classes.statistic_worker.nsDomainOldCountStatistic import NsDomainOldCountStatistic
from classes.statistic_worker.aDomainOldCountStatistic import ADomainOldCountStatistic


class Statistic(object):

    def __init__(self):
        """
        :return:
        """
        self.connection = get_mysql_connection()
        self.count_ptheread = 0
        self.process_list = []
        self.today = datetime.date.today()

    def _connect_mysql(self):
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

    def update_domain_count_statistic(self):
        """
        Обновление статистики по количеству доменов системам
        :return:
        """
        date = self.get_date_after_without_statistic('domain')

        if date is not None:
            for prefix in PREFIX_LIST:
                self.count_ptheread += 1
                worker = DomainCountStatistic(self.count_ptheread, date, self.today, prefix)
                worker.daemon = True
                self.process_list.append(worker)
                worker.start()

    def update_as_count_statistic(self):
        """
        Обновление статистики по автономным системам
        :return:
        """
        date = self.get_date_after_without_statistic('as')

        if date is not None:
            for prefix in PREFIX_LIST:
                self.count_ptheread += 1
                worker = AsCountStatistic(self.count_ptheread, date, self.today, prefix)
                worker.daemon = True
                self.process_list.append(worker)
                worker.start()

    def update_mx_count_statistic(self):
        """
        Обновлене статистики по MX серверам
        :return:
        """
        date = self.get_date_after_without_statistic('mx')

        if date is not None:
            for prefix in PREFIX_LIST:
                self.count_ptheread += 1
                worker = MxCountStatistic(self.count_ptheread, date, self.today, prefix)
                worker.daemon = True
                self.process_list.append(worker)
                worker.start()

    def update_ns_count_statistic(self):
        """
        Обновлене статистики по NS серверам
        :return:
        """
        date = self.get_date_after_without_statistic('ns')

        if date is not None:
            for prefix in PREFIX_LIST:
                self.count_ptheread += 1
                worker = NsCountStatistic(self.count_ptheread, date, self.today, prefix)
                worker.daemon = True
                self.process_list.append(worker)
                worker.start()

    def update_registrant_count_statistic(self):
        """
        Обновлене статистики по Регистраторам
        :return:
        """
        date = self.get_date_after_without_statistic('registrant')

        if date is not None:
            for prefix in PREFIX_LIST:
                self.count_ptheread += 1
                worker = RegistrantCountStatistic(self.count_ptheread, date, self.today, prefix)
                worker.daemon = True
                self.process_list.append(worker)
                worker.start()

    def update_a_count_statistic(self):
        """
        Обновлене статистики по A записям
        :return:
        """
        date = self.get_date_after_without_statistic('a')

        if date is not None:
            for prefix in PREFIX_LIST:
                self.count_ptheread += 1
                worker = ACountStatistic(self.count_ptheread, date, self.today, prefix)
                worker.daemon = True
                self.process_list.append(worker)
                worker.start()

    def update_cname_count_statistic(self):
        """
        Обновлене статистики по CNAME записям
        :return:
        """
        date = self.get_date_after_without_statistic('cname')

        if date is not None:
            for prefix in PREFIX_LIST:
                self.count_ptheread += 1
                worker = CnameCountStatistic(self.count_ptheread, date, self.today, prefix)
                worker.daemon = True
                self.process_list.append(worker)
                worker.start()

    def update_as_domain_old_count_statistic(self):
        """
        Обновлене статистики по среднему возрасту доменов на автономной системе
        :return:
        """
        date = self.get_date_after_without_statistic('as_domain_old')

        if date is not None:
            for prefix in PREFIX_LIST:
                self.count_ptheread += 1
                worker = AsDomainOldCountStatistic(self.count_ptheread, date, self.today, prefix)
                worker.daemon = True
                self.process_list.append(worker)
                worker.start()

    def update_ns_domain_old_count_statistic(self):
        """
        Обновлене статистики по среднему возрасту доменов на NS серверах
        :return:
        """
        date = self.get_date_after_without_statistic('ns_domain_old')

        if date is not None:
            for prefix in PREFIX_LIST:
                self.count_ptheread += 1
                worker = NsDomainOldCountStatistic(self.count_ptheread, date, self.today, prefix)
                worker.daemon = True
                self.process_list.append(worker)
                worker.start()

    def update_a_domain_old_count_statistic(self):
        """
        Обновлене статистики по среднему возрасту доменов на IP адресах
        :return:
        """
        date = self.get_date_after_without_statistic('a_domain_old')

        if date is not None:
            for prefix in PREFIX_LIST:
                self.count_ptheread += 1
                worker = ADomainOldCountStatistic(self.count_ptheread, date, self.today, prefix)
                worker.daemon = True
                self.process_list.append(worker)
                worker.start()

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

                worker = GroupProviderStatistic(i, search_string, data, zone, date)
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
                self._update_ns_domain_group_count_statistic_python(date, today, prefix, 25)

    def update_all_statistic(self):
        """
        Обновление всех статистик
        :return:
        """
        self.update_a_domain_old_count_statistic()
        self.update_ns_domain_old_count_statistic()
        self.update_as_domain_old_count_statistic()
        self.update_registrant_count_statistic()
        self.update_ns_count_statistic()
        self.update_mx_count_statistic()
        self.update_domain_count_statistic()
        self.update_as_count_statistic()
        self.update_a_count_statistic()
        self.update_cname_count_statistic()
        self.update_ns_domain_group_count_statistic()

        for process in self.process_list:
            try:
                # timeout 2 days
                process.join(1728000)
            except KeyboardInterrupt:
                return
