from datetime import datetime

from airflow import DAG
from airflow_valohai_plugin.operators.valohai_submit_execution_operator import ValohaiSubmitExecutionOperator
from airflow_valohai_plugin.operators.valohai_download_execution_outputs_operator import ValohaiDownloadExecutionOutputsOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 1, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG(
    'example_valohai_dag_time_limit',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
)

train_model = ValohaiSubmitExecutionOperator(
    task_id='train_model',
    project_name='tensorflow-example',
    step='train-model',
    environment='azure-westeurope-f2sv2',
    dag=dag,
    inputs={
        'dataset': 'https://valohaidemo.blob.core.windows.net/mnist/preprocessed_mnist.npz',
    },
    parameters={
        'epochs': 5,
        'learning_rate': 0.001,
    },
    time_limit=5,
)

download_model = ValohaiDownloadExecutionOutputsOperator(
    task_id='download_model',
    output_task=train_model,
    output_name='model.pb',
    dag=dag
)

train_model >> download_model
