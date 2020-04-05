__author__ = 'Alexey Y Manikin'

from classes.statistic_worker.statisticBaseClass import StatisticBaseClass
import MySQLdb
import datetime
from config.main import PREFIX_LIST_ZONE


class BegetNsToStatistic(StatisticBaseClass):

    def __init__(self, number: int, data: datetime, today: datetime, zone: str):
        """
        :param number:
        """
        StatisticBaseClass.__init__(self, number, 'beget_ns_to')
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
            sql = """SELECT 
            dh1.domain_id,
            dh1.domain_name, 
            dh1.tld, 
            dh1.ns1
        FROM
            domain_history AS dh1
        WHERE
            dh1.ns1_like_beget = 0
                AND dh1.date_start <= '%s'
                AND dh1.date_end > '%s'
                AND dh1.domain_id IN (SELECT 
                    dh.domain_id
                FROM
                    domain_history AS dh
                WHERE
                    dh.date_start <= DATE_SUB('%s', INTERVAL 1 DAY)
                        AND dh.date_end > DATE_SUB('%s', INTERVAL 1 DAY)
                        AND dh.ns1_like_beget = 1
                        AND dh.tld = %s)""" % (date, date, date, date, self.zone)

            cursor.execute(sql)
            data = cursor.fetchall()

            for row in data:
                sql_insert_date = " ('%s','%s','%s','%s', %s)" % (date,
                                                                  row['domain_id'],
                                                                  row['domain_name'],
                                                                  row['ns1'],
                                                                  self.zone)
                if len(sql_insert) > 5:
                    sql_insert += ", " + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            if len(sql_insert) > 1:
                sql = """INSERT INTO beget_domain_ns_to_count_statistic(`date`, 
                            `domain_id`, 
                            `domain_name`, 
                            `ns1_to`, 
                            `tld`) VALUE """ + sql_insert
                cursor.execute(sql)
                self.connection.commit()

            date += datetime.timedelta(days=1)
