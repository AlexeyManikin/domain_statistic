__author__ = 'Alexey Y Manikin'

import multiprocessing
from helpers.utils import *
import dns.resolver
from helpers.helperUnicode import *
from config.main import *
import MySQLdb
import traceback
from collections import defaultdict
from helpers.helpers import get_mysql_connection, is_int
from dns.resolver import NXDOMAIN, NoAnswer, Timeout, NoNameservers
import time
import SubnetTree
from classes.rpkiCheker import RpkiChecker
from helpers.helpersCollor import BColor
import queue
import pprint


class Resolver(multiprocessing.Process):
    DNS_TYPE_LENGTH = {'a': 16,
                       'aaaa': 54,
                       'mx': 69,
                       'txt': 250,
                       'ns': 44,
                       'cname': 44,
                       'nserrors': 80
                       }

    def __init__(self, number: int,
                 queue_in: multiprocessing.Queue,
                 dns_server: str,
                 array_net: SubnetTree.SubnetTree,
                 log_path: str or bool,
                 registrant_mutex: multiprocessing.Lock,
                 queue_statistic: multiprocessing.Queue):
        """
        """
        multiprocessing.Process.__init__(self, name="resolver_%s" % number)

        self.number = number
        self.queue = queue_in
        self.dns_server = dns_server
        self.queue_statistic = queue_statistic

        self.resolver = dns.resolver.Resolver()
        self.resolver.nameservers = [self.dns_server]

        # стандартное время ожидания велико, его нужно уменьшить
        # The total number of seconds to spend trying to get an answer to the question.
        self.resolver.lifetime = DEFAULT_TIMEOUT

        # The number of seconds to wait for a response from a server, before timing out.
        self.resolver.timeout = DEFAULT_TIMEOUT

        self.list_ip_address = {}
        self.array_net = array_net

        self.registrant_mutex = registrant_mutex

        self.log_path = log_path
        self.registrar = None

    @staticmethod
    def start_load_and_resolver_domain(net_array: SubnetTree.SubnetTree,
                                       work_path: str,
                                       delete_old: bool = True,
                                       count_thread: int = COUNT_THREAD,
                                       verbose: bool = False,
                                       resolve_dns: str = '127.0.0.1') -> None:
        """
        Запускам процессы резолвинга
        :return:
        """

        if verbose:
            log_path = os.path.abspath(os.path.join(work_path, 'log'))
            if not os.path.exists(log_path):
                os.makedirs(log_path)
        else:
            log_path = False

        # Разбиваем все домены в файлах на N массивов
        # пример формата строки из файла
        # 0--2.RU	REGRU-RU	15.06.2019	15.06.2020	16.07.2020	1
        queue_data = multiprocessing.Queue(MAX_DOMAIN_COUNT)
        queue_statistic = multiprocessing.Queue(count_thread + 5)
        counter_all = {}

        for prefix in PREFIX_LIST_ZONE.keys():
            BColor.process("Load prefix_list %s " % prefix)
            file_prefix = os.path.join(work_path, prefix + "_domains")
            file_domain_data = open(file_prefix)

            BColor.process("Load file %s " % file_prefix)
            line = file_domain_data.readline()
            counter_all[prefix] = 0
            while line:
                queue_data.put({'line': line, 'prefix': prefix})
                counter_all[prefix] += 1
                line = file_domain_data.readline()

                # if counter_all[prefix] > 1000:
                #     break

            BColor.process("All load zone %s -  %s" % (prefix, counter_all[prefix]))

        # Запускаем процессы парсинга доменов
        start_time = datetime.now()
        registrant_mutex = multiprocessing.Lock()
        process_list = []
        for i in range(0, count_thread):
            resolver = Resolver(i, queue_data, resolve_dns, net_array, log_path, registrant_mutex, queue_statistic)
            resolver.daemon = True
            process_list.append(resolver)
            resolver.start()

        if len(process_list):
            for process in process_list:
                try:
                    # timeout 2 days
                    process.join(1728000)
                except KeyboardInterrupt:
                    BColor.warning("Interrupted by user")
                    return

        queue_data.close()
        diff = datetime.now() - start_time

        all_time = 0
        all_count = 0
        while not queue_statistic.empty():
            statistic_data = queue_statistic.get()
            all_time += statistic_data['time_diff']
            all_count += statistic_data['count']

        performance_per_process = all_time / all_count
        performance = diff.seconds / all_count
        BColor.process(
            "Performance %f per process, total time %i per process, total count %i, performance %f, all time %i"
            % (performance_per_process, all_time, all_count, performance, diff.seconds))

        # После обработки всех доменов запускаем удаление доменов которые сегодня не обновлены
        if delete_old:
            Resolver.delete_not_updated_today(counter_all)

    def write_to_file(self, text: str, sql: bool = False) -> None:
        """
        Записываем подробный лог работы в файл
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
    def delete_not_updated_today(count_all_domain: dict or bool = False) -> None:
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
            cursor.execute(sql)
            cursor.execute(sql_trigger_disable)

            sql = "UPDATE domain SET load_today = 'N'"
            cursor.execute(sql)
            cursor.execute(sql_trigger_enable)
        else:
            for key_tld, tld_count_in_file in count_all_domain.items():
                cursor.execute(
                    "SELECT count(*) as domain_count FROM domain WHERE tld = '%s'" % PREFIX_LIST_ZONE[key_tld])
                count_in_base = cursor.fetchone()
                BColor.process("Count zone (%s) in file %s, in base %s"
                               % (str(key_tld), str(tld_count_in_file), str(count_in_base['domain_count'])))

                sql = "DELETE FROM domain WHERE load_today = 'N' AND tld = '%s'" % PREFIX_LIST_ZONE[key_tld]
                BColor.process(sql)
                cursor.execute(sql)
                cursor.execute(sql_trigger_disable)

                sql = "UPDATE domain SET load_today = 'N' WHERE tld = '%s'" % PREFIX_LIST_ZONE[key_tld]
                BColor.process(sql)
                cursor.execute(sql)
                cursor.execute(sql_trigger_enable)

        connection.commit()
        connection.close()

    def _connect_mysql(self) -> MySQLdb.connect:
        """
        :return:
        """
        self.connection = get_mysql_connection()
        return self.connection

    @staticmethod
    def _get_dns_record(resolver: dns.resolver.Resolver, domain_name: str, record_type: str) -> list:
        """
        Получить ресурсную запись данного типа от DNS сервера
        :return:
        """
        dns_records = []
        answers = resolver.query(domain_name, record_type)

        for dns_data in answers:
            if record_type == 'MX':
                row: bytes = dns_data.exchange.to_text().lower()
            else:
                row: bytes = dns_data.to_text().lower()

            # TODO:manikin Не понятно зачем это было сделано, проверить как будет реботать без этого куса
            try:
                row: bytes = row.decode()
            except:
                pass

            dns_records.append(row)
        return dns_records

    def get_ns_record(self, domain_name: str) -> dict:
        """
        Получаем массив с DNS записями
        :return:
        """
        domain_dns_data_list = {'nserrors': []}

        # получаем все интересные нам типы записей
        for record_type in ('A', 'NS', 'MX', 'TXT', 'AAAA', 'CNAME'):
            domain_dns_data_list[record_type.lower()] = []
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
                for record_type_second in ('A', 'NS', 'MX', 'TXT', 'AAAA', 'CNAME'):
                    domain_dns_data_list[record_type_second.lower()] = []
                break
            except:
                domain_dns_data_list['nserrors'].append("UNDEF-%s " % record_type)

        return domain_dns_data_list

    def _get_asn_array(self, domain_dns_data_list: dict) -> list:
        """
        Возвращаем массив AS
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

    def _on_duplicate_key_update(self, dns_data: dict,
                                 as_data: dict,
                                 register_info: dict,
                                 rpki_status: int) -> str:
        """
        Возвращаем сворфмированный SQL
        """
        update_sql_begin = " ON DUPLICATE KEY UPDATE "
        set_statement = " last_update = NOW(), load_today = 'Y'"

        if register_info['delegated'] == 'Y':
            for dns_type in dns_data:
                if dns_type == 'txt' or dns_type == 'cname' or dns_type == 'nserrors':

                    text = " ".join(dns_data[dns_type])
                    text = text[0:self.DNS_TYPE_LENGTH[dns_type]]

                    if dns_type == 'txt':
                        text = text.replace("\"", "")
                        text = text.replace("\'", "")
                        set_statement += ", %s = SUBSTRING('%s', 1, 250)" % (dns_type,
                                                                             self.connection.escape_string(text))
                    else:
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
                            set_statement += ", %s%s = NULL" % (dns_type, (int(value) + 1))
                        else:
                            if dns_type == 'a':
                                set_statement += ", %s%s = INET_ATON('%s')" % (dns_type, (int(value) + 1),
                                                                               self.connection.escape_string(
                                                                                   values[value])[
                                                                               0:self.DNS_TYPE_LENGTH[dns_type]])
                            elif dns_type == 'aaaa':
                                set_statement += ", %s%s = INET6_ATON('%s')" % (dns_type, (int(value) + 1),
                                                                                self.connection.escape_string(
                                                                                    values[value])[
                                                                                0:self.DNS_TYPE_LENGTH[dns_type]])
                            else:
                                set_statement += ", %s%s = '%s'" % (dns_type, (int(value) + 1),
                                                                    self.connection.escape_string(
                                                                        values[value])[
                                                                    0:self.DNS_TYPE_LENGTH[dns_type]])
            values = {0: None, 1: None, 2: None, 3: None}
            i = 0
            for record in as_data:
                if record != '' and i <= 3:
                    values[i] = record
                    i += 1

            for value in values:
                if values[value] is None or values[value] == '':
                    set_statement += ", asn%s = NULL" % (int(value) + 1)
                else:
                    set_statement += ", asn%s = '%s'" % ((int(value) + 1),
                                                         self.connection.escape_string(values[value]))

            set_statement += ", rpki = NULL"

        set_statement += ", register_date = STR_TO_DATE('%s', '%%d.%%m.%%Y')" % register_info['register_date']
        set_statement += ", register_date_end = STR_TO_DATE('%s', '%%d.%%m.%%Y')" % register_info['register_end_date']
        set_statement += ", free_date = STR_TO_DATE('%s', '%%d.%%m.%%Y')" % register_info['free_date']
        set_statement += ", registrant_id = %s" % self.get_registrar_id(register_info['registrant'])
        set_statement += ", delegated = '%s'" % register_info['delegated']
        return update_sql_begin + set_statement

    def _update_domain_row(self, dns_data: dict, as_data: dict, register_info: dict, rpki_status: int) -> str:
        """
        :return:
        """
        sql_insert = "INSERT INTO " \
                     "domain(tld, register_date, register_date_end, free_date, domain_name, registrant_id," \
                     " delegated, a1, a2, a3, a4, ns1, ns2, ns3, ns4, mx1, mx2, mx3, mx4, txt, asn1, " \
                     "asn2, asn3, asn4, aaaa1, aaaa2, aaaa3, aaaa4, cname, last_update, nserrors, rpki) VALUE "

        default_value = defaultdict(lambda: defaultdict(lambda: 'NULL'))

        for dns_type in dns_data:
            if dns_type == 'txt' or dns_type == 'cname' or dns_type == 'nserrors':

                text = " ".join(dns_data[dns_type])
                text = text[0:self.DNS_TYPE_LENGTH[dns_type]]

                if dns_type == 'txt':
                    text = text.replace("\"", "")
                    text = text.replace("\'", "")

                default_value[dns_type][dns_type] = "'%s'" % self.connection.escape_string(text)
            else:
                i = 0
                for dns_row in dns_data[dns_type]:
                    if dns_row != '' and i <= 3:
                        default_value[dns_type][i] = "'%s'" \
                                                     % self.connection.escape_string(
                            dns_row)[0:self.DNS_TYPE_LENGTH[dns_type]]
                        i += 1

        i = 0
        for dns_row in as_data:
            if dns_row != '' and i <= 3:
                default_value['asn'][i] = "'%s'" % self.connection.escape_string(dns_row)
                i += 1

        default_value['rpki'] = "NULL"

        sql_insert_date = """ (%s, STR_TO_DATE('%s', '%%d.%%m.%%Y'), STR_TO_DATE('%s', '%%d.%%m.%%Y'),
                                STR_TO_DATE('%s', '%%d.%%m.%%Y'), LOWER('%s'), LOWER('%s'),
                                '%s', INET_ATON(%s), INET_ATON(%s), INET_ATON(%s), INET_ATON(%s), 
                                %s, %s,  %s, %s, %s, %s, %s, %s, SUBSTRING(%s, 1, 250),
                                %s, %s, %s, %s, INET6_ATON(%s), INET6_ATON(%s), INET6_ATON(%s), INET6_ATON(%s), 
                                %s,  NOW(), %s, %s)""" \
                          % (PREFIX_LIST_ZONE[register_info['prefix']],
                             register_info['register_date'],
                             register_info['register_end_date'],
                             register_info['free_date'],
                             register_info['domain'],
                             self.get_registrar_id(register_info['registrant']),
                             register_info['delegated'],
                             default_value['a'][0],
                             default_value['a'][1],
                             default_value['a'][2],
                             default_value['a'][3],
                             default_value['ns'][0],
                             default_value['ns'][1],
                             default_value['ns'][2],
                             default_value['ns'][3],
                             default_value['mx'][0],
                             default_value['mx'][1],
                             default_value['mx'][2],
                             default_value['mx'][3],
                             default_value['txt']['txt'],
                             default_value['asn'][0],
                             default_value['asn'][1],
                             default_value['asn'][2],
                             default_value['asn'][3],
                             default_value['aaaa'][0],
                             default_value['aaaa'][1],
                             default_value['aaaa'][2],
                             default_value['aaaa'][3],
                             default_value['cname']['cname'],
                             default_value['nserrors']['nserrors'],
                             default_value['rpki'])
        sql_update = self._on_duplicate_key_update(dns_data, as_data, register_info, rpki_status)
        return sql_insert + sql_insert_date + sql_update

    def _update_registrant(self) -> None:
        """
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id, registrant FROM registrant")
        registrar_list = cursor.fetchall()

        self.registrar = {}
        for row in registrar_list:
            self.registrar[row['registrant']] = row['id']

    def get_registrar_id(self, registrar: str) -> int:
        """
        Получаем ID регистратора в БД, данная таблица кешируется в памяти.
        """
        registrar = registrar.lower()

        if self.registrar is None:
            self._update_registrant()

        if registrar in self.registrar:
            return self.registrar[registrar]
        else:
            self.registrant_mutex.acquire()
            try:
                # Блокировка необходима что бы 2 потока одновременно не записывали в БД одинаковые данные
                self._update_registrant()
                if registrar in self.registrar:
                    self.registrant_mutex.release()
                    return self.registrar[registrar]

                cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
                sql = "INSERT INTO registrant(registrant) VALUE(LOWER('%s'))" % registrar
                cursor.execute(sql)

            except Exception as e:
                print(e)

            self.registrant_mutex.release()
            self._update_registrant()
            return self.registrar[registrar]

    def run(self):
        """
        Запрашиваем DNS данные
        :return:
        """

        self.write_to_file(BColor.process("Process %s running" % self.number))
        added_domains = 0
        re_prefix = re.compile(r'\s*')
        start_time = datetime.now()

        try:
            self._connect_mysql()
            cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
            #rpki = RpkiChecker()

            while not self.queue.empty():
                domain_data = self.queue.get()
                try:
                    data = domain_data['line'].split("\t")

                    domain = re.sub(re_prefix, '', data[0])
                    delegated = re.sub(re_prefix, '', data[5])

                    if delegated == '1':
                        delegated = 'Y'
                        domain_dns_data_array = self.get_ns_record(domain)
                        as_array = self._get_asn_array(domain_dns_data_array)

                        # try:
                        #     status = rpki.check_ip(domain_dns_data_array['a'][0], as_array[0])
                        #     rpki_status = status['code']
                        # except:
                        #     rpki_status = -2

                        rpki_status = -2
                    else:
                        delegated = 'N'
                        domain_dns_data_array = {}
                        as_array = {}
                        rpki_status = -2

                    register_info = {'registrant': re.sub(re_prefix, '', data[1]),
                                     'register_date': re.sub(re_prefix, '', data[2]),
                                     'register_end_date': re.sub(re_prefix, '', data[3]),
                                     'free_date': re.sub(re_prefix, '', data[4]),
                                     'delegated': delegated,
                                     'domain': domain,
                                     'prefix': domain_data['prefix']}

                    run_sql = self._update_domain_row(domain_dns_data_array,
                                                      as_array,
                                                      register_info,
                                                      rpki_status)

                    run_sql = run_sql.replace("b\'", '')
                    run_sql = run_sql.replace("\'\'", '\'')

                    self.write_to_file(run_sql + ";", sql=True)

                    try:
                        cursor.execute(run_sql)
                        self.connection.commit()
                    except Exception:
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
                        self.write_to_file(BColor.process("Thread %i success resolved %i domains"
                                                          % (self.number, added_domains), pid=self.number))

                    # READ http://habrahabr.ru/post/178637/
                    data = None
                    domain = None
                    delegated = None
                    domain_dns_data_array = None
                    as_array = None
                    register_info = None
                    domain_id = None
                    run_sql = None

                except Exception:
                    pprint.pprint(domain_data)

                    data = domain_data['line'].split("\t")
                    domain = re.sub(re_prefix, '', data[0])

                    self.write_to_file(BColor.error("Domain %s work failed process number %i" % (domain, self.number)))
                    self.write_to_file(BColor.error(traceback.format_exc()))

            diff = datetime.now() - start_time
            performance = diff.seconds / added_domains

            self.queue_statistic.put({'time_diff': diff.seconds, 'performance': performance, 'count': added_domains})
            self.write_to_file(BColor.process(
                "Process %i done, processed %i domain (performance %f)" % (self.number, added_domains, performance),
                pid=self.number))
            self.connection.close()
            return 0
        except queue.Empty:
            diff = datetime.now() - start_time
            performance = diff.seconds / added_domains

            self.queue_statistic.put({'time_diff': diff.seconds, 'performance': performance, 'count': added_domains})
            self.write_to_file(BColor.process(
                "Process %i done queue is Empty = %i, processed %i domain (performance %f)"
                % (self.number, self.queue.empty(), added_domains, performance),
                pid=self.number))
            return 0
        except Exception:
            self.write_to_file(BColor.error("Process failed %i" % self.number, pid=self.number))
            self.write_to_file(BColor.error(traceback.format_exc()))
            return 1
