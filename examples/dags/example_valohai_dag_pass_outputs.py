from datetime import datetime
from functools import partial

from airflow import DAG
from airflow.operators.valohai import ValohaiSubmitExecutionOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 1, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG(
    'example_valohai_dag_pass_outputs',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
)


preprocess = ValohaiSubmitExecutionOperator(
    task_id='preprocess',
    project_name='tensorflow-example',
    step='Preprocess dataset (MNIST)',
    dag=dag,
    inputs={
        'test-set-images': 'https://valohai-mnist.s3.amazonaws.com/t10k-images-idx3-ubyte.gz',
        'test-set-labels': 'https://valohai-mnist.s3.amazonaws.com/t10k-labels-idx1-ubyte.gz',
        'training-set-images': 'https://valohai-mnist.s3.amazonaws.com/train-images-idx3-ubyte.gz',
        'training-set-labels': 'https://valohai-mnist.s3.amazonaws.com/train-labels-idx1-ubyte.gz'
    },
)

train = ValohaiSubmitExecutionOperator(
    task_id='train_model',
    project_name='tensorflow-example',
    step='Train model (MNIST)',
    dag=dag,
    inputs={
        'training-set-images': partial(
            ValohaiSubmitExecutionOperator.get_output_uri,
            task=preprocess,
            name='mnist-train-images.gz'),
        'training-set-labels': partial(
            ValohaiSubmitExecutionOperator.get_output_uri,
            task=preprocess,
            name='mnist-train-labels.gz'),
        'test-set-images': partial(
            ValohaiSubmitExecutionOperator.get_output_uri,
            task=preprocess,
            name='mnist-test-images.gz'),
        'test-set-labels': partial(
            ValohaiSubmitExecutionOperator.get_output_uri,
            task=preprocess,
            name='mnist-test-labels.gz'),
    },
    parameters={
        'dropout': 0.9,
        'learning_rate': 0.001,
        'max_steps': 300,
        'batch_size': 200,
    }
)

preprocess >> train
