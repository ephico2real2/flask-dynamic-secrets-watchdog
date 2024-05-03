### troubleshooting

If `pkill` is giving you trouble, switching to using `kill` to terminate processes can be a more controlled approach, especially when you know the specific process IDs (PIDs) of the processes you want to terminate. Here’s how you can integrate `kill` into your script:

### Using `kill` with Explicit PIDs
To use `kill` effectively, you'll need to track the PIDs of the processes you start in your script. Here’s a step-by-step approach to implementing this:

#### 1. **Store PIDs of Background Processes**
When you start a background process in Bash, you can capture its PID using the special variable `$!`, which holds the PID of the most recently executed background process. Store this PID in a variable or a file for later use.

```bash
startGunicorn() {
    gunicorn app:app &  # Start Gunicorn in the background
    echo $! > /tmp/gunicorn.pid  # Save the PID to a file
}

monitorDatabase() {
    python3 /usr/local/insights-queue/db_connector.py &
    echo $! > /tmp/database_monitor.pid  # Save the PID to a file
}
```

#### 2. **Modify Cleanup Function to Use `kill`**
Use the stored PIDs to terminate the processes in your cleanup function. If you stored the PIDs in files, you can read these files and use `kill` to terminate the processes.

```bash
cleanup() {
    echo "Cleaning up..."

    if [ -f /tmp/gunicorn.pid ]; then
        kill $(cat /tmp/gunicorn.pid) || echo "Failed to kill Gunicorn"
        rm /tmp/gunicorn.pid
    fi

    if [ -f /tmp/database_monitor.pid ]; then
        kill $(cat /tmp/database_monitor.pid) || echo "Failed to kill database monitor"
        rm /tmp/database_monitor.pid
    fi

    echo "All background processes killed."
}
```

#### 3. **Set Up Trap to Call Cleanup**
Ensure your script sets up a trap to call this cleanup function upon exiting or receiving interrupt signals.

```bash
trap cleanup EXIT SIGINT SIGTERM
```

#### 4. **Testing and Debugging**
- **Test your script thoroughly** to ensure that the processes are being started and killed as expected. Look for any errors in the log output when trying to kill the processes.
- **Debugging Tip**: You might want to add more verbose logging to your cleanup function to understand if the PIDs are being read correctly and if `kill` is executing as expected.

### Considerations for Using `kill`
- **Graceful Shutdown**: If you need to shut down services gracefully, consider using specific signals like `SIGTERM` (which `kill` sends by default) or `SIGQUIT`. You can specify the signal before the PID:
  ```bash
  kill -SIGTERM $(cat /tmp/gunicorn.pid)
  ```
- **Handling Missing PIDs**: Make sure your script handles cases where the PID files might not exist (if the processes never started correctly or if they already terminated for some reason).

By following these steps, you should be able to use `kill` effectively to manage the lifecycle of processes in your Bash scripts. This method gives you fine-grained control over which processes are terminated and when, making your script more robust and reliable.


`` ######################### ``

```

step 1: add timestamps to logs :
###########
/bin/echo "$(date '+%Y-%m-%d %H:%M:%S') - Setting up..." | /usr/bin/tee -a "${debugFile}"


##############
step 2: track process to be clean up

trap "cleanup" EXIT

cleanup() {
    echo "Cleaning up..."
    pkill -f monitorDatabase
    pkill -f monitorGunicorn
}

monitorDatabase &
monitorGunicorn
wait

```

`` HEALTH CHECKS ``

```
Using the `pgrep` command in a Bash script to check if a process like Gunicorn is running is a straightforward and effective approach for a liveness probe. This method is commonly used in various system administration tasks to quickly assess whether essential services are active, making it a suitable choice for both manual checks and automated monitoring systems, such as Kubernetes liveness probes.

Here's a detailed breakdown of how your script works and its implications:

```

### Script Explanation


```bash
#!/bin/bash
if pgrep -f 'your_app_process_name' > /dev/null; then
    echo "Process is running."
    exit 0
else
    echo "Process is not running."
    exit 1
fi

```

```
1. **Shebang**: `#!/bin/bash` - This line tells the operating system that this script should be run using Bash, which is the shell interpreter.

