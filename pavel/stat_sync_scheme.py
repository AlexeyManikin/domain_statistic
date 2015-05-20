#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Используем SQLAlchemy для удобного описания схемы
#

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, Boolean
from pavel import stat_config

db = create_engine(stat_config.db_url, echo=False)

metadata = MetaData()

domains = Table("domains", metadata, 
                Column('domain_id',         Integer,      primary_key=True),
                Column('domain_name',       String(256),  nullable = False),
                Column('registrar',         String(64),   nullable = False),
                Column('tld',               String(32),   nullable = False),  # ru/su/rf
                Column('register_date',     Date(),       nullable = False),  # дата регистрации
                Column('register_end_date', Date(),       nullable = False),  # дата окончания регистрации
                Column('free_date',         Date(),       nullable = False),  # дата фактического освобождения
                Column('delegated',         Boolean,      nullable = False),  # делегирован ли домен
                Column('ns',                String(512),  nullable = False, server_default=''),
                Column('mx',                String(512),  nullable = False, server_default=''),
                Column('a',                 String(512),  nullable = False, server_default=''),
                Column('txt',               String(1024), nullable = False, server_default=''),
                Column('soa',               String(256),  nullable = False, server_default=''),
                Column('ns_normal',         String(128),  nullable = False, server_default=''),
                Column('mx_normal',         String(128),  nullable = False, server_default=''),
                Column('asn',               String(512),  nullable = False, server_default=''),
                Column('asn_normal',        String(128),  nullable = False, server_default=''),
                Column('mx_count',          Integer()),
                Column('ns_count',          Integer()),
                Column('a_count',           Integer()),
                mysql_engine='MYISAM',)

# Memory

ips = Table("ips", metadata,
    Column('ip',   String(32), unique = True),
    Column('asn',  String(32), nullable = False, server_default = ''),
    Column('ptr',  String(32), nullable = False, server_default = ''),
    Column('used', Integer() ),
    mysql_engine='MYISAM',
)
# InnoDB

metadata.drop_all(db)
metadata.create_all(db)

 

