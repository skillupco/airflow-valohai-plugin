# Airflow Valohai Plugin

This is an integration between [Airflow](https://airflow.apache.org/) and [Valohai](https://valohai.com/) that allow Airflow tasks to launch executions in Valohai.

## Installation

#### For airflow>=1.10.2
Install this package directly from pypi.

```
pip install airflow-valohai-plugin
```

#### For airflow<1.10.2
Copy the contents of `airflow_valohai_plugin` into your `$AIRFLOW_HOME/plugins` folder.

You can read more about the use cases of [Airflow plugins](https://airflow.apache.org/plugins.html) in the official docs.

## Usage

Get a Valohai [API Token](https://app.valohai.com/auth/tokens/). Create a Valohai Connection in the Airflow UI with:
- Conn Id: valohai_default
- Conn Type: HTTP
- Host: app.valohai.com
- Password: REPLACE_WITH_API_TOKEN

After installing the plugin you can import the Valohai operators.

```
from airflow.operators.valohai import ValohaiSubmitExecutionOperator
```

## Examples

You can find the code of example Airflow DAGs and tasks in the [examples](https://github.com/Skillupco/airflow-valohai-plugin/blob/master/examples/dags) dags folder.

## Contributing

Check out the [contributing](https://github.com/Skillupco/airflow-valohai-plugin/blob/master/CONTRIBUTING.md) page.
