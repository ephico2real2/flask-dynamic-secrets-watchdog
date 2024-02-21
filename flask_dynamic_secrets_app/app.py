# app.py
import os
from flask import Flask, render_template
import mysql.connector
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    db_config = {
        'host': app.config['DATABASE_HOST'],
        'user': app.config['DATABASE_USER'],
        'password': app.config['DATABASE_PASSWORD'],
        'database': app.config['DATABASE_NAME'],
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT quote, author FROM quotes")  # Adjusted to match your table schema
    quotes = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', quotes=quotes)


if __name__ == "__main__":
    app.run(debug=True, port=3000)
