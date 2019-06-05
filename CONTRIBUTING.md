# Contributing

Contributions are welcome. Feel free to open an Issue or add a Pull Request.

## Developing

```
# Clone this repository
git clone https://github.com/Skillupco/airflow-valohai-plugin.git

# Enter the project
cd airflow-valohai-plugin

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install airflow-valohai-plugin in editable mode
pip install -e .
```

## Run the example DAGs

Install dev dependencies.
```
source venv/bin/activate
pip install -r requirements-dev.txt
```

Init the Airflow database
```
AIRFLOW_HOME=$PWD/examples airflow initdb
```

Start the webserver within the virtual environment in one terminal.
```
source venv/bin/activate
AIRFLOW_HOME=$PWD/examples airflow webserver -p 8181
```

Start the scheduler within the virtual environment in another terminal.
```
source venv/bin/activate
AIRFLOW_HOME=$PWD/examples airflow scheduler
```

Open the Airflow UI in your browser at [http://0.0.0.0:8181](http://0.0.0.0:8181)

Make sure you restart the webserver and scheduler after making changes to the plugin code so that they take effect.

## Run tests

```
# Activate the virtual environment
source venv/bin/activate

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
AIRFLOW_HOME=$PWD/tests ./run_unit_tests.sh

# Run linting
flake8 airflow_valohai_plugin tests examples setup.py
```