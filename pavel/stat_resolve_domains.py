#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Данный скрипт получает всю возможную DNS информацию о доменах 
#

# from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text, Date, Boolean
from threading import Thread
import sys

import oursql
from pavel.stat_utils import *




# для резволинга ASN
import SubnetTree
 
import time
import os

# socket.gethostbyname

from itertools import cycle

# enlarge conntrack buffer if work on OpenVZ VPS
os.system('sysctl -w net.ipv4.netfilter.ip_conntrack_max=655360')


# Считываем массив из БД в память
# db = create_engine(stat_config.db_url, echo=False)
conn = oursql.connect(host='127.0.0.1', user=stat_config.db_user, passwd=stat_config.db_password, db=stat_config.db_name, charset=None, use_unicode=False)
curs = conn.cursor(oursql.DictCursor)

# Очистим таблицу айпишников, так как сейчас начнем ее заполнять
curs.execute('DELETE FROM ips')

# Смысла обарабатывать не делегированные нету, так как DNS для них нету по факту,
# а не делегированных доменов в свою очередь около 600 тысяч в .ru
query = "SELECT domain_id, domain_name FROM domains WHERE delegated = 1 AND tld = 'ru' " + stat_config.limit_select_for_tests
curs.execute(query)
domains_list_as_array = curs.fetchall()

print "Success loaded %d domains into memory" % len(domains_list_as_array)

# Здесь будет number_of_threads массивов данных, каждый для своего потока
data_for_threads = []

for thread_number in range(0, stat_config.number_of_threads):
    data_for_threads.append( [] ) 

# Расфасуем данные по number_of_threads массивам
array_has_elements = True
while array_has_elements:
    # Собираем массив от 0 до number_of_threads-1 включительно
    for thread_number in range(0, stat_config.number_of_threads):
        # Выталкиваем поочереди первый элемент
        try:
            data_for_threads[thread_number].append( domains_list_as_array.pop() )
        except IndexError:
            # Да, так делать плохо, но так мы ловим конец массива
            array_has_elements = False
            break

# Чистим память
ns_list_as_array = None

print "Success devided all data in %d pieces" % stat_config.number_of_threads

# Для отладки. отображение размера массива
#for thread_number in range(0, stat_config.number_of_threads):
    # print "%d array length is %s" % (thread_number, len(data_for_threads[thread_number])) 

# Конструируем таблицу для быстрого разрешения IP в номер ASN
t = SubnetTree.SubnetTree()
file = open(stat_config.ip_asn_data_file, 'r')

result_file = open("/opt/result.dat", 'a')

for line in file:
    line = line.strip()
    domain_data = line.split("\t")    

    t[ domain_data[0] ] = domain_data[1]

print "Success loaded subnet tree (for IP to ASN fast resolve)"
# Ее грузим лишь 1 раз, она должна шарится для всех потоков

