__author__ = 'Alexey Y Manikin'

from helpers.helpers import get_mysql_connection
import datetime
import MySQLdb
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

from classes.statistic_worker.beget.begetAsFromStatistic import BegetAsFromStatistic
from classes.statistic_worker.beget.begetAsToStatistic import BegetAsToStatistic
from classes.statistic_worker.beget.begetNsFromStatistic import BegetNsFromStatistic
from classes.statistic_worker.beget.begetNsToStatistic import BegetNsToStatistic
from classes.statistic_worker.beget.begetRegistrantFromStatistic import BegetRegistrantFromStatistic
from classes.statistic_worker.beget.begetRegistrantToStatistic import BegetRegistrantToStatistic

from classes.statistic_worker.provider.providerAsFromStatistic import ProviderAsFromStatistic
from classes.statistic_worker.provider.providerAsToStatistic import ProviderAsToStatistic


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

    def get_date_after_without_statistic(self, table_prefix: str) -> datetime:
        """
        получить последнию дату без агригации данных
        :type table_prefix: unicode
        :rtype: date
        """
        today = datetime.date.today()
        date = datetime.date(START_YEAR, START_MONTH, START_DAY)
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            try:
                sql = "SELECT count(*) as count FROM %s_count_statistic WHERE date = '%s'" % (table_prefix, today)
                cursor.execute(sql)
                result = cursor.fetchone()
                if result['count'] != 0:
                    today += datetime.timedelta(days=1)
                    return today

                today -= datetime.timedelta(days=1)
            except MySQLdb.Error:
                print("Table %s_count_statistic dosn`t exist" % table_prefix)
                return today
        return today

    def update_domain_count_statistic(self):
        """
        Обновление статистики по количеству доменов системам
        :return:
        """
        date = self.get_date_after_without_statistic('domain')

        if date is not None:
            for prefix in PREFIX_LIST_ZONE.keys():
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
            for prefix in PREFIX_LIST_ZONE.keys():
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
            for prefix in PREFIX_LIST_ZONE.keys():
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
            for prefix in PREFIX_LIST_ZONE.keys():
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
            for prefix in PREFIX_LIST_ZONE.keys():
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
            for prefix in PREFIX_LIST_ZONE.keys():
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
            for prefix in PREFIX_LIST_ZONE.keys():
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
            for prefix in PREFIX_LIST_ZONE.keys():
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
            for prefix in PREFIX_LIST_ZONE.keys():
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
            for prefix in PREFIX_LIST_ZONE.keys():
                self.count_ptheread += 1
                worker = ADomainOldCountStatistic(self.count_ptheread, date, self.today, prefix)
                worker.daemon = True
                self.process_list.append(worker)
                worker.start()

    def update_ns_domain_group_count_statistic(self):
        """
        Обновлене статистики по груперованным провайдерам
        :return:
        """
        date = self.get_date_after_without_statistic('ns_domain_group')

        if date is not None:
            for prefix in PREFIX_LIST_ZONE.keys():
                GroupProviderStatistic.update_ns_domain_group_count_statistic_python(date, self.today, prefix, 25)

    def update_beget_as_from(self):
        """
        :return:
        """
        date = self.get_date_after_without_statistic('beget_domain_as_from')

        if date is not None:
            for prefix in PREFIX_LIST_ZONE.keys():
                self.count_ptheread += 1
                worker = BegetAsFromStatistic(self.count_ptheread, date, self.today, prefix)
                worker.daemon = True
                self.process_list.append(worker)
                worker.start()

    def update_beget_as_to(self):
        """
        :return:
        """
        date = self.get_date_after_without_statistic('beget_domain_as_to')

        if date is not None:
            for prefix in PREFIX_LIST_ZONE.keys():
                self.count_ptheread += 1
                worker = BegetAsToStatistic(self.count_ptheread, date, self.today, prefix)
                worker.daemon = True
                self.process_list.append(worker)
                worker.start()

    def update_beget_ns_from(self):
        """
        :return:
        """
        date = self.get_date_after_without_statistic('beget_domain_ns_from')

        if date is not None:
            for prefix in PREFIX_LIST_ZONE.keys():
                self.count_ptheread += 1
                worker = BegetNsFromStatistic(self.count_ptheread, date, self.today, prefix)
                worker.daemon = True
                self.process_list.append(worker)
                worker.start()

    def update_beget_ns_to(self):
        """
        :return:
        """
        date = self.get_date_after_without_statistic('beget_domain_ns_to')

        if date is not None:
            for prefix in PREFIX_LIST_ZONE.keys():
                self.count_ptheread += 1
                worker = BegetNsToStatistic(self.count_ptheread, date, self.today, prefix)
                worker.daemon = True
                self.process_list.append(worker)
                worker.start()

    def update_beget_registrant_from(self):
        """
        :return:
        """
        date = self.get_date_after_without_statistic('beget_domain_registrant_from')

        if date is not None:
            self.count_ptheread += 1
            worker = BegetRegistrantFromStatistic(self.count_ptheread, date, self.today)
            worker.daemon = True
            self.process_list.append(worker)
            worker.start()

    def update_beget_registrant_to(self):
        """
        :return:
        """
        date = self.get_date_after_without_statistic('beget_domain_registrant_to')

        if date is not None:
            self.count_ptheread += 1
            worker = BegetRegistrantToStatistic(self.count_ptheread, date, self.today)
            worker.daemon = True
            self.process_list.append(worker)
            worker.start()

    def _update_provider_as_from(self, provider: str, as_number: int):
        """
        :return:
        """
        ProviderAsFromStatistic.create_table(provider)
        date = self.get_date_after_without_statistic("%s_domain_as_from" % provider)

        if date is not None:
            for prefix in PREFIX_LIST_ZONE.keys():
                self.count_ptheread += 1
                worker = ProviderAsFromStatistic(self.count_ptheread, date, self.today, prefix, provider, as_number)
                worker.daemon = True
                self.process_list.append(worker)
                worker.start()

    def _update_provider_to_from(self, provider: str, as_number: int):
        """
        :return:
        """
        ProviderAsToStatistic.create_table(provider)
        date = self.get_date_after_without_statistic("%s_domain_as_to" % provider)

        if date is not None:
            for prefix in PREFIX_LIST_ZONE.keys():
                self.count_ptheread += 1
                worker = ProviderAsToStatistic(self.count_ptheread, date, self.today, prefix, provider, as_number)
                worker.daemon = True
                self.process_list.append(worker)
                worker.start()

    def update_provider_statistic(self, provider: str, as_number: int):
        self._update_provider_as_from(provider, as_number)
        self._update_provider_to_from(provider, as_number)

    def update_all_statistic(self):
        """
        Обновление всех статистик
        :return:
        """
        self.update_as_count_statistic()
        self.update_a_domain_old_count_statistic()
        self.update_ns_domain_old_count_statistic()
        self.update_as_domain_old_count_statistic()
        self.update_registrant_count_statistic()
        self.update_ns_count_statistic()
        self.update_mx_count_statistic()
        self.update_domain_count_statistic()
        self.update_a_count_statistic()
        self.update_cname_count_statistic()
        self.update_ns_domain_group_count_statistic()

        # beget statistic
        self.update_beget_as_from()
        self.update_beget_as_to()
        self.update_beget_registrant_from()
        self.update_beget_registrant_to()
        self.update_beget_ns_from()
        self.update_beget_ns_to()

        self.update_provider_statistic('netangels', 44128)
        self.update_provider_statistic('timeweb', 9123)

        for process in self.process_list:
            try:
                # timeout 2 days
                process.join(1728000)
            except KeyboardInterrupt:
                return

    def update_all_test_statistic(self):
        """
        Обновление всех статистик
        :return:
        """
        #self.update_provider_statistic('netangels', 44128)
        for process in self.process_list:
            try:
                process.join()
            except KeyboardInterrupt:
                return
