## Installation

For airflow>=1.10.2 you can install this package directly from Github, as Airflow uses setuptools to discover installed [Airflow plugins](https://airflow.apache.org/plugins.html#plugins-as-python-packages).

You can then import the Valohai operators and hooks with:

```
from airflow.hooks.valohai import ValohaiHook
from airflow.operators.valohai import ValohaiSubmitExecutionOperator
```

For older versions airflow<1.10.2  you need to manually add the code in the airflow plugins folder.

## Run tests

Create a virtual environment:

```python3 -m venv venv```

Activate the virtual environment:

```source venv/bin/activate```

Install test dependencies:

```pip install -r tests/requirements.txt```

Install airflow-valohai-plugin in editable mode:

```pip install -e .```

Run tests:

```AIRFLOW_HOME=$PWD/tests ./run_unit_tests.sh```

## Run linting

```flake8 airflow_valohai_plugin tests examples setup.py```

Make sure you restart the webserver and scheduler after making changes to plugins so that they take effect.