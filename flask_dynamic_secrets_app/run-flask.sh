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
export SECRETS_DIRS="/Users/olasumbo/Downloads/repo/myqsl/local_secrets"

echo "Starting Flask secrets watchdog..."
python flask_secrets_watchdog.py &

echo "Starting Flask application..."
FLASK_APP=app.py FLASK_RUN_PORT=3000 flask run &

# Wait for any process to exit
wait

# Perform cleanup
cleanup
