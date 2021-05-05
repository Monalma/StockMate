from flask import Flask
from flask import render_template
from flask import request
from flask import Flask, redirect, url_for, request
from flask import Flask,render_template, request
from flask_mysqldb import MySQL
from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,request,redirect,flash
import mysql.connector

import connection_info
app = Flask(__name__)

cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
mysql = MySQL(app)
cursor = cnx.cursor()

@app.route('/dashboard/<a>/')
def dashboard(a):
   if request.method == 'GET':
      emailID = a
      query = "select stockID, stockAmount, stockValue from userTransaction WHERE userAccountID = %s LIMIT 2;"
      print(query, a)
      cursor.execute(query, (a,))
      allInfo = cursor.fetchall()
      table = "<html><head><meta charset=\"UTF-8\"><meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>Stockmate</title><link rel=\"stylesheet\" href=\"/static/styles.css\"><title>Document</title><link rel=\"stylesheet\" href=\"https://use.fontawesome.com/releases/v5.6.1/css/all.css\"></head><body>"
      table += """<div class="header">
    <h2 class="logo">StockMate</h2>
    <input type="checkbox" id="chk">
    <label for="chk" class="show-menu-btn">
      <i class="fas fa-ellipsis-h"></i>
    </label>

    <ul class="menu">
      <a href = "http://localhost:5000/dashboard/"""+ a + """/">Dashboard</a>
      <a href=" """ + "http://localhost:5000/stocks/" + a + "/" + """ ">Stocks</a>
      <a href=" """ + "http://localhost:5000/transactions/" + a + "/"  +""" ">Transactions</a>
      <a href=" """ + "http://localhost:5000/watchlists/" + a + "/" +""" ">Watch Lists</a>
      <a href=" """ + "http://localhost:5000/friends/" + a + "/" +""" ">Friends</a>
      <a href=" """ + "http://localhost:5000/profile/" + a + "/" + """ ">Profile</a>
      <a href=" """ + "http://localhost:5000/login" + "" + """ ">Logout</a>
      <label for="chk" class="hide-menu-btn">
        <i class="fas fa-times"></i>
      </label>
    </ul>
  </div><br></br>"""
      print("Printing the length")
      print(allInfo)
      if allInfo == []:
         table += "<h1 class=\"stock_text\">You have no stock information!</h1></body></html>"
         return table
      table += "<h1 class=\"stock_text\">Your Recent Stocks</h1><table id=\"customers\">"
      table += " <tr> <th> Stock ID </th> <th> Stock Amount </th>  <th> Stock Value</th> "
      for i in allInfo:
         stock_id = i[0]
         stockAmount = i[1]
         stockValue = i[2]
         table += " <tr> <td>" + str(stock_id) + " </td> <td>" +str(stockAmount)+"</td> <td>" +str(stockValue)+ "</tr>"
      table += "</table>"
      table += "<br></br><h1 class=\"stock_text\">Your Lists</h1>"
      table += """<h1 class=\"stock_text\">Your Statistics</h1><br></br>Total Gain/Loss: """
      
      args = (a, (0, 'CHAR'), (0, 'CHAR'))
      result_args = cursor.callproc('GetNetAnalytics', args)
      table += str(result_args[1]) + "$<br></br>"
      table += "Percentage Gain/Loss: " + str((float(result_args[1])/float(result_args[2])) * 100) + "%<br></br>"
      args2 = (a, (0, 'CHAR'), (0, 'CHAR'), (0, 'CHAR'))
      result_args2 = cursor.callproc('GetTheBestStock', args2)
      table += "Most Profitable Stock: " + result_args2[1] + "<br></br>"
      table += "Price you bought " + result_args2[1] + " at: " + result_args2[2] + "$<br></br>"
      table += "Price of " + result_args2[1] + " right now: " + result_args2[3] + "$<br></br>"
      table += "</body> </html>"
      return table
   # else
   #    return 'welcome %s %s' % (a,b)

