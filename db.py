import uuid
import sqlite3
from sqlite3 import Error
from rich import print
from datetime import datetime
from pathlib import Path

def get_module_path():
    return Path(__file__).parent

def generate_id():
    return str(uuid.uuid4())

def init(db):
    """create a database connection to a SQLite database"""
    mod_path = get_module_path()
    try:
        conn = sqlite3.connect(
                mod_path/db, 
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        return conn
    except Error as e:
        print(e)

def execute(conn, sql, values=None):
    """
    Given connection, query and values execute.
    """
    cur = conn.cursor()
    if values:
        cur.execute(sql, values)
    else:
        cur.execute(sql)

    conn.commit()

    return cur

def create_event_table(conn):
    sql = ''' 
        CREATE TABLE IF NOT EXISTS events (
            id   TEXT PRIMARY KEY,
            name TEXT    NOT NULL,
            start TIMESTAMP NOT NULL,
            end TIMESTAMP NOT NULL,
            interval INTEGER NOT NULL
        );
    '''
    result = execute(conn, sql)

def add_event(conn, event):
    sql = '''
        INSERT INTO events(id, name, start, end, interval)
        VALUES(?, ?, ?, ?, ?)
    '''

    result = execute(conn, sql, event)

def get_row(cursor):
    return next(cursor, [None])

def get_event(conn, id_):
    sql = f"SELECT * from events where id = '{id_}'"
    cur = execute(conn, sql)
    event = get_row(cur)
    return event


if __name__ == "__main__":
    conn = init("./countdown.db")
    create_event_table(conn)

    # start = datetime.now()
    # end = datetime(year=2022, month=5, day=24)
    # add_event(conn, (generate_id(), 'task2', start, end, 1))
    event = get_event(conn, 'a9831f9e-7820-4a8d-8e5e-a2b78e182828')
    print(event)

