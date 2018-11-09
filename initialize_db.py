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
    study_name TEXT NOT NULL,
    pH FLOAT,
    TDS FLOAT,
    Temperature FLOAT,
    Turbidity FLOAT,
    TOC FLOAT,
    Hardness FLOAT,
    Alkalinity Float,
    timestamp DATETIME,
    notes TEXT
    );"""
    
    c.execute(observations_sql)
    
    studies_sql = """CREATE TABLE IF NOT EXISTS studies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    standard TEXT NOT NULL,
    test TEXT NOT NULL,
    study_name TEXT NOT NULL
    );"""
    
    c.execute(studies_sql)


init_db()

def populate_methods():
    conn = sqlite3.connect('db/test.db')
    c = conn.cursor()

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
                      'Turbidity': 'NTU',
                      'Hardness': 'ppm',
                      'Alkalinity': 'ppm'}
    for test in dict:
        print(dict[test])
        for param in dict[test]:
            c.execute(sql, [test, param, dict[test][param]])
    conn.commit()

# populate_methods()

