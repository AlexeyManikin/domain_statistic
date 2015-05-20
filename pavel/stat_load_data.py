#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Скрипт импортирует содержимое дампов доменов от Регистратора в MySQL 
#

from sqlalchemy import create_engine
from pavel import stat_config

db = create_engine(stat_config.db_url, echo=False)

print "Start loading domains in DB"

# Загружаем все домены в БД
load_data_query = "LOAD DATA INFILE '/opt/ru_open_statistics/domain_lists/%s_domains' INTO TABLE domains FIELDS TERMINATED BY '\t'  LINES TERMINATED BY '\n' (@domain_name, @registrar, @register_date, @register_end_date, @free_date, delegated) SET tld = '%s', register_date = STR_TO_DATE(@register_date, '%%%%d.%%%%m.%%%%Y'), register_end_date = STR_TO_DATE(@register_end_date, '%%%%d.%%%%m.%%%%Y'), free_date=STR_TO_DATE(@free_date, '%%%%d.%%%%m.%%%%Y'), domain_name = LOWER(@domain_name), registrar = LOWER(@registrar);"

# %%%% - требуется для того, чтобы после использования форматирования строк Питона поулчилось %%, которое в свою очреедь в MySQL означает ни что иное как обычный единственный знак прцоента

for zone in stat_config.processed_zones:
    print "Start load data for %s zone" % zone
    result = db.execute(load_data_query % (zone, zone))

print "Finished loading domains in DB"