@app.route('/signup',methods = ['POST', 'GET'])
def signup():
   if request.method == 'POST':
      firstName = request.form['firstName']
      lastName = request.form['lastName']
      email = request.form['email']
      password = request.form['password']
      query = "INSERT INTO user (emailID, firstName, lastName, password) VALUES (%s, %s, %s, %s);"
      print(query, (email, firstName, lastName, password))
      cursor.execute(query, (email, firstName, lastName, password,))
      cnx.commit()
      return redirect(url_for('login'))
   if request.method == 'GET':
      firstName = request.args.get('firstName')
      lastName = request.args.get('lastName')
      return render_template('signup.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']
      query = "SELECT COUNT(*) FROM user U WHERE U.emailID = %s AND U.password = %s;"
      cursor.execute(query, (email, password) )
      result = cursor.fetchall()
      print((result[0])[0])
      if (result[0])[0] == 1:
         return redirect(url_for('dashboard',a = email))
      else:
         print("Wrong User Name or Password!\n")
         return render_template('login.html')

   if request.method == 'GET':

      email = request.args.get('email')
      password = request.args.get('password')
      return render_template('login.html')

@app.route('/stocks/<a>/')
def stocks(a):
   if request.method == 'GET':
      query = "select stockID, stockAmount, stockValue from userTransaction WHERE userAccountID = %s;"
      print(query, a)
      cursor.execute(query, (a,))
      allInfo = cursor.fetchall()
      table = "<html><head><meta charset=\"UTF-8\"><meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>Stockmate</title><link rel=\"stylesheet\" href=\"/static/styles.css\"><title>Document</title><link rel=\"stylesheet\" href=\"https://use.fontawesome.com/releases/v5.6.1/css/all.css\"></head><body>"
      table += """<div class="header">
    <h2 class="logo">StockMate</h2>
    <input type="checkbox" id="chk">
    <label for="chk" class="show-menu-btn">
      <i class="fas fa-ellipsis-h"></i>
    </label>

    <ul class="menu">
      <a href = "http://localhost:5000/dashboard/"""+ a + """/">Dashboard</a>
      <a href=" """ + "http://localhost:5000/stocks/" + a + "/" + """ ">Stocks</a>
      <a href=" """ + "http://localhost:5000/transactions/" + a + "/"  +""" ">Transactions</a>
      <a href=" """ + "http://localhost:5000/watchlists/" + a + "/" +""" ">Watch Lists</a>
      <a href=" """ + "http://localhost:5000/friends/" + a + "/" +""" ">Friends</a>
      <a href=" """ + "http://localhost:5000/profile/" + a + "/" + """ ">Profile</a>
      <a href=" """ + "http://localhost:5000/login" + "" + """ ">Logout</a>
      <label for="chk" class="hide-menu-btn">
        <i class="fas fa-times"></i>
      </label>
    </ul>
  </div><br></br>"""
   table += """<h1 class=\"stock_text\">Trending Stocks</h1><br></br>"""
   cursor.execute("SELECT * FROM stock ORDER BY `stock id` LIMIT 0 , 30")

   allInfo = cursor.fetchall()

   for i in allInfo:
      print(i)

   table += "<table id=\"customers\">"
   table += " <tr> <th> Stock ID </th> <th> Price </th>  <th> Company</th> <th> Trade</th><th> Last Updated</th></th>"
   for i in allInfo:
      stock_id = i[0]
      stock_price = i[1]
      company = i[2]
      trade = i[3]
      last_updated = i[4]
      table += " <tr> <td>" + str(stock_id) + " </td> <td>" +str(stock_price)+"</td> <td>" +str(company)+ "</td> <td>" +str(trade)+ "</td> <td>" + str(last_updated) +"</td> </tr>"


   table += "</table></body> </html>"
   return table

