#!/usr/bin/python

import stat_config
import oursql

conn = oursql.connect(host='127.0.0.1', user=stat_config.db_user, passwd=stat_config.db_password, db=stat_config.db_name, charset=None, use_unicode=False)
curs = conn.cursor(oursql.DictCursor)

query = "select asn_normal, count(*)/(select  count(*) from domains where delegated = 1)*100 as cc from domains where asn != '' group by asn_normal order by cc desc limit 50;"

curs.execute(query)

import dns.resolver
resolver = dns.resolver.Resolver()

def get_asn_descrption(asn):
    try:
        answers = resolver.query('AS' + asn + '.asn.cymru.com', 'TXT')
    except dns.resolver.NXDOMAIN:
        return "can't identify ASN. You could try it: " + "bgp.he.net/AS" + asn

    asn_name = ''
    for record in answers:
        asn_name = record.to_text()

    asn_name = asn_name.split(' | ')[4]
    return asn_name

for i in curs:
    asn_name = get_asn_descrption(i['asn_normal']);

    print "%s %s %%" % ( asn_name, i['cc'] )
