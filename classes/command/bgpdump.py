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

    def __init__(self, path_in: str, path_out: str):
        """
        :type path_in: unicode
        :return:
        """
        super(Bgpdump, self).__init__("bgpdump")
        self.binary = [os.path.abspath(CURRENT_PATH+'/bin/bgpdump')]
        self.path_in = path_in
        self.path_out = path_out

    def get_command(self) -> list:
        """
        Вернуть команду запуска Bgpdump
        :return: возвращаем команду запуска
        :rtype: list
        """

        return self.binary + ["-O", self.path_out, self.path_in]
