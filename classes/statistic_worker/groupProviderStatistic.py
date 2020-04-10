__author__ = 'Alexey Y Manikin'

from classes.statistic_worker.statisticBaseClass import StatisticBaseClass
import MySQLdb
import datetime
from config.main import PREFIX_LIST_ZONE, MINIMUM_DOMAIN_COUNT, COUNT_THREAD_STATISTIC
from config.eq_domain import provider_eq


class GroupProviderStatisticSearchEngine(StatisticBaseClass):
    def __init__(self, number: int, date: datetime, zone_id: int, data_rows: list, key: str):
        """
        :param number:
        """
        StatisticBaseClass.__init__(self, number, "group_provider_sercher_")

        self.date = date
        self.zone_id = zone_id
        self.data_rows = data_rows
        self.key = key

    @staticmethod
    def _count_key(data_rows: list, key: str):
        """
        :return:
        """
        search_string = '.' + key + '.'
        count = 0

        for row in data_rows:
            if 'ns1' in row and row['ns1'] is not None and search_string in row['ns1']:
                count += 1
            elif 'ns2' in row and row['ns2'] is not None and search_string in row['ns2']:
                count += 1
            elif 'ns3' in row and row['ns3'] is not None and search_string in row['ns3']:
                count += 1
            elif 'ns4' in row and row['ns4'] is not None and search_string in row['ns4']:
                count += 1

        return count

    def _update(self):
        """
        :return:
        """
        count = self._count_key(self.data_rows, self.key)
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = 'INSERT INTO ns_domain_group_count_statistic' \
              + '(`date`, `ns_group`, `tld`, `count`) VALUE ' \
              + " ('%s','%s', %i, %i)" % (self.date, self.key, self.zone_id, count)
        cursor.execute(sql)


class GroupProviderStatistic(StatisticBaseClass):

    def __init__(self, number: int, data: datetime, today: datetime, zone: str):
        """
        :param number:
        """
        StatisticBaseClass.__init__(self, number, "group_provider_")

        self.today = today
        self.data = data
        self.zone_id = PREFIX_LIST_ZONE[zone]

        self.count_ptheread = 0
        self.process_list = []

    def _get_ns_data(self, ns_array: dict, date: datetime) -> dict:
        """
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)

        sql_has_data = """SELECT count(*) as count FROM ns_count_statistic
                          WHERE tld = %i AND date = '%s'""" % (self.zone_id, date)
        cursor.execute(sql_has_data)
        data = cursor.fetchone()

        if data['count'] == 0:
            # Вариант когда записей нет в статистикие по NS серверам
            for i in range(1, 5):
                if date == datetime.date.today():
                    sql = """SELECT ns%i as ns, count(*) as count FROM domain
                    WHERE delegated = 'Y' AND tld = %i 
                    GROUP BY ns%i
                    HAVING count(*) > %i
                    ORDER BY count(*) desc""" % (i, self.zone_id, i, MINIMUM_DOMAIN_COUNT)
                else:
                    sql = """SELECT ns%i as ns, count(*) as count FROM domain_history
                    WHERE delegated = 'Y' AND tld = %i AND date_start <= '%s' AND date_end >= '%s'
                    GROUP BY ns%i
                    HAVING count(*) > %i
                    ORDER BY count(*) desc""" % (i, self.zone_id, date, date, i, MINIMUM_DOMAIN_COUNT)

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
                     WHERE tld = %i AND date= '%s'""" % (self.zone_id, date)
            cursor.execute(sql)
            data = cursor.fetchall()
            for row in data:
                ns_array[row['ns']] = row['count']

        return ns_array

    def _get_data(self, date: datetime) -> list:
        """
        В зависимости от дня статистики обращаемся или к domain_history или к domain
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)

        if date == datetime.date.today():
            sql = """SELECT ns1, ns2, ns3, ns4 FROM domain
            WHERE delegated = 'Y' AND tld = %i """ % self.zone_id
        else:
            sql = """SELECT ns1, ns2, ns3, ns4 FROM domain_history
            WHERE delegated = 'Y' AND tld = %i AND date_start <= '%s' AND date_end >= '%s'""" % (self.zone_id,
                                                                                                 date,
                                                                                                 date)
        cursor.execute(sql)
        return cursor.fetchall()

    @staticmethod
    def _get_provider(key: str, split_ns: dict) -> str:
        """
        :return:
        """
        for provider_key in provider_eq:
            if provider_key in key:
                return provider_eq[provider_key]

        if '.net.ru.' in key or '.com.ua.' in key or '.net.in.' in key or '.net.ua.' in key:
            provider = split_ns[-4]
        else:
            provider = split_ns[-3]

        return provider

    def _update(self):
        """
        :return:
        """
        date = self.data
        today = self.today

        while date <= today:
            ns_array = {}
            provider_array = {}

            ns_array = self._get_ns_data(ns_array, date)

            for key in ns_array:
                try:
                    if key is not None:
                        split_ns = key.split('.')
                        if len(split_ns) > 2:
                            provider = self._get_provider(key, split_ns)

                            if provider in provider_array:
                                provider_array[provider] += ns_array[key]
                            else:
                                provider_array[provider] = ns_array[key]

                except Exception as e:
                    print(e)

            data = self._get_data(date)
            for key in provider_array:
                self.count_ptheread += 1
                worker = GroupProviderStatisticSearchEngine(self.count_ptheread, date, self.zone_id, data, key)
                worker.daemon = True
                self.process_list.append(worker)
                worker.start()

                if self.count_ptheread % COUNT_THREAD_STATISTIC == 0:
                    for process in self.process_list:
                        try:
                            # timeout 2 days
                            process.join(1728000)
                            self.process_list.remove(process)
                            self.count_ptheread -= 1
                        except KeyboardInterrupt:
                            return

            for process in self.process_list:
                try:
                    # timeout 2 days
                    process.join(1728000)
                    self.process_list.remove(process)
                    self.count_ptheread -= 1
                except KeyboardInterrupt:
                    return

            date += datetime.timedelta(days=1)
