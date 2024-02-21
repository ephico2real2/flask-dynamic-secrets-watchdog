# secrets_loader.py
import os

class SecretsLoader:
    def __init__(self, secrets_dirs):
        self.secrets_dirs = secrets_dirs
        self.secrets = {}
        self.load_secrets()

    def load_secrets(self):
        for directory in self.secrets_dirs:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r') as secret_file:
                    self.secrets[filename] = secret_file.read().strip()

    def get_credential(self, key):
        return self.secrets.get(key)
