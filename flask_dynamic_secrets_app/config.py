# config.py
import os
from secrets_loader import SecretsLoader

# Function to load secrets
def load_secrets():
    secrets_dirs_env = os.getenv('SECRETS_DIRS', './default/path/to/secrets').split(',')
    secrets_dirs = [dir.strip() for dir in secrets_dirs_env]
    return SecretsLoader(secrets_dirs)

class Config:
    # Initial loading of secrets
    secrets_loader = load_secrets()
    #SECRET_KEY = secrets_loader.get_credential('SECRET_KEY')
    DATABASE_HOST = secrets_loader.get_credential('MYSQL_HOSTNAME')
    DATABASE_USER = secrets_loader.get_credential('MYSQL_USERNAME')
    DATABASE_PASSWORD = secrets_loader.get_credential('MYSQL_PASSWORD')
    DATABASE_NAME = secrets_loader.get_credential('MYSQL_DB')

    @classmethod
    def reload(cls):
        # Reload secrets
        cls.secrets_loader = load_secrets()
       # cls.SECRET_KEY = cls.secrets_loader.get_credential('SECRET_KEY')
        cls.DATABASE_HOST = cls.secrets_loader.get_credential('MYSQL_HOSTNAME')
        cls.DATABASE_USER = cls.secrets_loader.get_credential('MYSQL_USERNAME')
        cls.DATABASE_PASSWORD = cls.secrets_loader.get_credential('MYSQL_PASSWORD')
        cls.DATABASE_NAME = cls.secrets_loader.get_credential('MYSQL_DB')
        # Add any other configurations that depend on secrets here

