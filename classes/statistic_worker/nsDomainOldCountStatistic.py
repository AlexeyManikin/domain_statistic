__author__ = 'Alexey Y Manikin'

from classes.statistic_worker.statisticBaseClass import StatisticBaseClass
import MySQLdb
import datetime
from config.main import MINIMUM_DOMAIN_COUNT, PREFIX_LIST_ZONE


class NsDomainOldCountStatistic(StatisticBaseClass):

    def __init__(self, number: int, data: datetime, today: datetime, zone: str):
        """
        :param number:
        """
        StatisticBaseClass.__init__(self, number, "ns_domain_old_count_")
        self.today = today
        self.data = data
        self.zone_id = PREFIX_LIST_ZONE[zone]

    def _get_data(self, number: int, date: datetime) -> list:
        """
        В зависимости от дня статистики обращаемся или к domain_history или к domain
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)

        if date == datetime.date.today():
            sql = """SELECT ns%i as ns, AVG(DATEDIFF(NOW(), register_date)) as old, count(*) as count
            FROM domain
            WHERE tld = %i AND delegated = 'Y'
            GROUP BY ns%i
            HAVING count(*) > %i
            ORDER BY count(*) desc""" % (number, self.zone_id, number, MINIMUM_DOMAIN_COUNT)
        else:
            sql = """SELECT ns%i as ns, AVG(DATEDIFF(NOW(), register_date)) as old, count(*) as count
            FROM domain_history
            WHERE tld = %i AND date_start <= '%s' AND date_end >= '%s' AND delegated = 'Y'
            GROUP BY ns%i
            HAVING count(*) > %i
            ORDER BY count(*) desc""" % (number, self.zone_id, date, date, number, MINIMUM_DOMAIN_COUNT)

        cursor.execute(sql)
        return cursor.fetchall()

    def _update(self):
        """
        :return:
        """
        date = self.data
        today = self.today

        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            ns_list = {}

            for i in range(1, 5):
                data = self._get_data(i, date)
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

                sql_insert_date = " ('%s', '%s', %i, '%s')" % (date, key, self.zone_id, old)
                if len(sql_insert) > 5:
                    sql_insert += ', ' + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            if len(sql_insert) > 1:
                sql = 'INSERT INTO ns_domain_old_count_statistic(`date`, `ns`, `tld`, `old`) VALUE ' + sql_insert
                cursor.execute(sql)

            date += datetime.timedelta(days=1)