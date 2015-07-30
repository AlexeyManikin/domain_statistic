# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'alexeyymanikin'

import multiprocessing
from helpers.utils import *
import dns.resolver
import SubnetTree
from helpers.helperUnicode import *
from config.main import *
import MySQLdb
import traceback
from collections import defaultdict
from helpers.helpers import get_mysql_connection, is_int
from dns.resolver import NXDOMAIN, NoAnswer, Timeout, NoNameservers
import time
from helpers.helpersCollor import BColor


class Resolver(multiprocessing.Process):

    def __init__(self, number, domains_list, dns_server, array_net, log_path):
        """
        :type number: int
        :type domains_list: list
        :type dns_server: unicode
        :type log_path: unicode
        :return:
        """
        multiprocessing.Process.__init__(self, name="resolver_%s" % number)
        self.number = number
        self.domains = domains_list
        self.dns_server = dns_server

        self.resolver = dns.resolver.Resolver()
        self.resolver.nameservers = [self.dns_server]
        # стандартное время ожидания велико, его нужно уменьшить

        # The total number of seconds to spend trying to get an answer to the question.
        self.resolver.lifetime = DEFAULT_TIMEOUT

        # The number of seconds to wait for a response from a server, before timing out.
        self.resolver.timeout = DEFAULT_TIMEOUT

        self.list_ip_address = {}
        self.array_net = array_net

        self.dns_type_length = {'a': 16,
                                'aaaa': 54,
                                'mx': 69,
                                'txt': 254,
                                'ns': 44,
                                'cname': 44,
                                'nserrors': 80
                                }

        self.log_path = log_path

    @staticmethod
    def start_load_and_resolver_domain(net_array, work_path, delete_old=True, count=COUNT_THREAD):
        """
        Запускам процессы резолвинга, процесс должен быть синглинтоном

        :param net_array:
        :param work_path:
        :param delete_old:
        :param count:
        :return:
        """

        log_path = os.path.abspath(os.path.join(work_path, 'log'))
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        data_for_process = []
        for thread_number in range(0, count):
            data_for_process.append([])

        for prefix in PREFIX_LIST:
            BColor.process("Load prefix_list %s " % prefix)
            file_prefix = os.path.join(work_path, prefix+"_domains")
            file_rib_data = open(file_prefix)

            BColor.process("Load file %s " % file_prefix)
            line = file_rib_data.readline()
            counter_all = 0
            i = 0

            while line:
                if i >= count:
                    i = 0

                data_for_process[i].append({'line': line, 'prefix': prefix})
                i += 1
                counter_all += 1
                line = file_rib_data.readline()

            BColor.process("All load zone %s" % counter_all)

            i = 0
            for data in data_for_process:
                BColor.process("data_for_process %s %s" % (i, len(data)))
                i += 1

        process_list = []
        for i in range(0, count):
            BColor.process("Start process to work %s %s" % (i, len(data_for_process[i])))
            resolver = Resolver(i,  data_for_process[i], '127.0.0.1', net_array, log_path)
            resolver.daemon = True
            process_list.append(resolver)
            resolver.start()

        BColor.process("Wait for threads finish...")
        for process in process_list:
            try:
                # timeout 2 days
                process.join(1728000)
            except KeyboardInterrupt:
                BColor.warning("Interrupted by user")
                return

        if delete_old:
            Resolver.delete_not_updated_today()

    def write_to_file(self, text, sql=False):
        """
        :type text: unicode
        :type sql: bool
        :return:
        """
        pid = str(os.getpid())
        if sql:
            log_file = os.path.abspath(os.path.join(self.log_path, 'sql_log_%s' % pid))
        else:
            log_file = os.path.abspath(os.path.join(self.log_path, 'log_%s' % pid))

        f = open(log_file, 'a')
        write_text = "%s\n" % str(text)
        f.write(write_text)
        f.close()

    @staticmethod
    def delete_not_updated_today():
        """
        :return:
        """
        connection = get_mysql_connection()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)

        BColor.process("DELETE FROM domain WHERE load_today = 'N'")
        cursor.execute("DELETE FROM domain WHERE load_today = 'N'")
        cursor.execute("SET @TRIGGER_DISABLED = 1")

        BColor.process("UPDATE domain SET load_today = 'N'")
        cursor.execute("UPDATE domain SET load_today = 'N'")
        cursor.execute("SET @TRIGGER_DISABLED = 0")
        connection.commit()
        connection.close()

    def _connect_mysql(self):
        """
        :return:
        """
        self.connection = get_mysql_connection()

    @staticmethod
    def get_dns_record(resolver, domain_name, record_type):
        """
        Получить ресурсную запись данного типа от DNS сервера
        :type resolver: dns.resolver.Resolver()
        :type domain_name: unicode
        :type record_type: unicode
        :return:
        """
        dns_records = []
        answers = resolver.query(domain_name, record_type)
        for rdata in answers:
            if record_type == 'MX':
                dns_records.append(rdata.exchange.to_text().lower())
            else:
                dns_records.append(rdata.to_text().lower())

        return dns_records

    def _get_ns_record(self, domain_name):
        """
        Получаем массив с DNS записями
        :type domain_name: unicode
        :return:
        """
        domain_dns_data_list = {'nserrors': ''}

        # получаем все интересные нам типы записей
        for record_type in ('NS', 'MX', 'A', 'TXT', 'AAAA', 'CNAME'):
            try:
                array_data = self.get_dns_record(self.resolver, domain_name, record_type)
                array_data.sort()
                domain_dns_data_list[record_type.lower()] = array_data
            except NXDOMAIN:
                domain_dns_data_list['nserrors'] += 'NXDOMAIN-%s ' % record_type
            except NoAnswer:
                domain_dns_data_list['nserrors'] += 'NoAnswer-%s ' % record_type
            except Timeout:
                domain_dns_data_list['nserrors'] += 'Timeout-%s ' % record_type
            except NoNameservers:
                domain_dns_data_list['nserrors'] += 'NoNS-%s ' % record_type
            except:
                domain_dns_data_list['nserrors'] += 'UNDEF-%s ' % record_type

        return domain_dns_data_list

    def _get_asn_array(self, domain_dns_data_list):
        """
        Возвращаем массив AS
        :param domain_dns_data_list: list
        :return:
        """
        asn_for_a_records_array = []
        if 'a' in domain_dns_data_list and len(domain_dns_data_list['a']) > 0:
            for ip in domain_dns_data_list['a']:
                ip_as_str_byte = as_bytes(ip)
                if ip_as_str_byte not in self.list_ip_address:
                    try:
                        # необходимо так как иногда возвращаеся 217.112.32.0/20	{3216,6939,40966}
                        as_number = self.array_net[ip_as_str_byte]
                        if is_int(as_number):
                            self.list_ip_address[ip_as_str_byte] = as_number
                        else:
                            try:
                                as_number = str(as_number).replace("{", "").replace("}", "").split(",")[0]
                                if is_int(as_number):
                                    self.list_ip_address[ip_as_str_byte] = as_number
                                else:
                                    self.list_ip_address[ip_as_str_byte] = '-1'
                            except:
                                self.list_ip_address[ip_as_str_byte] = '-1'
                    except KeyError:
                        self.list_ip_address[ip_as_str_byte] = '-1'
                asn_for_a_records_array.append(self.list_ip_address[ip_as_str_byte])
        return asn_for_a_records_array

    def _update_domain(self, dns_data, as_data, domain_id, register_info):
        """
        Возвращаем сворфмированный SQL
        :param dns_data:
        :param as_data:
        :param domain_id:
        :return:
        """
        update_sql_begin = "UPDATE domain SET "
        update_sql_end = " WHERE id = %s " % domain_id
        set_statement = " last_update = NOW(), load_today = 'Y'"

        if register_info['delegated'] == 'Y':
            for dns_type in dns_data:
                if dns_type == 'txt' or dns_type == 'cname' or dns_type == 'nserrors':
                    set_statement += ", %s = '%s'" \
                                     % (dns_type,
                                        self.connection.escape_string(
                                            " ".join(dns_data[dns_type])[0:self.dns_type_length[dns_type]])
                                        )

                else:
                    values = {0: None, 1: None, 2: None, 3: None}
                    i = 0
                    for record in dns_data[dns_type]:
                        if record != '' and i <= 3:
                            values[i] = record
                            i += 1

                    for value in values:
                        if values[value] is None or values[value] == '':
                            set_statement += ", %s%s = NULL" % (dns_type, (int(value)+1))
                        else:
                            set_statement += ", %s%s = '%s'" % (dns_type, (int(value)+1),
                                                                self.connection.escape_string(
                                                                    values[value])[0:self.dns_type_length[dns_type]])

            values = {0: None, 1: None, 2: None, 3: None}
            i = 0
            for record in as_data:
                if record != '' and i <= 3:
                    values[i] = record
                    i += 1

            for value in values:
                if values[value] is None or values[value] == '':
                    set_statement += ", asn%s = NULL" % (int(value)+1)
                else:
                    set_statement += ", asn%s = '%s'" % ((int(value)+1),
                                                         self.connection.escape_string(values[value]))

        set_statement += ", register_date = STR_TO_DATE('%s', '%%d.%%m.%%Y')" % register_info['register_date']
        set_statement += ", register_date_end = STR_TO_DATE('%s', '%%d.%%m.%%Y')" % register_info['register_end_date']
        set_statement += ", free_date = STR_TO_DATE('%s', '%%d.%%m.%%Y')" % register_info['free_date']
        set_statement += ", registrant = LOWER('%s')" % register_info['registrant']
        set_statement += ", delegated = '%s'" % register_info['delegated']

        return update_sql_begin + set_statement + update_sql_end

    def _insert_domain(self, dns_data, as_data, register_info):
        """
        :param dns_data:
        :param as_data:
        :param register_info:
        :return:
        """
        sql_insert = "INSERT INTO " \
                     "domain(tld, register_date, register_date_end, free_date, domain_name, registrant," \
                     " delegated, a1, a2, a3, a4, ns1, ns2, ns3, ns4, mx1, mx2, mx3, mx4, txt, asn1, " \
                     "asn2, asn3, asn4, aaaa1, aaaa2, aaaa3, aaaa4, cname, last_update, nserrors) VALUE "

        default_value = defaultdict(lambda: defaultdict(lambda: 'NULL'))

        for dns_type in dns_data:
            if dns_type == 'txt' or dns_type == 'cname' or dns_type == 'nserrors':
                default_value[dns_type][dns_type] = "'%s'" \
                                                    % self.connection.escape_string(
                    " ".join(dns_data[dns_type])[0:self.dns_type_length[dns_type]])
            else:
                i = 0
                for dns_row in dns_data[dns_type]:
                    if dns_row != '' and i <= 3:
                        default_value[dns_type][i] = "'%s'" \
                                                     % self.connection.escape_string(
                            dns_row)[0:self.dns_type_length[dns_type]]
                        i += 1

        i = 0
        for dns_row in as_data:
            if dns_row != '' and i <= 3:
                default_value['asn'][i] = "'%s'" % self.connection.escape_string(dns_row)
                i += 1

        sql_insert_date = """ ('%s', STR_TO_DATE('%s', '%%d.%%m.%%Y'), STR_TO_DATE('%s', '%%d.%%m.%%Y'),
                                STR_TO_DATE('%s', '%%d.%%m.%%Y'), LOWER('%s'), LOWER('%s'),
                                '%s', %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s,
                                %s, %s, %s, %s, %s, %s, %s, %s, %s,  NOW(), %s)""" \
                          % (register_info['prefix'], register_info['register_date'],
                             register_info['register_end_date'], register_info['free_date'],
                             register_info['domain'], register_info['registrant'], register_info['delegated'],
                             default_value['a'][0], default_value['a'][1],  default_value['a'][2],
                             default_value['a'][3], default_value['ns'][0], default_value['ns'][1],
                             default_value['ns'][2], default_value['ns'][3], default_value['mx'][0],
                             default_value['mx'][1], default_value['mx'][2],  default_value['mx'][3],
                             default_value['txt']['txt'], default_value['asn'][0], default_value['asn'][1],
                             default_value['asn'][2], default_value['asn'][3],
                             default_value['aaaa'][0], default_value['aaaa'][1], default_value['aaaa'][2],
                             default_value['aaaa'][3], default_value['cname']['cname'],
                             default_value['nserrors']['nserrors'])

        return sql_insert + sql_insert_date

    def run(self):
        """
        Запрашиваем DNS данные
        :return:
        """

        try:
            self.write_to_file(BColor.process("Process %s running " % self.number))

            added_domains = 0
            re_prefix = re.compile(r'\s*')
            self._connect_mysql()
            cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)

            # сюда добавляем айпишники, что находятся среди  А записей
            for domain_data in self.domains:
                try:
                    data = domain_data['line'].split("\t")

                    domain = re.sub(re_prefix, '', data[0])
                    delegated = re.sub(re_prefix, '', data[5])

                    if delegated == '1':
                        delegated = 'Y'
                        domain_dns_data_array = self._get_ns_record(domain)
                        as_array = self._get_asn_array(domain_dns_data_array)
                    else:
                        delegated = 'N'
                        domain_dns_data_array = {}
                        as_array = {}

                    register_info = {'registrant': re.sub(re_prefix, '', data[1]),
                                     'register_date': re.sub(re_prefix, '', data[2]),
                                     'register_end_date': re.sub(re_prefix, '', data[3]),
                                     'free_date': re.sub(re_prefix, '', data[4]),
                                     'delegated': delegated,
                                     'domain': domain,
                                     'prefix': domain_data['prefix']}

                    cursor.execute("SELECT id FROM domain WHERE domain_name = LOWER('%s')" % domain)
                    domain_id = cursor.fetchone()

                    if not domain_id:
                        run_sql = self._insert_domain(domain_dns_data_array, as_array, register_info)
                    else:
                        run_sql = self._update_domain(domain_dns_data_array, as_array, domain_id['id'],
                                                      register_info)

                    self.write_to_file(run_sql, sql=True)

                    try:
                        cursor.execute(run_sql)
                        self.connection.commit()
                    except:
                        self.write_to_file(BColor.error("MySQL exceptions (SQL %s)" % run_sql))
                        self.write_to_file(BColor.error(traceback.format_exc()))

                        # try again
                        time.sleep(5)
                        self._connect_mysql()
                        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
                        cursor.execute(run_sql)
                        self.connection.commit()

                    added_domains += 1

                    if (added_domains % 1000) == 0:
                        self.write_to_file(BColor.process("Thread %d success resolved %d domains"
                                                          % (self.number, added_domains), pid=self.number))
                except:
                    data = domain_data['line'].split("\t")
                    domain = re.sub(re_prefix, '', data[0])

                    self.write_to_file(BColor.error("Domain %s work failed process number %s" % (domain, self.number)))
                    self.write_to_file(BColor.error(traceback.format_exc()))

            self.write_to_file(BColor.process("Process %s done " % self.number))
            self.connection.close()
            return 0
        except:
            self.write_to_file(BColor.error("Process failed %s" % self.number))
            self.write_to_file(BColor.error(traceback.format_exc()))
            return 1
