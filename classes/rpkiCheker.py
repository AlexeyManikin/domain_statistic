# -*- coding: utf-8 -*-
__author__ = 'alexeyymanikin'

import re
import urllib.request, urllib.error, urllib.parse
import json
import SubnetTree
from helpers.helperUnicode import as_bytes
from config.main import PRKI_JSON_URL
import MySQLdb
from helpers.helpers import get_mysql_connection
from helpers.helpersCollor import BColor
import time

RPKI_ERROR = -2
RPKI_LOAD_ERROR = -1
PRKI_VALID = 0
PRKI_INVALID_AS = 1
PRKI_INVALID_NOT_FOUND = 2

RETURN_STATUS = {
    RPKI_ERROR: 'system error',
    RPKI_LOAD_ERROR: 'load date error',
    PRKI_VALID: 'ip address is valid',
    PRKI_INVALID_AS: 'ip address not in valid AS',
    PRKI_INVALID_NOT_FOUND: 'not found row'
}


class RpkiChecker(object):
    def __init__(self):
        """
        :return:
        """
        try:
            self.load_flag = True
            self.subnet_list = self.load_rpki_list()
            if not self.subnet_list:
                self.load_flag = False
        except:
            self.load_flag = False

    @staticmethod
    def load_data_from_rpki_server(url_server):
        """
        :type url_server: string
        :rtype: bool | string
        """
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'}
        try:
            req = urllib.request.Request(url_server, None, headers)
            response = urllib.request.urlopen(req)
            if int(response.getcode()) == 200:
                return response.read()
            else:
                return False
        except urllib.error.URLError:
            return False

    def load_rpki_list(self):
        """
        :rtype: subnetTree.SubnetTree
        """
        json_string = self.load_data_from_rpki_server(PRKI_JSON_URL)

        if not json_string:
            return False

        data_array = json.loads(json_string)['roas']
        subnet_list_tree = SubnetTree.SubnetTree()
        as_prefix = re.compile('^AS(.*?)$')
        for index in data_array:
            match = as_prefix.findall(index['asn'])
            if match:
                asn = int(match[0])
            else:
                asn = 0

            subnet_list_tree[as_bytes(index['prefix'])] = {'prefix': index['prefix'],
                                                           'ta': index['ta'],
                                                           'asn': asn,
                                                           'maxLength': index['maxLength']}
        return subnet_list_tree

    @staticmethod
    def delete_not_updated_today():
        """
        :return:
        """
        connection = get_mysql_connection()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        sql_trigger_enable = "SET @TRIGGER_DISABLED = 0"
        sql_trigger_disable = "SET @TRIGGER_DISABLED = 1"

        sql = "DELETE FROM rpki WHERE load_today = 'N'"
        BColor.process(sql)
        cursor.execute(sql)
        cursor.execute(sql_trigger_disable)

        sql = "UPDATE rpki SET load_today = 'N'"
        BColor.process(sql)
        cursor.execute(sql)
        cursor.execute(sql_trigger_enable)

        connection.commit()
        connection.close()

    def update_base(self):
        """
        :return:
        """
        json_string = self.load_data_from_rpki_server(PRKI_JSON_URL)

        if not json_string:
            return False

        data_array = json.loads(json_string)['roas']
        as_prefix = re.compile('^AS(.*?)$')
        connection = get_mysql_connection()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)

        for index in data_array:
            match = as_prefix.findall(index['asn'])
            if match:
                asn = int(match[0])
            else:
                asn = 0

            run_sql = """SELECT id FROM rpki 
                         WHERE prefix = '%s' AND maxLength = '%s' AND asn = '%s'""" % (index['prefix'],
                                                                                       index['maxLength'],
                                                                                       asn)
            cursor.execute(run_sql)
            rpki_id = cursor.fetchone()

            if not rpki_id:
                run_sql = """INSERT INTO rpki(prefix, maxLength, asn, ta, last_update) 
                             VALUE('%s', '%s', '%s', '%s', NOW()) """ % (index['prefix'],
                                                                         index['maxLength'],
                                                                         asn, index['ta'])
            else:
                run_sql = "UPDATE rpki SET last_update = NOW(), load_today = 'Y', ta = '%s' " % (index['ta']) \
                          + "WHERE prefix = '%s' AND maxLength = '%s' AND asn = '%s'" % (index['prefix'],
                                                                                         index['maxLength'],
                                                                                         asn)

            try:
                cursor.execute(run_sql)
                connection.commit()

            except Exception:
                # try again
                time.sleep(5)
                connection = get_mysql_connection()
                cursor = connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(run_sql)
                connection.commit()

        connection.close()
        self.delete_not_updated_today()

    def check_ip(self, ip, asn):
        """
        :type ip: string
        :type asn: int
        :rtype: list
        """
        if not self.load_flag:
            return {'code': RPKI_LOAD_ERROR,
                    'description': RETURN_STATUS[RPKI_LOAD_ERROR]}

        try:
            ip_data = self.subnet_list[as_bytes(ip)]
            if ip_data['asn'] == asn:
                return {'code': PRKI_VALID,
                        'rpki': ip_data,
                        'description': RETURN_STATUS[PRKI_VALID]}
            else:
                return {'code': PRKI_INVALID_AS,
                        'rpki': ip_data,
                        'description': RETURN_STATUS[PRKI_INVALID_AS]}
        except KeyError:
            return {'code': PRKI_INVALID_NOT_FOUND,
                    'description': RETURN_STATUS[PRKI_INVALID_NOT_FOUND]}
        except:
            return {'code': RPKI_ERROR,
                    'description': RETURN_STATUS[RPKI_ERROR]}
