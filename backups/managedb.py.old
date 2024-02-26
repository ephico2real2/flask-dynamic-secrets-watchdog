# managedb.py
import os
import sys
import time
import mysql.connector
from mysql.connector import Error

def initialize_database(app):
    db_config = {
        'host': app.config['DATABASE_HOST'],
        'user': app.config['DATABASE_USER'],
        'password': app.config['DATABASE_PASSWORD'],
        'database': app.config['DATABASE_NAME'],
    }

    max_retries = 5
    wait_seconds = 10
    connected = False

    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect to the database. Attempt {attempt + 1} of {max_retries}")
            # Connect to MySQL server
            cnx = mysql.connector.connect(**db_config)
            cursor = cnx.cursor()
            print("Database connection successful.")
            connected = True
            
            # Path to your SQL script
            script_path = os.path.join(os.path.dirname(__file__), 'db', 'quotes-init.sql')
            
            # Open and execute the SQL file
            with open(script_path, 'r') as file:
                sql_script = file.read()
            for statement in sql_script.split(';'):
                if statement.strip():
                    try:
                        cursor.execute(statement)
                        cnx.commit()
                    except mysql.connector.Error as err:
                        print(f"Failed executing statement:\n{statement}\nError: {err}")
            
            cursor.close()
            cnx.close()
            break  # Break the loop if connection and script execution are successful
        except Error as err:
            print(f"Connection attempt failed: {err}")
            time.sleep(wait_seconds)  # Wait before retrying

    if not connected:
        print("Failed to connect to the database after several attempts.")
