# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'alexeyymanikin'

import sys
from config.main import *

PROGRAM_NAME = 'console'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, CURRENT_DIR)
logfile = os.path.join(CURRENT_DIR, '%s.debug' % (PROGRAM_NAME))

import traceback
import SubnetTree
from helpers.helperUnicode import *
from classes.downloader import Downloader
from classes.converter import Converter
from classes.resolver import Resolver

def save_prefix_list(prefix_list, file_name):
    """
    Сохраняем информацию об AS в файл
    :param prefix_list:
    :param file_name:
    :return:
    """
    saved_file = open(file_name, 'w')
    for index in prefix_list:
        saved_file.write(index + '\t' + as_list[index] + '\n')
    saved_file.close()

def load_prefix_list_from_file(file_name):
    """
    Загрузка из файла
    :param file_name:
    :return:
    """
    as_list = SubnetTree.SubnetTree()
    as_list_file = open(file_name, 'r')

    for line in as_list_file:
        line = line.strip()
        domain_data = line.split("\t")
        as_list[as_bytes(domain_data[0])] = as_bytes(domain_data[1])

    return as_list

def print_log(show_log,text):
    if show_log:
        print text

if __name__ == "__main__":
    show_log = True
    try:

        downloder = Downloader()
        print_log(show_log, "Download files")
        path = downloder.download_data_for_current_date()

        print_log(show_log, "Unzip file")
        converter = Converter(path)

        print_log(show_log, "Parce rib file")
        converter.parce_file_rib_file_to()

        print_log(show_log, "Get AS list")
        as_list = converter.convert_rib_to_net_as()

        print_log(show_log, "Save AS list")
        save_prefix_list(as_list, path + 'prefix_list')
        #print_log(show_log, "Load as list")
        #as_list = load_prefix_list_from_file(path + '/prefix_list')

        print_log(show_log, "Start resolv")
        Resolver.start_load_and_resolver_domain(as_list, path+'/work')

    except Exception as e:
        print "Got an exception: %s" % e.message
        print traceback.format_exc()
# EOF
