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
    def start_load_and_resolver_domain(net_array, work_path, delete_old=True, count=COUNT_THREAD, verbose=False,
                                       count_cycle=10, resolve_dns='127.0.0.1'):
        """
        Запускам процессы резолвинга

        :param net_array: unicode|list
        :type work_path: unicode
        :type delete_old: bool
        :type count: int
        :type verbose: bool
        :type count_cycle: int
        :type resolve_dns: unicode
        :return:
        """

        if verbose:
            log_path = os.path.abspath(os.path.join(work_path, 'log'))
            if not os.path.exists(log_path):
                os.makedirs(log_path)
        else:
            log_path = False

        count_array_data = count * count_cycle
        data_for_process = []
        for thread_number in range(0, count_array_data):
            data_for_process.append([])

        counter_all = {}

        for prefix in PREFIX_LIST:
            BColor.process("Load prefix_list %s " % prefix)
            file_prefix = os.path.join(work_path, prefix+"_domains")
            file_rib_data = open(file_prefix)

            BColor.process("Load file %s " % file_prefix)
            line = file_rib_data.readline()
            counter_all[prefix] = 0
            while line:
                data_for_process[counter_all[prefix] % count_array_data].append({'line': line, 'prefix': prefix})
                counter_all[prefix] += 1
                line = file_rib_data.readline()

            BColor.process("All load zone %s -  %s" % (prefix, counter_all[prefix]))

        process_list = []
        for i in range(0, count_array_data):
            BColor.process("Start process to work %s %s" % (i, len(data_for_process[i])))
            resolver = Resolver(i,  data_for_process[i], resolve_dns, net_array, log_path)
            resolver.daemon = True
            process_list.append(resolver)
            resolver.start()

            if i !=0 and i % count == 0:
                BColor.process("Wait for threads finish...")
                for process in process_list:
                    try:
                        # timeout 2 days
                        process.join(1728000)
                    except KeyboardInterrupt:
                        BColor.warning("Interrupted by user")
                        return
                process_list = []

        if len(process_list):
            for process in process_list:
                try:
                    # timeout 2 days
                    process.join(1728000)
                except KeyboardInterrupt:
                    BColor.warning("Interrupted by user")
                    return

        if delete_old:
            Resolver.delete_not_updated_today(counter_all)

    def write_to_file(self, text, sql=False):
        """
        Записываем подробный лог работы в файл

        :type text: unicode
        :type sql: bool
        :return:
        """

        if not self.log_path:
            return

        pid = str(os.getpid())
        if sql:
            log_file = os.path.abspath(os.path.join(self.log_path, 'sql_log_%s' % pid))
        else:
            log_file = os.path.abspath(os.path.join(self.log_path, 'log_%s' % pid))

        file_handler = open(log_file, 'a')
        writing_text = "%s\n" % str(text)
        file_handler.write(writing_text)
        file_handler.close()

    @staticmethod
    def delete_not_updated_today(count_all_domain=False):
        """
        :type count_all_domain: bool|dict
        :return:
        """
        connection = get_mysql_connection()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        sql_trigger_enable = "SET @TRIGGER_DISABLED = 0"
        sql_trigger_disable = "SET @TRIGGER_DISABLED = 1"

        if not count_all_domain:
            sql = "DELETE FROM domain WHERE load_today = 'N'"
            BColor.process(sql)
            cursor.execute(sql)
            cursor.execute(sql_trigger_disable)

            sql = "UPDATE domain SET load_today = 'N'"
            BColor.process(sql)
            cursor.execute(sql)
            cursor.execute(sql_trigger_enable)
        else:
            for key_tld, tld_count_in_file in count_all_domain.iteritems():
                cursor.execute("SELECT count(*) as domain_count FROM domain WHERE tld = '%s'" % str(key_tld))
                count_in_base = cursor.fetchone()
                BColor.process("Count zone (%s) in file %s, in base %s"
                               % (str(key_tld), str(tld_count_in_file), str(count_in_base['domain_count'])))

                if count_in_base and int(count_in_base['domain_count']) >= int(tld_count_in_file):
                    sql = "DELETE FROM domain WHERE load_today = 'N' AND tld = '%s'" % str(key_tld)
                    BColor.process(sql)
                    cursor.execute(sql)
                    cursor.execute(sql_trigger_disable)

                    sql = "UPDATE domain SET load_today = 'N' WHERE tld = '%s'" % str(key_tld)
                    BColor.process(sql)
                    cursor.execute(sql)
                    cursor.execute(sql_trigger_enable)
                else:
                    BColor.error("TLD %s - count in file %s, count in base %s"
                                 % (str(key_tld), str(count_in_base), str(tld_count_in_file)))
        connection.commit()
        connection.close()

    def _connect_mysql(self):
        """
        :return:
        """
        self.connection = get_mysql_connection()

    def _get_dns_record(self, resolver, domain_name, record_type):
        """
        Получить ресурсную запись данного типа от DNS сервера
        :type resolver: dns.resolver.Resolver()
        :type domain_name: unicode
        :type record_type: unicode
        :return:
        """
        dns_records = []
        answers = resolver.query(domain_name, record_type)
        for dns_data in answers:
            if record_type == 'MX':
                dns_records.append(dns_data.exchange.to_text().lower())
            else:
                dns_records.append(dns_data.to_text().lower())

        return dns_records

    def _get_ns_record(self, domain_name):
        """
        Получаем массив с DNS записями
        :type domain_name: unicode
        :return:
        """
        domain_dns_data_list = {'nserrors': []}

        # получаем все интересные нам типы записей
        for record_type in ('A', 'NS', 'MX', 'TXT', 'AAAA', 'CNAME'):
            try:
                array_data = self._get_dns_record(self.resolver, domain_name, record_type)
                array_data.sort()
                domain_dns_data_list[record_type.lower()] = array_data
            except NXDOMAIN:
                domain_dns_data_list['nserrors'].append("NXDOMAIN-%s " % record_type)
            except NoAnswer:
                pass
            except Timeout:
                domain_dns_data_list['nserrors'].append("Timeout-%s " % record_type)
            except NoNameservers:
                domain_dns_data_list['nserrors'].append("NoNS-%s " % record_type)
                break
            except:
                domain_dns_data_list['nserrors'].append("UNDEF-%s " % record_type)

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
                    text = " ".join(dns_data[dns_type])[0:self.dns_type_length[dns_type]]
                    if dns_type == 'txt':
                        text = text.replace("\"", "")
                    set_statement += ", %s = '%s'" % (dns_type, self.connection.escape_string(text))
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
                text = " ".join(dns_data[dns_type])[0:self.dns_type_length[dns_type]]
                if dns_type == 'txt':
                    text = text.replace("\"", "")

                default_value[dns_type][dns_type] = "'%s'" % self.connection.escape_string(text)
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
            self.write_to_file(BColor.process("Process %s running, need work %s domains"
                                              % (self.number, len(self.domains))))

            added_domains = 0
            re_prefix = re.compile(r'\s*')
            self._connect_mysql()
            cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)

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

                    self.write_to_file(run_sql + ";", sql=True)

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

                    # USE http://habrahabr.ru/post/178637/
                    data = None
                    domain = None
                    delegated = None
                    domain_dns_data_array = None
                    as_array = None
                    register_info = None
                    domain_id = None
                    run_sql = None


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