class resolveThread(Thread):
    def __init__(self, number, db_url, domains_list, dns_server):
        #print "Thread %d is initiated..." % number
        Thread.__init__(self)
        self.number     = number
        self.domains    = domains_list
        self.db_url     = db_url
        self.dns_server = dns_server
    def run(self):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [self.dns_server]
        # стандартное время ожидания велико, его нужно уменьшить
    
        # The total number of seconds to spend trying to get an answer to the question.
        resolver.lifetime = 1.0
        # The number of seconds to wait for a response from a server, before timing out.
        resolver.timeout = 1.0

        print "Thread %d started with dns %s and %s domains to process" % ( self.number, self.dns_server, len(self.domains))

        added_domains = 0
        
        # сюда добавляем айпишники, что находятся среди  А записей
        add_ip = {}

        add_to_db_queue = []
        for domain_data in self.domains: 
            domain_id   = domain_data['domain_id']
            domain_name = domain_data['domain_name']
            domain_delegation_status = False

            # У нас все делегированы
            domain_delegation_status = True 

            domain_dns_data = {}
            domain_dns_data_list = {} 
  

            # получаем все интересные нам типы записей
            for record_type in ('NS', 'MX', 'A', 'TXT', 'SOA'):
                # получаем данные в виде массива
                array_data = get_dns_record(resolver, domain_name, record_type)
                # сортируем его для единообразия
                array_data.sort()
                # Собираем строку для помещения в mysql
                string_data = " ".join(array_data)

                # часть оставляем во вложенных массивах для пост-обработки
                domain_dns_data_list[ record_type.lower() ] = array_data
                # строками в базу
                domain_dns_data[ record_type.lower() ] = string_data

            # нормализованные ns, mx, asn
            ns_normal = ''
            mx_normal = ''
            asn_normal = '' 
 
            # пересчет числа mx, ns, a
            a_count  = 0
            mx_count = 0
            ns_count = 0

            if len(domain_dns_data['ns']):
                ns_array = domain_dns_data['ns'].split(' ')
                ns_count = len(ns_array)
  
                ns_normal = normalize_domain_list(ns_array)
  
            if len(domain_dns_data['mx']):
                mx_array = domain_dns_data['mx'].split(' ')
                mx_count = len(mx_array)
  
                mx_normal = normalize_domain_list(mx_array)

            if len(domain_dns_data['a']):
                a_array = domain_dns_data['a'].split(' ')
                a_count = len(a_array)

            # список АСН
            asn_for_a_records_array = []  
            asn_for_a_records_string = ''

            if len(domain_dns_data['a']) > 0:
                a_array = domain_dns_data['a'].split(' ')
        
                for ip in a_array:
                    if add_ip.has_key(ip):
                        # Этот IP встретился нам второй раз и его ASN мы уже знаем
                        add_ip[ip]['count'] = add_ip[ip]['count'] + 1
                    else:
                        # IP встретился нам впервые
                        add_ip[ip] = {}

                        # Получаем ASN лишь для новых IP
                        add_ip[ip]['count'] = 1
                        # осуществляем резолвинг ASN
                        try:
                            add_ip[ip]['asn'] = t[ ip ]
                        except KeyError:
                            # такая ошибка случается, когда у нас некорректный IP
                            add_ip[ip]['asn'] = ''
                    
                    # на данном шаге мы точно знаем ASN IP адреса
                    asn_for_a_records_array.append(add_ip[ip]['asn'])
                   
                # Обрабатываем все A записи 
                asn_for_a_records_string = " ".join(asn_for_a_records_array)
                # а тут надо провести нормализацию asn
                asn_normal = normalize_asn(asn_for_a_records_array) 


            # Добавляем в массив задачу на изменение данных
            current_domain_data = (domain_dns_data['ns'], ns_normal, ns_count, domain_dns_data['mx'], mx_normal, mx_count ,domain_dns_data['txt'], domain_dns_data['a'], a_count, domain_dns_data['soa'], asn_for_a_records_string, asn_normal, domain_id )
            add_to_db_queue.append(  current_domain_data )

            # Пишем в лог
            current_domain_data_for_file = (domain_id, domain_name, domain_dns_data['ns'], ns_normal, ns_count, domain_dns_data['mx'], mx_normal, mx_count ,domain_dns_data['txt'], domain_dns_data['a'], a_count, domain_dns_data['soa'], asn_for_a_records_string, asn_normal)
            data_as_string = ':'.join(map(str, current_domain_data))
            result_file.write(data_as_string + "\n")
            current_domain_data_for_file = None
 
            added_domains = added_domains + 1
    
            if (added_domains % 500 == 0):
                print "Thread %d success resolved %d domains" % (self.number, added_domains)            
       
        # Создаем новый коннект к БД, это обязательно! Он не потокобезопасен!
        # db = create_engine(self.db_url, echo=False)        
        # TODO ПЕРЕДАВАТЬ параметры бд диктом
        conn = oursql.connect(host='127.0.0.1', user=stat_config.db_user, passwd=stat_config.db_password, db=stat_config.db_name, charset=None, use_unicode=False)
        curs = conn.cursor(oursql.DictCursor)
 
        # за один заход добавляем данные
        print "Thread %d start update db" % (self.number)
        start_time = time.time()   
 
        #### Попробуем заменить UPDATE на insert
        ### curs.execute('DELETE FROM domains')

        # по тестам, разницы между UPDATE LOW_PRIORITY и простым UPDATE нету.
        update_query = 'UPDATE domains SET ns=?, ns_normal=?, ns_count=?, mx=?, mx_normal=?, mx_count=?, txt=?, a=?, a_count=?, soa=?, asn=?, asn_normal=? WHERE domain_id = ?'
        curs.executemany(update_query, add_to_db_queue)

        #insert_query = 'INSERT INTO domains (ns,ns_normal,ns_count,mx,mx_normal,mx_count,txt,a,a_count,soa,asn,asn_normal,domain_id) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'
        #curs.executemany(insert_query, add_to_db_queue)

        db_update_time = time.time() - start_time
        print "Thread %d finished update db time %d seconds" % (self.number,db_update_time)

        # TODO: сделать какую-то защиту от дубликации
        # print "Thread %d start mass ip add" % (self.number)
        # add_ip_rows = []
        # for i in add_ip.keys():
        #     add_ip_rows.append( [ i, add_ip[i]['count'], add_ip[i]['asn'] ] )

        # insert_query = 'INSERT INTO ips (ip, used, asn) VALUES(?, ?, ?)'
        # curs.executemany( insert_query, add_ip_rows)
        # print "Thread %d finished mass ip add" % (self.number)


# print "Start threads! Show must go on!"

threads_list = []

# Собираем циклический список из DNS серверов для равномерной инициализации
dns_cycle = cycle( stat_config.dns_servers_list )

for i in range (0, stat_config.number_of_threads):
    thread_object = resolveThread(i, stat_config.db_url, data_for_threads[i], dns_cycle.next())
    # С этим флагом дочерние потоки будут убиты при остановке основного процесса
    thread_object.daemon = True
    threads_list.append(thread_object)
    thread_object.start()
    # даем смещение, чтобы немного разгрузить mysql
    # time.sleep(1)


print "Wait for threads finish..."
for thread in threads_list:
    # Разраешаем корректное отключение программы
    try:
        thread.join()
    except KeyboardInterrupt:
        print "Interrupted by user"
        sys.exit(1)
