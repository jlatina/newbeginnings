# Copyright 2023 Jeanette Villanueva 
import mysql.connector
from mysql.connector.errors import Error  
from flask import Flask, request, jsonify
from db import db_connect
#import uuid 
import random 
import datetime 

# https://pynative.com/python-mysql-database-connection/#h-how-to-connect-mysql-database-in-python

# create a Flask app 
app = Flask(__name__)   

# HARDCODED DATA 
folder_names = ["Pictures", "Important Info", "Education", "Miscellaneous"]
table = "doc_info" # hardcoded for now 
username = "jivillan" # hardcoded for now 

""" method to upload any file from their drive to the database """
## need to edit the code so that it gets one of the files retrieved from postman, so it uploads all of them , not just one at a time.
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename, filetype = file.filename.split(".", 1)
    folder_name = folder_names[3] # hardcoded for now 
    
    # MySQL database connection
    status = db_connect()  
    db = mysql.connector.connect(user='root', host='localhost', database='fy_app_db')
    cursor = db.cursor(buffered=True) 
    
    if (status == "success" and file is not None):
        # randomly generate ID for doc_id
        random_int = random.randint(1, 1000)

        print(f'table = {table}')
        if table == "doc_info":
            sql_query = "INSERT INTO fy_app_db.doc_info(folder_name, doc_id, doc_name, doc_type) VALUES(%s, %s, %s, %s)"
            data = (folder_name, random_int, filename, filetype)
        elif table == "doc_drive":
            sql_query = "INSERT INTO fy_app_db.doc_drive(username, folder_name, date_uploaded) VALUES(%s, %s, %s)"
            data = (username, folder_name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        try:
            # Check if the connection is still alive before adding to table
            if not db.is_connected():
                db.reconnect(attempts=3, delay=0)
            else:
                # Execute and commit the inserts into the respective table
                cursor.execute(sql_query, data)
                db.commit() 
                print(f"Data successfully added to table={table}")
                status = "success"

            # If still connected to the database after adding, close it
            if db.is_connected():
                if cursor is not None:
                    cursor.close()
                db.close()
                print("MySQL connection is closed") 

        except Error as e:
            print(f"Error will adding to table ={table}", e) 
            status = "failure"
                   
    return status



"""method to access a particular file from their drive"""
@app.route('/access', methods=['GET'])
def access_file():
   
   #retrieve folder & file name specifed from postman params 
   folder = request.args.get('folder')
   filename = request.args.get('file')


   # MySQL database connection
   status = db_connect()  
   db = mysql.connector.connect(user='root', host='localhost', database='fy_app_db')
   
   # create seperate cursors for the differnt tables
   drive_cursor = db.cursor(buffered=True)
   file_cursor = db.cursor(buffered=True)

   if (status == "success" and filename is not None and folder is not None):
    
    # two different queries based on folder & file name
    folder_query = f"SELECT * FROM fy_app_db.doc_drive WHERE folder_name='{folder}'"
    file_query = f"SELECT * FROM fy_app_db.doc_info WHERE folder_name='{folder}'AND doc_name='{filename}'"
   
    try:
        # Check if the connection is still alive before adding to table
        if not db.is_connected():
            db.reconnect(attempts=3, delay=0)
        else:
            # execute queries 
            drive_cursor.execute(folder_query)
            folder_status = drive_cursor.fetchall() 
            file_cursor.execute(file_query) 
            file_status = file_cursor.fetchall()
            status = "success" 
            overall_status = folder_status + file_status

        if overall_status is not None:
                # print the info contained in the rows doc_info since
                for row in file_status: 
                    print(f"row = {row} from doc_info table")

        if db.is_connected():
                if (file_cursor is not None and drive_cursor is not None):
                    drive_cursor.close()
                    file_cursor.close()
                db.close()
                print("MySQL connection is closed") 
    except Error as e:
        print(f"Error will adding to table ={table}", e) 
        status = "failure"   

   return status

def main():
    #result = upload_file()
    result = access_file()
    print(f"result = {result}")
if __name__=="__main__":
  # main()
   app.run()