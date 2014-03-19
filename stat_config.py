# -*- coding: utf-8 -*-

# Конфиг файл
db_user = 'stat_user'
db_password = 'eer6paigaus2aeGa'
db_name = 'stat'

db_url = 'mysql://%s:%s@127.0.0.1/%s' % (db_user, db_password, db_name)

DEBUG=False

# Используем локальный резольвер
dns_servers_list = [
#'8.8.8.8',
'127.0.0.1',
#'8.8.4.4'
] 


processed_zones = ['ru', 'su', 'rf']
#processed_zones = [ 'ru' ]

# Для тестов ограничиваем число обрабатываемых доменов
limit_select_for_tests = "LIMIT 10000"
# Для продакшена снимаем:
#limit_select_for_tests = ""

# продакшен: 100 потоков
number_of_threads = 100
ip_asn_data_file = '/opt/bgp/asn.txt'

# Списки эквивалентности доменов, используются для схлопывания ns/mx
eq_domains = { 
    'google.com'  : 'googlemail.com',
    'timeweb.ru'  : 'timeweb.org',
    # The Secondary (Slave) Domain Name System (DNS) Server of Itlibitum, Corp.
    'primary.su'  : 'secondary.su',
    # Hetzner Online AG DNS Service
    'first-ns.de'  : 'second-ns.de',
    'first-ns.de'  : 'second-ns.com',
    'second-ns.de' : 'second-ns.com',
}   
