import psycopg2
from .config import db_config

"""
Connection handler for PostgreSQL Database
"""


class DataBaseError(Exception):
    """Error during connecting to database"""


conn = None
cur = None


def connect():
    global conn, cur
    params = db_config()
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise DataBaseError


def check():
    """Check DB Connection"""
    global conn
    try:
        if conn.closed == 0:
            return
        else:
            connect()
            return
    except (Exception, psycopg2.DatabaseError, psycopg2.InterfaceError, psycopg2.OperationalError) as err:
        print(err)
        raise DataBaseError


def insert(table, fields, data, rows = 1):
    global cur
    query = "INSERT INTO " + table + " "
    columns = ""
    vals = ""
    for i in range(rows):
        columns = columns + fields[i] + ","
    columns = columns[:-1]
    query = query + "(" + columns + ")" + " VALUES "
    for i in range(rows):
        vals = vals + "'"
        vals = vals + data[i] + "'"
        vals = vals + ","
    vals = vals[:-1]
    query = query + "(" + vals + ")"
    # Sending Query
    check()
    cur.execute(query)
    conn.commit()

