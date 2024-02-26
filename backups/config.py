# config.py
import os
from secrets_loader import SecretsLoader

secrets_dirs_env = os.getenv('SECRETS_DIRS', './default/path/to/secrets').split(',')
secrets_dirs = [dir.strip() for dir in secrets_dirs_env]

secrets_loader = SecretsLoader(secrets_dirs)

class Config:
    SECRET_KEY = secrets_loader.get_credential('SECRET_KEY')
    DATABASE_HOST = secrets_loader.get_credential('MYSQL_HOSTNAME')
    DATABASE_USER = secrets_loader.get_credential('MYSQL_USERNAME')
    DATABASE_PASSWORD = secrets_loader.get_credential('MYSQL_PASSWORD')
    DATABASE_NAME = secrets_loader.get_credential('MYSQL_DB')
