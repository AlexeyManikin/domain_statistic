#!/usr/bin/python

import stat_config
import oursql

conn = oursql.connect(host='127.0.0.1', user=stat_config.db_user, passwd=stat_config.db_password, db=stat_config.db_name, charset=None, use_unicode=False)
curs = conn.cursor(oursql.DictCursor)

query = "select asn_normal, count(*)/(select  count(*) from domains where delegated = 1)*100 as cc from domains where asn != '' group by asn_normal order by cc desc limit 50;"

curs.execute(query)

import dns.resolver
resolver = dns.resolver.Resolver()

for i in curs:
    answers = resolver.query('AS' + i['asn_normal'] + '.asn.cymru.com', 'TXT')
    asn_name = ''
    for record in answers:
        asn_name = record.to_text()

    asn_name = asn_name.split(' | ')[4]

    print "%s %s %%" % ( asn_name, i['cc'] )
