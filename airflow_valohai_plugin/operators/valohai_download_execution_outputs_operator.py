import os
import re
from urllib.request import urlretrieve
import logging

from airflow.models import BaseOperator
from airflow.configuration import AIRFLOW_HOME


class ValohaiDownloadExecutionOutputsOperator(BaseOperator):
    """
    Downloads outputs locally from a previous ValohaiSubmitExecutionOperator
    task that stored output details in XCOM. By default it downloads all outputs.

    Args:
        output_task (TaskInstance): instance of a ValohaiSubmitExecutionOperator
            task that produced the outputs.
        output_name (str, optional): filter output name to download.
        output_name_pattern (str, optional): filter output name to download
            with a regex.
        output_path (str, optional): relative path to AIRFLOW_HOME where to
            store the outputs locally. By default stores ouputs in AIRFLOW_HOME.
    """
    ui_color = '#fff'
    ui_fgcolor = '#000'

    def __init__(
        self,
        output_task,
        output_name=None,
        output_name_pattern=None,
        output_path='.',
        *args,
        **kwargs
    ):
        super(ValohaiDownloadExecutionOutputsOperator, self).__init__(*args, **kwargs)
        self.output_dag_id = output_task.dag_id
        self.output_task_id = output_task.task_id
        self.output_name = output_name
        self.output_name_pattern = output_name_pattern
        self.output_path = output_path

    def get_output_path(self, name):
        return os.path.join(AIRFLOW_HOME, self.output_path, name)

    def execute(self, context):
        execution_details = context['ti'].xcom_pull(
            dag_id=self.output_dag_id,
            task_ids=self.output_task_id,
            include_prior_dates=True)

        for output in execution_details['outputs']:
            if self.output_name:
                if not self.output_name == output['name']:
                    logging.info('Ignore ouput name {}'.format(
                        output['name']))
                    continue
                output_name = self.output_name
            elif self.output_name_pattern:
                name_match = re.match(self.output_name_pattern, output['name'])
                if not name_match:
                    logging.info('Ignore ouput name {} because failed to match pattern {}'.format(
                        output['name'], self.output_name_pattern))
                    continue
                output_name = name_match.group(0)
            else:
                output_name = output['name']

            output_path = self.get_output_path(output_name)
            urlretrieve(output['url'], output_path)
            logging.info('Downloaded output {} to: {}'.format(output_name, output_path))