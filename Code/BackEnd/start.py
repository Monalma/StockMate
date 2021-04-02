from flask import Flask
from flask import render_template
from flask import request
from flask import Flask, redirect, url_for, request
from flask import Flask,render_template, request
from flask_mysqldb import MySQL
from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

import connection_info
app = Flask(__name__)

cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
mysql = MySQL(app)
cursor = cnx.cursor()

@app.route('/dashboard/<a>/<b>')
def dashboard(a, b):
   return 'welcome %s %s' % (a,b)

@app.route('/signup',methods = ['POST', 'GET'])
def signup():
   if request.method == 'POST':
      firstName = request.form['firstName']
      lastName = request.form['lastName']
      email = request.form['email']
      password = request.form['password']
      query = "INSERT INTO user (emailID, firstName, lastName, password) VALUES ('" + email+"', '"+ firstName +"', '"+lastName +"', '" + password+"');"
      print(query)
      cursor.execute(query)
      cnx.commit()
      # cursor.close()
      # cnx.close()
      return redirect(url_for('dashboard',a = firstName, b = lastName))
   if request.method == 'GET':
      firstName = request.args.get('firstName')
      lastName = request.args.get('lastName')
      return render_template('signup.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']
      query = "SELECT COUNT(*) FROM user U WHERE U.emailID ='" + email + "' AND U.password ='" + password + "';"
      cursor.execute(query)
      result = cursor.fetchall()
      print((result[0])[0])
      if (result[0])[0] == 1:
         return redirect(url_for('dashboard',a = email, b = password))
   if request.method == 'GET':
      email = request.args.get('email')
      password = request.args.get('password')
      return render_template('login.html')


if __name__ == '__main__':
   app.run(debug = True)