# Airflow Valohai Plugin

This is an integration between Airflow and Valohai that allow Airflow tasks to launch executions in Valohai. It adds classes `ValohaiHook` and `ValohaiSubmitExecutionOperator` to be used in Airflow.

[Airflow](https://airflow.apache.org/) is a platform to programmatically author, schedule and monitor workflows.

[Valohai](https://valohai.com/) is a platform scale your Machine Learning with Machine Orchestration and Version Control.


## Installation

### airflow>=1.10.2
Install this package directly from Github (and soon pypi).

```
pip install git+https://github.com/Skillupco/airflow-valohai-plugin
```

### airflow<1.10.2
Copy the contents of `airflow_valohai_plugin` into your `$AIRFLOW_HOME/plugins` folder.

You can read more about the use cases of [Airflow plugins](https://airflow.apache.org/plugins.html) in the official docs.

## Usage

Get a Valohai [API Token](https://app.valohai.com/auth/tokens/).

Create a Valohai Connection in the Airflow UI.

![](/docs/img/airflow-connection-ui.png)

After installing the plugin you can import the Valohai operators.

```
from airflow.operators.valohai import ValohaiSubmitExecutionOperator
```

You can find the code of example Airflow DAGs and tasks in the [examples](https://github.com/Skillupco/airflow-valohai-plugin/blob/master/examples/dags) dags folder. Monitor your task from the Airflow UI.

![](/docs/img/airflow-dag-view.png)

## Contributing

Check out the [contributing](https://github.com/Skillupco/airflow-valohai-plugin/blob/master/CONTRIBUTING.md) page.
