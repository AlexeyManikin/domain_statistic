__author__ = 'Alexey Y Manikin'

from classes.statistic_worker.statisticBaseClass import StatisticBaseClass
import MySQLdb
import datetime
from config.main import MINIMUM_DOMAIN_COUNT, PREFIX_LIST_ZONE


class ACountStatistic(StatisticBaseClass):

    def __init__(self, number: int, data: datetime, today: datetime, zone: str):
        """
        :param number:
        """
        StatisticBaseClass.__init__(self, number, "a_count_")

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
            sql = """SELECT a%i as a, asn%i as asn, count(*) as count FROM domain
            WHERE delegated = 'Y' AND tld = %i 
            GROUP BY a%i
            HAVING count(*) > %i
            ORDER BY count(*) desc""" % (number, number, self.zone_id, number, MINIMUM_DOMAIN_COUNT)
        else:
            sql = """SELECT a%i as a, asn%i as asn, count(*) as count FROM domain_history
            WHERE delegated = 'Y' AND tld = %i AND date_start <= '%s' AND date_end >= '%s'
            GROUP BY a%i
            HAVING count(*) > %i
            ORDER BY count(*) desc""" % (number, number, self.zone_id, date, date, number, MINIMUM_DOMAIN_COUNT)

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
            a_array = {}
            asn_array = {}

            for i in range(1, 5):
                data = self._get_data(i, date)
                for row in data:
                    if row['a'] is None:
                        row['a'] = 0

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

                sql_insert_date = " ('%s', %i,'%s', '%s', '%s')" % (date,
                                                                    self.zone_id,
                                                                    key,
                                                                    a_array[key],
                                                                    asn)
                if len(sql_insert) > 5:
                    sql_insert += ', ' + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            if len(sql_insert) > 1:
                sql = 'INSERT INTO a_count_statistic(`date`, `tld`, `a`, `count`, `asn`) VALUE ' + sql_insert
                cursor.execute(sql)

            date += datetime.timedelta(days=1)