2. **Process Check**: `pgrep -f 'your_app_process_name' > /dev/null` - This command uses `pgrep` to search for processes whose command line arguments match the pattern 'your_app_process_name'. The `-f` option is crucial because it makes `pgrep` look at the full command line, not just the command name.

3. **Output Redirection**: `> /dev/null` - Standard output is redirected to `/dev/null`, which is a way to discard any output. This is used here because you're only interested in the exit status of `pgrep`, not the output.

4. **Conditional Execution**:
   - `if` statement evaluates the exit status of `pgrep`.
   - If `pgrep` finds a match (i.e., the process exists), it returns `0` (success), and the script echoes "Process is running." and exits with `0`, indicating success.
   - If `pgrep` does not find a match, it returns a non-zero status, the script echoes "Process is not running." and exits with `1`, indicating failure.

### Usage as a Health Check

You can use this script as part of a health check system in various environments:
- **Direct Monitoring**: Run the script manually or set it up as a cron job to check the process status periodically.
- **Container Orchestration Systems**: In Kubernetes, for example, you could set this script as a liveness probe to ensure your container is restarted if Gunicorn is not running:

```

```yaml
livenessProbe:
  exec:
    command:
    - /path/to/check_gunicorn_script.sh
  initialDelaySeconds: 10
  periodSeconds: 30
```

### Modifications for Gunicorn

To specifically check for a Gunicorn process, you should modify the 'your_app_process_name' placeholder to something more specific that you would expect to find in the Gunicorn command line. For example, if your Gunicorn process runs an app called `app:app`, you might use:

```bash
#!/bin/bash
if pgrep -f 'gunicorn app:app' > /dev/null; then
    echo "Gunicorn process is running."
    exit 0
else
    echo "Gunicorn process is not running."
    exit 1
fi
```

This script is simple yet effective for ensuring that critical components like Gunicorn are operational, and it is very adaptable to different monitoring or orchestration frameworks.

```


`` ####################### ``

```

```bash

#!/bin/bash

# Define global variables...

# Function definitions...

# Main setup function
setup() {
    # Setup directories and files...
}

# Main start function
start() {
    # Log start message...
}

# Function to start Gunicorn
startGunicorn() {
    /bin/echo "Starting Gunicorn..." | /usr/bin/tee -a "${debugFile}"
    cd /usr/local/insights-queue/ || exit
    gunicorn app:app 2>&1 | /usr/bin/tee -a "${debugFile}" &
}

# Continuously monitor database connection
monitorDatabase() {
    while true; do
        /bin/echo "Attempting to connect to MySQL..." | /usr/bin/tee -a "${debugFile}"
        python3 /usr/local/insights-queue/db_connector.py
        local status=$?

        if [ $status -eq 0 ]; then
            /bin/echo "MySQL database connection successful." | /usr/bin/tee -a "${debugFile}"
        else
            /bin/echo "Failed to connect to MySQL database. Retrying in 1 minute..." | /usr/bin/tee -a "${debugFile}"
            pkill -f 'gunicorn app:app'
        fi

        sleep 60  # Sleep for a minute before next check
    done
}

# Continuously monitor Gunicorn server
monitorGunicorn() {
    while true; do
        /bin/echo "Checking for existing gunicorn processes..." | /usr/bin/tee -a "${debugFile}"
        pgrep -f 'gunicorn app:app'
        if [ $? -ne 0 ]; then
            startGunicorn
        fi

        sleep 60  # Sleep for a minute before next check
    done
}

# Start the main setup and start functions
setup
start

