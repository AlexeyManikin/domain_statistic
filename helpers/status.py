__author__ = 'Alexey Y Manikin'

import multiprocessing
import time
from tqdm import tqdm
import os.path


class Status(multiprocessing.Process):

    def __init__(self, queue_in: multiprocessing.Queue, log_path: str or bool):
        """
        """
        multiprocessing.Process.__init__(self, name="print_status")
        self.queue = queue_in
        self.log_path = log_path
        self.all_count = self.queue.qsize()
        self.tqdm = None
        self.file_write = None

        if self.log_path:
            dirname = os.path.dirname(self.log_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            self.file_write = open(log_path, "w", encoding="utf-8")
            self.tqdm = tqdm(desc="Progress update domain",
                             total=self.queue.qsize(),
                             file=self.file_write)

    def __del__(self):
        """
        Закрываем файл если он был открыт
        :return:
        """
        if self.file_write:
            self.file_write.close()

    def run(self):
        """
        Запрашиваем DNS данные
        :return:
        """

        while not self.queue.empty():
            count_work = self.all_count - self.queue.qsize()
            update = count_work - self.tqdm.n
            self.tqdm.update(update)
            self.tqdm.refresh()
            time.sleep(10)

        self.tqdm.close()
