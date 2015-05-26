# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'alexeyymanikin'

from threading import Thread
from helpers.utils import *
import dns.resolver
import SubnetTree
from helpers.helperUnicode import *
import pprint
from config.main import *
import MySQLdb
import sys
from helpers.helpers import get_mysql_connection

class Resolver(Thread):

    def __init__(self, number, domains_list, dns_server, array_net):
        """
        :type number:
        :param domains_list:
        :param dns_server:
        :return:
        """
        Thread.__init__(self)
        self.number = number
        self.domains = domains_list
        self.dns_server = dns_server

        self.resolver = dns.resolver.Resolver()
        self.resolver.nameservers = [self.dns_server]
        # стандартное время ожидания велико, его нужно уменьшить

        # The total number of seconds to spend trying to get an answer to the question.
        self.resolver.lifetime = 3.0

        # The number of seconds to wait for a response from a server, before timing out.
        self.resolver.timeout = 3.0

        self.ip_addr = {}
        self.array_net = array_net

    @staticmethod
    def _connect_mysql_static():
        """
        Возвращаем коннект к MySQL
        :return:
        """
        return get_mysql_connection()

    @staticmethod
    def start_resolver(net_array, count=COUNT_THREAD):
        """
        Запускам процессы резолвинга
        :param net_array:
        :param count:
        :return:
        """

        connection = Resolver._connect_mysql_static()
        curs = connection.cursor(MySQLdb.cursors.DictCursor)

        curs.execute("SELECT id as domain_id, domain_name FROM domain_tmp WHERE delegated = 1")
        domains_list_as_array = curs.fetchall()

        data_for_threads = []
        for thread_number in range(0, count):
            data_for_threads.append([])

        i = 0
        for domain in domains_list_as_array:
            if i >= count:
                i = 0
            data_for_threads[i].append(domain)
            i += 1

        threads_list = []

        for i in range (0, count):
            resovler = Resolver(i,  data_for_threads[i], '127.0.0.1', net_array)
            resovler.daemon = True
            threads_list.append(resovler)
            resovler.start()

        print "Wait for threads finish..."
        for thread in threads_list:
            try:
                thread.join()
            except KeyboardInterrupt:
                print "Interrupted by user"
                sys.exit(1)

    def _connect_mysql(self):
        """
        :param connection:
        :return:
        """
        self.connection = Resolver._connect_mysql_static()

    def _get_ns_record(self, domain_name):
        """
        Получаем массив с DNS записями
        :type domain_name: unicode
        :return:
        """

        domain_dns_data_string = {}
        domain_dns_data_list = {}

        # получаем все интересные нам типы записей
        for record_type in ('NS', 'MX', 'A', 'TXT', 'AAAA'):
            # получаем данные в виде массива
            array_data = get_dns_record(self.resolver, domain_name, record_type)
            array_data.sort()

            # часть оставляем во вложенных массивах для пост-обработки
            domain_dns_data_list[record_type.lower()] = array_data
            domain_dns_data_string[record_type.lower()] = "|".join(array_data)

        return {'domain_dns_data_string': domain_dns_data_string,
                'domain_dns_data_list': domain_dns_data_list}

    def _get_normalaze_data(self, domain_dns_data_list):
        """
        :param domain_dns_data_list:
        :return:
        """

        # список АСН
        asn_for_a_records_array = []
        asn_for_a_records_string = ''
        asn_normal = ''

        if len(domain_dns_data_list['a']) > 0:
            for ip in domain_dns_data_list['a']:

                if self.ip_addr.has_key(ip):
                    # Этот IP встретился нам второй раз и его ASN мы уже знаем
                    self.ip_addr[ip]['count'] += 1
                else:
                    # IP встретился нам впервые
                    self.ip_addr[ip] = {'count': 1}
                    # осуществляем резолвинг ASN
                    try:
                        self.ip_addr[ip]['asn'] = self.array_net[as_bytes(ip)]
                    except KeyError:
                        # такая ошибка случается, когда у нас некорректный IP
                        self.ip_addr[ip]['asn'] = ''

                asn_for_a_records_array.append(self.ip_addr[ip]['asn'])

            # Обрабатываем все A записи
            asn_for_a_records_string = " ".join(asn_for_a_records_array)
            asn_normal = normalize_asn(asn_for_a_records_array)

        return {'asn_for_a_records_array': asn_for_a_records_array,
                'asn_for_a_records_string': asn_for_a_records_string,
                'asn_normal': asn_normal}

    def run(self):
        """
        Запрашиваем DNS данные
        :return:
        """
        added_domains = 0
        self._connect_mysql()
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)

        # сюда добавляем айпишники, что находятся среди  А записей
        for domain_data in self.domains:
            print "Thread " + str(self.number) + " domain " \
                  + str(domain_data['domain_id']) + " " + domain_data['domain_name']

            domain_dns_data_array = self._get_ns_record(domain_data['domain_name'])
            normalize_value = self._get_normalaze_data(domain_dns_data_array['domain_dns_data_list'])

            sql_text = """UPDATE  domain_tmp SET
                                          ns = %s,
                                          mx = %s,
                                          a = %s,
                                          aaaa = %s,
                                          txt = %s,
                                          asn_text = %s
                       WHERE id = %s"""

            try:
                cursor.execute(sql_text, (as_default_string(domain_dns_data_array['domain_dns_data_string']['ns']),
                                          as_default_string(domain_dns_data_array['domain_dns_data_string']['mx']),
                                          as_default_string(domain_dns_data_array['domain_dns_data_string']['a']),
                                          as_default_string(domain_dns_data_array['domain_dns_data_string']['aaaa']),
                                          as_default_string(domain_dns_data_array['domain_dns_data_string']['txt']),
                                          as_default_string(normalize_value['asn_for_a_records_string']),
                                          as_default_string(str(domain_data['domain_id'])))
                               )
                self.connection.commit()
            except:
                self._connect_mysql()
                cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(sql_text, (as_default_string(domain_dns_data_array['domain_dns_data_string']['ns']),
                                          as_default_string(domain_dns_data_array['domain_dns_data_string']['mx']),
                                          as_default_string(domain_dns_data_array['domain_dns_data_string']['a']),
                                          as_default_string(domain_dns_data_array['domain_dns_data_string']['aaaa']),
                                          as_default_string(domain_dns_data_array['domain_dns_data_string']['txt']),
                                          as_default_string(normalize_value['asn_for_a_records_string']),
                                          as_default_string(str(domain_data['domain_id']))))
                self.connection.commit()

            added_domains += 1

            if (added_domains % 500) == 0:
                print "Thread %d success resolved %d domains" % (self.number, added_domains)
