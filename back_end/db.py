# Copyright 2023 Jeanette Villanueva 
import mysql.connector
from mysql.connector import Error  
from flask import Flask, request
# https://pynative.com/python-mysql-database-connection/#h-how-to-connect-mysql-database-in-python



"""method to connect to data base 
    return connection_status: whether or not the user was able to succesfully connect 
     status_code = 100 : success
     status_code = 400 : failure 
"""

def db_connect():
    connection = None
    try:
        connection = mysql.connector.connect(user = 'root', host='localhost',
                                            database= 'fy_app_db')
        if connection.is_connected():
            mysql_version = connection.get_server_info()
            print("Connected to MySQL Server version ", mysql_version)
            cursor = connection.cursor()
            cursor.execute("select database();")
            db_name = cursor.fetchone()
            print("You're connected to database: ", db_name)
            status_code = 100 

    except Error as e:
        print("Error while connecting to MySQL", e)
        status_code = 400
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

    return (status_code,connection)         

# Connect to the MySQL database
db = db_connect()

# create a Flask app 
app = Flask(__name__)



""" method to upload any file from their drive to the database """
@app.route('/upload', methods=['POST'])
def upload_file():
    status = "failed"
    file = request.files['file']

    return status 




"""method to access a particular file from their drive"""
@app.route('/upload', methods=['GET'])
def access_file():
    status = "file does not exist"
    file = request.files['file']

    my_cursor = db.cursor(buffered= True) 
    return status



def main():
    result = db_connect()
    print(result)
if __name__=="__main__":
    main()
    app.run(debug=True)