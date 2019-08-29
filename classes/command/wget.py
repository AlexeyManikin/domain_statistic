# -*- coding: utf-8 -*-
__author__ = 'alexeyymanikin'
from classes.command.command import Command
DEFAULT_ARGUMENTS = []


class Wget(Command):
    """
    Класс для работы с Wget
    """

    OPTIONS = {
        "quiet": type(None),
    }
    ':type : dict'

    def __init__(self, url, path):
        """
        :type url: unicode
        :type path: unicode
        :return:
        """
        super(Wget, self).__init__("wget")
        self.url = url
        self.path = path

    def get_command(self):
        """
        Вернуть команду запуска mysqldump
        :return: возвращаем команду запуска
        :rtype: list
        """

        return self.binary + [self.url, '-O', self.path]