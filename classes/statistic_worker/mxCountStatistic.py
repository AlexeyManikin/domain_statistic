__author__ = 'Alexey Y Manikin'

from classes.statistic_worker.statisticBaseClass import StatisticBaseClass
import MySQLdb
import datetime
from config.main import MINIMUM_DOMAIN_COUNT, PREFIX_LIST_ZONE


class MxCountStatistic(StatisticBaseClass):

    def __init__(self, number: int, data: datetime, today: datetime, zone: str):
        """
        :param number:
        """
        StatisticBaseClass.__init__(self, number, "mx_count_")
        self.today = today
        self.data = data
        self.zone = PREFIX_LIST_ZONE[zone]

    def _update(self):
        """
        :return:
        """
        date = self.data
        today = self.today

        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            sql_insert = ''
            mx_array = {}

            for i in range(1, 5):
                sql = """SELECT mx%s as mx, count(*) as count FROM domain_history
    WHERE delegated = 'Y' AND tld = %s AND date_start <= '%s' AND date_end >= '%s'
    GROUP BY mx%s
    HAVING count(*) > %s
    ORDER BY count(*) desc""" % (i, self.zone, date, date, i, MINIMUM_DOMAIN_COUNT)

                cursor.execute(sql)
                data = cursor.fetchall()

                for row in data:
                    if row['mx'] in mx_array:
                        mx_array[row['mx']] += row['count']
                    else:
                        mx_array[row['mx']] = row['count']

            for key in mx_array:
                sql_insert_date = " ('%s', %s,'%s', '%s')" % (date, self.zone, key, mx_array[key])
                if len(sql_insert) > 5:
                    sql_insert += ", " + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            if len(sql_insert) > 1:
                sql = 'INSERT INTO mx_count_statistic(`date`, `tld`, `mx`, `count`) VALUE ' + sql_insert
                cursor.execute(sql)

            date += datetime.timedelta(days=1)
