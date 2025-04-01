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
folder_names = ["Pictures", "Important Info", "Education", "Poems"]
table = "doc_info" # hardcoded for now 
username = "jivillan" # hardcoded for now 

schema_1 = "doc_drive_schema"
schema_2 = "doc_info_schema"
schema_3 = "user_schema"

""" method to upload any file from their drive to the database """
## need to edit the code so that it gets one of the files retrieved from postman, so it uploads all of them , not just one at a time.
@app.route('/upload', methods=['POST'])
def upload_file():

    # Check if there's a file provided or not 
    if 'file' not in request.files:
        return jsonify({"status": "failure", "message": "No file provided"}), 400
    

    file = request.files['file']
    filename, filetype = file.filename.rsplit(".", 1)
    folder_name = folder_names[3] # hardcoded for now 
    
    # status = db_connect()  

    try:
         # MySQL database connection
        db = mysql.connector.connect(user='root', host='localhost')
        cursor = db.cursor(buffered=True) 

        # Ensure the connection is alive
        if not db.is_connected():
            db.reconnect(attempts=3, delay=0)

    # if (status == "success" and file is not None):
    
        if table == "doc_info":
            sql_query = f"""
            INSERT INTO {schema_2}.doc_info (folder_name, doc_name, doc_type) 
            VALUES (%s, %s, %s)"""
            data = (folder_name, filename, filetype) # doc_id is auto-increment
        elif table == "doc_drive":
            sql_query = f"""
            INSERT INTO {schema_1}.doc_drive (username, folder_name, date_uploaded) 
            VALUES (%s, %s, %s)"""
            data = (username, folder_name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

        cursor.execute(sql_query, data)
        db.commit() 

        # ✅ Check if rows were affected (i.e., the insert was successful)
        if cursor.rowcount > 0:
            return jsonify({
                "status": "success", 
                "message": f"File uploaded successfully into {table} table"
                })
        else:
            return jsonify({
                "status": "failure", 
                "message": "No rows affected, file may not have been inserted"
                }), 500

    except Error as e:
        return jsonify({"status": "failure", "error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

"""method to access a particular file from their drive"""
@app.route('/access', methods=['GET'])
def access_file():
    # Retrieve folder & file name specified from Postman params
    folder = request.args.get('folder')
    filename = request.args.get('file')
    
    # Check if there's a folder or file provided
    if not folder or not filename:
        return jsonify({
            "status": "failure",
              "message": "Missing folder or file parameter"
              }), 400
    
    try:
        # MySQL database connection
        db = mysql.connector.connect(user='root', host='localhost')
        cursor = db.cursor(dictionary=True)  # Use dictionary=True for JSON serialization

        # Ensure the connection is alive
        if not db.is_connected():
            db.reconnect(attempts=3, delay=0)

        # Two different queries based on folder & file name
        folder_query = f"SELECT * FROM {schema_1}.doc_drive WHERE folder_name=%s"
        file_query = f"SELECT * FROM {schema_2}.doc_info WHERE folder_name=%s AND doc_name=%s"
        
        # Execute queries for both tables
        cursor.execute(folder_query, (folder,))
        folder_status = cursor.fetchall()
        
        cursor.execute(file_query, (folder, filename))
        file_status = cursor.fetchall()
        
        # Separate responses for each query
        if folder_status:
            folder_response = {"status": "success", "data": folder_status}
        else:
            folder_response = {"status": "failure", "message": "Folder not found in doc_drive"}

        if file_status:
            file_response = {"status": "success", "data": file_status}
        else:
            file_response = {"status": "failure", "message": "File not found in doc_info"}

        # Return both responses
        return jsonify({
            "folder_status": folder_response,
            "file_status": file_response
        }), 200

    except Error as e:
        return jsonify({"status": "failure", "error": str(e)}), 500
    
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def main():
    #result = upload_file()
    result = access_file()
    print(f"result = {result}")
if __name__=="__main__":
  # main()
   app.run()
