# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'alexeyymanikin'

import sys
from config.main import *

PROGRAM_NAME = 'update_domain'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, CURRENT_DIR)
logfile = os.path.join(CURRENT_DIR, '%s.debug' % PROGRAM_NAME)

import traceback
import SubnetTree
from helpers.helperUnicode import *
from helpers.helpers import check_prog_run
from classes.downloader import Downloader
from classes.converter import Converter
from classes.resolver import Resolver
from helpers.helpersCollor import BColor
import argparse


def save_prefix_list(prefix_list, file_name):
    """
    Сохраняем информацию об AS в файл
    :param prefix_list:
    :param file_name:
    :return:
    """
    saved_file = open(file_name, 'w')
    for index in prefix_list:
        saved_file.write(index + '\t' + prefix_list[index] + '\n')
    saved_file.close()


def load_prefix_list_from_file(file_name):
    """
    Загрузка из файла
    :param file_name:
    :return:
    """
    subnet_list_tree = SubnetTree.SubnetTree()
    as_list_file = open(file_name, 'r')

    for line in as_list_file:
        line = line.strip()
        domain_data = line.split("\t")
        subnet_list_tree[as_bytes(domain_data[0])] = as_bytes(domain_data[1])

    return subnet_list_tree


def load_prefix_list_from_var(prefix_list):
    """
    Загрузка данных из переменной
    :return:
    """
    subnet_list_tree = SubnetTree.SubnetTree()
    for index in prefix_list:
        subnet_list_tree[as_bytes(index)] = as_bytes(prefix_list[index])

    return subnet_list_tree


if __name__ == "__main__":
    try:
        if check_prog_run(PROGRAM_NAME):
            BColor.error("Program %s already running" % PROGRAM_NAME)
            sys.exit(1)

        parser = argparse.ArgumentParser(add_help=True, version='1.0')

        parser.add_argument('-d', '--dir', type=str, help="Do`t download data, use exist from dir", action="store")
        parser.add_argument('-s', '--show_verbose', help="Show verbose log", action="count")
        parser.add_argument('-D', '--delete_old', type=bool, help="Do`t delete removed domains", action="store")
        parser.add_argument('-n', '--name_server', type=str, help="Set name server", action="store")
        args = parser.parse_args()

        if args.show_verbose:
            BColor.ok("Use verbose")

        if not args.dir:
            BColor.process("Download files")
            path = Downloader.download_data_for_current_date()
            BColor.ok("Path to work dir %s" % path)

            BColor.process("Unzip file")
            converter = Converter(path, delete_work_dir=(not args.show_verbose))

            BColor.process("Parsing rib file")
            converter.parce_file_rib_file_to()

            BColor.process("Get AS list")
            as_list_text = converter.convert_rib_to_net_as()

            BColor.process("Save AS list")
            path_to_prefix_file = os.path.abspath(os.path.join(path, 'prefix_list'))
            save_prefix_list(as_list_text, path_to_prefix_file)

            BColor.process("Load AS list")
            as_list = load_prefix_list_from_var(as_list_text)

        else:
            path = args.dir
            BColor.ok("Use data path %s" % path)
            path_to_prefix_file = os.path.abspath(os.path.join(path, 'prefix_list'))
            as_list = load_prefix_list_from_file(path_to_prefix_file)

        BColor.process("Start resolve")

        delete_old = True
        if args.delete_old:
            BColor.ok("Not delete removed domains")
            delete_old = False

        name_server = '127.0.0.1'
        if args.name_server:
            BColor.ok("Use name server %s" % args.name_server)
            name_server = args.name_server

        Resolver.start_load_and_resolver_domain(as_list, os.path.abspath(os.path.join(path, 'work')),
                                                delete_old=delete_old, verbose=args.show_verbose,
                                                resolve_dns=name_server)

    except Exception as e:
        BColor.error("Got an exception: %s" % e.message)
        print traceback.format_exc()
