## Phase 2



Sure! Let's update the `run.sh` script to set the `FLASK_APP`, `FLASK_RUN_HOST`, and `FLASK_RUN_PORT` environment variables before running the Flask application.

### Updated `run.sh` Script

```bash
#!/bin/bash

# Set environment variables
export TEMPLATE_REPO_DIR=service_configurator_templates
export FLASK_APP=app.py
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=5000

# Check if the SSH_KEY environment variable is set
if [ -z "$SSH_KEY" ]; then
  echo "SSH_KEY environment variable is not set. Exiting."
  exit 1
fi

# Write the SSH key to a file
echo "$SSH_KEY" > /root/.ssh/id_rsa
chmod 600 /root/.ssh/id_rsa

# Check if GitHub's SSH key is already in known_hosts
if ! grep -q "github.com" /root/.ssh/known_hosts; then
  echo "GitHub SSH key not found in known_hosts. Scanning and adding it."
  ssh-keyscan github.com >> /root/.ssh/known_hosts
else
  echo "GitHub SSH key already in known_hosts."
fi

# Check if the REPO_URL environment variable is set
if [ -z "$REPO_URL" ]; then
  echo "REPO_URL environment variable is not set. Exiting."
  exit 1
fi

# Clone private repository or perform tasks requiring SSH access
if git clone $REPO_URL /service_configurator_app/${TEMPLATE_REPO_DIR}; then
  echo "Repository cloned successfully."
else
  echo "Failed to clone repository. Exiting."
  exit 1
fi

# Change to the cloned repository directory
cd /service_configurator_app/${TEMPLATE_REPO_DIR}

# Start the Flask application
flask run
```

### Updated Dockerfile (for reference)

```Dockerfile
# syntax=docker/dockerfile:1

# Use the official Ubuntu image as the base image
FROM ubuntu:22.04

# Set the working directory inside the container
WORKDIR /service_configurator_app

# Set environment variables
ENV FLASK_APP=app.py
ENV TZ=Europe/London
ENV TERM=xterm
ENV TEMPLATE_REPO_DIR=service_configurator_templates

# Install tzdata and configure it non-interactively
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    apt-get update && \
    apt-get install -y tzdata && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean

# Install system dependencies and Python
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3.10-distutils \
    curl \
    software-properties-common \
    gcc \
    libblas-dev \
    libatlas-base-dev \
    libsasl2-dev \
    nano \
    python3-pip \
    python3-setuptools \
    python3-venv \
    python3-wheel \
    tzdata \
    zlib1g-dev \
    libssl-dev \
    mysql-client \
    default-libmysqlclient-dev \
    xmlsec1 \
    git \
    openssh-client \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

# Set up default Python version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 && \
    update-alternatives --set python /usr/bin/python3.10

# Create the .ssh and log directory
RUN mkdir -p /root/.ssh && \
    mkdir -p /opt/python/log

# Add GitHub to known hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

# Copy all files from the current directory to the working directory in the container
COPY . /service_configurator_app

# Install Python dependencies from requirements.txt
RUN if [ -f requirements.txt ]; then \
       python3 -m pip install --no-cache-dir -r requirements.txt; \
    fi

# Copy the run.sh script to the container
COPY run.sh /service_configurator_app/run.sh
RUN chmod +x /service_configurator_app/run.sh

# Open port for access to the application outside the container
EXPOSE 5000

# Command to run the application
# Run the run.sh script
CMD ["/service_configurator_app/run.sh"]
```

### Build and Run the Docker Image

1. **Build the Docker Image**:

   ```bash
   docker build -t python-flask-app .
   ```

2. **Run the Docker Container**: Pass the SSH key and the repository URL as environment variables.

   ```bash
   docker run -p 5000:5000 -e SSH_KEY="$(cat ~/.ssh/id_rsa)" -e REPO_URL=git@github.com:your-private-repo.git python-flask-app
   ```

### Explanation

- **run.sh**:
  - Sets the `TEMPLATE_REPO_DIR`, `FLASK_APP`, `FLASK_RUN_HOST`, and `FLASK_RUN_PORT` environment variables.
  - Checks if the `SSH_KEY` environment variable is set.
  - Creates the SSH key file from the environment variable and sets the necessary permissions.
  - Checks if GitHub's SSH key is already present in the `known_hosts` file. If not, it scans and adds it.
  - Checks if the `REPO_URL` environment variable is set.
  - Clones the private repository using the `REPO_URL` environment variable.
  - Changes the directory to the cloned repository.
  - Starts the Flask application using `flask run`.

This setup ensures that all necessary environment variables are set, and the GitHub SSH key is checked and added only if it does not already exist, reducing unnecessary network operations.
#########




