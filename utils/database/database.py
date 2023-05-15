import sqlite3
from sqlite3 import Error
import logging

from accessify import private


class DbConnector:

    def __init__(self, path, tables_queries_list):
        """
        init database handler and editor
        :param path: desired path to db file
        :param tables_queries_list: queries for db setup
        """
        self.path = path
        logging.basicConfig(level=logging.INFO, filename="bd_log.log",
                            filemode="w",
                            format="%(asctime)s %(levelname)s %(message)s")
        self.connection = self.__create_connection(self.path)
        self.__setup_db(self.connection, tables_queries_list)


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
            logging.info("Connection to SQLite DB successful")
        except Error as e:
            logging.error(f"The error {e} occurred")
        return conn

    @classmethod
    def __setup_db(cls, connection, tables_queries_list):
        """
        Create tables from tables queries list
        :param conn: the Connection object
        """
        cur = connection.cursor()

        for query in tables_queries_list:
            try:
                cur.execute(query)
                logging.info('Table created successfully')
            except Error as e:
                logging.error(f'The error {e} occurred')

        connection.commit()

    def select_all_analysis_types(self):
        """
        Query all rows in the analysis table
        :return: rows with name + abbreviation
        """
        cur = self.connection.cursor()
        query = "SELECT name, abbreviation FROM analysis_value_type"

        try:
            cur.execute(query)
            logging.info('All analysis types were successfully selected')
        except Error as e:
            logging.error(
                f'The error {e} occurred while selecting all analysis types')

        # коммит не нужен, т.к. бд никак не изменяется
        # conn.commit()

        # Создаем список кортежей вида [(name, abb), (name, abb)]
        rows = cur.fetchall()
        return rows

    def select_analysis_info_by_type(self, analysis_type):
        """
        Query all data for every analysis of the selected type
        :param analysis_type: name of the selected analysis type
        :return: all information about selected analysis
        """
        cur = self.connection.cursor()
        type_id = self.select_analysis_value_type_id_by_name(analysis_type)

        query = "SELECT * FROM analysis_value WHERE analysis_type_id = (?)"

        try:
            cur.execute(query, (type_id,))
            logging.info('Analysis info by type was successfully selected')

        except Error as e:
            logging.error(f'The error {e} occurred while selecting analysis'
                          f'info by type')

        # conn.commit()
        rows = cur.fetchall()

        return rows

    def select_lab_id_by_name(self, name):
        """
        Query lab id by name
        :return: id of the lab
        """
        cur = self.connection.cursor()
        query = "SELECT id FROM laboratory WHERE name = (?)"

        try:
            cur.execute(query, (name,))
            logging.info('Selecting lab_id by name executed successfully')

        except Error as e:
            logging.error(f'The error {e} occurred while selecting lab_id by '
                          f'name')

        rows = cur.fetchone()
        return rows if rows is None else rows[0]

    def insert_lab(self, lab):
        """
        Insert new lab
        :param lab: name of the lab
        """
        if self.select_lab_id_by_name(lab) is not None:
            return

        cur = self.connection.cursor()
        query = f"INSERT INTO laboratory (name) VALUES (?)"

        try:
            cur.execute(query, (lab,))
            self.connection.commit()
            logging.info('Lab was successfully added')
        except Error as e:
            logging.error(f'The error {e} occurred while adding new lab')

    def select_analysis_value_type_id_by_name(self, name):
        """
        Query analysis_value_type id by name. Internal function
        :param name: name of the selected analysis type
        :return: id of the type
        """
        cur = self.connection.cursor()
        query = "SELECT id FROM analysis_value_type WHERE name = (?)"

        try:
            cur.execute(query, (name,))
            logging.info(
                'Analysis value type id was successfully selected by name')

        except Error as e:
            logging.error(f'The error {e} occurred while selecting '
                          f'analysis type id by name')

        rows = cur.fetchone()
        return rows if rows is None else rows[0]

    def insert_analysis_value_type(self, name):
        """
        Insert analysis value type
        :param name: name of the new analysis
        :return:
        """
        if self.select_analysis_value_type_id_by_name(name) \
                is not None:
            return

        cur = self.connection.cursor()
        query = f"INSERT INTO analysis_value_type (name) VALUES (?)"

        try:
            cur.execute(query, (name,))
            self.connection.commit()
            logging.info('Analysis value type was inserted successfully')
        except Error as e:
            logging.error(f'The error {e} occurred while inserting analysis '
                          f'value type')

    def insert_analysis_value(self, data):
        """
        Insert analysis value with all additional info
        :param data: format of data:
        ("laboratory_id", "analysis_value_type_id", "is_numeric",
        "result_text", "result_value", "unit", "limit_is_numeric",
        "reference", "upper_limit", "lower_limit", "time_stamp")
        :return:
        """

        # пока что без таблицы units

        if data[2] == 0:
            if data[4] == 0:
                query = f"INSERT INTO analysis_value (" \
                        f"lab_id, analysis_type_id, is_result_numeric," \
                        f"result_text, is_reference_numeric," \
                        f"reference, time_stamp) " \
                        f"VALUES (?,?,?,?,?,?,?)"
            else:
                query = f"INSERT INTO analysis_value (" \
                        f"lab_id, analysis_type_id, is_result_numeric," \
                        f"result_text, is_reference_numeric," \
                        f"upper_limit, lower_limit, time_stamp) " \
                        f"VALUES (?,?,?,?,?,?,?,?)"
        else:
            if data[4] == 0:
                query = f"INSERT INTO analysis_value (" \
                        f"lab_id, analysis_type_id, is_result_numeric," \
                        f"result_value, is_reference_numeric," \
                        f"reference, time_stamp) " \
                        f"VALUES (?,?,?,?,?,?,?)"
            else:
                query = f"INSERT INTO analysis_value (" \
                        f"lab_id, analysis_type_id, is_result_numeric," \
                        f"result_value, is_reference_numeric," \
                        f"upper_limit, lower_limit, time_stamp) " \
                        f"VALUES (?,?,?,?,?,?,?,?)"

        cur = self.connection.cursor()
        try:
            cur.execute(query, data)
            self.connection.commit()
            logging.info('Analysis value was inserted successfully')
        except Error as e:
            logging.error(f'The error {e} occurred while inserting analysis '
                          f'value')

    def delete(self, table, data):
        return

# Нужно добавить таблицу для перевода единиц вида:
# id_1 | id_2 | factor - необходимо заполнить заранее
# И таблицу с сопоставлением единиц измерения и id:
# id | name
