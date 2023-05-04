# Copyright 2023 Jeanette Villanueva  
#from sample_data import *
import mysql.connector
from mysql.connector.errors import Error  
from flask import Flask, request, jsonify, make_response
from db import db_connect
import datetime
import jwt 

# create a Flask app 
app = Flask(__name__)   

@app.route('/login', methods=['POST'])
def login():

    # MySQL database connection
    status = db_connect()  
    db = mysql.connector.connect(user='root', host='localhost', database='fy_app_db')
    cursor = db.cursor(buffered=True) 
   
    if (status == "success"):

        users = request.json.get('users')
        
        # grab all the user data from Postman 
        for user_data in users:
            # get user input from request body 
            user_name = user_data.get('user_name')
            pwd = user_data.get('pwd')
            
            # check if the length of the user_name and password is valid to what is specified in mysql db
            if ((len(user_name) and len(pwd)) <= 100):
        
                # check if user exists in the database
                cursor.execute("SELECT * FROM fy_app_db.users WHERE username = %s", (user_name,))
                user = cursor.fetchone()

                # create new user if user does not exist in the database
                if user is None:
                    insert_sql = ("INSERT INTO users (username, pwd, first_login) VALUES (%s, %s,%s)")
                    user_data = (user_name, pwd, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                    cursor.execute(insert_sql, user_data)
                    db.commit()
                else:
                    # check if password is correct
                    if user[2] != pwd:
                        return make_response(jsonify({'message': 'Invalid password'}), 401)

                # authentication 
                # generate JWT token for each user 
                token_payload = {'user_name': user_name, 'pwd': pwd, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)}
                token = jwt.encode(token_payload, 'mysecretkey', algorithm='HS256')

                # return JWT token as HTTP-only cookie
                response = make_response(jsonify({'message': 'Login successful'}), 200)
                response.set_cookie('access_token', token, httponly=True)

         # If still connected to the database after adding, close it
        if db.is_connected():
            if cursor is not None:
                cursor.close()
                db.close()
                print("MySQL connection is closed")    
    else:
        status =  "not connected"
    
    return status 


if __name__ == '__main__':
    app.run()