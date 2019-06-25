from airflow.plugins_manager import AirflowPlugin

from airflow_valohai_plugin.hooks.valohai_hook import ValohaiHook
from airflow_valohai_plugin.operators.valohai_submit_execution_operator import ValohaiSubmitExecutionOperator
from airflow_valohai_plugin.operators.valohai_download_execution_outputs_operator import \
    ValohaiDownloadExecutionOutputsOperator


class ValohaiPlugin(AirflowPlugin):
    name = "valohai"
    hooks = [ValohaiHook]
    operators = [ValohaiSubmitExecutionOperator, ValohaiDownloadExecutionOutputsOperator]