# Run the monitoring functions in the background
monitorDatabase &
monitorGunicorn &
```

In this updated script:

- The `monitorDatabase()` function continuously monitors the database connection.
- The `monitorGunicorn()` function continuously monitors the Gunicorn server.
- Both functions are started in the background (`&`) after the setup and start functions.
- Gunicorn is started in the `startGunicorn()` function when the database connection is successful.
- If the database connection fails, the Gunicorn server is stopped using `pkill`.

With these modifications, both the database connection and the Gunicorn server will be continuously monitored in the background, ensuring that Gunicorn is running whenever the database is accessible.


f the database connection starts failing after the application has been running successfully, the behavior will depend on how the script is configured to handle database connection failures.

In the provided script, if the database connection fails during the continuous monitoring process:

### Detection of Database Connection Failure:

- The monitorDatabase() function continuously attempts to connect to the MySQL database using the db_connector.py script.
  If the connection attempt fails, the script logs an error message indicating the failure to connect to the MySQL database.
- Stopping Gunicorn Server:
  Upon detecting a database connection failure, the script stops the Gunicorn server using pkill -f 'gunicorn app:app'.
- Retrying Database Connection:
  The script will continue attempting to reconnect to the database at regular intervals (every minute, as specified by sleep 60).
  Once the database connection is restored and successful (status -eq 0), the script 
  will start the Gunicorn server again using the startGunicorn() function.
- Logging:
  Throughout this process, the script logs relevant messages to the debug file, providing visibility into the status of database connectivity and the actions taken by the script.

```

`` ##################### ``

```python

#db_connector.py

"""
Initial DB connector for when app starts up to ensure the database is accessible before running the app.
"""

# pylint: disable=import-error

import os
import time
import logging
import mysql.connector
from mysql.connector import Error
from secrets_config import SecretConfig

# Configure logging for the module
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Initialize the database with the necessary schema on application start
DB_CONFIG = {
    'host': os.environ.get('MYSQL_HOST'),
    'user': SecretConfig.DATABASE_USERNAME,
    'password': SecretConfig.DATABASE_PASSWORD,
    'database': os.environ.get('MYSQL_NAME'),
}
RETRIES = 5
CONNECTED = False
WAIT = 10

# If running in Kubernetes, assess the DB connection
if os.environ.get('SECRETS_DIRS'):
    for attempt in range(RETRIES):
        try:
            logger.info(f"Attempting to connect to the database. Attempt {attempt + 1} of {RETRIES}")
            cnx = mysql.connector.connect(**DB_CONFIG)
            cursor = cnx.cursor()
            logger.info("Database connection successful.")
            cursor.close()
            cnx.close()
            CONNECTED = True
            break  # Exit loop after successful connection
        except Error as err:
            logger.warning(f"Connection attempt failed: {err}")
            time.sleep(WAIT)

    if not CONNECTED:
        logger.error("Failed to connect to the database after several attempts. Restarting application")
        os._exit(1)  # Non-zero exit code for failure
    else:
        os._exit(0)  # Zero exit code for success


```




`` RUNING DB checks in the background ``

```
#!/bin/bash

##########################################################################################
################################### Global Variables #####################################
##########################################################################################

# Overall name of the family of software we are installing, with extension removed
swTitle="Docker Run Script"

# Log directory
debugDir="/var/log/managed"

# Log file
debugFile="${debugDir}/dotmobi-run.log"

# Script Version
ver="1.0"

# Logging dir for app
logsDir="/usr/local/insights-queue/logs"

# Environment variables
export GUNICORN_CMD_ARGS="\
  --bind=0.0.0.0:5002 \
  --access-logfile '-' \
  --error-logfile '-' \
  --workers=1 \
  --timeout=0 \
  --worker-class=gevent \
  --worker-connections=1000 \
  --access-logformat='%(t)s %(l)s %({X-Forwarded-For}i)s %(l)s %(r)s %(s)s %(b)s %(f)s %(a)s'"

##########################################################################################
#################################### Start functions #####################################
##########################################################################################

setup()
{
    /bin/echo "Setup logs and directories..."
    # Ensure the debug directory exists
    if [ ! -d "${debugDir}" ]; then
        /bin/mkdir -p "${debugDir}"
    fi
    # Ensure the debug file exists
    if [ ! -f "${debugFile}" ]; then
        /usr/bin/touch "${debugFile}"
    fi
    # Ensure the logs directory exists
    if [ ! -d "${logsDir}" ]; then
        /bin/mkdir -p "${logsDir}"
    fi
}

start()
{
    /bin/echo "Started: ${swTitle} ${ver}" | /usr/bin/tee -a "${debugFile}"
}

mysqlPing()
{
    while true; do
        /bin/echo "Attempting to connect to MySQL..." | /usr/bin/tee -a "${debugFile}"
        python3 /usr/local/insights-queue/db_connector.py
        local status=$?

        if [ $status -eq 0 ]; then
            /bin/echo "MySQL database connection successful." | /usr/bin/tee -a "${debugFile}"
            break
        else
            /bin/echo "Failed to connect to MySQL database. Retrying in 1 minute..." | /usr/bin/tee -a "${debugFile}"
            sleep 60
        fi
    done
}

startGunicorn()
{
    /bin/echo "Checking for existing gunicorn processes..." | /usr/bin/tee -a "${debugFile}"
    pkill -f 'gunicorn app:app'
    sleep 2
    /bin/echo "Starting new gunicorn process..." | /usr/bin/tee -a "${debugFile}"
    cd /usr/local/insights-queue/ || exit
    gunicorn app:app 2>&1 | /usr/bin/tee -a "${debugFile}" &
}

##########################################################################################
#################################### End functions #######################################
##########################################################################################

setup
start
(mysqlPing && startGunicorn) &

```

