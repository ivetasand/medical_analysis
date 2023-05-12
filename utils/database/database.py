import sqlite3
from utils.constants.database import *
from sqlite3 import Error


def create_connection(path):
    connector = None
    try:
        connector = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error {e} occurred")

    return connector


def execute_query(connector, query, value=False):
    cursor = connector.cursor()
    try:
        if value:
            cursor.execute(query, value)
        else:
            cursor.execute(query)
        connector.commit()
        print('Query executed successfully')

    except Error as e:
        print(f'The error {e} occurred')


def execute_many_query(connector, query, value=False):
    cursor = connector.cursor()
    try:
        if value:
            cursor.executemany(query, value)
        else:
            cursor.executemany(query)
        connector.commit()
        print('Query executed successfully')

    except Error as e:
        print(f'The error {e} occurred')


def setup_db(connector):
    for query in TABLES_LIST:
        execute_query(connector, query)


def select_all_analysis_types(connector):
    query = "SELECT name, abbreviation FROM analysis_value_type"
    return execute_query(connector, query)


def select_by_analysis_type(connector, analysis_type):
    query = "SELECT * FROM analysis_value WHERE analysis_item_id = (?)"
    return execute_query(connector, query, analysis_type)


def insert(connector, table, value):
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