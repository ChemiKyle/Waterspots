
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


@app.route('/', methods=['POST'])
def login():
    user = str(request.form['username'])
    password = str(request.form['password'])
    cur.execute('SELECT * FROM users WHERE name = \'{}\' AND password = \'{}\';'.format(user, password))
    response = cur.fetchone()
    if response != None:
        print(response, 'OK')
        return render_template('entry.html', methods = ['Metals', 'Organics'])
    else:
        print(response, 'not OK')
        flash('Invalid login or password')
        return render_template('login.html')

@app.route('/entry')
def enter_log():
    # conn = sqlite3.connect
    methods = ['Metals', 'Organics']
    return render_template('entry.html', methods = methods)

if __name__ == "__main__":
    app.secret_key = 'bottom text'
    db = sqlite3.connect('db/test.db', check_same_thread=False)
    cur = db.cursor()
    app.run(debug=True)
