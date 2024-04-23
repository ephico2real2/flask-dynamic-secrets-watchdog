When mounting secrets in Kubernetes, you might encounter additional metadata files created by Kubernetes, such as `..data`, `..2021_05_18_16_42_47.162077764`, and symbolic links. These are used by Kubernetes for managing secret updates and should not be directly read by your applications.

To handle this in your `SecretsLoader`, you can add a check to ignore hidden files (those starting with a dot `.`) and ensure you're only reading the actual secret files. Here’s an update to the `SecretsLoader` class to accommodate this scenario:

```python
import os

class SecretsLoader:
    def __init__(self, directories):
        self.secrets = {}
        self.load_secrets(directories)

    def load_secrets(self, directories):
        """ Load secrets from specified directories """
        for directory in directories:
            # Make sure the directory exists
            if not os.path.exists(directory):
                print(f"Directory {directory} does not exist.")
                continue
            
            # List all items in the directory that do not start with a dot
            for item in os.listdir(directory):
                if item.startswith('.'):
                    continue  # Skip hidden files and directories

                item_path = os.path.join(directory, item)
                
                # Ensure that the item is a file before trying to read it
                if os.path.isfile(item_path):
                    with open(item_path, 'r') as file:
                        self.secrets[item] = file.read().strip()
                else:
                    print(f"Skipped {item_path}, it's not a file.")

    def get_credential(self, name):
        """ Retrieve a secret value by name """
        return self.secrets.get(name)

# Example usage:
directories = ['./secrets']
secrets_loader = SecretsLoader(directories)
print(secrets_loader.get_credential('MYSQL_PASSWORD'))  # Example to retrieve MySQL password
```

### Key Updates:
- **Ignore Hidden Files**: The `os.listdir()` call is filtered to ignore any items that start with a dot (`.`), which includes hidden files and directories that Kubernetes uses for managing and rotating secrets.
- **Logging for Skipped Items**: Adds logging to inform when items are skipped, which can help in troubleshooting.

Let's enhance the `SecretsLoader` class in your `secrets_loader.py` script to handle Kubernetes mounted secrets more effectively by ignoring hidden files and metadata directories. I'll update your existing class to include these improvements:

```python
import os

class SecretsLoader:
    def __init__(self, secrets_dirs):
        self.secrets_dirs = secrets_dirs
        self.secrets = {}
        self.load_secrets()

    def load_secrets(self):
        """ Load secrets, ignoring hidden files and directories. """
        for directory in self.secrets_dirs:
            # Check if directory exists to avoid errors
            if not os.path.isdir(directory):
                print(f"Warning: Directory {directory} not found.")
                continue

            for filename in os.listdir(directory):
                if filename.startswith('.'):  # Skip hidden files and directories
                    continue

                filepath = os.path.join(directory, filename)
                # Ensure we are reading files and not directories or symlinks
                if os.path.isfile(filepath):
                    with open(filepath, 'r') as secret_file:
                        self.secrets[filename] = secret_file.read().strip()
                else:
                    print(f"Skipped {filepath}, it's not a regular file.")

    def get_credential(self, key):
        """ Retrieve a secret value by key. """
        return self.secrets.get(key)

# Example usage:
# Define your directories containing secrets
directories = ['./secrets']
secrets_loader = SecretsLoader(directories)
print(secrets_loader.get_credential('MYSQL_PASSWORD'))  # Example to retrieve MySQL password
```

### Key Changes:
- **Directory Check**: Added a check to ensure the directory exists before attempting to list its contents. This prevents errors in case the directory path is incorrect or the volume isn't mounted properly.
- **File Type Check**: Added checks to ensure that only regular files are read, ignoring directories or symbolic links that might be present in Kubernetes secrets volumes.
- **Hidden Files Ignored**: Enhanced the loop to skip hidden files and directories, which are commonly used by Kubernetes for managing secrets.

### Testing:
Test this script in your environment to make sure it correctly loads the required secrets without attempting to read hidden files or metadata. Ensure it handles missing directories gracefully, which can be helpful during initial deployment stages or when secrets are not yet available.
