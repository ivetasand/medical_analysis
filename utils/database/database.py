import sqlite3
from utils.constants.database import *
from sqlite3 import Error


def create_connection(path):
    """ create a database connection to the SQLite database
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


# def execute_query(connector, query, value=False):
#     cursor = connector.cursor()
#     try:
#         if value:
#             cursor.execute(query, value)
#         else:
#             cursor.execute(query)
#         connector.commit()
#         print('Query executed successfully')
#
#     except Error as e:
#         print(f'The error {e} occurred')


# def execute_many_query(connector, query, value=False):
#     cursor = connector.cursor()
#     try:
#         if value:
#             cursor.executemany(query, value)
#         else:
#             cursor.executemany(query)
#         connector.commit()
#         print('Query executed successfully')
#
#     except Error as e:
#         print(f'The error {e} occurred')


def setup_db(conn):
    """
    Create tables from tables queries list
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()

    for query in TABLES_QUERIES_LIST:
        try:
            cur.execute(query)
            print('Query executed successfully')

        except Error as e:
            print(f'The error {e} occurred')
    conn.commit()


def select_all_analysis_types(conn):
    """
    Query all rows in the analysis table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    query = "SELECT name, abbreviation FROM analysis_value_type"

    try:
        cur.execute(query)
        print('Query executed successfully')

    except Error as e:
        print(f'The error {e} occurred')
    conn.commit()
    rows = cur.fetchall()

    return rows


def select_analysis_by_type(conn, analysis_type):
    """
    Query analysis by type
    :param conn: the Connection object
    :param analysis_type: type of the selected analysis
    :return: result rows
    """
    cur = conn.cursor()
    query = "SELECT * FROM analysis_value WHERE analysis_item_id = (?)"

    try:
        cur.execute(query, (analysis_type,))
        print('Query executed successfully')

    except Error as e:
        print(f'The error {e} occurred')
    conn.commit()
    rows = cur.fetchall()
    return rows


def insert_analysis(connector, table, value):
    val_str = "?," * (len(value) - 1)

    query = f"INSERT INTO {table} VALUES ({val_str})"

    if type(value[0]) not in [tuple, list]:
        execute_query(connector, query, value)
    else:
        execute_many_query(connector, query, value)

    return True


def delete(connector, table, data):
    return


connection = create_connection(DATABASE_PATH)
setup_db(connection)
# select_by_analysis_type(connection, 5)

data_sample = {"laboratory": [["name1"], ["name2"]],
               "analysis_value_type": [["name1", "abbreviation1"],
                                       ["name2", "abbreviation2"]],
               "analysis_item": [["name1", '']],
               "analysis_value": [
                   ["lab_id1", "analysis_item_id1", "is_numeric1",
                    "result_text1", "result_value", "name",
                    "upper_limit", "lower_limit", "time_stamp"]]
               }

data_sample_new = {[""], [], []
                   }

    # "laboratory": [["name1"], ["name2"]],
    #            "analysis_value_type": [["name1", "abbreviation1"],
    #                                    ["name2", "abbreviation2"]],
    #            "analysis_item": [["name1", '']],
    #            "analysis_value": [
    #                ["lab_id1", "analysis_item_id1", "is_numeric1",
    #                 "result_text1", "result_value", "name",
    #                 "upper_limit", "lower_limit", "time_stamp"]]
    #            }
