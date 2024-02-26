---

# Flask Dynamic Secrets App README

## Overview

This Flask application demonstrates dynamic secret loading and automatic configuration reloads, designed for environments where secrets are rotated frequently. It can reload its configuration in response to changes in secrets without requiring a restart, ensuring minimal downtime and enhanced security.

## Components

### app.py

- **Description**: This is the main Flask application file. It defines web routes, views, and logic for handling web requests and responses. It serves as the entry point for running the Flask web server.
- **Related Components**: Interacts with `config.py` for application settings, `secrets_loader.py` for loading secrets, and `managedb.py` for database connection management.

### config.py

- **Description**: Contains configuration settings for the Flask application. It imports settings such as database credentials and secret keys from `secrets_loader.py`, configuring the Flask app settings dynamically.
- **Related Components**: Utilizes `secrets_loader.py` to load secret values into the application's configuration.

### secrets_loader.py

- **Description**: Responsible for loading secret values (e.g., database credentials) from specified directories. It is utilized by `config.py` to inject these secrets into the application's configuration dynamically.
- **Related Components**: Used by `config.py` and indirectly affects `app.py` and `managedb.py` through configuration.

### managedb.py

- **Description**: Contains functions for initializing and reconfiguring the database connection based on loaded secrets. It includes `initialize_database` for setting up the database schema at startup and `reconfigure_database` for dynamically updating database connection settings if secrets change.
- **Related Components**: Called by `app.py` to manage database connections and affected by `secrets_loader.py` through dynamic secret loading.

### flask_secrets_watchdog.py

- **Description**: Implements a watchdog listener that monitors changes to the secrets files. Upon detecting changes, it triggers reloading configurations or reinitializing database connections. It collaborates with `secrets_loader.py` to reload secrets and `managedb.py` for any database reconfiguration needs.
- **Related Components**: Works alongside `app.py` as a separate process, utilizing `secrets_loader.py` for secret reloading and `managedb.py` for database reconfigurations.

### run-flask.sh

- **Description**: A script to start the Flask application and the secrets watchdog simultaneously. It ensures that the application is always running with the latest configuration and secrets by monitoring for changes and triggering reloads as necessary.
- **Related Components**: It is the bootstrap script that integrates `flask_secrets_watchdog.py` with the Flask application, ensuring that the dynamic reloading mechanism is always active.

## Component Interaction Diagram

```bash
                                                        +----------------------+
                                                        |      run-flask.sh    |
                                                        +----------+-----------+
                                                                    |
                                                                    v
                                                        +----------+-----------+
                                    +-----------------+  Flask Application   +-----------------+
                                    |                 +----------+-----------+                 |
                                    |                            |                               |
                                    |                            |                               |
                                    v                            v                               v
                        +--------------+-------+       +------------+------------+       +---------+---------+
                        | secrets_loader.py   |       | flask_secrets_watchdog.py|       |   config.py        |
                        +--------------+-------+       +------------+------------+       +---------+---------+
                                    |                            |                               |
                                    |                            |                               |
                                    v                            v                               v
                            +--------+--------+       +-----------+-----------+         +--------+--------+
                            |   Secrets       |       |  Watch for changes in |         | Load secrets and |
                            | Directory/File  |       |  secrets directory    |         | update app config|
                            +-----------------+       +-----------+-----------+         +------------------+
                                                                    |
                                                                    |
                                                                    v
                                                        +-----------+-----------+
                                                        |   on_secrets_changed() |
                                                        |   function in Flask    |
                                                        |   app triggers reload  |
                                                        +-----------+-----------+
                                                                    |
                                                                    v
                                                        +-----------+-----------+
                                                        | Reload Flask app's    |
                                                        | configuration and     |
                                                        | re-establish database |
                                                        | connection            |
                                                        +-----------------------+

```

## Getting Started

Refer to the initial README sections for detailed setup instructions, including local development setup, Docker Compose usage, accessing the application, health checks, and metrics.

---