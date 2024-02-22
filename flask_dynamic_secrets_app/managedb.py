# managedb.py
import os
import mysql.connector

def initialize_database(app):
    db_config = {
        'host': app.config['DATABASE_HOST'],
        'user': app.config['DATABASE_USER'],
        'password': app.config['DATABASE_PASSWORD'],
        'database': app.config['DATABASE_NAME'],
    }

    # Connect to MySQL server
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    # Path to your SQL script
    script_path = os.path.join(os.path.dirname(__file__), 'db', 'quotes-init.sql')

    # Open and execute the SQL file
    with open(script_path, 'r') as file:
        sql_script = file.read()
    for statement in sql_script.split(';'):
        if statement.strip():
            try:
                cursor.execute(statement)
            except mysql.connector.Error as err:
                print(f"Failed executing statement:\n{statement}\nError: {err}")

    cnx.commit()
    cursor.close()
    cnx.close()