### Script Overview
- Global Variables: Defines environment variables and paths that will be used throughout the script. This includes settings for the Gunicorn web server, and paths for log directories and files.
Functions:

- setup(): Prepares the environment by ensuring necessary directories and files exist. It checks and creates the main log directory (debugDir), the main log file (debugFile), and the application-specific logs directory (logsDir).

- start(): Logs the start of the script execution, appending the script title and version to the main log file.
mysqlPing(): Attempts to connect to the MySQL database in a continuous loop. It calls db_connector.py using Python, checks its exit status, and logs the outcome. If the connection is successful, it breaks out of the loop. If unsuccessful, it waits for a minute and tries again.

- startGunicorn(): Stops any existing instance of Gunicorn running the application, ensuring a clean state before starting a new instance. It then navigates to the application directory and starts Gunicorn with the specified parameters, directing output to the log file.

### Execution Flow:
- Setup: Initializes the environment and logs directories.
- Start Logging: Marks the start of the script processing.
- Database Connection and Gunicorn Start: The script starts a subshell that first runs the mysqlPing() function to ensure the database is accessible. Once a successful connection is established, it triggers the - -- startGunicorn() function to start the web server. Both functions log their progress to the specified log file.
### Running in the Background
The combination of mysqlPing() and startGunicorn() runs in a subshell in the background (&). This allows the script to continue or complete without waiting for these functions to finish. This is particularly useful in environments like Kubernetes where you might want the container to be marked as ready or continue with other initialization tasks while still ensuring the application starts correctly once the database is available.




