import sqlite3
from utils.constants.database import *
from sqlite3 import Error
from accessify import private, protected


class DbConnector:
    def __init__(self, path):
        self.path = path
        self.connection = self.__create_connection(self.path)
        self.__setup_db(self.connection)
        self.__select_lab_id_by_name(self.connection, 1)

    @classmethod
    def __create_connection(cls, path):
        """
        create a database connection to the SQLite database
            specified by the db_file
        :param path: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error {e} occurred")
        return conn

    @classmethod
    def __setup_db(cls, connection):
        """
        Create tables from tables queries list
        :param conn: the Connection object
        :return:
        """
        cur = connection.cursor()

        for query in TABLES_QUERIES_LIST:
            try:
                cur.execute(query)
                print('Query executed successfully')

            except Error as e:
                print(f'The error {e} occurred')

        connection.commit()

    def select_all_analysis_types(self):
        """
        Query all rows in the analysis table
        :param conn: the Connection object
        :return:
        """
        cur = self.connection.cursor()
        query = "SELECT name, abbreviation FROM analysis_value_type"

        try:
            cur.execute(query)
            print('Query executed successfully')

        except Error as e:
            print(f'The error {e} occurred')

        # коммит не нужен, т.к. бд никак не изменяется
        # conn.commit()

        # Создаем список кортежей вида [(name, abb), (name, abb)]
        rows = cur.fetchall()
        return rows

    @classmethod
    def __select_analysis_id_by_type(cls, connection, analysis_type):
        """
        Query analysis id by type. Internal function
        :param analysis_type: name of the selected analysis type
        :return: id of the type
        """
        cur = connection.cursor()
        query = "SELECT id FROM analysis_value_type WHERE name = (?)"

        try:
            cur.execute(query, (analysis_type,))
            print('Query executed successfully')

        except Error as e:
            print(f'The error {e} occurred')

        # conn.commit()
        rows = cur.fetchone()

        return rows[0][0]

    def select_analysis_info_by_type(self, analysis_type):
        """
        Query all analysis of the selected type. Public function
        :param conn: the Connection object
        :param analysis_type: name of the selected analysis type
        :return: all information about selected analysis
        """
        cur = self.connection.cursor()
        query = "SELECT * FROM analysis_value WHERE analysis_type_id = (?)"
        analysis_type = self.__select_analysis_id_by_type(self.connection,
                                                          analysis_type)

        try:
            cur.execute(query, (analysis_type,))
            print('Query executed successfully')

        except Error as e:
            print(f'The error {e} occurred')

        # conn.commit()
        rows = cur.fetchall()

        return rows

    @classmethod
    def __select_lab_id_by_name(cls, connection, name):
        """
        Query analysis id by type. Internal function
        :param analysis_type: name of the selected analysis type
        :return: id of the type
        """
        cur = connection.cursor()
        query = "SELECT id FROM laboratory WHERE name = (?)"

        try:
            cur.execute(query, (name,))
            print('Query executed successfully')

        except Error as e:
            print(f'The error {e} occurred')
        # conn.commit()
        rows = cur.fetchone()
        print(rows)
        return rows if rows is None else rows[0][0]

    def insert_lab(self, lab):
        if self.__select_lab_id_by_name is not None:
            return

        cur = self.connection.cursor()
        query = f"INSERT INTO laboratory (name) VALUES ({lab})"

        try:
            cur.execute(query)
            print('Query executed successfully')
            self.connection.commit()
        except Error as e:
            print(f'The error {e} occurred')

    @classmethod
    def __select_analysis_value_type_id_by_name(cls, connection, name):
        """
        Query analysis id by type. Internal function
        :param analysis_type: name of the selected analysis type
        :return: id of the type
        """
        cur = connection.cursor()
        query = "SELECT id FROM analysis_value_type WHERE name = (?)"

        try:
            cur.execute(query, (name,))
            print('Query executed successfully')

        except Error as e:
            print(f'The error {e} occurred')
        # conn.commit()
        rows = cur.fetchone()
        print(rows)
        return rows if rows is None else rows[0][0]

    def insert_analysis_value_type(self, name):
        if self.__select_analysis_value_type_id_by_name(self.connection, name)\
                is not None:
            return

        cur = self.connection.cursor()
        query = f"INSERT INTO laboratory (name) VALUES ({name})"

        try:
            cur.execute(query, (id,))
            print('Query executed successfully')
            self.connection.commit()
        except Error as e:
            print(f'The error {e} occurred')

    def insert_analysis_value(self, data):
        # ["laboratory_id", "analysis_value_type_id", "is_numeric",
        # "result_text", "result_value", "unit", "limit_is_numeric",
        # "reference", "upper_limit", "lower_limit", "time_stamp"]

        cur = self.connection.cursor()
        # query = f"INSERT INTO laboratory (name) VALUES ({name})"

        try:
            # cur.execute(query, (id,))
            print('Query executed successfully')

        except Error as e:
            print(f'The error {e} occurred')
    def delete(self, table, data):
        return


db = DbConnector(DATABASE_PATH)

data_sample_new = [["laboratory_name", "analysis_value_type_name", "is_numeric",
                    "result_text", "result_value", "unit", "limit_is_numeric",
                    "reference", "upper_limit", "lower_limit", "time_stamp"],
                   [], []
                   ]

data_sample_for_testing = \
    [
        ["днком", "ВПЧ типы 51,56", 0, "не обнаружено",
         "LgВПЧ/10^5 эпит.клеток", 0, "не обнаружено", "2022-01-27"],
        ["гемотест", "витамин А", 1, 0.5, "мкг/мл", 1, 0.2, 0.8, "2023-05-14"]
    ]

# Нужно добавить таблицу для перевода единиц вида:
# id_1 | id_2 | factor - необходимо заполнить заранее
# И таблицу с сопоставлением единиц измерения и id:
# id | name
