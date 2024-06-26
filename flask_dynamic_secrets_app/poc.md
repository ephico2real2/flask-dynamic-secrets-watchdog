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
