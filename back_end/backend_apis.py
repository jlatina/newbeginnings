# Copyright 2023 Jeanette Villanueva 
import mysql.connector
from mysql.connector.errors import Error  
from flask import Flask, request
from db import db_connect
import uuid 
import datetime 

# https://pynative.com/python-mysql-database-connection/#h-how-to-connect-mysql-database-in-python

# create a Flask app 
app = Flask(__name__)   

# HARDCODED DATA 
folder_names = ["Pictures", "Important Info", "Education", "Miscellaneous"]
table = "doc_info" # hardcoded for now 
username = "jivillan" # hardcoded for now 

""" method to upload any file from their drive to the database """
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']  ## will retrieve 'test.rtf'
    filename, type = file.filename.split(".", 1)
    folder_name = folder_names[3] # hardcoded for now 
 
    # MySql Database connections 
    status = db_connect()  
    db = mysql.connector.connect(user='root', host='localhost', database='fy_app_db')
    cursor = db.cursor(buffered=True) 

    if status == "success" and file is not None:
        # randomly generate ID for doc_id 
        random_uuid = uuid.uuid4()
        random_int = int(random_uuid.int)
        print(f'table = {table}')
        if table == "doc_info":
            sql_query = "INSERT INTO fy_app_db.{table}(folder_name, doc_id, doc_name, doc_type) VALUES(%s, %s, %s, %s)"
            data = (folder_name, random_int, filename, type)
        elif table == "doc_drive":
            sql_query = "INSERT INTO fy_app_db.{table}(username, foldername, date_uploaded) VALUES(%s, %s, %s)"
            data = (username, folder_name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        else:
            try:
                # close the connection & cursor bc you are no longer uploading     
                if db.is_connected():
                    if cursor is not None:
                        cursor.close()
                        db.close()
                        print("MySQL connection is closed") 

                # Check if the connection is still alive
                if not db.is_connected():
                    db.reconnect(attempts=3, delay=0)
                else:
                    # Execute & commit the inserts into the prospective table 
                    cursor.execute(sql_query, data)
                    db.commit() 
                    print(f"Data successfully added to database={db.database}")
                    status = "success"
                
            except Error as e:
                print("Error while adding to doc_info", e) 
                status = "failure"
        
            finally:
                if db.is_connected():
                    if cursor is not None:
                        cursor.close()
                        db.close()
                        print("MySQL connection is closed") 
    return status



"""method to access a particular file from their drive"""
# @app.route('/access', methods=['GET'])
# def access_file():
#     file = request.files['file']

#     my_cursor = db.cursor(buffered= True) 
#     return status

# def main():
#     result = upload_file()
#     print(f"result = {result}")
if __name__=="__main__":
  # main()
   app.run()