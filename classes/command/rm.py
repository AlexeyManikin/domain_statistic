# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'alekseymanikin'

from classes.command.command import Command
import os


class RmCommand(Command):
    """
    Класс для работы с rm
    """

    OPTIONS = {}
    ':type : dict'

    DEFAULT_ARGUMENTS = []
    ':type : list'

    def __init__(self, path):
        """
        :return:
        """

        super(RmCommand, self).__init__("rm")

        self.path = path
        self.set_options(self.DEFAULT_ARGUMENTS)

    def set_path(self, path):
        """
        :rtype path: unicode
        :return:
        """
        if check_path_storage_disk(path):
            self.path = path
            return True
        return False

    def get_command(self):
        """
        :return: возвращаем команду запуска
        :rtype: list
        """
        args = self.get_args()
        path = os.path.abspath(self.path)
        return self.binary + ["-rf"] + ["--one-file-system"] + args + [path]