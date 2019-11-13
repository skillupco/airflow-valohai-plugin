from functools import partial

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException

from airflow_valohai_plugin.hooks.valohai_hook import ValohaiHook


def resolve_callables(d, context):
    resolved_d = {}
    for key, value in d.items():
        if callable(value):
            resolved_d[key] = value(context)
        else:
            resolved_d[key] = value
    return resolved_d


class ValohaiSubmitExecutionOperator(BaseOperator):
    """
    Launches a Valohai execution from an Airflow task.

    Args:
        project_name (str): name of the project.
        step (str): name of the step.
        inputs (dict, optional): file inputs dictionary with name in keys and url in values.
        parameters (dict, optional): parameters with name in keys and value in values.
        environment (str, optional): cloud environment to launch the execution.
            By default it takes the environment in the Valohai UI settings.
        commit (str, optional): commit hash.
            By default it fetches the latest commit.
        branch (str, optional): branch name in the code repository.
            By default it takes master.
        tags (list, optional): tags to add to the execution.
    """
    ui_color = '#002f6c'
    ui_fgcolor = '#fff'

    @apply_defaults
    def __init__(
        self,
        project_name,
        step,
        inputs={},
        parameters={},
        environment=None,
        commit=None,
        branch='master',
        tags=[],
        valohai_conn_id='valohai_default',
        *args,
        **kwargs
    ):
        super(ValohaiSubmitExecutionOperator, self).__init__(*args, **kwargs)
        self.project_name = project_name
        self.step = step
        self.inputs = inputs
        self.parameters = parameters
        self.environment = environment
        self.commit = commit
        self.branch = branch
        self.tags = tags
        self.valohai_conn_id = valohai_conn_id

    def get_hook(self):
        return ValohaiHook(
            self.valohai_conn_id
        )

    @staticmethod
    def get_output_uri(task=None, name=None):
        def _get_output_uri(context, task=None, name=None):
            execution_details = context['ti'].xcom_pull(
                dag_id=task.dag_id,
                task_ids=task.task_id,
                include_prior_dates=True
            )

            for output in execution_details['outputs']:
                if output['name'] == name:
                    return ['datum://{}'.format(output['id'])]

            raise AirflowException('Failed to find uri for input with name {}'.format(name))
        return partial(_get_output_uri, task=task, name=name)

    def execute(self, context):
        hook = self.get_hook()

        # Pushes execution status to XCOM
        return hook.submit_execution(
            self.project_name,
            self.step,
            resolve_callables(self.inputs, context),
            resolve_callables(self.parameters, context),
            self.environment,
            self.commit,
            self.branch,
            self.tags
        )
