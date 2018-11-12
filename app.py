
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

# TODO: create a home page
@app.route('/home', methods=['POST', 'GET'])
def home():
#    if current_user.is_authenticated:
    studies_sql = """SELECT study_name FROM studies;"""
    studies = cur.execute(studies_sql).fetchall()
    if request.method == 'POST':
        dest = str(request.form['destination'])
        session['study'] = str(request.form['study'])
        return redirect(url_for(dest))
    return render_template('homepage.html', studies = studies)
#    if not session.get('logged_in'):
#        return render_template('login.html')

@app.route('/calculations')
def calculations():
    return render_template('chem_calcs.html')

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
            return redirect(url_for('home'))
        else:
            print(response, 'not OK')
            flash('Invalid login or password')
    return render_template('login.html')

@app.route('/enter_new_study', methods=['POST','GET'])
def enter_new_study():
    standards_sql = """SELECT DISTINCT standard FROM standard_water_parameters;"""
    standards = cur.execute(standards_sql).fetchall()

    # TODO: AJAX
    tests_sql = """SELECT DISTINCT test FROM standard_water_parameters;"""
    tests = cur.execute(tests_sql).fetchall()
    
    analytes_sql = """SELECT DISTINCT analyte from standard_analytes;"""
    analytes = cur.execute(analytes_sql).fetchall()

    if request.method == 'POST':
        entry = {}
        for key, val in request.form.items():
            entry[key] = val
        columns = ", ".join(entry.keys())
        placeholders = ":"+", :".join(entry.keys())
        sql = """INSERT INTO studies ({})
        VALUES({})""".format(columns, placeholders)
        cur.execute(sql, entry)
        db.commit()
    return render_template('enter_new_study.html',
                           standards = standards,
                           tests = tests,
                           analytes = analytes)


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


@app.route('/observation_entry', methods=['POST', 'GET'])
def observation_entry():
    # TODO: change this to AJAX call on this page instead of needing homepage
    test_sql = """SELECT test FROM studies WHERE study_name = ?"""
    test = cur.execute(test_sql, [session['study']]).fetchone()[0]

    sql = """SELECT param, units FROM standard_water_parameters WHERE test = ?"""
    parameters = (cur.execute(sql, [test])).fetchall() # parameters load from a db
    if request.method == 'POST':
        dict = {}
        dict['timestamp'] = dt.now()
        for item, val in request.form.items():
            dict[item] =  val
        print(dict)
        # TODO: pick parameters based on test method
        columns = ", ".join(dict.keys())
        placeholders = ":"+", :".join(dict.keys())
        sql = """INSERT INTO observations ({})
        VALUES({})""".format(columns, placeholders)
        cur.execute(sql, dict)
        db.commit()
    return render_template('make_entry.html', parameters = parameters)


if __name__ == "__main__":
    app.secret_key = 'bottom text'
    db = sqlite3.connect('db/test.db', check_same_thread=False)
    cur = db.cursor()
    app.run(debug=True, host = '0.0.0.0')
