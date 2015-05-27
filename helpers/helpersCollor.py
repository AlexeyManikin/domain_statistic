# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'alexeyymanikin'

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

class BColor():

    @staticmethod
    def parce_message(message):
        """
        Красивый вывод в консоль
        :param message:
        :return:
        """
        message = message.replace("<RESET>",   RESET_SEQ).replace("<BOLD>", BOLD_SEQ)
        message = message.replace("<BLUE>",    COLOR_SEQ % (30 + BLUE))
        message = message.replace("<GREEN>",   COLOR_SEQ % (30 + GREEN))
        message = message.replace("<RED>",     COLOR_SEQ % (30 + RED))
        message = message.replace("<BLACK>",   COLOR_SEQ % (30 + BLACK))
        message = message.replace("<YELLOW>",  COLOR_SEQ % (30 + YELLOW))
        message = message.replace("<MAGENTA>", COLOR_SEQ % (30 + MAGENTA))
        message = message.replace("<CYAN>",    COLOR_SEQ % (30 + CYAN))
        message = message.replace("<WHITE>",   COLOR_SEQ % (30 + WHITE))
        return message
