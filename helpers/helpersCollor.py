# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
import os
import traceback

__author__ = 'alexeyymanikin'

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


class BColor(object):

    STATUS_OK = 'ok'
    STATUS_PROCESS = 'process'
    STATUS_WARNING = 'warning'
    STATUS_ERROR = 'error'

    def __init__(self):
        pass

    @staticmethod
    def parsing_message(message):
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

    @staticmethod
    def format_message(message_type, message, pid=None):
        """
        Вывод сообщения на консоль в формате
        [дата] PID TYPE: message
        :param message_type: unicode
        :param message: unicode
        :return:
        """
        try:
            date = BColor.parsing_message("[ " + time.strftime("%m/%d/%y %H:%M:%S") + " ] ")
            if pid is None:
                pid = BColor.parsing_message("<BOLD> PID: " + str(os.getpid()) + "<RESET>")
            else:
                pid = BColor.parsing_message("<BOLD> Process number: " + str(pid) + ", PID: " + str(os.getpid())
                                             + "<RESET>")

            if message_type == BColor.STATUS_OK:
                message_type = BColor.parsing_message(' <GREEN> STATUS: <RESET>')
            elif message_type == BColor.STATUS_WARNING:
                message_type = BColor.parsing_message(' <YELLOW> WARNING: <RESET>')
            elif message_type == BColor.STATUS_PROCESS:
                message_type = BColor.parsing_message(' <BLUE> PROCESS: <RESET>')
            else:
                message_type = BColor.parsing_message(' <RED> ERROR: <RESET>')

            print date + pid + message_type + " " + BColor.parsing_message(message)
            return date + pid + message_type + " " + BColor.parsing_message(message)
        except:
            print traceback.format_exc()
            return traceback.format_exc()

    @staticmethod
    def ok(message, pid=None):
        """
        :type message: unicode
        :type pid: int
        :rtype: unicode
        """
        return BColor.format_message(BColor.STATUS_OK, message, pid=pid)

    @staticmethod
    def warning(message, pid=None):
        """
        :type message: unicode
        :type pid: int
        :rtype: unicode
        """
        return BColor.format_message(BColor.STATUS_WARNING, message, pid=pid)

    @staticmethod
    def error(message, pid=None):
        """
        :type message: unicode
        :type pid: int
        :rtype: unicode
        """
        return BColor.format_message(BColor.STATUS_ERROR, message, pid=pid)

    @staticmethod
    def process(message, pid=None):
        """
        :type message: unicode
        :type pid: int
        :rtype: unicode
        """
        return BColor.format_message(BColor.STATUS_PROCESS, message + "... ", pid=pid)
