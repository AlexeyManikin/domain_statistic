# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import types
import os
import re

from classes.misc.helperUnicode import as_default_string
from base.exc import Error
from classes.command.command import Command


class RsyncCommand(Command):
    """
    Класс для работы с утилитой Rsync
    """

    OPTIONS = {
        "i-d": types.BooleanType,
        "verbose": types.NoneType,
        "no-append": types.BooleanType,
        "no-devices": types.BooleanType,
        "blocking-io": types.BooleanType,
        "no-8": types.BooleanType,
        "remote-option": types.UnicodeType,
        "backup-dir": types.UnicodeType,
        "link-dest": types.UnicodeType,
        "no-sparse": types.BooleanType,
        "suffix": types.UnicodeType,
        "groupmap": types.UnicodeType,
        "relative": types.BooleanType,
        "no-J": types.BooleanType,
        "no-v": types.BooleanType,
        "preallocate": types.NoneType,
        "omit-link-times": types.BooleanType,
        "log-file-format": types.UnicodeType,
        "xattrs": types.NoneType,
        "protect-args": types.BooleanType,
        "no-S": types.BooleanType,
        "delete": types.NoneType,
        "hard-links": types.NoneType,
        "delete-excluded": types.NoneType,
        "no-acls": types.BooleanType,
        "contimeout": types.IntType,
        "no-recursive": types.BooleanType,
        "no-y": types.BooleanType,
        "executability": types.NoneType,
        "no-fuzzy": types.BooleanType,
        "no-contimeout": types.BooleanType,
        "no-W": types.BooleanType,
        "no-xattrs": types.BooleanType,
        "password-file": types.UnicodeType,
        "no-i": types.BooleanType,
        "motd": types.BooleanType,
        "no-bwlimit": types.BooleanType,
        "copy-dest": types.UnicodeType,
        "whole-file": types.BooleanType,
        "no-force": types.BooleanType,
        "existing": types.NoneType,
        "progress": types.BooleanType,
        "version": types.NoneType,
        "super": types.BooleanType,
        "stats": types.NoneType,
        "recursive": types.NoneType,
        "log-format": types.UnicodeType,
        "rsync-path": types.UnicodeType,
        "no-backup": types.BooleanType,
        "update": types.NoneType,
        "protocol": types.IntType,
        "no-i-r": types.BooleanType,
        "delay-updates": types.BooleanType,
        "no-dirs": types.BooleanType,
        "debug": types.UnicodeType,
        "no-A": types.BooleanType,
        "address": types.UnicodeType,
        "no-r": types.BooleanType,
        "max-size": types.UnicodeType,
        "links": types.BooleanType,
        "no-H": types.BooleanType,
        "no-p": types.BooleanType,
        "ignore-existing": types.NoneType,
        "files-from": types.UnicodeType,
        "partial-dir": types.UnicodeType,
        "no-ignore-errors": types.NoneType,
        "copy-dirlinks": types.NoneType,
        "no-times": types.BooleanType,
        "no-checksum": types.BooleanType,
        "from0": types.BooleanType,
        "devices": types.BooleanType,
        "no-implied-dirs": types.BooleanType,
        "no-verbose": types.BooleanType,
        "no-R": types.BooleanType,
        "8-bit-output": types.BooleanType,
        "no-protect-args": types.BooleanType,
        "no-from0": types.BooleanType,
        "no-g": types.BooleanType,
        "block-size": types.IntType,
        "include": types.UnicodeType,
        "no-relative": types.BooleanType,
        "munge-links": types.BooleanType,
        "sparse": types.BooleanType,
        "partial": types.BooleanType,
        "exclude-from": types.UnicodeType,
        "min-size": types.UnicodeType,
        "out-format": types.UnicodeType,
        "no-x": types.BooleanType,
        "no-m": types.BooleanType,
        "no-z": types.BooleanType,
        "quiet": types.NoneType,
        "owner": types.BooleanType,
        "ipv6": types.BooleanType,
        "human-readable": types.NoneType,
        "no-human-readable": types.NoneType,
        "specials": types.BooleanType,
        "no-owner": types.BooleanType,
        "no-compress": types.BooleanType,
        "no-inplace": types.BooleanType,
        "chmod": types.UnicodeType,
        "no-numeric-ids": types.BooleanType,
        "omit-dir-times": types.BooleanType,
        "no-delay-updates": types.BooleanType,
        "inplace": types.BooleanType,
        "no-super": types.BooleanType,
        "sockopts": types.UnicodeType,
        "no-progress": types.BooleanType,
        "no-D": types.NoneType,
        "no-h": types.BooleanType,
        "no-t": types.BooleanType,
        "no-i-d": types.BooleanType,
        "checksum": types.BooleanType,
        "no-partial": types.BooleanType,
        "no-group": types.BooleanType,
        "timeout": types.IntType,
        "no-8-bit-output": types.BooleanType,
        "skip-compress": types.UnicodeType,
        "inc-recursive": types.BooleanType,
        "old-dirs": types.BooleanType,
        "read-batch": types.UnicodeType,
        "include-from": types.UnicodeType,
        "no-hard-links": types.BooleanType,
        "chown": types.UnicodeType,
        "old-d": types.BooleanType,
        "size-only": types.NoneType,
        "no-links": types.BooleanType,
        "usermap": types.UnicodeType,
        "perms": types.NoneType,
        "iconv": types.UnicodeType,
        "delete-after": types.NoneType,
        "no-specials": types.BooleanType,
        "delete-delay": types.BooleanType,
        "temp-dir": types.UnicodeType,
        "one-file-system": types.NoneType,
        "no-s": types.BooleanType,
        "group": types.BooleanType,
        "no-d": types.BooleanType,
        "copy-links": types.NoneType,
        "i-r": types.BooleanType,
        "backup": types.BooleanType,
        "info": types.UnicodeType,
        "ignore-errors": types.NoneType,
        "modify-window": types.IntType,
        "del": types.NoneType,
        "delete-before": types.NoneType,
        "filter": types.UnicodeType,
        "append-verify": types.BooleanType,
        "no-perms": types.NoneType,
        "keep-dirlinks": types.NoneType,
        "no-iconv": types.NoneType,
        "no-blocking-io": types.BooleanType,
        "no-whole-file": types.BooleanType,
        "no-o": types.BooleanType,
        "times": types.NoneType,
        "implied-dirs": types.BooleanType,
        "exclude": types.UnicodeType,
        "dry-run": types.NoneType,
        "itemize-changes": types.NoneType,
        "log-file": types.UnicodeType,
        "max-delete": types.IntType,
        "acls": types.NoneType,
        "write-batch": types.UnicodeType,
        "server": types.NoneType,
        "no-detach": types.NoneType,
        "dparam": types.UnicodeType,
        "ipv4": types.BooleanType,
        "port": types.IntType,
        "checksum-seed": types.IntType,
        "sender": types.NoneType,
        "compress": types.NoneType,
        "no-l": types.BooleanType,
        "no-munge-links": types.BooleanType,
        "fuzzy": types.NoneType,
        "msgs2stderr": types.NoneType,
        "outbuf": types.UnicodeType,
        "bwlimit": types.UnicodeType,
        "no-X": types.BooleanType,
        "compare-dest": types.UnicodeType,
        "rsh": types.UnicodeType,
        "no-c": types.BooleanType,
        "detach": types.NoneType,
        "append": types.NoneType,
        "cvs-exclude": types.NoneType,
        "no-inc-recursive": types.BooleanType,
        "no-O": types.BooleanType,
        "help": types.NoneType,
        "dirs": types.BooleanType,
        "daemon": types.NoneType,
        "no-timeout": types.BooleanType,
        "archive": types.NoneType,
        "compress-level": types.IntType,
        "force": types.BooleanType,
        "list-only": types.BooleanType,
        "delete-during": types.BooleanType,
        "numeric-ids": types.BooleanType,
        "ignore-times": types.NoneType,
        "fake-super": types.BooleanType,
        "no-motd": types.BooleanType,
        "config": types.UnicodeType,
        "qsort": types.NoneType,
        "only-write-batch": types.UnicodeType,
        "safe-links": types.NoneType,
        "remove-source-files": types.NoneType,
        "delete-missing-args": types.NoneType
    }
    ":type: dict"

    DEFAULT_ARGUMENTS = ["perms",
                         "times",
                         "recursive",
                         "safe-links",
                         "stats",
                         "ignore-errors"]
    ":type: dict"

    HARDLINK_ARGUMENTS = ["itemize-changes",
                          "itemize-changes",
                          "hard-links",
                          "one-file-system",
                          "quiet",
                          {"timeout": 600},
                          {"log-file-format": u"%n %l"}]
    ":type: dict"

    RSYNC_BACKUP_ARGUMENTS = ["stats",
                              "no-human-readable",
                              "archive",
                              "safe-links",
                              "hard-links",
                              "ignore-errors",
                              "one-file-system"]
    ":type: dict"

    RSYNC_BACKUP_EXCLUDE = [{"exclude": "*.file.tar.zip"},
                            {"exclude": "*.file.tar.gz"},
                            {"exclude": "*.access.log*"},
                            {"exclude": "*.vsftpd.log"},
                            {"exclude": "*.*.*.sql*"},
                            {"exclude": "BACKUP"},
                            {"exclude": "archive"},
                            {"exclude": "beget_tmp"},
                            {"exclude": ".beget"},
                            {"exclude": "PHP_errors.log"},
                            {"exclude": ".beget*"},
                            {"exclude": "*beget_tmp*"}]
    ":type: dict"

    def __init__(self, source, destination, log_file=None, options=None):
        """
        :param source: откуда копируем
        :type source: str|unicode
        :param destination: куда
        :type destination: str|unicode
        :param log_file:
        :type log_file: str|unicode|None
        :return:
        """
        self.source = as_default_string(source)
        self.destination = as_default_string(destination)
        super(RsyncCommand, self).__init__("rsync")

        if options is not None:
            self.set_options(options)
        else:
            self.set_options(self.DEFAULT_ARGUMENTS)

        if log_file is not None:
            self.set_option("log-file", log_file)

    def get_command(self, path=None):
        """
        Получение команды
        :type path: unicode|None
        :return:
        """
        args = self.get_args()

        # hack to ensure 'include' is always before exclude
        args.sort(key=lambda x: '' if x.startswith('--include=') else x)
        if path:
            return self.binary + args + [self.source, self.destination + "/" + path]
        else:
            return self.binary + args + [self.source, self.destination]

    def get_command_delete_exclude(self, path, exclude):
        """
        Удаляем все кроме exclude
        :type tmp_dir: unicode
        :type path: unicode
        :type exclude: list
        :return:
        """

        for dir in exclude:
            self.set_option("exclude", dir)

        args = self.get_args()
        # hack to ensure 'include' is always before exclude
        args.sort(key=lambda x: '' if x.startswith('--include=') else x)

        return self.binary + args + ['-av', '--delete',  self.source,  self.destination + '/' + path + '/']

    def get_command_create_dir(self, path):
        """
        Дать команду для создания пути
        :param path: unicode
        :return:
        """

        if path[0:1] == '/':
            return self.binary + ['-q', '/dev/null',  self.destination + path + '/']

        return self.binary + ['-q', '/dev/null',  self.destination + '/' + path + '/']

    def set_params_make_hardlink(self, hardlinks_to, custom_options):
        """
        Устанавливаем параметры для локального бекапа, c использованием хардлинков
        :type hardlinks_to: str|unicode
        :type custom_options: list
        :return:
        """

        if type(custom_options) is not list:
            raise Error("custom_options must be a list")

        self.set_options(self.HARDLINK_ARGUMENTS)
        self.set_options(["stats", "no-human-readable", "delete"])
        self.set_options(custom_options)
        if hardlinks_to is not None:
            self.set_option("link-dest", hardlinks_to)

    def set_params_rsync_backup(self, delete=True, hardlinks_to=None, log_format=None, custom_options=[]):
        """
        Получаем команду для бекапа на удаленные сервера
        :type hardlinks_to: str|unicode|None
        :type log_format: str|unicode|None
        :type custom_options: list
        :return:
        """
        if type(custom_options) is not list:
            raise Error("custom_options must be a list")

        self.set_options(self.RSYNC_BACKUP_ARGUMENTS)

        if delete:
            self.set_option("delete")

        if log_format is not None:
            self.set_option("log-file-format", log_format)

        if hardlinks_to is not None:
            self.set_option("link-dest", hardlinks_to)

        self.set_options(self.RSYNC_BACKUP_EXCLUDE)

        if os.path.isfile("/etc/backup/exclude"):
            self.set_option("exclude-from", "/etc/backup/exclude")

        self.set_options(custom_options)

    def set_changet_list_file(self, list):
        """
        Указывает перекачивать только список файлов указанных в файле list
        :param list:
        :return:
        """
        if os.path.isfile(list):
            self.set_option("delete-missing-args")
            self.set_option("files-from", list)
        else:
            print "RSYNC"

    @staticmethod
    def parse_stats(output):
        try:
            number_of_files = int(
                re.search(
                    'Number of files: (\d+)',
                    output,
                    re.MULTILINE).group(1))
            total_file_size = int(
                re.search(
                    'Total file size: (\d+)',
                    output,
                    re.MULTILINE).group(1))
            total_bytes_sent = int(
                re.search(
                    'Total bytes sent: (\d+)',
                    output,
                    re.MULTILINE).group(1))

            return (number_of_files, total_file_size, total_bytes_sent)
        except:
            raise Error('Can`t parsing rsync output')
