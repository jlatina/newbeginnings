import mysql.connector
from mysql.connector import Error  


"""method to connect to data base 
    return connection_status: whether or not the user was able to succesfully connect 
     status_code = "success"
     status_code = "failure"
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
            status_code = "success" 

    except Error as e:
        print("Error while connecting to MySQL", e)
        status_code = "failure"
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()
   # print(f"db_connect() returning status_code={status_code} and connection={connection}")
    return status_code

def main():
    result = db_connect()
    print(result)
if __name__=="__main__":
    main()   