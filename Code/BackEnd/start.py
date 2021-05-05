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
         table += " <tr> <td>" + str(stock_id) + " </td> <td>" +str(stockAmount)+"</td> <td>" + "$" + str(stockValue)+ "</tr>"
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
   cursor.execute("SELECT * FROM stock ORDER BY Price LIMIT 0 , 30")

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

@app.route('/watchlists/<a>/', methods = ['POST', 'GET'])
def watchlists(a):
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

      totalTables = "select listName, listID from watchList where userAccountID = %s;"
      cursor.execute(totalTables, (a,))
      allInfo = cursor.fetchall()
      if allInfo == []:
            table += "<h1 class=\"stock_text\">You have no watchlists, please add one!</h1><br></br>"
      else:
         totalLists = len(allInfo)
         while totalLists > 0:
            # print(allInfo)
            currList = allInfo[len(allInfo) - totalLists][0]
            tickID = allInfo[len(allInfo) - totalLists][1]
            # currList = currList[2 : -1]
            # tickID = tickID[2 : -1]
            # print("TICKER ID = " + str(tickID))
            query = """Select s.stockID, s.Price, s.lastUpdated, s.companyName, s.Exchange, w.isFav
                        From watchList w, listedStock ls, stock s
                        Where w.userAccountID = %s and ls.listID = w.listID and w.listID = """ + str(tickID) + """ and ls.StockID = s.stockID;"""
            cursor.execute(query, (a,))
            valToPutInTable = cursor.fetchall()
            if (valToPutInTable == []):
               totalLists -= 1
               continue
            if valToPutInTable[0][5] == True:
               table += """<h1 class=\"stock_text\">List Favourited: """ + str(currList) + """</h1><br></br>"""
            else:
               table += """<h1 class=\"stock_text\">""" + str(currList) + """</h1><br></br>"""
            table += "<table id=\"watchList\">"
            table += " <tr><th> Stock Ticker </th> <th> Price </th> <th> Last Updated </th>  <th> Company Name</th> <th> Exchange</th> "
            for i in valToPutInTable:
               stock_id = i[0]
               stockValue = i[1]
               lastUpdatedVal = i[2]
               companyNameVal = i[3]
               exchangeVal = i[4]
               table += " <tr><td>" + str(stock_id) + " </td> <td>" + str(stockValue) + " </td> <td>" +str(lastUpdatedVal)+"</td> <td>" +str(companyNameVal)+ "</td> <td>" + str(exchangeVal)+ "</tr>"
            table += "</table><br></br>"

            totalLists -= 1

      table += """<h1 class=\"stock_text\">Create a new list here</h1>"""
      table += """<form action = "http://localhost:5000/watchlists/"""+ a + """/" method = "post">    
      <div class="">
         <div class="">"""
      table += """<input class="li_txt_box" id="listNameNewList" name = "listNameNewList"type="text" placeholder="List Name"><br></br>
               <label for="isFavourite">Is the Stock meant to be Favourited?</label>
               <select name="isFavouriteNewList" id="isFavouriteNewList">
                  <option value="unknown">Please Select an option</option>
                  <option value="true">True</option>
                  <option value="false">False</option>
               </select>
               <br><br>
               <label for="isPublic">Is the Stock meant for Public?</label>
               <select name="isPublicNewList" id="isPublicNewList">
                  <option value="unknown">Please Select an option</option>
                  <option value="true">True</option>
                  <option value="false">False</option>
               </select>
               <br><br>
         </div>
      </div>
      """
      # table += """<button type = "submit" value = "Submit" id="li_but"><a style="color: white; text-decoration: none;">Submit</a></button>"""

      stocksQuery = "SELECT `stockID` FROM stock LIMIT 250;"
      cursor.execute(stocksQuery)
      stocksResult = cursor.fetchall()
      

      table += """<h1 class=\"stock_text\">Add to a list here</h1>"""
      table += """<div class="">
         <div class="">
               <select class="li_txt_box" id="stockIDAddList" name = "stockIDAddList" > 
               <option value="unknown">Please select a stock ticker ID</option>
               """
      for i in stocksResult:
         table += """<option value =\"""" + i[0] + "\">" + i[0] + "</option>"
      table += """</select><br></br>
               <select class="li_txt_box" id="listIDAddList" name = "listIDAddList" >
               <option value="unknown">Please select a List</option>"""
      for i in allInfo:
         table += """<option value =\"""" + i[1] + "\">" + i[0] + "</option>"
      table += """ </select><br></br>
         </div>
      </div>
      """

      table += """<div class="">
         <div class="">
       """
      table += """<h1 class=\"stock_text\">Update a List </h1><br></br>
      <select class="li_txt_box" id="stockIDUpdate" name = "stockIDUpdate" >
      <option value="unknown">Please select a List</option>"""
      
      for i in allInfo:
         table += """<option value =\"""" + i[1] + "\">" + i[0] + "</option>"
      table += """</select><br></br>
               <input class="li_txt_box" id="listNameUpdate" name = "listNameUpdate"type="text" placeholder="Change List Name"><br></br>
               <label for="isFavourite">Is the Stock meant to be Favourited?</label>
               <select name="isFavouriteUpdate" id="isFavouriteUpdate">
                  <option value="unknown">Please Select an option</option>
                  <option value="true">True</option>
                  <option value="false">False</option>
               </select>
               <br><br>
               <label for="isPublic">Is the Stock meant for Public?</label>
               <select name="isPublicUpdate" id="isPublicUpdate">
                  <option value="unknown">Please Select an option</option>
                  <option value="true">True</option>
                  <option value="false">False</option>
               </select>
               <br><br>
               </div>
      </div>
      """
      table += """<div class="">
         <div class="">
       """
      table += """<h1 class=\"stock_text\">Delete Contents in list </h1><br></br>
      <select class="li_txt_box" id="stockIDModify" name = "stockIDModify" >
      <option value="unknown">Please select a List</option>"""
      
      for i in allInfo:
         table += """<option value =\"""" + i[1] + "\">" + i[0] + "</option>"
      table += """</select><br></br>
               <input class="li_txt_box" id="listNameModify" name = "listNameModify"type="text" placeholder="Enter Stock Ticker ID you want to delete"><br></br>
               <label for="Do you want to Delete the Entire List?">Do you want to Delete the Entire List?</label>
               <select name="isDeleteModify" id="isDeleteModify">
                  <option value="unkown">Please Select an option</option>
                  <option value="false">No</option>
                  <option value="true">Yes</option>
               </select>
               <br><br>
               </div>
      </div>
      """
      table += """<button type = "submit" value = "Submit" id="li_but"><a style="color: white; text-decoration: none;">Submit</a></button>"""
      table += """</form> """
      table += "</body> </html>"
      return table
   if request.method == 'POST':

      #Create New List
      newListArr = []
      listNameNewList = request.form['listNameNewList']
      if listNameNewList == "":
         listNameNewList = "unknown"
      isFavouriteNewList = request.form['isFavouriteNewList']
      isPublicNewList = request.form['isPublicNewList']
      newListArr.append(str(listNameNewList))
      newListArr.append(str(isFavouriteNewList))
      newListArr.append(str(isPublicNewList))
      print("New List Arr = " + str(newListArr))
      if "unknown" not in newListArr:
         getNextTransaction = "SELECT MAX(listID) FROM watchList;"
         cursor.execute(getNextTransaction)
         getNextTrans = cursor.fetchall()
         getNext = int((getNextTrans[0])[0]) + 1
         transactionID = str(getNext)
         query = """Insert into watchList values(%s, %s, %s, %s, %s)"""
         favInt = 0
         if (isFavouriteNewList.lower() == "true"):
            favInt = 1
         publicInt = 0
         if (isPublicNewList.lower() == "true"):
            publicInt = 1
         cursor.execute(query, (transactionID, listNameNewList, publicInt, favInt, a))
         cnx.commit()  

      #Add To List
      addListArr = []
      stockIDAddList = request.form['stockIDAddList']
      listIDAddList = request.form['listIDAddList']
      addListArr.append(str(stockIDAddList))
      addListArr.append(str(listIDAddList))
      print("addListArr = " + str(addListArr))
      if "unknown" not in addListArr:
         query = """Insert into listedStock values(%s, %s)"""
         cursor.execute(query, (listIDAddList, stockIDAddList))
         cnx.commit() 

      #Update A List
      updateListArr = []
      stockIDUpdate = request.form['stockIDUpdate']
      listNameUpdate = request.form['listNameUpdate']
      if listNameUpdate == "":
         listNameUpdate = "unknown"
      isFavouriteUpdate = request.form['isFavouriteUpdate']
      isPublicUpdate = request.form['isPublicUpdate']
      updateListArr.append(str(stockIDUpdate))
      updateListArr.append(str(listNameUpdate))
      updateListArr.append(str(isFavouriteUpdate))
      updateListArr.append(str(isPublicUpdate))
      if "unknown" not in updateListArr:
         query = """update watchList set listName = %s, isPublic = %s, isFav = %s where listID = %s"""
         favInt = 0
         if (isFavouriteUpdate.lower() == "true"):
            favInt = 1
         publicInt = 0
         if (isPublicUpdate.lower() == "true"):
            publicInt = 1
         cursor.execute(query, (listNameUpdate, publicInt, favInt, stockIDUpdate))
         cnx.commit() 

      print("Update List Arr = " + str(updateListArr))

      #Modify
      modifyListArr = []
      stockIDModify = request.form['stockIDModify']
      listNameModify = request.form['listNameModify'] # Textbox
      isDeleteModify = request.form['isDeleteModify']
      modifyListArr.append(str(stockIDModify))
      modifyListArr.append(str(listNameModify))
      modifyListArr.append(str(isDeleteModify))
      print("modify List = " + str(modifyListArr))
      if "unknown" not in modifyListArr:
         if isDeleteModify.lower() == "false" and listNameModify == "":
            listNameModify = "unknown"
         else:
            if isDeleteModify.lower() == "true":
               query = """delete from watchList WHERE listID = %s;"""
               cursor.execute(query, (stockIDModify,))
               query = """delete from listedStock WHERE listID = %s;"""
               cursor.execute(query, (stockIDModify,))
               cnx.commit()
            else:
               query = """delete from listedStock WHERE stockID = %s;"""
               cursor.execute(query, (listNameModify,))
               cnx.commit()
            
      return redirect(url_for('watchlists', a = a))

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
      stocksQuery = "SELECT `stockID` FROM stock LIMIT 100;"
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

