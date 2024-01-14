# pylint: disable=W0718
# pylint: disable=C0103
# pylint: disable=W0707
# pylint: disable=E0401
# pylint: disable=W0602

"""
Connection handler for PostgresSQL Database
"""

import psycopg2
from psycopg2 import sql
from psycopg2.sql import Composed

from .config import db_config


class DataBaseError(Exception):
    """Error during connecting to database"""


params = db_config()

try:
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
    raise DataBaseError


def connect():
    """Connect to database"""
    global conn, cur, params
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
    except (Exception, psycopg2.DatabaseError) as err:
        print(err)
        raise DataBaseError


def check():
    """Check DB Connection"""
    global conn
    try:
        if conn.closed == 0:
            return
        connect()
        return
    except Exception as err:
        print(err)
        raise DataBaseError from err


def insert(table, fields, data, rows=1):
    """Insertion of data to a table"""
    global cur
    check()
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
    cur.execute(query)
    conn.commit()


def get_user(table: str, data: list):
    """Fetches some data from table using username and password"""
    global cur
    check()
    field_data = [data[0][1], data[1][1]]
    fields = [data[0][0], data[1][0]]
    query = form_get_query(table, fields, field_data)
    cur.execute(query)
    return cur.fetchone()


def form_get_query(table_name: str, fields: list, data: list) -> Composed:
    """Generate sql query for get_user()"""
    stmt = sql.SQL("""
        SELECT 
            * 
        FROM
            {table}
        WHERE
            {cred_1}={data_1}
        AND
            {cred_2}={data_2} 
    """).format(
        table=sql.Identifier(table_name),
        cred_1=sql.Identifier(fields[0]),
        cred_2=sql.Identifier(fields[1]),
        data_1=sql.Literal(data[0]),
        data_2=sql.Literal(data[1])
    )
    return stmt
