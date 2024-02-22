#!/bin/bash

# Ensure the script exits on any error
set -e

# Function to kill all background processes upon exiting
cleanup() {
    echo "Stopping all processes..."
    pkill -P $$
    echo "All processes stopped."
}

# Trap SIGINT (Ctrl+C) and SIGTERM signals and cleanup before exiting
trap cleanup SIGINT SIGTERM

# Define the paths to your secrets directories as an environment variable
export SECRETS_DIRS="${SECRETS_DIRS:-./secrets}"

echo "Starting Flask secrets watchdog..."
python flask_secrets_watchdog.py &

echo "Starting Flask application with Gunicorn..."
# Adjust the number of workers, threads, and port as necessary
gunicorn --log-level info --bind :3000 app:app &

# Wait for any process to exit
wait

# Perform cleanup
cleanup