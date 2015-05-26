# -*- coding: utf-8 -*-
# Служебная библиотека

#  python-dnspython
from datetime import datetime
from config.eq_domain import eq_domains
import re

from dns.resolver import NXDOMAIN, NoAnswer, Timeout, NoNameservers
#from pavel import stat_config


def convert_string_to_date(date):
    """
    Дату в строчном представлении конвертируем в объект 01.02.2009
    :type date: unicode
    :rtype: datetime
    """
    format = "%d.%m.%Y"
    return datetime.strptime(date, format)

def load_domains_file_to_memory(file_name):
    """
    функция читает файл и сохраняет его строки как массив
    :type file_name: unicode
    :return:
    """
    file = open(file_name, 'r')
    domains_list_as_array = []
    readed_lines = 0
    for line in file:
        # Убираем разделитель в конце строки
        line = line.strip()
        domain_data = line.split("\t")
        domains_list_as_array.append(domain_data)
  
        readed_lines = readed_lines + 1
        if readed_lines > 100:
            break
  
    return domains_list_as_array

def get_dns_record(resolver, domain_name, record_type):
    """
    Получить ресурсную запись данного типа от DNS сервера
    :type resolver: Resolver
    :type domain_name: unicode
    :type record_type: unicode
    :return:
    """
    dns_records = []
    try:
        answers = resolver.query(domain_name, record_type)
        for rdata in answers:
            if record_type == 'MX':
                dns_records.append(rdata.exchange.to_text().lower())
            else:
                dns_records.append(rdata.to_text().lower())
    except NXDOMAIN:
        #print "Not found dns server for domain %s" % domain_data[0]
        return dns_records
    except NoAnswer:
        #print "No answer from DNS for %s" % domain_data[0]
        return dns_records
    except Timeout:
        # Потом дополнительно верифицировать эти домены, возможно, по whois
        # print "Timeout for domain %s" % domain_data[0]
        return dns_records
    except NoNameservers:
        # print "No dns server for %s" % domain_data[0]
        return dns_records
  
    return dns_records

def normalize_domain_list(domain_names):
    """
    Из списка доменов в стиле:
    ns1.fastvps.ru, ns2.fastvps.ru делает fastvps.ru
    если не получилось, то выдает слово conflict
    :param domain_names:
    :return:
    """
    # нормализованная форма домена
    domain_normalized = ''
  
    if len(domain_names) == 0:
        return 'conflict'
  
    for domain in domain_names:
        # Убираем точку в конце доменов
        domain = domain.rstrip('.')
  
        # Вычленяем часть домена с отброшенным поддоменом верхнего уровня
        # ns4.fastvps.ru => fastvps.ru
        m = re.match(r".*?(\w+\.[a-z]+)$", domain)
        if m:
            domain_normalized_temp = m.group(1)
  
            # Если это первая итерация
            if len(domain_normalized) == 0:
                # Инициализируем нормализованное значение
                domain_normalized = domain_normalized_temp
  
            # Нам попался домен, который отличается от большинства, то есть:
            # ns3.fastvps.ru ns3.masterhost.ru
            if not compare_domains(domain_normalized_temp, domain_normalized):
                return 'conflict'
  
    return domain_normalized

def compare_domains(domain_first, domain_second):
    """
    Кастомный компаратор доменов, некоторые домены нужно сравнивать сложно
    :param domain_first:
    :param domain_second:
    :return:
    """
    if domain_first == domain_second:
        return True
  
    if (eq_domains.has_key(domain_first) and eq_domains[domain_first] == domain_second) or \
        (eq_domains.has_key(domain_second) and eq_domains[domain_second] == domain_first):
        return True
  
    return False

def normalize_asn(asn_list):
    """
    нормализация списка ASN, все номера ASN должны быть идентичны
    :param asn_list:
    :return:
    """
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