`` run.sh Bash scripts start ``
```bash
#!/bin/bash

##########################################################################################
################################### Global Variables #####################################
##########################################################################################

# Overall name of the family of software we are installing, with extension removed
swTitle="Docker Run Script"

# Log directory
debugDir="/var/log/managed"

# Log file
debugFile="${debugDir}/dotmobi-run.log"

# Script Version
ver="1.0"

# Logging dir for app
logsDir="/usr/local/insights-queue/logs"

# Environment variables
export GUNICORN_CMD_ARGS="\
  --bind=0.0.0.0:5002 \
  --access-logfile '-' \
  --error-logfile '-' \
  --workers=1 \
  --timeout=0 \
  --worker-class=gevent \
  --worker-connections=1000 \
  --access-logformat='%(t)s %(l)s %({X-Forwarded-For}i)s %(l)s %(r)s %(s)s %(b)s %(f)s %(a)s'"

##########################################################################################
#################################### Start functions #####################################
##########################################################################################

setup()
{
    # Make sure we're root & creating logging dirs
    if [ "$(id -u)" != "0" ]; then
        /bin/echo "ERROR: This script must be run as root" 1>&2
        exit 1
    fi

    if [ ! -d "${debugDir}" ]; then
        /bin/mkdir -p "${debugDir}"
        /bin/chmod -R 777 "${debugDir}"
    fi

    if [ ! -f "${debugFile}" ]; then
        /usr/bin/touch "${debugFile}"
    fi

    if [ ! -d "${logsDir}" ]; then
        /bin/mkdir -p "${logsDir}"
        /bin/chmod -R 777 "${logsDir}"
    fi
}

start()
{
    # Logging start
    /bin/echo "Started: ${swTitle} ${ver}" | /usr/bin/tee -a "${debugFile}"
}

mysqlPing()
{
    # Attempt to connect to the database with retries
    local max_attempts=5
    local attempt=1
    while [ $attempt -le $max_attempts ]; do
        /bin/echo "Attempt $attempt to connect to MySQL..." | /usr/bin/tee -a "${debugFile}"
        python3 /usr/local/insights-queue/db_connector.py
        local status=$?

        if [ $status -eq 0 ]; then
            /bin/echo "MySQL database connection successful." | /usr/bin/tee -a "${debugFile}"
            break
        else
            /bin/echo "Failed to connect to MySQL database. Retrying in 1 minute..." | /usr/bin/tee -a "${debugFile}"
            ((attempt++))
            sleep 60
        fi
    done

    if [ $attempt -gt $max_attempts ]; then
        /bin/echo "Failed to connect after $max_attempts attempts. Exiting." | /usr/bin/tee -a "${debugFile}"
        exit 1
    fi
}

startGunicorn()
{
    /bin/echo "Checking for existing gunicorn processes..." | /usr/bin/tee -a "${debugFile}"
    # Find and kill any existing Gunicorn processes
    pkill -f 'gunicorn app:app'
    # Wait a moment to ensure the processes have been terminated
    sleep 2
    /bin/echo "Starting new gunicorn process..." | /usr/bin/tee -a "${debugFile}"
    cd /usr/local/insights-queue/ || exit
    gunicorn app:app 2>&1 | /usr/bin/tee -a "${debugFile}"
}

##########################################################################################
#################################### End functions #######################################
##########################################################################################

# Execute functions
setup
start
mysqlPing
startGunicorn


```


The current setup in the `run.sh` script you have will indeed capture the exit codes returned by the `db_connector.py` script effectively. Here’s a quick breakdown of how that works:

### How Exit Codes are Handled
- In the `mysqlPing` function of the `run.sh` script, after invoking `db_connector.py` with the command `python3 /usr/local/insights-queue/db_connector.py`, the exit code from this Python script is captured into the variable `status` using the command `local status=$?`.
- The `$?` variable in Bash holds the exit status of the last command executed, which in this case is the Python script. Since the Python script has been modified to exit with `0` on success and `1` on failure, this exit status correctly reflects whether the database connection was successful.
- Based on the value of `status`, the script decides what to do next. If `status` is `0` (success), the script breaks out of the loop and proceeds. If `status` is not `0` (failure), it prints a failure message, waits for a minute, and tries again, unless it has reached the maximum number of attempts.

### Review of Relevant `mysqlPing` Section
```bash
mysqlPing()
{
    local max_attempts=5
    local attempt=1
    while [ $attempt -le $max_attempts ]; do
        /bin/echo "Attempt $attempt to connect to MySQL..." | /usr/bin/tee -a "${debugFile}"
        python3 /usr/local/insights-queue/db_connector.py
        local status=$?

        if [ $status -eq 0 ]; then
            /bin/echo "MySQL database connection successful." | /usr/bin/tee -a "${debugFile}"
            break
        else
            /bin/echo "Failed to connect to MySQL database. Retrying in 1 minute..." | /usr/bin/tee -a "${debugFile}"
            ((attempt++))
            sleep 60
        fi
    done

    if [ $attempt -gt $max_attempts ]; then
        /bin/echo "Failed to connect after $max_attempts attempts. Exiting." | /usr/bin/tee -a "${debugFile}"
        exit 1
    fi
}
```

### Ensuring Robustness
This handling mechanism is generally robust for startup scripts where a service must ensure dependencies (like a database connection) are in place before proceeding. However, ensure that the Python script (`db_connector.py`) does not catch all exceptions and return a `0` status mistakenly. It should accurately reflect the state of the connection attempt.

This design ensures that the shell script is tightly integrated with the outcomes of the Python database connection checks, facilitating reliable service start-up sequencing.



