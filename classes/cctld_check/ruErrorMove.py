# -*- coding: utf-8 -*-
# Проверка на соблюдения сроков переносов доменов. В соотвествии с правилами сcctld.ru нельзя переносить домен
# если с предыдущего переноса прошло менее 30 дней
__author__ = 'Alexey Y Manikin'

from helpers.helpers import get_mysql_connection
import MySQLdb


class RuErrorMove(object):
    def __init__(self):
        """
        :return:
        """
        self._connect_mysql()

    def _connect_mysql(self):
        """
        :return:
        """
        self.connection = get_mysql_connection()

    @staticmethod
    def _find_move_errors(domain_array):
        """
        :param domain_array:
        :return:
        """
        domain_array_last = {}

        current_domain = 0
        count_domain = len(domain_array)

        for domain_name in domain_array:
            new_data = []
            old_registrar = ''

            for domain_data in domain_array[domain_name]:
                if old_registrar != domain_data['registrant']:
                    new_data.append(domain_data)
                    old_registrar = domain_data['registrant']

            domain_array[domain_name] = new_data

            if len(domain_array[domain_name]) > 2:
                number = 0
                last_date_start = 0
                last_register_date = 0
                flag = 0
                count_update = 1

                for domain_change_data in domain_array[domain_name]:
                    if number == 0:
                        last_date_start = domain_change_data['date_start']
                        last_register_date = domain_change_data['register_date']
                        number = number + 1
                    else:
                        new_date_start = domain_change_data['date_start']
                        new_register_date = domain_change_data['register_date']
                        delta = new_date_start - last_date_start

                        #print("delta = %s, %s, %s" % (delta.days, last_register_date, new_register_date))
                        if last_register_date == new_register_date:
                            count_update = count_update + 1
                        else:
                            count_update = 0

                        if delta.days < 29 and count_update > 2:
                            flag = 1

                        number = number + 1
                        last_date_start = new_date_start
                        last_register_date = domain_change_data['register_date']
                    if flag == 1:
                        domain_array_last[domain_name] = domain_array[domain_name]
                        continue

            current_domain = current_domain + 1
            if current_domain % 10000 == 1:
                print("count = %s/%s" % (current_domain, count_domain))

        return domain_array_last

    def get_domain_info(self):
        """
        :return:
        """
        domain_array = {}
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """SELECT domain_name, date_start, registrant, free_date, register_date
FROM domain_history 
WHERE date_start > '2018-01-01' ORDER BY id
"""

        cursor.execute(sql)
        data = cursor.fetchall()

        for row in data:
            domain_data = {'registrant': row['registrant'],
                           'date_start': row['date_start'],
                           'date_free': row['free_date'],
                           'register_date': row['register_date']}

            if row['domain_name'] in domain_array:
                domain_array[row['domain_name']].append(domain_data)
            else:
                domain_array[row['domain_name']] = [domain_data]

        return self._find_move_errors(domain_array)

    def run(self):
        domain_list = self.get_domain_info()
        for domain_name, data in list(domain_list.items()):
            print((" %s:" % domain_name))
            for item in data:
                print(("   %s - %s (%s)" % (item['date_start'], item['registrant'], item['register_date'])))
