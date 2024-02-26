Creating a README for running the Flask app locally with Python virtual environment and populating secrets:

### Setting Up and Running Locally

#### Prerequisites

- Python 3.8+
- pip
- virtualenv (optional but recommended)

#### Step 1: Clone Repository

Clone the repository to your local machine and navigate into the project directory:

```bash
git clone [REPOSITORY_URL] flask-dynamic-secrets-watchdog
cd flask-dynamic-secrets-watchdog
```

Replace `[REPOSITORY_URL]` with the actual URL of your git repository.

#### Step 2: Create Python Virtual Environment

It's recommended to use a virtual environment for Python projects to manage dependencies efficiently.

```bash
python3 -m venv venv
```

Activate the virtual environment:

- On Windows:
  ```bash
  .\venv\Scripts\activate
  ```
- On macOS and Linux:
  ```bash
  source venv/bin/activate
  ```

#### Step 3: Install Dependencies

Install the required Python packages from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

#### Step 4: Create Secrets Directory

Create a `./secrets` directory at the project root and populate it with your MySQL secrets:

```bash
mkdir -p ./secrets
echo "db" > ./secrets/MYSQL_HOSTNAME
echo "root" > ./secrets/MYSQL_USERNAME
echo "london123" > ./secrets/MYSQL_PASSWORD
echo "quotes" > ./secrets/MYSQL_DB
echo "3306" > ./secrets/MYSQL_PORT
```

#### Step 5: Run the Flask Application

Before running the application, make sure to set the `FLASK_APP` environment variable:

```bash
export FLASK_APP=app.py
```

For Windows CMD, use:

```cmd
set FLASK_APP=app.py
```

For Windows PowerShell, use:

```powershell
$env:FLASK_APP = "app.py"
```

Now, run the Flask application:

```bash
flask run --port=3000
```

Alternatively, if you're using Gunicorn as your WSGI HTTP server:

```bash
gunicorn --workers=3 --bind=0.0.0.0:3000 app:app
```

#### Step 6: Access the Application

Open your web browser and navigate to `http://localhost:3000` to access the Flask application. 

### Running with Docker (Optional)

If you prefer running the application within a Docker container, ensure Docker and Docker Compose are installed on your machine. Adjust the `docker-compose.yml` file as necessary to fit your setup, especially the secrets volume mount and environment variables.
