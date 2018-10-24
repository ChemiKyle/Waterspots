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
    param text NOT NULL,
    units text
    );"""

    c.execute(methods_sql)

    observations_sql = """CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    study TEXT NOT NULL,
    pH FLOAT,
    TDS FLOAT,
    Temperature FLOAT,
    Turbidity FLOAT,
    TOC FLOAT,
    timestamp DATETIME,
    notes TEXT
    );"""

    c.execute(observations_sql)


init_db()

def populate_methods():
    conn = sqlite3.connect('db/test.db')
    c = conn.cursor()
    sqlite3.conn

    sql = """INSERT INTO test_methods (
    name, param, units)
    VALUES(?,?,?)"""

    tests = ['Organics', 'Metals']
    dict = {}
    dict['Organics'] = {'pH': '',
                        'TDS': 'ppm',
                        'Temperature': 'C',
                        'Turbidity': 'NTU',
                        'TOC': 'ppm'}
    dict['Metals'] = {'pH': '',
                      'TDS': 'ppm',
                      'Temperature':'C',
                      'Turbidity': 'NTU'}
    for test in dict:
        print(dict[test])
        for param in dict[test]:
            c.execute(sql, [test, param, dict[test][param]])
    conn.commit()

# populate_methods()
