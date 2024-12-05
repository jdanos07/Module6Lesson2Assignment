
import mysql.connector
from mysql.connector import Error

def connect_database():
    db_name1 = 'gym_db'
    user = 'root'
    password = 'J!strM3str'
    host = 'localhost'

    try:
        connection1 = mysql.connector.connect(
            database = db_name1,
            user = user,
            password = password,
            host = host
        )
      
        print("Connected to MySql")
        return connection1
    
    except Error as e:
        print(f'Error: {e}')
        return None

#connection testing:

#     finally:
#         connection1.close
#         print('Disonnected')

# connect_database()

