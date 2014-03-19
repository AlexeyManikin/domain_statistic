#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# TODO добавить прогресс нормализацонной обработки
#

#
# Данный скрипт обрабатывает полученные DNS данные в пределах БД
#

import stat_config
#from sqlalchemy import create_engine,text
import re
import SubnetTree
import oursql
import sys
import os


# Конструируем таблицу для быстрого разрешения IP в номер ASN
t = SubnetTree.SubnetTree()
file = open(stat_config.ip_asn_data_file, 'r')

for line in file:
    line = line.strip()
    domain_data = line.split("\t")    

    t[ domain_data[0] ] = domain_data[1]

print "Success loaded subnet tree (for IP to ASN fast resolve)"

# Выбираем все делегированные домены, DNS данных о неделегирвоанных у нас все равно нет
# db = create_engine(stat_config.db_url, echo=False)
conn = oursql.connect(host='127.0.0.1', user=stat_config.db_user, passwd=stat_config.db_password, db=stat_config.db_name, charset=None, use_unicode=False)
curs = conn.cursor(oursql.DictCursor)

query = "SELECT domain_name, domain_id, a, ns, mx FROM domains WHERE delegated != 0"
curs.execute(query)
domains_list_as_array = curs.fetchall()

print "Success loaded %d domains into memory" % len(domains_list_as_array)

# Очистим таблицу айпишников, так как сейчас начнем ее заполнять
curs.execute('DELETE FROM ips')
print "Clean up ips table"


# нормализация списка ASN, все номера ASN должны быть идентичны
def normalize_asn(asn_list):
    asn_normalized = ''

    for asn in asn_list:
        if len(asn_normalized) == 0:
            # иницируем нормализованное значение
            asn_normalized = asn
        else:
            # уже инициировались, сравниванием
            if asn != asn_normalized:
                return 'conflict'

    return asn_normalized

processed_domains = 0
data_change_rows = []
add_ip = {}

for domain_data in domains_list_as_array:
    domain_name = domain_data['domain_name']
    domain_id   = domain_data['domain_id']

    a  = domain_data['a'] 
    ns = domain_data['ns']
    mx = domain_data['mx']

    if len(a):
        a_array = a.split(' ')
        a_count = len(a_array)

    # список АСН
    asn_for_a_records_array = [] 
    asn_for_a_records_string = ''

    if len(a) > 0:
        a_array = a.split(' ')
        for ip in a_array:
            if add_ip.has_key(ip):
                # Этот IP встретился нам второй раз
                add_ip[ip]['count'] = add_ip[ip]['count'] + 1
            else:
                # IP встретился нам впервые
                add_ip[ip] = {}

                add_ip[ip]['count'] = 1
                # осуществляем резолвинг ASN
                try:
                    add_ip[ip]['asn'] = t[ ip ]
                except KeyError:
                    # такая ошибка случается, когда у нас некорректный IP
                    add_ip[ip]['asn'] = ''
                    

            # на данном шаге мы точно знаем ASN IP адреса
            asn_for_a_records_array.append(add_ip[ip]['asn'])

    asn_for_a_records_string = " ".join(asn_for_a_records_array)
    # а тут надо провести нормализацию asn
    asn_normal = normalize_asn(asn_for_a_records_array) 

    append_data = (mx_count, ns_count, a_count, mx_normal, ns_normal, asn_for_a_records_string, asn_norman, domain_id)
    data_as_string = ':'.join(append_data);
    print data_as_string
    
    data_change_rows.append( append_data )
    processed_domains = processed_domains + 1

    if processed_domains % 1000 == 0:
        print "Sucessful processed %d domains" % processed_domains

print "Start mass ip add"
add_ip_rows = []
for i in add_ip.keys():
    add_ip_rows.append( [ i, add_ip[i]['count'], add_ip[i]['asn'] ] )

insert_query = 'INSERT INTO ips (ip, used, asn) VALUES(?, ?, ?)'
curs.executemany( insert_query, add_ip_rows)
print "Finish mass ip add"

print "Start mass update domains in db"
# Теперь все изменения в бд, что мы насобирали надо вкатить в базу
update_query = 'UPDATE domains SET mx_count=?, ns_count=?, a_count=?, mx_normal=?, ns_normal=?, asn=?, asn_normal=? WHERE domain_id=?'
curs.executemany(update_query, data_change_rows)
print "Finished mass update"
