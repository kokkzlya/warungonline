import contextlib
import sqlite3
from flask import Flask


def init_app(app: Flask):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT,
        password TEXT,
        name TEXT,
        role TEXT
    )
    """
    )
    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        name TEXT,
        description TEXT,
        category TEXT,
        price REAL,
        stock INTEGER
    )
    """
    )
    con.commit()
    con.close()

@contextlib.contextmanager
def get_conn():
    conn = sqlite3.connect("database.db")
    try:
        yield conn
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        conn.close()
