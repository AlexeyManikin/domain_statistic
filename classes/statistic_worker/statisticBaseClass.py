__author__ = 'Alexey Y Manikin'

from helpers.helpers import get_mysql_connection
import multiprocessing
import MySQLdb


class StatisticBaseClass(multiprocessing.Process):

    BEGET_AS: int = 198610
    BEGET_REGISTRANT: str = 'beget-ru'

    def __init__(self, number: int, statistic_type: str):
        """
        :param number:
        """
        multiprocessing.Process.__init__(self, name="%s_%i" % (statistic_type, number))
        self.number = number
        self.connection = None

    def _connect_mysql(self) -> MySQLdb.connect:
        """
        :return:
        """
        self.connection = get_mysql_connection()
        return self.connection

    @staticmethod
    def create_db_if_not_exist(table_definition: str):
        """
        :return:
        """
        connection = get_mysql_connection()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)

        sql = "SET sql_notes = 0"
        cursor.execute(sql)
        sql = table_definition
        cursor.execute(sql)
        sql = "SET sql_notes = 1"
        cursor.execute(sql)

        connection.close()

    @staticmethod
    def get_beget_registrant(cursor) -> int:
        """
        :return:
        """
        sql = "SELECT id FROM registrant WHERE registrant = '%s' LIMIT 1" % StatisticBaseClass.BEGET_REGISTRANT
        cursor.execute(sql)
        result = cursor.fetchone()

        if result:
            return result['id']

        return 0

    def _update(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def run(self):
        """
        Обрабатываем массив записываем в БД
        :return:
        """
        self._connect_mysql()
        self._update()
        self.connection.commit()
        self.connection.close()
