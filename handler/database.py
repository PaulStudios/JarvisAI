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


def insert(table, fields: list, data: list) -> None:
    """Insertion of data to a table"""
    global cur
    check()
    query = form_insert_query(table, fields, data)
    # Sending Query
    check()
    cur.execute(query)
    conn.commit()


def form_insert_query(table_name: str, fields: list, data: list) -> Composed:
    """Generate sql query for get_user()"""
    stmt = sql.SQL("""
        INSERT INTO 
            {table}
        (
            {fields}
        ) VALUES (
            {user_data}
        )
    """).format(
        table=sql.Identifier(table_name),
        fields=sql.SQL(',').join(
            sql.Identifier(n) for n in fields
        ),
        user_data=sql.SQL(',').join(
            sql.Literal(n) for n in data
        )
    )
    return stmt


def get_user(table: str, data: list):
    """Fetches some data from table using username and password"""
    global cur
    query = form_get_query(table, data[0], data[1])
    check()
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
    """).format(
        table=sql.Identifier(table_name),
        cred_1=sql.Identifier(fields),
        data_1=sql.Literal(data)
    )
    return stmt
