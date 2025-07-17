# Basic Server

This code is meant as a starting point for building out a Flask server.
The initial version is intended to provide a Flask app that handles PDF file uploads, processes them, reports progress, and returns the processed files.
The initial PDF process reverses the page order and rotated the pages 180 degrees.

## Contributing

This repo uses [uv](https://docs.astral.sh/uv/) for configuring the Python virtual environment.
As prerequisites, you will need both Python and uv installed and accessible in you path.
If needed, refer to the linked documentation for installing [python](https://www.python.org/downloads/) and [uv](https://docs.astral.sh/uv/getting-started/installation/).
Both Python and uv should be able to be installed on a system as a local install without admin priveleges.

After cloning the repo, navigate into the base folder and setup your python enviornemnet as follows:

```bash
cd basic-server
uv sync
```

Once the virtual environment is configured, activate the environment from the base folder by running the following:

```bash
source .venv/Scripts/activate
```

Then configure the [isort](https://pycqa.github.io/isort/), [black](https://black.readthedocs.io/en/stable/index.html), and [flake8](https://flake8.pycqa.org/en/latest/) pre-commit hooks by running the following. You can view and make changes to the enforced rules using the `tox.ini` file.

```bash
pre-commit install
```

## Backend Flask Server

### Redis Server

The docker run command below exposes redis-server on port 6379 and RedisInsight on port 8001. You can use RedisInsight by pointing your browser to http://localhost:8001.

```bash
# install
$ docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

### Celery Worker

Start the Celery worker, for handling background tasks:

```bash
celery -A app.celery worker --loglevel=info
```

### Flask Application

Run the Flask application by running the command:

```bash
python app.py
```

### Upload a File

You can upload a test file as follows:

```bash
$ curl -X POST -F "file=@path/to/your/file.pdf" http://localhost:5000/upload

{
  "task_id": "3f58dc79-e66e-4a0f-8538-e5c414343733"
}
```

If successful, you should get a return value containing the task ID, as shown.


### Check the Status

You can check the status of the processing using the returned task ID by running:

```bash
$ curl http://localhost:5000/status/3f58dc79-e66e-4a0f-8538-e5c414343733

{
  "progress": 0,
  "state": "SUCCESS"
}
```

The above example illustrates a successful run. If the process has not yet completed, the response would look more like the following:

```bash
{
    "state": "PROCESSING",
    "progress": 50,
    "annotated_file": null
}

### Downloading the Processed File

Once the task has completed, the status...
