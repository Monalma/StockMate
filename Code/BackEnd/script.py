# Submission instructions:
# the skeleton files include Q11.py and connection_info.py
# connection_info.py contains your connection parameters, including your database password.
# Q11.py is where you write your program that generates the HTML report.
# Your code should save the html report in the orders.html file (see code below)
# Submit only your Q11.py in Brightspace.

import mysql.connector

import connection_info

try:
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
except:
    print("Could not connect to SQL database!")
    exit()

finally:
    print("Process executed. Shutting down.")

cursor = cnx.cursor()

cursor.execute("SELECT * FROM stock ORDER BY `stock id` LIMIT 0 , 30")

allInfo = cursor.fetchall()

for i in allInfo:
    print(i)

table = "<html><head><meta charset=\"UTF-8\"><meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>Stockmate</title><link rel=\"stylesheet\" href=\"./styles.css\"><title>Document</title></head><body><table id=\"customers\">"
table += " <tr> <th> Stock ID </th> <th> Price </th>  <th> Company</th> <th> Trade</th><th> Last Updated</th></th>"
for i in allInfo:
    stock_id = i[0]
    stock_price = i[1]
    company = i[2]
    trade = i[3]
    last_updated = i[4]
    table += " <tr> <td>" + str(stock_id) + " </td> <td>" +str(stock_price)+"</td> <td>" +str(company)+ "</td> <td>" +str(trade)+ "</td> <td>" + str(last_updated) +"</td> </tr>"


table += "</table></body> </html>"
f = open("stocks.html", "w")
f.write(table)
f.close()

cursor.close()
cnx.close()
