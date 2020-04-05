__author__ = 'Alexey Y Manikin'

from classes.statistic_worker.statisticBaseClass import StatisticBaseClass
import MySQLdb
import datetime


class BegetRegistrantToStatistic(StatisticBaseClass):

    def __init__(self, number: int, data: datetime, today: datetime):
        """
        :param number:
        """
        StatisticBaseClass.__init__(self, number, 'beget_registrant_to')
        self.today = today
        self.data = data

    def _update(self):
        """
        :type date: date
        :type today: date
        :return:
        """
        date = self.data
        today = self.today

        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        registrant_id: int = self.get_beget_registrant(cursor)

        while date <= today:
            sql_insert = ''
            sql = """SELECT 
            dh1.domain_id,
            dh1.domain_name, 
            dh1.registrant_id
        FROM
            domain_history AS dh1
        WHERE
                dh1.registrant_id != %i
                AND dh1.date_start <= '%s'
                AND dh1.date_end > '%s'
                AND dh1.domain_id IN (SELECT 
                    dh.domain_id
                FROM
                    domain_history AS dh
                WHERE
                    dh.date_start <= DATE_SUB('%s', INTERVAL 1 DAY)
                        AND dh.date_end > DATE_SUB('%s', INTERVAL 1 DAY)
                        AND dh.registrant_id = %i)
                        """ % (registrant_id, date, date, date, date, registrant_id)

            cursor.execute(sql)
            data = cursor.fetchall()

            for row in data:
                sql_insert_date = " ('%s','%s','%s','%s')" % (date,
                                                              row['domain_id'],
                                                              row['domain_name'],
                                                              row['registrant_id'])
                if len(sql_insert) > 5:
                    sql_insert += ", " + sql_insert_date
                else:
                    sql_insert += sql_insert_date

            if len(sql_insert) > 1:
                sql = """INSERT INTO beget_domain_registrant_to_count_statistic(`date`, 
                            `domain_id`, 
                            `domain_name`, 
                            `registrant_id_to`) VALUE """ + sql_insert
                cursor.execute(sql)
                self.connection.commit()

            date += datetime.timedelta(days=1)

