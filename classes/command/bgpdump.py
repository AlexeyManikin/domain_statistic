# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'alexeyymanikin'

from classes.command.command import Command
from config.main import *

DEFAULT_ARGUMENTS = []


class Bgpdump(Command):
    """
    Класс для работы с Bgpdump
    """

    OPTIONS = {
    }
    ':type : dict'

    def __init__(self, path):
        """
        :type path: unicode
        :return:
        """
        super(Bgpdump, self).__init__("ls")
        self.binary = [os.path.abspath(CURRENT_PATH+'/bin/bgpdump')]
        self.path = path

    def get_command(self):
        """
        Вернуть команду запуска Bgpdump
        :return: возвращаем команду запуска
        :rtype: list
        """

        return self.binary + [self.path]
