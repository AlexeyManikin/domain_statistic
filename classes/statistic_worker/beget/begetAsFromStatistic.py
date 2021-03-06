__author__ = 'Alexey Y Manikin'

from classes.statistic_worker.statisticBaseClass import StatisticBaseClass
import MySQLdb
import datetime
from config.main import PREFIX_LIST_ZONE


class BegetAsFromStatistic(StatisticBaseClass):

    def __init__(self, number: int, data: datetime, today: datetime, zone: str):
        """
        :param number:
        """
        StatisticBaseClass.__init__(self, number, 'beget_as_from')
        self.today = today
        self.data = data
        self.zone = PREFIX_LIST_ZONE[zone]

    def _update(self):
        """
        :type date: date
        :type today: date
        :type zone: unicode
        :return:
        """
        date = self.data
        today = self.today

        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        while date <= today:
            sql_insert = ''
            sql = """SELECT 
    dh2.domain_name, 
    dh2.tld, 
    dh2.asn1
FROM
    domain_history AS dh2
WHERE
    dh2.date_start <= DATE_SUB('%s', INTERVAL 1 DAY)
        AND dh2.date_end > DATE_SUB('%s', INTERVAL 1 DAY)
        AND dh2.domain_name IN (SELECT 
            dh1.domain_name
        FROM
            domain_history AS dh1
        WHERE
            dh1.asn1 = %i
                AND dh1.date_start <= '%s'
                AND dh1.date_end > '%s'
                AND dh1.delegated = 'Y'
                AND dh1.domain_name IN (SELECT 
                    dh.domain_name
                FROM
                    domain_history AS dh
                WHERE
                    dh.date_start <= DATE_SUB('%s', INTERVAL 1 DAY)
                        AND dh.date_end > DATE_SUB('%s', INTERVAL 1 DAY)
                        AND dh.asn1 != %i
                        AND dh.delegated = 'Y'
                        AND dh.tld = %s))""" % (date, date, self.BEGET_AS, date, date, date,
                                                date, self.BEGET_AS, self.zone)

            cursor.execute(sql)
            data = cursor.fetchall()

            for row in data:
                sql_insert_date = " ('%s','%s','%s', %s)" % (date, row['domain_name'], row['asn1'], self.zone)
                if len(sql_insert) > 5:
                    sql_insert += ", " + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            if len(sql_insert) > 1:
                sql = """INSERT INTO beget_domain_as_from_count_statistic(`date`, 
                            `domain_name`, 
                            `as_from`, 
                            `tld`) VALUE """ + sql_insert
                cursor.execute(sql)
                self.connection.commit()

            date += datetime.timedelta(days=1)