@app.route('/friends/<a>/',methods = ['POST', 'GET'])
def friends(a):
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

      query = """SELECT friendAccountID, firstName, LastName FROM userFriends JOIN user ON friendAccountID = emailID WHERE userAccountID = %s;"""
      print(query, a)
      cursor.execute(query, (a,))
      allInfo = cursor.fetchall()
      if allInfo == []:
            table += "<h1 class=\"stock_text\">You do not have any friends on StockMate yet!</h1><br></br>"
      else:
         table += """<h1 class=\"stock_text\">Your Friends</h1><br></br>"""
         table += "<table id=\"customers\">"
         table += " <tr><th>FriendID</th><th> Name </th> <th>Net Gain/Loss</th> <th> Net Gain/Loss % </th> "
         for i in allInfo:
            friendAccountID = i[0]
            firstName = i[1]
            lastName = i[2]
            args = (friendAccountID, (0, 'CHAR'), (0, 'CHAR'))
            result_args = cursor.callproc('GetNetAnalytics', args)
            perc = str((float(result_args[1])/float(result_args[2])) * 100) + "%"
            table += " <tr><td>" + friendAccountID + "</td><td>" + str(firstName) + " " + str(lastName) + " </td> <td>" + str(result_args[1]) + "$ </td> <td>" + perc + "</tr>"
         table += "</table><br></br>"
      table += """<h1 class=\"stock_text\">Add a friend here</h1>"""
      table += """<form action = "http://localhost:5000/friends/"""+ a + """/" method = "post">    
      <div class="">
         <div class="">
               <input class="li_txt_box" id="friendIDAdd" name = "friendIDAdd"type="text" placeholder="friendID"><br></br>
         </div>
      </div>
      """
      table += """<h1 class=\"stock_text\">Remove a friend here</h1><br></br>"""
      table += """<input class="li_txt_box" id="friendIDRemove" name = "friendIDRemove"type="text" placeholder="friendID"><br></br>"""
      table += """<button type = "submit" value = "Submit" id="li_but"><a style="color: white; text-decoration: none;">Submit</a></button>"""
      table += """</form> """
      table += "</body> </html>"
      friendIDAdd = request.args.get('friendIDAdd')
      friendIDRemove = request.args.get('friendIDRemove')
      return table
   if request.method == 'POST':
      friendIDAdd = request.form['friendIDAdd']
      friendIDRemove = request.form['friendIDRemove']
      if friendIDAdd != "":
         print("FriendID Empty!")
         addFriendQuery = "INSERT INTO userFriends VALUES(%s, %s);"
         cursor.execute(addFriendQuery, (friendIDAdd, a))
         cursor.execute(addFriendQuery, (a, friendIDAdd))
         cnx.commit()

      if friendIDRemove != "":
         removeFriendQuery = "DELETE FROM userFriends WHERE userAccountID = %s AND friendAccountID = %s;"
         print(removeFriendQuery, (friendIDRemove, a))
         cursor.execute(removeFriendQuery, (friendIDRemove, a))
         cursor.execute(removeFriendQuery, (a, friendIDRemove))
         cnx.commit()
      print("The trasactions details are")
      print(friendIDAdd)
      print(friendIDRemove)
      return redirect(url_for('friends', a = a))

if __name__ == '__main__':
   app.run(debug = True)