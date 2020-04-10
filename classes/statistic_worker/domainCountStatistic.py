__author__ = 'Alexey Y Manikin'

from classes.statistic_worker.statisticBaseClass import StatisticBaseClass
import MySQLdb
import datetime
from config.main import PREFIX_LIST_ZONE


class DomainCountStatistic(StatisticBaseClass):

    def __init__(self, number: int, data: datetime, today: datetime, zone: str):
        """
        :param number:
        """
        StatisticBaseClass.__init__(self, number, "domain_count_")
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
            sql = """SELECT count(*) as count FROM domain
            WHERE tld = %i 
            ORDER BY count(*) desc""" % self.zone_id
        else:
            sql = """SELECT count(*) as count FROM domain_history
            WHERE tld = %i AND date_start <= '%s' AND date_end >= '%s'
            ORDER BY count(*) desc""" % (self.zone_id, date, date)

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
            data = self._get_data(date)
            for row in data:
                sql_insert_date = " ('%s', %i, '%s')" % (date, self.zone_id, row['count'])
                if len(sql_insert) > 5:
                    sql_insert += ", " + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            if len(sql_insert) > 1:
                sql = 'INSERT INTO domain_count_statistic(`date`, `tld`, `count`) VALUE ' + sql_insert
                cursor.execute(sql)
                self.connection.commit()

            date += datetime.timedelta(days=1)
