#!/bin/bash

# Define the project directory name
PROJECT_DIR="flask_dynamic_secrets_app"

# Create the project directory and subdirectories
mkdir -p $PROJECT_DIR/templates

# Navigate into the project directory
cd $PROJECT_DIR

# Create Python script files
touch flask_secrets_watchdog.py config.py app.py secrets_loader.py requirements.txt

# Create the HTML template file
touch templates/index.html

# Populate requirements.txt with Flask, mysql-connector-python, and watchdog versions
echo "Flask==2.0.1
mysql-connector-python==8.0.23
watchdog==2.1.2" > requirements.txt

# Populate index.html with a basic HTML structure
echo "<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>Quotes</title>
</head>
<body>
    <h1>Quotes</h1>
    <ul>
        <!-- Quotes will be inserted here -->
    </ul>
</body>
</html>" > templates/index.html

# Provide feedback that the script has finished
echo "Flask application structure initialized in $PROJECT_DIR"

# List the contents of the project directory
echo "Project directory structure:"
tree ../$PROJECT_DIR
