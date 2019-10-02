# Airflow Valohai Plugin

Integration between [Airflow](https://airflow.apache.org/) and [Valohai](https://valohai.com/) that allow Airflow tasks to launch executions in Valohai.

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

Get a Valohai [API Token](https://app.valohai.com/auth/tokens/).

Create a Valohai Connection in the Airflow UI with:
- Conn Id: valohai_default
- Conn Type: HTTP
- Host: app.valohai.com
- Password: REPLACE_WITH_API_TOKEN

There are two operators that you can import.

```
from airflow.operators.valohai import ValohaiSubmitExecutionOperator, ValohaiDownloadExecutionOutputsOperator
```

You can then create tasks and assign them to your DAGs.

### ValohaiSubmitExecutionOperator

```
train_model = ValohaiSubmitExecutionOperator(
    task_id='train_model',
    project_name='tensorflow-example',
    step='Train model (MNIST)',
    dag=dag,
)
```

### ValohaiDownloadExecutionOutputsOperator

```
from airflow.operators.valohai import ValohaiDownloadExecutionOutputsOperator

download_model = ValohaiDownloadExecutionOutputsOperator(
    task_id='download_model',
    output_task=train_model,
    output_name='model.pb',
    dag=dag
)
```

And create dependencies between your tasks.

```
train_model >> download_model
```

## Examples

You can find the complete code of example Airflow DAGs in the [examples](https://github.com/Skillupco/airflow-valohai-plugin/blob/master/examples/dags) folder.

## Contributing

Check out the [contributing](https://github.com/Skillupco/airflow-valohai-plugin/blob/master/CONTRIBUTING.md) page.
