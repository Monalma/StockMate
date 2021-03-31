from flask import Flask
from flask import render_template
from flask import request

from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/dashboard/<a>/<b>')
def dashboard(a, b):
   return 'welcome %s %s' % (a,b)

@app.route('/signup',methods = ['POST', 'GET'])
def signup():
   if request.method == 'POST':
      firstName = request.form['firstName']
      lastName = request.form['lastName']
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
      return redirect(url_for('dashboard',a = email, b = password))
   if request.method == 'GET':
      email = request.args.get('email')
      password = request.args.get('password')
      return render_template('login.html')


if __name__ == '__main__':
   app.run(debug = True)