## Phase 1
I apologize for the misunderstanding. I'll adjust the Dockerfile to correctly handle the `requirements.txt` in the `service_configurator_app` directory.

### Updated Dockerfile

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install required dependencies
RUN apt-get update && \
    apt-get install -y git openssh-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create the .ssh directory and log directory
RUN mkdir -p /root/.ssh && mkdir -p /opt/python/log

# Add GitHub to known hosts to avoid SSH prompt
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

# Define build arguments
ARG SSH_KEY
ARG REPO_URL

# Use the build arguments
RUN if [ -n "$SSH_KEY" ]; then \
        echo "$SSH_KEY" > /root/.ssh/id_rsa && \
        chmod 600 /root/.ssh/id_rsa; \
    fi

RUN if [ -n "$REPO_URL" ]; then \
        git clone $REPO_URL /service_configurator_app/private-repo; \
    fi

# Set the working directory
WORKDIR /service_configurator_app

# Copy the current directory contents into the container at /service_configurator_app
COPY . /service_configurator_app

# Install any needed packages specified in requirements.txt
RUN if [ -f requirements.txt ]; then \
        pip install --no-cache-dir -r requirements.txt; \
    fi

# Copy the run.sh script to the container
COPY run.sh /service_configurator_app/run.sh
RUN chmod +x /service_configurator_app/run.sh

# Expose port 5000
EXPOSE 5000

# Run the run.sh script
CMD ["/service_configurator_app/run.sh"]
```

### Updated `run.sh` Script

```bash
#!/bin/bash

# Start the Flask application
cd /service_configurator_app/private-repo
flask run --host=0.0.0.0 --port=5000
```

### Build and Run the Docker Image

1. **Build the Docker Image**: Pass the SSH key and the repository URL as build arguments.

   ```bash
   docker build --build-arg SSH_KEY="$(cat ~/.ssh/id_rsa)" --build-arg REPO_URL=git@github.com:your-private-repo.git -t python-flask-app .
   ```

2. **Run the Docker Container**:

   ```bash
   docker run -p 5000:5000 python-flask-app
   ```

### Explanation

- **Dockerfile**:
  - Installs necessary dependencies (`git`, `openssh-client`).
  - Creates the `.ssh` directory and the log directory `/opt/python/log`.
  - Adds GitHub to known hosts during the build process using `ssh-keyscan`.
  - Accepts `SSH_KEY` and `REPO_URL` as build arguments.
  - Uses these arguments to create the SSH key file and clone the private repository, if provided.
  - Sets the working directory to `service_configurator_app`.
  - Copies the application files and the `run.sh` script to the working directory.
  - Installs Python dependencies specified in `requirements.txt` located in the working directory.
  - Exposes port 5000 for the Flask application.
  - Sets the `run.sh` script as the entry point.

- **run.sh**:
  - Changes the directory to the cloned repository.
  - Starts the Flask application using `flask run` to bind to all interfaces (`0.0.0.0`) on port 5000.

This setup ensures that the necessary directories are created, and the application is set up correctly with the specified working directory and log directory.

###########







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



Certainly! Here is the revised JIRA story without the sub-tasks and with the role specified as a DevOps Engineer:

---

**JIRA Story**

**Issue Type**: `Story`

**Summary**: `Containerize Flask Application with Git Integration and Dynamic SSH Key Handling`

**Description**:

As a DevOps Engineer, I want to containerize the Flask application with dynamic SSH key handling and repository cloning, so that the application can securely access private repositories during the build process.

**Acceptance Criteria**:

1. The Dockerfile should:
   - Install necessary dependencies including `git` and `openssh-client`.
   - Create required directories (`/root/.ssh` and `/opt/python/log`).
   - Add GitHub to known hosts.
   - Accept `SSH_KEY` and `REPO_URL` as build arguments.
   - Use the `SSH_KEY` argument to create an SSH key file.
   - Clone the specified repository using the `REPO_URL` argument, if provided.
   - Set the working directory to `service_configurator_app`.
   - Copy application files to the working directory.
   - Install Python dependencies from `requirements.txt` in the working directory.
   - Expose port 5000.
   - Set `run.sh` as the entry point.

2. The `run.sh` script should:
   - Change the directory to the cloned repository.
   - Start the Flask application using `flask run` to bind to all interfaces (`0.0.0.0`) on port 5000.

**Tasks**:
- [ ] Create a Dockerfile that meets the specified criteria.
- [ ] Create a `run.sh` script that starts the Flask application.
- [ ] Test the Dockerfile and `run.sh` script to ensure the application runs correctly.
- [ ] Document the build and run process.

---
