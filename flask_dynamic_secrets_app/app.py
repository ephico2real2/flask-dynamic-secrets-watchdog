#app.py
import os
import sys
import requests
import logging
import time
from flask import Flask, render_template, jsonify, redirect, url_for, request, abort, Response
import mysql.connector
from mysql.connector import Error
from prometheus_client import Counter, Gauge, Histogram, Summary, start_http_server
import psutil  # For accessing system details, including CPU usage
from config import Config
from managedb import initialize_database, reconfigure_database
from flask import current_app
from contextlib import contextmanager


# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Start Prometheus metrics server on port 8000
start_http_server(8000)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Prometheus metrics
# HTTP request counter
request_count = Counter('http_req_total', 'HTTP Requests Total')

# System memory and CPU usage gauges
memory_usage = Gauge('memory_usage_bytes', 'System Memory Usage')
cpu_usage = Gauge('cpu_usage_percent', 'System CPU Usage Percent')

# Threading metrics
thread_count = Gauge('system_thread_count', 'Number of system threads')
context_switches = Gauge('system_context_switches_total', 'Total number of context switches')

# HTTP request latency histogram and response size summary
request_latency = Histogram('http_request_latency_seconds', 'HTTP request latency in seconds')
response_size = Summary('http_response_size_bytes', 'HTTP response size in bytes')

@contextmanager
def app_context():
    with app.app_context():
        yield

def update_system_metrics():
    """Update system-related metrics, including memory and CPU usage."""
    with app_context():
        memory_usage.set(psutil.virtual_memory().used)
        cpu_usage.set(psutil.cpu_percent())

def update_threading_metrics():
    """Update threading-related metrics."""
    with app_context():
        thread_count.set(psutil.Process().num_threads())
        context_switches.set(psutil.cpu_stats().ctx_switches)

@app.before_request
def before_request_func():
    """Log request details, increment request counter, and start latency measurement."""
    logger.info(f"Received {request.method} request to {request.path} from {request.remote_addr}")
    request.start_time = time.time()
    request_count.inc()

@app.after_request
def after_request_func(response):
    """Log response details, measure and observe request latency and response size."""
    latency = time.time() - request.start_time
    request_latency.observe(latency)
    response_size.observe(len(response.get_data(as_text=True)))
    logger.info(f"Responded to {request.method} request to {request.path} with status {response.status_code}")
    return response


# Initialize the database with the app's config
with app.app_context():
    initialize_database(app)

@app.route('/metrics')
def proxy_metrics():
    # Make a request to the Prometheus metrics server
    response = requests.get('http://localhost:8000/metrics')

    # Return the response content and content type to the client
    return Response(response.content, content_type=response.headers['Content-Type'])

@app.route('/reload-config', methods=['POST'])
def reload_config():
    # Implement security checks here...
    Config.reload()  # Reload the configurations
    app.config.from_object(Config)  # Apply the updated configurations
    reconfigure_database(app)  # Additional step if needed to reconfigure the DB
    return jsonify({'message': 'Configurations reloaded successfully'}), 200

def get_db_connection():
    """Establishes a connection to the database and returns the connection object."""
    try:
        connection = mysql.connector.connect(
            host=app.config['DATABASE_HOST'],
            user=app.config['DATABASE_USER'],
            password=app.config['DATABASE_PASSWORD'],
            database=app.config['DATABASE_NAME'],
        )
        return connection
    except Error as e:
        logger.error(f"Error connecting to the database: {e}")
        sys.exit(1)

@app.route('/health')
def health_check():
    health_status = {'app': {'status': 'running', 'message': 'Application is up and running.'}}

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchall()
            health_status['database'] = {'status': 'connected', 'message': 'Database connection successful.'}
    except Exception as e:
        logger.exception("Failed to connect to the database during health check")  # Log exception with traceback
        health_status['database'] = {'status': 'error', 'message': f'Database connection failed: {e}'}

    health_status['overall'] = 'healthy' if health_status.get('database', {}).get('status') == 'connected' else 'unhealthy'
    overall_status = 200 if health_status['overall'] == 'healthy' else 500

    return jsonify(health_status), overall_status

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT quote, author FROM quotes")
    quotes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', quotes=quotes)

@app.route('/quotes')
def redirect_to_api_quotes():
    return redirect(url_for('quotes_api'))

@app.route('/api/quotes', endpoint='quotes_api')
def quotes_api():
    try:
        response = requests.get('https://api.quotable.io/random')
        data = response.json()
        quote, author = data['content'], data['author']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM quotes WHERE quote = %s", (quote,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO quotes (quote, author) VALUES (%s, %s)", (quote, author))
            conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'quote': quote, 'author': author})
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500
    except Error as err:
        return jsonify({'error': f'Database error: {err}'}), 500

@app.route('/api/quotes/duplicates')
def show_duplicates():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT quote, COUNT(quote) AS cnt
        FROM quotes
        GROUP BY quote
        HAVING cnt > 1
    """)
    duplicates = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{'quote': quote, 'count': count} for quote, count in duplicates])

@app.route('/api/quotes/duplicates/delete', methods=['POST'])
def delete_duplicates():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE q1 FROM quotes q1
        INNER JOIN quotes q2 
        WHERE q1.id > q2.id AND q1.quote = q2.quote
    """)
    affected_rows = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    #return jsonify({'message': f'Deleted {affected_rows} duplicate quotes'})
    return jsonify({'success': True, 'reload': True})

if __name__ == "__main__":
    # Start up the server to expose the metrics.
    app.run(debug=True, port=3000)
