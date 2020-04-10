__author__ = 'Alexey Y Manikin'

from classes.statistic_worker.statisticBaseClass import StatisticBaseClass
import MySQLdb
import datetime
from config.main import MINIMUM_DOMAIN_COUNT, PREFIX_LIST_ZONE


class AsDomainOldCountStatistic(StatisticBaseClass):

    def __init__(self, number: int, data: datetime, today: datetime, zone: str):
        """
        :param number:
        """
        StatisticBaseClass.__init__(self, number, "domain_old_count_")

        self.today = today
        self.data = data
        self.zone_id = PREFIX_LIST_ZONE[zone]

    def _get_data(self, date: datetime) -> list:
        """
        В зависимости от дня статистики обращаемся или к domain_history или к domain
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)

        if date == datetime.date.today():
            sql = """SELECT asn1 as asn, AVG(DATEDIFF(NOW(), register_date)) as old, count(*) as count
            FROM domain
            WHERE tld = %i AND delegated = 'Y'
            GROUP BY asn1
            HAVING count(*) > %i
            ORDER BY count(*) desc""" % (self.zone_id, MINIMUM_DOMAIN_COUNT)
        else:
            sql = """SELECT asn1 as asn, AVG(DATEDIFF(NOW(), register_date)) as old, count(*) as count
            FROM domain_history
            WHERE tld = %i AND date_start <= '%s' AND date_end >= '%s' AND delegated = 'Y'
            GROUP BY asn1
            HAVING count(*) > %i
            ORDER BY count(*) desc""" % (self.zone_id, date, date, MINIMUM_DOMAIN_COUNT)

        cursor.execute(sql)
        return cursor.fetchall()

    def _update(self):
        """
        Особого смысла смотреть по всем 4 а записям не вижу, только лишняя нагрузка на базу. На данные
        статистики почти не влияет.
        :return:
        """
        date = self.data
        today = self.today

        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            sql_insert = ""
            data = self._get_data(date)
            for row in data:

                if row['asn'] is None or row['asn'] == 'None':
                    row['asn'] = 0

                sql_insert_date = " ('%s','%s', %i, '%s')" % (date, row['asn'], self.zone_id, row['old'])
                if len(sql_insert) > 5:
                    sql_insert += ', ' + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            if len(sql_insert) > 1:
                sql = 'INSERT INTO as_domain_old_count_statistic(`date`, `asn`, `tld`, `old`) VALUE ' + sql_insert
                cursor.execute(sql)

            date += datetime.timedelta(days=1)
