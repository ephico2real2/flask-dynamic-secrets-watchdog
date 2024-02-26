# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends procps default-mysql-client curl lsof \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && \
    chmod +x run-flask.sh

# Make port 3000 available to the world outside this container
EXPOSE 3000 8000

# Set environment variable for Flask and secrets directory
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=3000
# Setting the SECRETS_DIRS environment variable
ENV SECRETS_DIRS=/usr/src/app/secrets

# Create a non-root user and switch to it for security
RUN adduser --disabled-password --gecos '' myuser
USER myuser

# Run app.py when the container launches
CMD ["./run-flask.sh"]

