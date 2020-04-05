__author__ = 'Alexey Y Manikin'

from helpers.helpers import get_mysql_connection
import datetime
import MySQLdb
from pprint import pprint
from datetime import datetime


class ShowAsStatistic(object):
    def __init__(self):
        """
        :return:
        """
        self.connection = get_mysql_connection()

    def _connect_mysql(self):
        """
        :return:
        """
        self.connection = get_mysql_connection()

    def get_info_to_as_now(self, as_number, date_start):
        """
        :param as_number:
        :param date_start:
        :param date_end:
        :return:
        """
        sql = """
SELECT 
    t.asn1 AS 'Number',
    asl.descriptions AS 'Descriptions',
    t.count AS 'Count'
FROM
    (SELECT 
        dh2.asn1, COUNT(*) AS count
    FROM
        domain_history AS dh2
    WHERE
        dh2.date_start <= '{1}'
            AND dh2.date_end > '{1}'
            AND dh2.domain_id IN (SELECT 
                dh1.id
            FROM
                domain AS dh1
            WHERE
                dh1.asn1 = {0}
                    AND dh1.ns1 != 'ns1.expired.reg.ru.'
                    AND dh1.ns1 != 'expirepages-kiae-1.nic.ru.'
                    AND dh1.ns1 != 'ns1.expired.r01.ru.'
                    AND dh1.ns1 != 'ns1.expiring.salenames.ru.'
                    AND dh1.ns1 != 'expired1.axelname.ru.'
                    AND dh1.ns1 != 'ns1.expired.domenus.ru.'
                    AND dh1.a1 != '31.31.205.163'
                    AND dh1.id IN (SELECT 
                        dh.domain_id
                    FROM
                        domain_history AS dh
                    WHERE
                        dh.date_start <= '{1}'
                            AND dh.date_end > '{1}'
                            AND dh.asn1 != {0}))
    GROUP BY dh2.asn1) AS t
        LEFT JOIN
    as_list AS asl ON (t.asn1 = asl.id)
ORDER BY t.count;""".format(as_number, date_start)

        return_array = []
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)

        data = cursor.fetchall()
        for row in data:
            if row['count'] > 10:
                return_array[row['Number']] = { 'as_number': row['Number'],
                                                'as_description': row['Descriptions'],
                                                'count': row['Count']}
            else:
                if '0' in return_array:
                    count = row['count'] + return_array[0]['count']
                    return_array[0] = {'as_number': 0,
                                       'as_description': "--",
                                       'count': count}
                else:
                    return_array[0] = {'as_number': 0,
                                       'as_description': "--",
                                       'count': row['count']}

        return return_array





