from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import time
from werkzeug.utils import redirect
import logging
import socket

app = Flask(__name__)
hostname = socket.gethostname()
IPaddr = socket.gethostbyname(hostname)
logging.basicConfig(filename='log.log', encoding='utf-8')
details = ('Visitor: ', hostname, 'IP Address: ', IPaddr)
logging.error(details)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'toor'
app.config['MYSQL_DB'] = 'metset'

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("index.html")



@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password =%s', (email,password))
        account=cursor.fetchone()
        
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            msg = 'Logged in succesfully'
            time.sleep(1)
            return redirect('/')
        else:
            msg='Incorrect email/password'
    return render_template('login.html', msg=msg)

@app.route('/register', methods=['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'email' in request.form and 'password' in request.form:
       firstname = request.form['firstname']
       lastname = request.form['lastname']
       email = request.form['email']
       password = request.form['password']
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute('SELECT * FROM accounts WHERE email = %s', (email,))
       account = cursor.fetchone()

       if account:
        msg = 'Email already exists. Please Login.'
       elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        msg = 'Invalid email address'
       elif not firstname or not email or not lastname or not password:
           msg='Please fill in all the details.'
       else:
           cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (firstname, lastname, email, password))
           mysql.connection.commit()
           msg = 'Registration successful.'
    
    elif request.method == 'POST':
        msg='Registration Incomplete!'

    return render_template('register.html', msg=msg)
if __name__ == "__main__":
    app.run(debug=True)