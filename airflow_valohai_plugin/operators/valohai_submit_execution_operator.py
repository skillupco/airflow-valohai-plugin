from airflow.models import BaseOperator

from airflow_valohai_plugin.hooks.valohai_hook import ValohaiHook


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

    def execute(self, context):
        hook = self.get_hook()

        # Pushes execution status to XCOM
        return hook.submit_execution(
            self.project_name,
            self.step,
            self.inputs,
            self.parameters,
            self.environment,
            self.commit,
            self.branch,
            self.tags
        )
