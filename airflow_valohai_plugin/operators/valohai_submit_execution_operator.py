from airflow.models import BaseOperator

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

    @staticmethod
    def get_output_uri(context, task=None, name=None):
        execution_details = context['ti'].xcom_pull(
            dag_id=task.dag_id,
            task_ids=task.task_id,
            include_prior_dates=True
        )

        for output in execution_details['outputs']:
            if output['name'] == name:
                return ['datum://{}'.format(output['id'])]

        raise Exception('Failed to find uri for input with name {}'.format(output))

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
