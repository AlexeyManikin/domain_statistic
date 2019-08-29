# -*- coding: utf-8 -*-
__author__ = 'alexeyymanikin'

import MySQLdb
from helpers.helpersCollor import BColor
from helpers.helpers import get_mysql_connection


class DbNormalization(object):

    def __init__(self, show_log: bool=False):
        """
        :return:
        """
        self.connection = get_mysql_connection()
        self.show_log = show_log

    def __del__(self):
        """
        Подчисщаем за собой все
        :return:
        """
        self.connection.close()

    def _normalization_delete_record(self):
        """
        Нормализация удаленных и вновь добавленных доменов. То есть если домен был удален и зарегистрирован,
        у него должна быть одна история
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)

        sql = """SELECT DISTINCT domain_id AS domain_id FROM domain_history
WHERE domain_id NOT IN (SELECT id FROM domain)"""
        cursor.execute(sql)
        data = cursor.fetchall()

        count_deleted_domain = len(data)
        current_domain = 0
        count_not_update = 0
        count_update = 0

        if self.show_log:
            BColor.ok("All deleted domain is %s" % count_deleted_domain)

        for row in data:
            if current_domain % 10000 == 1:
                if self.show_log:
                    updated_percent = round(count_update / (current_domain / 100))
                    BColor.process("Current domain %s/%s (updated %s percent)" % (current_domain,
                                                                                  count_deleted_domain,
                                                                                  updated_percent))

                self.connection.commit()

            sql = "SELECT DISTINCT domain_name FROM domain_history WHERE domain_id = %s" % (row['domain_id'])
            cursor.execute(sql)
            domain_history = cursor.fetchone()

            sql = "SELECT id FROM domain WHERE domain_name = '%s'" % (domain_history['domain_name'])
            cursor.execute(sql)
            domain = cursor.fetchone()

            if domain:
                sql_update = "UPDATE domain_history SET domain_id = %s WHERE domain_id = %s" % (domain['id'],
                                                                                                row['domain_id'])
                cursor.execute(sql_update)
                count_update += 1
            else:
                count_not_update += 1

            current_domain += 1

    @staticmethod
    def _set_domain_fields(row: dict) -> dict:
        """
        :param row:
        :return:
        """
        domain_fields = {'registrant_id': row['registrant_id'],
                         'register_date': row['register_date'],
                         'register_date_end': row['register_date_end'],
                         'free_date': row['free_date'],
                         'delegated': row['delegated'],
                         'a1': row['a1'],
                         'a2': row['a2'],
                         'a3': row['a3'],
                         'a4': row['a4'],
                         'ns1': row['ns1'],
                         'ns2': row['ns2'],
                         'ns3': row['ns3'],
                         'ns4': row['ns4'],
                         'mx1': row['mx1'],
                         'mx2': row['mx2'],
                         'mx3': row['mx3'],
                         'mx4': row['mx4'],
                         'txt': row['txt'],
                         'asn1': row['asn1'],
                         'asn2': row['asn2'],
                         'asn3': row['asn3'],
                         'asn4': row['asn4'],
                         'aaaa1': row['aaaa1'],
                         'aaaa2': row['aaaa2'],
                         'aaaa3': row['aaaa3'],
                         'aaaa4': row['aaaa4'],
                         'nserrors': row['nserrors'],
                         'id': row['id'],
                         'date_end': row['date_end'],
                         'date_start': row['date_start']
                         }
        return domain_fields

    @staticmethod
    def _compare_domain_fields(old: dict, new: dict) -> bool:
        """
        :param old:
        :param new:
        :return:
        """
        if old['registrant_id'] == new['registrant_id'] \
                and old['register_date'] == new['register_date'] \
                and old['register_date_end'] == new['register_date_end'] \
                and old['free_date'] == new['free_date'] \
                and old['delegated'] == new['delegated'] \
                and old['a1'] == new['a1'] \
                and old['a2'] == new['a2'] \
                and old['a3'] == new['a3'] \
                and old['a4'] == new['a4'] \
                and old['ns1'] == new['ns1'] \
                and old['ns2'] == new['ns2'] \
                and old['ns3'] == new['ns3'] \
                and old['ns4'] == new['ns4'] \
                and old['mx1'] == new['mx1'] \
                and old['mx2'] == new['mx2'] \
                and old['mx3'] == new['mx3'] \
                and old['mx4'] == new['mx4'] \
                and old['txt'] == new['txt'] \
                and old['asn1'] == new['asn1'] \
                and old['asn2'] == new['asn2'] \
                and old['asn3'] == new['asn3'] \
                and old['asn4'] == new['asn4'] \
                and old['aaaa1'] == new['aaaa1'] \
                and old['aaaa2'] == new['aaaa2'] \
                and old['aaaa3'] == new['aaaa3'] \
                and old['aaaa4'] == new['aaaa4'] \
                and old['nserrors'] == new['nserrors']:
            return True
        return False

    def _normalization_duplicate_records(self):
        """
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "SELECT DISTINCT domain_id AS domain_id FROM domain_history"
        cursor.execute(sql)
        data = cursor.fetchall()

        current_domain: int = 0

        for row in data:
            sql = "SELECT * FROM domain_history WHERE domain_id = %s ORDER BY id" % (row['domain_id'])
            print(sql)
            cursor.execute(sql)
            domain_data = cursor.fetchall()

            domain_fields_old: dict[str, str] = {'registrant_id': '',
                                                 'register_date': '',
                                                 'register_date_end': '',
                                                 'free_date': '',
                                                 'delegated': '',
                                                 'a1': '',
                                                 'a2': '',
                                                 'a3': '',
                                                 'a4': '',
                                                 'ns1': '',
                                                 'ns2': '',
                                                 'ns3': '',
                                                 'ns4': '',
                                                 'mx1': '',
                                                 'mx2': '',
                                                 'mx3': '',
                                                 'mx4': '',
                                                 'txt': '',
                                                 'asn1': '',
                                                 'asn2': '',
                                                 'asn3': '',
                                                 'asn4': '',
                                                 'aaaa1': '',
                                                 'aaaa2': '',
                                                 'aaaa3': '',
                                                 'aaaa4': '',
                                                 'nserrors': '',
                                                 'date_end': '',
                                                 'date_start': '',
                                                 'id': ''
                                                 }

            for row_domain in domain_data:
                domain_fields_new = self._set_domain_fields(row_domain)
                if self._compare_domain_fields(domain_fields_old, domain_fields_new):
                    sql = "UPDATE domain_history SET date_end = '%s' WHERE id = %s" % (domain_fields_new['date_end'],
                                                                                       domain_fields_old['id'])
                    cursor.execute(sql)
                    sql = "DELETE FROM domain_history WHERE id = %s" % domain_fields_new['id']
                    cursor.execute(sql)

                    current_domain = current_domain + 1
                    if current_domain % 1000 == 1:
                        self.connection.commit()

                    print("domain: %s - old_row %s, new_row %s" % (row_domain['domain_name'],
                                                                   domain_fields_old['id'],
                                                                   domain_fields_new['id']))
                else:
                    domain_fields_old = domain_fields_new

            self.connection.commit()

    def _normalization_one_domain(self, domain_id: int):
        """
        :type domain_id: int
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "SELECT * FROM domain_history WHERE domain_id = %s ORDER BY id" % domain_id
        cursor.execute(sql)
        domain_data = cursor.fetchall()

        domain_fields_old: dict[str, str] = {'registrant_id': '',
                                             'register_date': '',
                                             'register_date_end': '',
                                             'free_date': '',
                                             'delegated': '',
                                             'a1': '',
                                             'a2': '',
                                             'a3': '',
                                             'a4': '',
                                             'ns1': '',
                                             'ns2': '',
                                             'ns3': '',
                                             'ns4': '',
                                             'mx1': '',
                                             'mx2': '',
                                             'mx3': '',
                                             'mx4': '',
                                             'txt': '',
                                             'asn1': '',
                                             'asn2': '',
                                             'asn3': '',
                                             'asn4': '',
                                             'aaaa1': '',
                                             'aaaa2': '',
                                             'aaaa3': '',
                                             'aaaa4': '',
                                             'nserrors': '',
                                             'date_end': '',
                                             'date_start': '',
                                             'id': ''
                                             }

        for row_domain in domain_data:
            domain_fields_new = self._set_domain_fields(row_domain)

            if domain_fields_new['date_start'] == domain_fields_new['date_end'] \
                and domain_fields_new['register_date'] == domain_fields_old['register_date'] \
                    and domain_fields_new['date_start'] != domain_fields_old['date_end']:

                sql = "UPDATE domain_history SET date_start = '%s' WHERE id = %s" % (domain_fields_old['date_end'],
                                                                                     domain_fields_new['id'])
                cursor.execute(sql)
                self.connection.commit()

            domain_fields_old = domain_fields_new

    def normalization_domain_date(self):
        """
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "SELECT DISTINCT domain_id AS domain_id FROM domain_history"
        cursor.execute(sql)
        data = cursor.fetchall()

        current_domain: int = 0

        for row in data:
            self._normalization_one_domain(row['domain_id'])
            current_domain = current_domain + 1
            if current_domain % 10000 == 1:
                print("current domain %s" % current_domain)

    def normalization_db(self):
        """
        Обновление всех статистик
        :return:
        """
        self._normalization_delete_record()
        # self._normalization_duplicate_records()
        # self.normalization_domain_date()
