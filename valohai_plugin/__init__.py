from airflow.plugins_manager import AirflowPlugin

from valohai_plugin.hooks.valohai_hook import ValohaiHook
from valohai_plugin.operators.valohai_operator import ValohaiSubmitExecutionOperator


class ValohaiPlugin(AirflowPlugin):
    name = "valohai_plugin"
    hooks = [ValohaiHook]
    operators = [ValohaiSubmitExecutionOperator]