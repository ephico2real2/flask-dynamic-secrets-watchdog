# app.py
import os
from flask import Flask, render_template, jsonify, redirect, url_for
import requests
import mysql.connector
from config import Config
# Import the initialize_database function
from managedb import initialize_database

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database with the app's config
with app.app_context():
    initialize_database(app)

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

@app.route('/quotes')
def redirect_to_api_quotes():
    return redirect(url_for('quotes_api'))

@app.route('/api/quotes', endpoint='quotes_api')
def quotes_api():
    try:
        response = requests.get('https://api.quotable.io/random')
        data = response.json()
        quote = data['content']
        author = data['author']

        # Connect to the database
        db_config = {
            'host': app.config['DATABASE_HOST'],
            'user': app.config['DATABASE_USER'],
            'password': app.config['DATABASE_PASSWORD'],
            'database': app.config['DATABASE_NAME'],
        }
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insert the fetched quote into the database
        insert_query = "INSERT INTO quotes (quote, author) VALUES (%s, %s)"
        cursor.execute(insert_query, (quote, author))
        connection.commit()

        # Close the connection
        cursor.close()
        connection.close()

        return jsonify({'quote': quote, 'author': author})
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500
    except mysql.connector.Error as err:
        return jsonify({'error': 'Database error: ' + str(err)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=3000)
