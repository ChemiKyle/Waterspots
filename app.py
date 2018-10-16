
__author__      = "Kyle Chesney"

from flask import *
from flask_login import LoginManager
import sqlite3
from datetime import datetime as dt

app = Flask(__name__)
login = LoginManager(app)


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
    return(user, password)

@app.route('/entry')
def enter_log():
    # conn = sqlite3.connect
    methods = ['Metals', 'Organics']
    return render_template('entry.html', methods = methods)

if __name__ == "__main__":
    app.run(debug=True)
