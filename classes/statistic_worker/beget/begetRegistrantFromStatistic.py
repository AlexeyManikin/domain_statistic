__author__ = 'Alexey Y Manikin'

from classes.statistic_worker.statisticBaseClass import StatisticBaseClass
import MySQLdb
import datetime


class BegetRegistrantFromStatistic(StatisticBaseClass):

    def __init__(self, number: int, data: datetime, today: datetime):
        """
        :param number:
        """
        StatisticBaseClass.__init__(self, number, 'beget_registrant_from')
        self.today = today
        self.data = data

    def _update(self):
        """
        :return:
        """
        date = self.data
        today = self.today

        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        registrant_id: int = self.get_beget_registrant(self.connection)

        while date <= today:
            sql_insert = ''
            sql = """SELECT  
    dh2.domain_name, 
    dh2.registrant_id
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
                dh1.registrant_id = %i
                AND dh1.date_start <= '%s'
                AND dh1.date_end > '%s'
                AND dh1.domain_name IN (SELECT 
                    dh.domain_name
                FROM
                    domain_history AS dh
                WHERE
                    dh.date_start <= DATE_SUB('%s', INTERVAL 1 DAY)
                        AND dh.date_end > DATE_SUB('%s', INTERVAL 1 DAY)
                        AND dh.registrant_id != %i))
                        """ % (date, date, registrant_id, date, date, date, date, registrant_id)

            cursor.execute(sql)
            data = cursor.fetchall()

            for row in data:
                sql_insert_date = " ('%s','%s','%s')" % (date, row['domain_name'], row['registrant_id'])
                if len(sql_insert) > 5:
                    sql_insert += ", " + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            if len(sql_insert) > 1:
                sql = """INSERT INTO beget_domain_registrant_from_count_statistic(`date`, 
                            `domain_name`, 
                            `registrant_id_from`) VALUE """ + sql_insert
                cursor.execute(sql)
                self.connection.commit()

            date += datetime.timedelta(days=1)
