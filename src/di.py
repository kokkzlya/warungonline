import inject
import sqlite3

from db import get_conn

def init_app(app):
    def configure(binder):
        binder.bind_to_provider(sqlite3.Connection, get_conn)
    inject.configure(configure)