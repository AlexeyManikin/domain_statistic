__author__ = 'Alexey Y Manikin'

from classes.statistic_worker.statisticBaseClass import StatisticBaseClass
import MySQLdb
import datetime
from config.main import MINIMUM_DOMAIN_COUNT, PREFIX_LIST_ZONE


class AsCountStatistic(StatisticBaseClass):

    def __init__(self, number: int, data: datetime, today: datetime, zone: str):
        """
        :param number:
        """
        StatisticBaseClass.__init__(self, number, "as_count_")

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
            as_array = {}

            sql = """SELECT asn1 as as_number, count(*) as count FROM domain_history
   WHERE delegated = 'Y' AND tld = %s AND date_start <= '%s' AND date_end > '%s'
   GROUP BY asn1
   HAVING count(*) > %s
   ORDER BY count(*) desc""" % (self.zone, date, date, MINIMUM_DOMAIN_COUNT)

            cursor.execute(sql)
            data = cursor.fetchall()

            for row in data:
                if row['as_number'] is None:
                    asn = 0
                else:
                    asn = row['as_number']

                as_array[asn] = row['count']

            for key in as_array:
                sql_insert_date = " ('%s', %s,'%s', '%s')" % (date, self.zone, key, as_array[key])
                if len(sql_insert) > 5:
                    sql_insert += ', ' + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            if len(sql_insert) > 1:
                sql = 'INSERT INTO as_count_statistic(`date`, `tld`, `asn`, `count`) VALUE ' + sql_insert
                cursor.execute(sql)
                self.connection.commit()

            date += datetime.timedelta(days=1)
