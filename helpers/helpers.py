# -*- coding: utf-8 -*-
__author__ = 'vladislav'

import psutil
import socket
import subprocess
import errno
import pwd
import time
import signal
import MySQLdb
from config.main import *
from Queue import Queue
from helperUnicode import as_default_string, as_unicode
from threading import Thread
import socket


def is_int(s):
    """
    Проверяем что переменная  INT
    :param s:
    :return:
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def check_prog_run(process_name):
    """
    Проверка на запущенность программы
    :type process_name: unicode
    :return:
    """
    global lock_socket   # Without this our lock gets garbage collected
    lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        lock_socket.bind('\0' + process_name)
        return False
    except socket.error:
        return True


def get_mysql_connection():
    """
    :return:
    """
    connection = MySQLdb.connect(host=MYSQL_HOST,
                                 port=MYSQL_PORT,
                                 user=MYSQL_USER,
                                 db=MYSQL_DATABASE,
                                 passwd=MYSQL_PASSWD,
                                 use_unicode=True,
                                 charset="utf8")

    connection.query("SET SESSION wait_timeout = 36000")
    connection.query("SET @@sql_mode:=TRADITIONAL")

    return connection


def get_hostname():
    """

    :return:
    """
    hostname_parts = socket.gethostname().split(".")
    if len(hostname_parts) > 0:
        return hostname_parts[0]
    else:
        raise EnvironmentError("Cannot get hostname")


def get_util(name):
    """

    :param name:
    :return:
    """
    command = ["/bin/which", name]

    env = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"}
    p = SubprocessRunner(command=command, env=env)
    p.run()

    return p.wait().rstrip("\n")


def pid_exists(pid):
    """
    Check whether pid exists in the current process table
    :param pid:
    :return:
    """
    if pid < 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError as e:
        return e.errno == errno.EPERM
    else:
        return True


def kill_child_processes(parent_pid, sig=signal.SIGTERM):
    """

    :param parent_pid:
    :param sig:
    :return:
    """
    p = psutil.Process(parent_pid)
    child_pid = p.children(recursive=True)
    for pid in child_pid:
        os.kill(pid.pid, sig)


def microtime(get_as_float=False):
    """

    :param get_as_float:
    :return:
    """
    if get_as_float:
        return time.time()
    else:
        return '%d' % time.time()


class SubprocessRunner(object):

    def __init__(self, command, logger=None, nice=19, log_prefix="subprocess", **process_options):
        """

        :param command:
        :param logger:
        :param nice:
        :param log_prefix:
        :param process_options:
        :return:
        """
        self.command = command
        self.nice = nice
        self.logger = logger
        self.process = None
        self.log_prefix = log_prefix

        self.process_options = self._extend_options(process_options)

    def run(self):
        """

        :return:
        """
        try:
            if self.logger:
                self.logger.debug("%s : execute command %s" % (as_unicode(self.log_prefix), as_unicode(self.command)))
        except:
            # на случай если в комманде возникнет UNICODE/DECODE error
            # может быть в случае передачи русских символов например в пути
            if self.logger:
                self.logger.error("%s : Error when write log" % (as_unicode(self.log_prefix)))

        command = map(lambda item: as_default_string(item), self.command)
        self.process = subprocess.Popen(command, **self.process_options)

    def wait(self, extended_return=False, write_output_in_log=True):
        """

        :param extended_return:
        :param write_output_in_log:
        :return:
        """
        out, err = self.process.communicate()

        try:
            if err != "":
                if self.logger:
                    self.logger.error("%s : Error: %s" % (as_unicode(self.log_prefix), as_unicode(err)))

            if write_output_in_log and self.logger:
                self.logger.debug("%s : command output: %s" % (as_unicode(self.log_prefix), as_unicode(out)))

        except:
            if self.logger:
                self.logger.error("%s : Error when write log" % (as_unicode(self.log_prefix)))

        return (out, err, self.process.returncode) if extended_return else out

    def iterate(self):
        """

        :return:
        """
        try:
            if self.logger:
                self.logger.debug("%s : iterate command %s" % (as_unicode(self.log_prefix), as_unicode(self.command)))
        except Exception as e:
            # на случай если в комманде возникнет UNICODE/DECODE error
            # может быть в случае передачи русских символов например в пути
            if self.logger:
                self.logger.error("%s : Error when write log: %s" % (as_unicode(self.log_prefix), str(e)))

        def enqueue_output(out, queue):
            for line in iter(out.readline, ""):
                queue.put(line.rstrip('\n'))
            out.close()

        def enqueue_errors(err, queue):
            for line in iter(err.readline, ""):
                queue.put(line.rstrip('\n'))
            err.close()

        command = map(lambda item: as_default_string(item), self.command)
        self.process = subprocess.Popen(command, **self.process_options)

        q_out = Queue()
        q_err = Queue()

        t_out = Thread(target=enqueue_output, args=(self.process.stdout, q_out))
        t_out.daemon = True
        t_out.start()

        t_err = Thread(target=enqueue_errors, args=(self.process.stderr, q_err))
        t_err.daemon = True
        t_err.start()

        while True:
            if not q_err.empty():
                err_output = q_err.get()
            else:
                err_output = ""

            if err_output != "":
                if self.logger:
                    self.logger.error("%s : Error: %s" % (as_unicode(self.log_prefix), as_unicode(err_output)))
                raise Exception(err_output)

            if not q_out.empty():
                line_output = q_out.get()
            else:
                line_output = ""

            code = self.process.poll()

            if self.logger:
                try:
                    self.logger.debug(
                        "%s : command iterate: %s" % (as_unicode(self.log_prefix), as_unicode(line_output)))
                except Exception as e:
                    # на случай если в комманде возникнет UNICODE/DECODE error
                    # может быть в случае передачи русских символов например в пути
                    self.logger.error(
                        "%s : Error when write command iterate log: %s" % (as_unicode(self.log_prefix), str(e)))

            if line_output == "":
                if code is not None:
                    self.logger.debug("%s : command iterate end" % as_unicode(self.log_prefix))
                    break

            yield line_output

    def _extend_options(self, options):
        """

        :param options:
        :return:
        """
        options['cwd'] = options.get('cwd', None)
        options['preexec_fn'] = options.get('preexec_fn', self.pre_exec)
        options['stderr'] = options.get('stderr', subprocess.PIPE)
        options['stdout'] = options.get('stdout', subprocess.PIPE)

        return options

    def pre_exec(self):
        """
        sets nice, ionice to process
        :return:
        """
        os.nice(self.nice)
        p = psutil.Process(os.getpid())
        p.ionice(psutil.IOPRIO_CLASS_IDLE)


class PwRepository(object):
    pws = {}

    @staticmethod
    def get(login):
        """

        :param login:
        :return:
        """
        if login in PwRepository.pws:
            return PwRepository.pws[login]
        else:
            pw = pwd.getpwnam(login)
            PwRepository.pws[login] = pw
            return pw