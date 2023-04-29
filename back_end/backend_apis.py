# Copyright 2023 Jeanette Villanueva 
import mysql.connector
from mysql.connector import Error  
from flask import Flask, request
from db import db_connect
import uuid
# https://pynative.com/python-mysql-database-connection/#h-how-to-connect-mysql-database-in-python

# create a Flask app 
app = Flask(__name__)   

# Connect to the MySQL database
status, db = db_connect()

#sample folder name 
folder_names = ["Pictures", "Important Info", "Education", "Miscellaneous"]




""" method to upload any file from their drive to the database """
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']  ## will retrieve 'test.rtf'
    filename,type = file.filename.split(".", 1)
    cursor = db.cursor()


    if status == "success" and file is not None:
        # randomly generate ID for doc_id 
        random_uuid = uuid.uuid4()
        random_int = int(random_uuid.int)
        try: 
            sql_query  = "INSERT INTO doc_info (folder_name, doc_id, doc_name, doc_type) VALUES(%s, %s, %s, %s)"
            data = (folder_names[3], random_int, filename, type)
            cursor.execute(sql_query, data)
            db.commit() #commits the insertions
            print("Data successfully added to mysql table: doc_info ")
            status = "success"
        except Error as e:
         print("Error while adding to doc_content", e) 
         status = "failure"

    return status 




"""method to access a particular file from their drive"""
# @app.route('/access', methods=['GET'])
# def access_file():
#     file = request.files['file']

#     my_cursor = db.cursor(buffered= True) 
#     return status



if __name__=="__main__":
    app.run(debug=True)