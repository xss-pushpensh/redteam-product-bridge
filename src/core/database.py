import sqlite3
import os
from contextlib import contextmanager
DB_PATH = os.getenv("DB_PATH", "./data/bridge.db")

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
