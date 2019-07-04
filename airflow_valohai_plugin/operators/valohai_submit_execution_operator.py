from airflow.models import BaseOperator

from airflow_valohai_plugin.hooks.valohai_hook import ValohaiHook


class ValohaiSubmitExecutionOperator(BaseOperator):
    ui_color = '#002f6c'
    ui_fgcolor = '#fff'

    def __init__(
        self,
        project_name,
        step,
        inputs=None,
        parameters=None,
        environment=None,
        commit=None,
        branch='master',
        tags=None,
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
