Got it. Here’s the updated `run.sh` script to use `flask run`:

### New `run.sh` Script

```bash
#!/bin/bash

# Check if the SSH_KEY environment variable is set
if [ -z "$SSH_KEY" ]; then
  echo "SSH_KEY environment variable is not set. Exiting."
  exit 1
fi

# Write the SSH key to a file
echo "$SSH_KEY" > /root/.ssh/id_rsa
chmod 600 /root/.ssh/id_rsa

# Clone private repository or perform tasks requiring SSH access
# Replace 'your-private-repo.git' with the actual repository URL
git clone git@github.com:your-private-repo.git /app/private-repo

# Start the Flask application
flask run --host=0.0.0.0 --port=5000
```

### Complete Dockerfile

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install required dependencies
RUN apt-get update && \
    apt-get install -y git openssh-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create the .ssh directory
RUN mkdir -p /root/.ssh

# Add GitHub to known hosts to avoid SSH prompt
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the run.sh script to the container
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

# Expose port 5000
EXPOSE 5000

# Run the run.sh script
CMD ["/app/run.sh"]
```

### Build and Run the Docker Image

1. **Build the Docker Image**:

   ```bash
   docker build -t python-flask-app .
   ```

2. **Run the Docker Container**: Run the container and pass the SSH key as an environment variable.

   ```bash
   docker run -p 5000:5000 -e SSH_KEY="$(cat ~/.ssh/id_rsa)" python-flask-app
   ```

### Explanation

- **Dockerfile**:
  - Installs necessary dependencies (`git`, `openssh-client`).
  - Creates the `.ssh` directory.
  - Adds GitHub to the known hosts during the build process using `ssh-keyscan`.
  - Copies the application files and the `run.sh` script.
  - Installs Python dependencies specified in `requirements.txt`.
  - Exposes port 5000 for the Flask application.
  - Sets the `run.sh` script as the entry point.

- **run.sh**:
  - Checks if the `SSH_KEY` environment variable is set.
  - Creates the SSH key file from the environment variable and sets the necessary permissions.
  - Clones a private repository using the SSH key.
  - Starts the Flask application using `flask run` to bind to all interfaces (`0.0.0.0`) on port 5000.

This setup ensures that your Flask application is started correctly using `flask run`, making it accessible on port 5000.
