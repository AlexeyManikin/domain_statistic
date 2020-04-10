__author__ = 'Alexey Y Manikin'

from classes.statistic_worker.statisticBaseClass import StatisticBaseClass
import MySQLdb
import datetime
from config.main import MINIMUM_DOMAIN_COUNT, PREFIX_LIST_ZONE


class NsCountStatistic(StatisticBaseClass):

    def __init__(self, number: int, data: datetime, today: datetime, zone: str):
        """
        :param number:
        """
        StatisticBaseClass.__init__(self, number, "ns_count_")
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
            sql = """SELECT ns%i as ns, count(*) as count FROM domain
            WHERE delegated = 'Y' AND tld = %i 
            GROUP BY ns%i
            HAVING count(*) > %i
            ORDER BY count(*) desc""" % (number, self.zone_id, number, MINIMUM_DOMAIN_COUNT)
        else:
            sql = """SELECT ns%i as ns, count(*) as count FROM domain_history
            WHERE delegated = 'Y' AND tld = %i AND date_start <= '%s' AND date_end >= '%s'
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
            sql_insert = ''
            ns_array = {}

            for i in range(1, 5):
                data = self._get_data(i, date)

                for row in data:
                    if row['ns'] in ns_array:
                        ns_array[row['ns']] += row['count']
                    else:
                        ns_array[row['ns']] = row['count']

            for key in ns_array:
                sql_insert_date = " ('%s', %i, '%s', '%s')" % (date, self.zone_id, key, ns_array[key])
                if len(sql_insert) > 5:
                    sql_insert += ', ' + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            if len(sql_insert) > 1:
                sql = 'INSERT INTO ns_count_statistic(`date`, `tld`, `ns`, `count`) VALUE ' + sql_insert
                cursor.execute(sql)

            date += datetime.timedelta(days=1)
