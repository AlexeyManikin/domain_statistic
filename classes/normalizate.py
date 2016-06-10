# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'alexeyymanikin'

import MySQLdb
from helpers.helpersCollor import BColor

from helpers.helpers import get_mysql_connection


class DbNormalizate(object):

    def __init__(self, show_log=False):
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

        if self.show_log:
            BColor.ok("Select deleted domain from domain_history")

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
            if self.show_log:
                BColor.process("Current domain %s/%s" % (current_domain, count_deleted_domain))
                BColor.ok("Updated %s, not updated %s" % (count_update, count_not_update))

            sql = "SELECT DISTINCT domain_name FROM domain_history WHERE domain_id = %s" % (row['domain_id'])
            BColor.warning(sql)
            cursor.execute(sql)
            domain_history = cursor.fetchone()

            sql = "SELECT id FROM domain WHERE domain_name = '%s'" % (domain_history['domain_name'])
            BColor.warning(sql)
            cursor.execute(sql)
            domain = cursor.fetchone()

            if domain:
                if self.show_log:
                    BColor.warning("Domain %s (%s) has new domain_id = %s" % (domain_history['domain_name'],
                                                                              row['domain_id'],
                                                                              domain['id']))

                sql_update = "UPDATE domain_history SET domain_id = %s WHERE domain_id = %s" % (domain['id'],
                                                                                                row['domain_id'])
                cursor.execute(sql_update)
                count_update += 1
            else:
                count_not_update += 1

            current_domain += 1

    def normalization_db(self):
        """
        Обновление всех статистик
        :return:
        """
        self._normalization_delete_record()
