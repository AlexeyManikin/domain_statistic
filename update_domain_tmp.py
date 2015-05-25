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

if __name__ == "__main__":
    try:
        downloder = Downloader()
        path = downloder.download_data_for_current_date()
        converter = Converter(path)
        converter.load_domain_file_in_base()
        converter.parce_file_rib_file_to()
        as_list = converter.convert_rib_to_net_as()

        # save_prefix_list(as_list, path + '/work/prefix_list')
        # as_list = load_prefix_list_from_file(path + '/work/prefix_list')

        Resolver.start_resolver(as_list)

    except Exception as e:
        print "Got an exception: %s" % e.message
        print traceback.format_exc()
# EOF
