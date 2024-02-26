# app.py
import os
import sys
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

        db_config = {
            'host': app.config['DATABASE_HOST'],
            'user': app.config['DATABASE_USER'],
            'password': app.config['DATABASE_PASSWORD'],
            'database': app.config['DATABASE_NAME'],
        }
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check if the quote already exists
        select_query = "SELECT COUNT(*) FROM quotes WHERE quote = %s"
        cursor.execute(select_query, (quote,))
        if cursor.fetchone()[0] == 0:
            # The quote doesn't exist, insert it into the database
            insert_query = "INSERT INTO quotes (quote, author) VALUES (%s, %s)"
            cursor.execute(insert_query, (quote, author))
            connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'quote': quote, 'author': author})
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500
    except mysql.connector.Error as err:
        return jsonify({'error': 'Database error: ' + str(err)}), 500


@app.route('/api/quotes/duplicates')
def show_duplicates():
    db_config = {
        'host': app.config['DATABASE_HOST'],
        'user': app.config['DATABASE_USER'],
        'password': app.config['DATABASE_PASSWORD'],
        'database': app.config['DATABASE_NAME'],
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Find duplicates
    cursor.execute("""
        SELECT quote, COUNT(quote) as cnt
        FROM quotes
        GROUP BY quote
        HAVING cnt > 1
    """)
    duplicates = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify([{'quote': quote, 'count': count} for quote, count in duplicates])

@app.route('/api/quotes/duplicates/delete', methods=['POST'])
def delete_duplicates():
    db_config = {
        'host': app.config['DATABASE_HOST'],
        'user': app.config['DATABASE_USER'],
        'password': app.config['DATABASE_PASSWORD'],
        'database': app.config['DATABASE_NAME'],
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Delete duplicates, keeping the quote with the lowest id
    cursor.execute("""
        DELETE q1 FROM quotes q1
        INNER JOIN quotes q2 
        WHERE 
            q1.id > q2.id AND 
            q1.quote = q2.quote
    """)
    connection.commit()

    affected_rows = cursor.rowcount

    cursor.close()
    connection.close()

    return jsonify({'message': f'Deleted {affected_rows} duplicate quotes'})




if __name__ == "__main__":
    app.run(debug=True, port=3000)
