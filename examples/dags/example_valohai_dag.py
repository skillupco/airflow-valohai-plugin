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
    'example_valohai_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
)

train_model = ValohaiSubmitExecutionOperator(
    task_id='train_model',
    project_name='tensorflow-example',
    step='Train model (MNIST)',
    dag=dag,
    inputs={
        'test-set-images': 'https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz',
        'test-set-labels': 'https://valohai-mnist.s3.amazonaws.com/t10k-labels-idx1-ubyte.gz',
        'training-set-images': 'https://valohai-mnist.s3.amazonaws.com/train-images-idx3-ubyte.gz',
        'training-set-labels': 'https://valohai-mnist.s3.amazonaws.com/train-labels-idx1-ubyte.gz'
    },
    parameters={
        'dropout': 0.9,
        'learning_rate': 0.001,
        'max_steps': 300,
        'batch_size': 200,
    }
)

download_model = ValohaiDownloadExecutionOutputsOperator(
    task_id='download_model',
    output_task=train_model,
    output_name='model.pb',
    dag=dag
)

train_model >> download_model
