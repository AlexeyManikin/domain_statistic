__author__ = 'Alexey Y Manikin'

from classes.statistic_worker.statisticBaseClass import StatisticBaseClass
import MySQLdb
import datetime
from helpers.helpers import get_mysql_connection
from config.main import PREFIX_LIST_ZONE, COUNT_THREAD, MINIMUM_DOMAIN_COUNT


class GroupProviderStatistic(StatisticBaseClass):

    def __init__(self, number: int, key, data: list, zone: str, date: datetime):
        """
        :param number:
        """
        StatisticBaseClass.__init__(self, number, "resolver_")

        self.key = key
        self.data = data
        self.date = date
        self.zone = PREFIX_LIST_ZONE[zone]

    def _update(self):
        """
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

        sql_insert_date = " ('%s','%s', %s,'%s')" % (self.date, self.key, self.zone, count)
        sql = 'INSERT INTO ns_domain_group_count_statistic(`date`, `ns_group`, `tld`, `count`) VALUE ' \
              + sql_insert_date

        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)

    @staticmethod
    def update_ns_domain_group_count_statistic_python(date: datetime, today: datetime, zone: str,
                                                      count: int = COUNT_THREAD):
        """
        Реализация на питоне с использованием процессов
        """
        zone_id = PREFIX_LIST_ZONE[zone]

        while date <= today:
            connection = get_mysql_connection()
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)

            ns_array = {}
            provider_array = {}

            sql_has_data = """SELECT count(*) as count FROM ns_count_statistic
                              WHERE tld = '%s' AND date = '%s'""" % (zone_id, date)
            cursor.execute(sql_has_data)
            data = cursor.fetchone()

            if data['count'] == 0:
                # Вариант когда записей нет в статистикие по NS серверам
                for i in range(1, 5):
                    sql = """SELECT ns%s as ns, count(*) as count FROM domain_history
                            WHERE delegated = 'Y' AND tld = '%s' AND date_start <= '%s' AND date_end >= '%s'
                            GROUP BY ns%s
                            HAVING count(*) > %s
                            ORDER BY count(*) desc""" % (i, zone_id, date, date, i, MINIMUM_DOMAIN_COUNT)

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
                        WHERE tld = '%s' AND date= '%s'""" % (zone_id, date)
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
                    print(e)

            sql = """SELECT ns1, ns2, ns3, ns4 FROM domain_history
                    WHERE delegated = 'Y' AND tld = '%s' AND date_start <= '%s' AND date_end >= '%s'
            """ % (zone_id, date, date)
            cursor.execute(sql)
            data = cursor.fetchall()

            connection.close()

            process_list = []
            i = 0

            for key in provider_array:
                search_string = key

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