@app.route('/transactions/<a>/',methods = ['POST', 'GET'])
def transactions(a):
   if request.method == 'GET':
      table = "<html><head><meta charset=\"UTF-8\"><meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>Stockmate</title><link rel=\"stylesheet\" href=\"/static/styles.css\"><title>Document</title><link rel=\"stylesheet\" href=\"https://use.fontawesome.com/releases/v5.6.1/css/all.css\"></head><body>"
      table += """<div class="header">
    <h2 class="logo">StockMate</h2>
    <input type="checkbox" id="chk">
    <label for="chk" class="show-menu-btn">
      <i class="fas fa-ellipsis-h"></i>
    </label>

    <ul class="menu">
      <a href = "http://localhost:5000/dashboard/"""+ a + """/">Dashboard</a>
      <a href=" """ + "http://localhost:5000/stocks/" + a + "/" + """ ">Stocks</a>
      <a href=" """ + "http://localhost:5000/transactions/" + a + "/"  +""" ">Transactions</a>
      <a href=" """ + "http://localhost:5000/watchlists/" + a + "/" +""" ">Watch Lists</a>
      <a href=" """ + "http://localhost:5000/friends/" + a + "/" +""" ">Friends</a>
      <a href=" """ + "http://localhost:5000/profile/" + a + "/" + """ ">Profile</a>
      <a href=" """ + "http://localhost:5000/login" + "" + """ ">Logout</a>
      <label for="chk" class="hide-menu-btn">
        <i class="fas fa-times"></i>
      </label>
    </ul>
      </div><br></br>"""

      query = "select transactionID, stockID, stockAmount, stockValue from userTransaction WHERE userAccountID = %s;"
      print(query, a)
      cursor.execute(query, (a,))
      allInfo = cursor.fetchall()
      if allInfo == []:
            table += "<h1 class=\"stock_text\">You have no transactions!</h1><br></br>"
      else:
         table += """<h1 class=\"stock_text\">Your Transactions</h1><br></br>"""
         table += "<table id=\"customers\">"
         table += " <tr><th> Transaction ID </th> <th> Stock ID </th> <th> Stock Amount </th>  <th> Stock Value</th> "
         for i in allInfo:
            transactionID = i[0]
            stock_id = i[1]
            stockAmount = i[2]
            stockValue = i[3]
            table += " <tr><td>" + str(transactionID) + " </td> <td>" + str(stock_id) + " </td> <td>" +str(stockAmount)+"</td> <td>" +str(stockValue)+ "</tr>"
         table += "</table><br></br>"
      stocksQuery = "SELECT `Stock ID` FROM stock LIMIT 100;"
      cursor.execute(stocksQuery)
      stocksResult = cursor.fetchall()
      table += """<h1 class=\"stock_text\">Add a transaction here</h1>"""
      table += """<form action = "http://localhost:5000/transactions/"""+ a + """/" method = "post">    
      <div class="">
         <div class="">
               <select class="li_txt_box" id="stockID" name = "stockID" > """
      for i in stocksResult:
         # print(i[0])
         table += """<option value =\"""" + i[0] + "\">" + i[0] + "</option>"
      table += """</select><br></br>
               <input class="li_txt_box" id="stockAmount" name = "stockAmount"type="text" placeholder="stockAmount"><br></br>
               <input class="li_txt_box" id="stockValue" name = "stockValue"type="text" placeholder="stockValue"><br></br>
         </div>
      </div>
      """
      table += """<h1 class=\"stock_text\">Remove a transaction here</h1><br></br>"""
      table += """<input class="li_txt_box" id="transaction" name = "transaction"type="text" placeholder="transactionID"><br></br>"""
      table += """<button type = "submit" value = "Submit" id="li_but"><a style="color: white; text-decoration: none;">Submit</a></button>"""
      table += """</form> """
      table += "</body> </html>"
      stockID = request.args.get('stockID')
      stockAmount = request.args.get('stockAmount')
      stockValue = request.args.get('stockValue')
      transaction = request.args.get('transaction')
      return table
   if request.method == 'POST':
      stockID = request.form['stockID']
      stockAmount = request.form['stockAmount']
      stockValue = request.form['stockValue']
      transaction = request.form['transaction']
      if stockAmount != "" and stockValue != "" and stockValue != "":
         print("stockAmount Empty!")
         getNextTransaction = "SELECT MAX(transactionID) FROM userTransaction;"
         cursor.execute(getNextTransaction)
         getNextTrans = cursor.fetchall()
         getNext = int((getNextTrans[0])[0]) + 1
         transactionID = str(getNext)
         print("The new transaction ID is")
         print(transactionID)
         insertQuery = "INSERT INTO userTransaction (transactionID, stockID, stockAmount, stockValue, userAccountID, type) VALUES (%s, %s, %s, %s, %s, %s)"
         cursor.execute(insertQuery, (transactionID, stockID, stockAmount, stockValue, a, "1"))
         cnx.commit()
      if transaction != "":
         removeQuery = "DELETE FROM userTransaction WHERE userAccountID = %s AND transactionID = %s;"
         print(removeQuery, (a, transaction))
         cursor.execute(removeQuery, (a, transaction,))
         cnx.commit()
      print("The trasactions details are")
      print(stockID)
      print(stockAmount)
      print(stockValue)
      print(transaction)
      return redirect(url_for('transactions', a = a))

if __name__ == '__main__':
   app.run(debug = True)