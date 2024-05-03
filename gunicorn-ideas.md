### troubleshooting

```bash

# Export logsDir if it needs to be known by other processes started by this script
export logsDir="/usr/local/insights-queue/logs"

# Ensure the directory exists
mkdir -p $logsDir


cleanup() {
    echo "Cleaning up..."

    # Adjusted to use $logsDir environment variable for PID file locations
    if [ -f "$logsDir/gunicorn.pid" ]; then
        kill $(cat "$logsDir/gunicorn.pid") || echo "Failed to kill Gunicorn"
        rm "$logsDir/gunicorn.pid"
    fi

    echo "All Gunicorn background processes killed."
}

```

```bash
#!/bin/bash

# Define global variables
debugFile="$logsDir/debug.log"  # Adjust debug log file to use logsDir
gunicornPidFile="$logsDir/gunicorn.pid"  # File to store the PID of Gunicorn
databasePidFile="$logsDir/database_monitor.pid"  # File to store the PID of database monitor

# Function to start Gunicorn
startGunicorn() {
    echo "Starting Gunicorn..." | tee -a "${debugFile}"
    cd /usr/local/insights-queue/ || exit 1  # Exit with error if directory change fails

    # Start Gunicorn in a subshell and capture its PID
    (gunicorn app:app 2>&1 & echo $! > "${gunicornPidFile}") | tee -a "${debugFile}" &

    echo "Gunicorn started with PID $(cat $gunicornPidFile)" | tee -a "${debugFile}"
}


# Function to continuously monitor database connection
monitorDatabase() {
    while true; do
        echo "Attempting to connect to MySQL..." | tee -a "${debugFile}"
        # Start the Python database connection check without using a subshell for PID capture
        python3 /usr/local/insights-queue/db_connector.py 2>&1 &
        echo $! > "${databasePidFile}"
        # Use the captured PID to wait for the process to finish
        wait $(cat "${databasePidFile}")
        local status=$?

        if [ $status -eq 0 ]; then
            echo "MySQL database connection successful." | tee -a "${debugFile}"
        else
            echo "Failed to connect to MySQL database. Invoking cleanup and monitoring Gunicorn..." | tee -a "${debugFile}"
            cleanup  # Invoke cleanup to handle shutting down processes cleanly
            # Assume monitorGunicorn is already running and will handle Gunicorn restart
        fi
        sleep 60  # Sleep for a minute before next check
    done
}



monitorGunicorn() {
    while true; do
        echo "Checking for existing Gunicorn processes..." | tee -a "${debugFile}"
        if ! pgrep -f 'gunicorn app:app' > /dev/null; then
            echo "Gunicorn process not found, starting Gunicorn..." | tee -a "${debugFile}"
            startGunicorn  # Call startGunicorn function to manage Gunicorn startup
            # After attempting to start, check if Gunicorn is running
            if ! pgrep -f 'gunicorn app:app' > /dev/null; then
                echo "Failed to start Gunicorn." | tee -a "${debugFile}"
            else
                echo "Gunicorn started successfully with PID $(cat $gunicornPidFile)." | tee -a "${debugFile}"
            fi
        else
            echo "Gunicorn is running." | tee -a "${debugFile}"
        fi

        sleep 60  # Sleep for a minute before next check
    done
}



# Set environment variable (make sure this is set or exported before this script runs)
export logsDir="/usr/local/insights-queue/logs"

# Ensure directory exists
mkdir -p $logsDir

# Start the main setup and start functions
monitorDatabase &
monitorGunicorn &
wait

```

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
