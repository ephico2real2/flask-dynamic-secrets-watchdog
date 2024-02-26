Creating a README for running the Flask app with Docker Compose:

### Setting Up and Running with Docker Compose

#### Prerequisites

- Docker
- Docker Compose

Ensure Docker and Docker Compose are installed on your system. You can verify the installations by running `docker --version` and `docker-compose --version`.

#### Step 1: Clone Repository

First, clone the repository to your local machine and navigate into the project directory:

```bash
git clone https://github.com/ephico2real2/flask-dynamic-secrets-watchdog.git
cd flask-dynamic-secrets-watchdog && ls -al
cd ./flask_dynamic_secrets_app
```


#### Step 2: Create Secrets

Before starting the Docker containers, create a `./secrets` directory in the project root ("flask_dynamic_secrets_app" - folder) and populate it with your MySQL secrets. This directory will be mounted into the Docker container to configure the Flask app:

```bash
mkdir -p ./secrets
echo "db" > ./secrets/MYSQL_HOSTNAME
echo "root" > ./secrets/MYSQL_USERNAME
echo "london123" > ./secrets/MYSQL_PASSWORD
echo "quotes" > ./secrets/MYSQL_DB
echo "3306" > ./secrets/MYSQL_PORT
```

#### Step 3: Run Docker Compose

Use Docker Compose to build and start the containers specified in your `docker-compose.yml` file. The `--build` flag ensures that Docker images are built or rebuilt if necessary:

```bash
docker-compose up --build
```

This command starts all the services defined in your `docker-compose.yml` file. By default, Docker Compose looks for a file named `docker-compose.yml` in the current directory.

#### Step 4: Access the Application

With the containers running, you can access the Flask application by navigating to `http://localhost:3000` in your web browser.

#### Interacting with the Container

If you need to execute commands inside a running container, use the `docker exec` command. For example, to open a shell session inside your Flask app's container:

```bash
docker exec -it <container_name_or_id> /bin/sh
```

You can find the container name or ID by listing all running containers with `docker ps`. For a service named `app` in `docker-compose.yml`, the container name is usually prefixed with the project directory name, such as `flask_dynamic_secrets_app-app-1`. Adjust the container name accordingly based on your `docker ps` output.

Example:

```bash
docker exec -it flask_dynamic_secrets_app-app-1 /bin/sh
```

This command opens an interactive shell (`/bin/sh`) inside the specified container, allowing you to run commands directly inside the container environment.

### Stopping Containers

To stop and remove all running containers defined in your `docker-compose.yml` file, run:

```bash
docker-compose down
```

This command stops all services, removes the containers, and networks created by `docker-compose up`.

## Interacting with the Flask Application Endpoints

This document explains how to access and interact with the metrics and health check endpoints of our Flask application, as well as how to invoke the API to delete duplicate quotes.

### Accessing Metrics

The `/metrics` endpoint exposes various metrics of the Flask application, suitable for scraping by Prometheus.

#### Using a Browser
To view the metrics, navigate to:
```
http://localhost:3000/metrics
```

#### Using Curl
To fetch the metrics using `curl`:
```sh
curl http://localhost:3000/metrics
```

### Checking Application Health

The `/health` endpoint provides information about the health of the application and its connection to the database.

#### Using a Browser
To check the application health, navigate to:
```
http://localhost:3000/health
```

#### Using Curl
To fetch the health status using `curl`:
```sh
curl http://localhost:3000/health
```

### Deleting Duplicate Quotes

The application provides an API endpoint to delete duplicate quotes from the database. This can help clean up any redundant entries.

#### Using Curl
To invoke the API to delete duplicate quotes, use the following `curl` command:
```sh
curl -X POST http://localhost:3000/api/quotes/duplicates/delete
```

This command sends a POST request to the endpoint responsible for deleting duplicate quotes. On successful deletion, the API will return a message indicating the number of quotes deleted and instruct the client to reload the page if necessary.

### Notes
- The `/metrics` and `/health` endpoints are meant for monitoring and health-checking purposes and provide valuable insights into the application's performance and status.
- The delete duplicates API (`/api/quotes/duplicates/delete`) is a utility endpoint to help maintain the integrity of the data in the application. It's a POST request to ensure deliberate invocation.
