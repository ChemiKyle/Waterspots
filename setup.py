import sqlite3

def init_db():
    conn = sqlite3.connect('db/test.db')
    c = conn.cursor()

    user_sql = """CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    password text NOT NULL
    );"""

    c.execute(user_sql)

    methods_sql = """CREATE TABLE IF NOT EXISTS test_methods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    params text NOT NULL
    );"""

    c.execute(methods_sql)

    observations_sql = """CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    study TEXT NOT NULL,
    pH FLOAT,
    TDS FLOAT,
    Temperature FLOAT,
    Turbidity FLOAT,
    timestamp DATETIME
    );"""

    c.execute(observations_sql)

init_db()
