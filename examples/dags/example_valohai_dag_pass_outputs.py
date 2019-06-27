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


class ValohaiTrainOperator(ValohaiSubmitExecutionOperator):

    def execute(self, context):
        dag_id = dag.dag_id
        task_id = preprocess.task_id

        self.inputs = {
            'training-set-images': self.get_output_uri(
                dag_id, task_id, 'mnist-train-images.gz', context),
            'training-set-labels': self.get_output_uri(
                dag_id, task_id, 'mnist-train-labels.gz', context),
            'test-set-images': self.get_output_uri(
                dag_id, task_id, 'mnist-test-images.gz', context),
            'test-set-labels': self.get_output_uri(
                dag_id, task_id, 'mnist-test-labels.gz', context),
        }
        super().execute(context)


train = ValohaiTrainOperator(
    task_id='train_model',
    project_name='tensorflow-example',
    step='Train model (MNIST)',
    dag=dag,
    inputs={},
    parameters={
        'dropout': 0.9,
        'learning_rate': 0.001,
        'max_steps': 300,
        'batch_size': 200,
    }
)

preprocess >> train
