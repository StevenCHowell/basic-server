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
