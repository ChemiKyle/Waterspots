
__author__      = "Kyle Chesney"

from flask import *
from flask_login import LoginManager
# TODO: Research SQLAlchemy vs raw SQL
#from flask_sqlalchemy import SQLAlchemy
# TODO: MariaDB vs PostgreSQL, re: audit trail
import sqlite3
from datetime import datetime as dt

app = Flask(__name__)
login = LoginManager(app)
#db = SQLAlchemy()

@app.route('/')
def home():
#    if current_user.is_authenticated:
    return render_template('login.html')
#    if not session.get('logged_in'):
#        return render_template('login.html')


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print('login')
        user = str(request.form['username'])
        password = str(request.form['password'])
        cur.execute("SELECT * FROM users WHERE name = ? AND password = ?;", [user, password])
        response = cur.fetchone()
        if response != None:
            print(response, 'OK')
            return redirect(url_for('entry_type'))
        else:
            print(response, 'not OK')
            flash('Invalid login or password')
    return render_template('login.html')



# Getting here should be GET so users can bookmark data entry
@app.route('/entry_type', methods=['POST', 'GET'])
def entry_type():
    if request.method == 'POST':
        test_type = request.form['test_method']
        session['method'] = test_type
        print(str(test_type))
        return redirect(url_for('enter_test_point'))
        # conn = sqlite3.connect
    methods = ['Metals', 'Organics']
    return render_template('select_method.html', methods = methods)


@app.route('/entry', methods=['POST', 'GET'])
def enter_test_point():
    meth = session['method']
    print(meth)
    sql = """SELECT name, param, units FROM test_methods WHERE name = ?"""
    print(cur.execute(sql, str(meth)))
    if request.method == 'POST':
        dict = {}
        dict['study'] = 'test'
        dict['timestamp'] = dt.now()
        for item, val in request.form.items():
            dict[item] =  val
        print(dict)
        # TODO: pick parameters based on test method
        sql = """INSERT INTO observations (study, pH, TDS, Turbidity, Temperature, timestamp, notes)
        VALUES(?,?,?,?,?,?,?)"""
        cur.execute(sql, tuple(dict[k] for k in dict.keys()))
        db.commit()
    # TODO: parameters load from a db for every test method
    parameters = ['study', 'pH', 'TDS', 'Turbidity', 'Temperature', 'notes']
    return render_template('make_entry.html', parameters = parameters)


if __name__ == "__main__":
    app.secret_key = 'bottom text'
    db = sqlite3.connect('db/test.db', check_same_thread=False)
    cur = db.cursor()
    app.run(debug=True, host = '0.0.0.0')
