# Contributing

Contributions are welcome. Feel free to open an Issue or add a Pull Request.

## Developing in your local environment

```
# Clone this repository
git clone https://github.com/Skillupco/airflow-valohai-plugin.git

# Enter the project
cd airflow-valohai-plugin

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dev dependencies
pip install -r requirements-dev.txt

# Install airflow-valohai-plugin in editable mode
pip install -e .
```

## Developing in VSCode development container

Make sure you have installed `devcontainer` CLI on your host machine: https://code.visualstudio.com/docs/remote/devcontainer-cli

In your host terminal:
```
# Clone this repository
git clone https://github.com/Skillupco/airflow-valohai-plugin.git

# Open the project with VSCode
cd airflow-valohai-plugin
devcontainer open
```

In your VSCode container temrinal:
```
# Install dev dependencies
pip install -r requirements-dev.txt

# Install airflow-valohai-plugin in editable mode
pip install -e .
```

## Run the example DAGs

Clean up residual Airflow files.
```
rm -f examples/airflow.cfg examples/airflow.db examples/unittests.cfg
```

Init the Airflow database.
```
AIRFLOW_HOME=$PWD/examples AIRFLOW__CORE__LOAD_EXAMPLES=False airflow db init
```

Start the webserver within the virtual environment in one terminal.
```
source venv/bin/activate # if in local environment
AIRFLOW_HOME=$PWD/examples airflow webserver -p 8181
```

Start the scheduler within the virtual environment in another terminal.
```
source venv/bin/activate # if in local environment
AIRFLOW_HOME=$PWD/examples AIRFLOW__CORE__LOAD_EXAMPLES=False airflow scheduler
```

Open the Airflow UI in your browser at [http://localhost:8181](http://localhost:8181)

Make sure you create a Valohai Connection in the Airflow UI with:
- Conn Id: valohai_default
- Conn Type: HTTP
- Host: app.valohai.com
- Password: REPLACE_WITH_API_TOKEN

Make sure you restart the webserver and scheduler after making changes to the plugin code so that they take effect.

## Run tests

```
# Activate the virtual environment
source venv/bin/activate # if in local environment

# Run tests
AIRFLOW_HOME=$PWD/tests ./run_unit_tests.sh
```

## Run linting
```
flake8 airflow_valohai_plugin tests examples setup.py
```

## Release a new version

Create a PR to increment the version in `setup.py`.

Locally, build a distribution with `python3 setup.py sdist bdist_wheel`.

Install `twine` with `pip install twine`

Upload the distribution to pypi with `twine upload dist/*`.

You will be asked for your credentials.