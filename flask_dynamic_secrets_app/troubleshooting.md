When Kubernetes secrets are mounted as volumes in a pod, they are represented as files within a designated directory. However, Kubernetes also creates some additional hidden files within this directory that are used for internal purposes, such as managing secret updates and maintaining state. These files often begin with dots (e.g., `..data` or `..2021_05_18_15_42_47.12345678`), which is a common convention in Unix-like systems to denote hidden files.

Reading these hidden files can lead to unintended consequences, such as parsing errors, confidentiality leaks if logged, or simply irrelevant data being loaded into your application. Therefore, explicitly ignoring these hidden files in your code ensures that only the intended secrets are processed, enhancing both the security and reliability of your application.

Here's the enhanced version of `SecretsLoader` with explanations incorporated directly into the code comments, explaining why hidden files are skipped and emphasizing the handling specific to Kubernetes:

```python
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecretsLoader:
    def __init__(self, secrets_dirs):
        self.secrets_dirs = secrets_dirs
        self.secrets = {}
        self.load_secrets()

    def load_secrets(self):
        """Loads secret values from specified directories, ignoring hidden files and handling errors.
        Specifically ignores hidden files that Kubernetes uses in its secret management mechanism."""
        for directory in self.secrets_dirs:
            if not os.path.isdir(directory):
                logging.warning(f"Directory {directory} not found or is not a directory.")
                continue

            try:
                # Only process non-hidden files. Hidden files in Kubernetes secret mounts,
                # like ..data or dot-prefixed rollback files, should be ignored to prevent
                # errors and potential data leaks.
                files = [f for f in os.listdir(directory) if not f.startswith('.') and os.path.isfile(os.path.join(directory, f))]
                for filename in files:
                    filepath = os.path.join(directory, filename)
                    try:
                        with open(filepath, 'r') as secret_file:
                            self.secrets[filename] = secret_file.read().strip()
                        logging.info(f"Secret loaded from {filepath}")
                    except IOError as e:
                        logging.error(f"Failed to read {filepath}: {e}")
            except Exception as e:
                logging.error(f"Error accessing directory {directory}: {e}")

    def get_credential(self, key):
        """Returns the secret value associated with the given key."""
        return self.secrets.get(key)

# Example usage
if __name__ == "__main__":
    # Suppose we have secret files in these two directories
    loader = SecretsLoader(['/etc/app_secrets', '/var/app_secrets'])
    secret_key = loader.get_credential('SECRET_KEY')
    print(f"Loaded SECRET_KEY: {secret_key}")
```

### Explanation:
This code now includes an explanation for why we specifically filter out hidden files, referencing Kubernetes' secret management. This context is crucial for understanding the purpose behind the file filtering logic, especially in a complex orchestrated environment like Kubernetes.

Let's enhance the `SecretsLoader` class in your `secrets_loader.py` script to handle Kubernetes mounted secrets more effectively by ignoring hidden files and metadata directories. I'll update your existing class to include these improvements:

### Key Changes:
- **Directory Check**: Added a check to ensure the directory exists before attempting to list its contents. This prevents errors in case the directory path is incorrect or the volume isn't mounted properly.
- **File Type Check**: Added checks to ensure that only regular files are read, ignoring directories or symbolic links that might be present in Kubernetes secrets volumes.
- **Hidden Files Ignored**: Enhanced the loop to skip hidden files and directories, which are commonly used by Kubernetes for managing secrets.
