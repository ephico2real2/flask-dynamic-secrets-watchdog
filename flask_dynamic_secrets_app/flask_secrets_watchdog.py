# flask_secrets_watchdog.py
import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
from secrets_loader import SecretsLoader
from app import app  # Adjust import as needed for your Flask app structure

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FlaskSecretsChangeHandler(FileSystemEventHandler):
    def __init__(self, secrets_dirs, callback):
        self.secrets_dirs = secrets_dirs
        self.callback = callback

    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"Detected modification in: {event.src_path}")
            self.callback()

    def on_deleted(self, event):
        if not event.is_directory:
            logging.info(f"Detected deletion of: {event.src_path}")
            self.callback()

def on_secrets_changed():
    logging.info("Secrets changed. Reloading configuration...")
    secrets_dirs_env = os.getenv('SECRETS_DIRS', './default/path/to/secrets').split(',')
    secrets_dirs = [dir.strip() for dir in secrets_dirs_env]
    secrets_loader = SecretsLoader(secrets_dirs)
    app.config['SECRET_KEY'] = secrets_loader.get_credential('SECRET_KEY')
    logging.info("Configuration successfully reloaded.")

def run_watchdog():
    secrets_dirs_env = os.getenv('SECRETS_DIRS', './default/path/to/secrets').split(',')
    secrets_dirs = [dir.strip() for dir in secrets_dirs_env]
    event_handler = FlaskSecretsChangeHandler(secrets_dirs, on_secrets_changed)
    observer = Observer()
    for directory in secrets_dirs:
        observer.schedule(event_handler, directory, recursive=False)
    observer.start()
    logging.info(f"Starting Flask secrets watchdog for directories: {', '.join(secrets_dirs)}")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    run_watchdog()
