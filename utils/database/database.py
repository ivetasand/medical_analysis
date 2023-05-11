import sqlite3
from utils.constants.database import *
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error {e} occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print('Query executed successfully')

    except Error as e:
        print(f'The error {e} occurred')


def setup_db(connection):
    for query in TABLES_LIST:
        execute_query(connection, query)


def select(connection, table):
    return


def add(connection, table, data):
    return


def delete(connection, table, data):
    return


connection = create_connection(DATABASE_PATH)
setup_db(connection)
