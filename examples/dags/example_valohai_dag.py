from datetime import datetime

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
    'example_valohai_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
)

ValohaiSubmitExecutionOperator(
    dag=dag,
    task_id='example_valohai_operator',
    project_name='predict_future',
    step='train',
    inputs={},
    parameters={},
)
