#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  Неактуален!!!!
# Скрипт для получения всей возможной информации по интересующим нас айпишникам из баз RIR
#

import SubnetTree
from pavel import stat_config
from sqlalchemy import create_engine, text

# Конструируем таблицу для быстрого разрешения IP в номер ASN
t = SubnetTree.SubnetTree()
file = open(stat_config.ip_asn_data_file, 'r')

for line in file:
    line = line.strip()
    domain_data = line.split("\t")    

    t[ domain_data[0] ] = domain_data[1]

print "success loaded subnet tree"

db = create_engine(stat_config.db_url, echo=False)

query = "SELECT ip FROM ips ORDER BY ip"
result = db.execute(query)
ips_list_as_array = result.fetchall()

print "Start asn checking for %d ips" % len(ips_list_as_array)

for i in ips_list_as_array:
    ip = i[0]
    asn = t[ ip ]

    # print "IP %s belongs ans %s" % (ip, asn)
    update_query = text('UPDATE ips SET asn = :asn WHERE ip = :ip')
    result = db.execute(update_query, { 'asn' : asn, 'ip' : ip })

   
print "Finished!" 
