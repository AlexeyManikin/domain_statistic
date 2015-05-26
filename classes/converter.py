# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'alexeyymanikin'

import shutil
import re
import pprint
import MySQLdb
from classes.command.gunzip import Gunzip
from classes.command.bgpdump import Bgpdump
from helpers.helpers import *
from config.main import *


class Converter(object):

    def __init__(self, path, mysql_connection=False):
        """
        В качестве параметра передается путь до рабочей директории
        :rtype path: unicode
        """
        self.path = path
        self.work_path = self._create_work_dir()
        self.prefix = ['ru', 'su', 'rf']

        for prefix in self.prefix:
            shutil.copy(os.path.join(self.path, prefix+'_domains.gz'), self.work_path)

        if mysql_connection:
            self.connection = mysql_connection
        else:
            self.connection = MySQLdb.connect(host=MYSQL_HOST,
                                              user=MYSQL_USER,
                                              db=MYSQL_DATABASE,
                                              passwd=MYSQL_PASSWD,
                                              use_unicode=True,
                                              charset="utf8")

            self.connection.query("SET SESSION wait_timeout = 36000")
            self.connection.query("SET @@sql_mode:=TRADITIONAL")

    def __del__(self):
        """
        Подчисщаем за собой все
        :return:
        """
        self._remove_worl_dir()

    def _create_work_dir(self):
        """
        Создает директорию с текущей датой в download
        :rtype: unicode
        """
        work_path = os.path.abspath(os.path.join(self.path, 'work'))
        if not os.path.exists(work_path):
            os.makedirs(work_path)

        return work_path

    def _remove_worl_dir(self):
        """
        Подчищаем за собой
        :return:
        """
        if self.work_path:
            shutil.rmtree(self.work_path)
        pass

    def unzip_file(self, path_file):
        """
        :rtype path_file: unicode
        :return:
        """
        gunzip = Gunzip(path_file)
        command = gunzip.get_command()

        p = SubprocessRunner(command=command)
        p.run()
        p.wait(write_output_in_log=False)
        if p.process.returncode != 0:
            return False

        return True

    def load_domain_file_in_base(self):
        """
        Еще надо в БД загружать =)
        :return:
        """
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("TRUNCATE TABLE domain_tmp")
        re_prefix = re.compile(r'\s*')

        for prefix in self.prefix:

            print "Run unzip %s" % os.path.join(self.work_path, prefix+"_domains.gz")
            self.unzip_file(os.path.join(self.work_path, prefix+"_domains.gz"))
            file_prefix = os.path.join(self.work_path, prefix+"_domains")
            print "Prefix %s" % os.path.join(self.work_path, prefix+"_domains")

            sql_insert = "INSERT INTO " \
                         "domain_tmp(tld, register_date, register_date_end, free_date, domain_name, registrant," \
                         " delegated) VALUES "
            sql_insert_date = ""

            print "Start parce"
            file_rib_data = open(file_prefix)
            line = file_rib_data.readline()
            counter = 0
            counter_all = 0

            while line:
                if counter > 999:
                    print counter_all
                    cursor.execute(sql_insert + sql_insert_date)
                    self.connection.commit()
                    sql_insert_date = ""
                    counter = 0
                else:
                    if sql_insert_date != "":
                        sql_insert_date += ", "

                data = line.split("\t")

                domain = re.sub(re_prefix, '', data[0])
                registrant = re.sub(re_prefix, '', data[1])
                register_date = re.sub(re_prefix, '', data[2])
                register_end_date = re.sub(re_prefix, '', data[3])
                free_date = re.sub(re_prefix, '', data[4])
                deligated = re.sub(re_prefix, '', data[5])

                if deligated == '1':
                    deligated = 'Y'
                else:
                    deligated = 'N'

                sql_insert_date += """
                                    ('%s',
                                    STR_TO_DATE('%s', '%%d.%%m.%%Y'),
                                    STR_TO_DATE('%s', '%%d.%%m.%%Y'),
                                    STR_TO_DATE('%s', '%%d.%%m.%%Y'),
                                    LOWER('%s'),
                                    LOWER('%s'),
                                    '%s')""" % (prefix,
                                                register_date,
                                                register_end_date,
                                                free_date,
                                                domain,
                                                registrant,
                                                deligated)

                counter += 1
                counter_all += 1
                line = file_rib_data.readline()

    def parce_file_rib_file_to(self, path_rib_file=False, path_to=False):
        """
        :type path_rib_file: unicode
        :type path_to: unicode
        :rtype: unicode
        """

        if not path_rib_file:
            path_rib_file = os.path.abspath(os.path.join(self.path, 'rib.bz2'))
            path_to = os.path.abspath(os.path.join(self.work_path, 'rib'))

        bgpdump = Bgpdump(path_rib_file)
        command = bgpdump.get_command()

        shutil.rmtree(path_to, ignore_errors=True)
        file_rib = open(path_to, 'w')

        p = SubprocessRunner(command=command, stdout=file_rib)
        p.run()
        p.wait(write_output_in_log=False)
        file_rib.close()

        return path_to

    def convert_rib_to_net_as(self, path_rib_file=False):
        """
        # Input rows format:
        # TIME: 12/19/11 08:00:01
        # TYPE: TABLE_DUMP_V2/IPV4_UNICAST
        # PREFIX: 46.4.0.0/16
        # SEQUENCE: 23998
        # FROM: 80.91.255.62 AS1299
        # ORIGINATED: 12/08/11 05:45:51
        # ORIGIN: IGP
        # ASPATH: 1299 13237 24940 24940 24940 24940 24940
        # NEXT_HOP: 80.91.255.62
        # AGGREGATOR: AS24940 213.133.96.18

        :type path_rib_file: unicode
        :return:
        """

        if not path_rib_file:
            path_rib_file = os.path.abspath(os.path.join(self.work_path, 'rib'))

        re_prefix = re.compile('^PREFIX:\s+(.*?)$')
        re_aspath = re.compile('^ASPATH:\s(.*?)$')
        re_blank = re.compile('^\s+$')

        network_as = {}
        prefix = ''
        as_path = ''

        file_rib_data = open(path_rib_file)
        line = file_rib_data.readline()
        while line:
            symbol = line[0]
            if symbol == 'T' or symbol == 'S' or symbol == 'F' or symbol == 'O' or symbol == 'N':
                line = file_rib_data.readline()
                continue

            if symbol == 'P':
                match = re_prefix.findall(line)
                if match:
                    prefix = match[0]
                    line = file_rib_data.readline()
                    continue

            if symbol == 'A':
                match = re_aspath.findall(line)
                if match:
                    as_path = match[0].split(" ")[-1]
                    line = file_rib_data.readline()
                    continue

            match = re_blank.findall(line)
            if match and prefix != '':
                network_as[prefix] = as_path

            line = file_rib_data.readline()

        file_rib_data.close()
        return network_as