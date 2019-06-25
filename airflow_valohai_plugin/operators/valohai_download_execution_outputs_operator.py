import os
import re
from urllib.request import urlretrieve
import logging

from airflow.models import BaseOperator
from airflow.configuration import AIRFLOW_HOME


class ValohaiDownloadExecutionOutputsOperator(BaseOperator):
    """
    Downloads outputs locally from a ValohaiSubmitExecutionOperator
    tasks that stored outputs details in XCOM.

    Args:
        output_task_id (str): id of the ValohaiSubmitExecutionOperator
            task that produced the outputs.
        output_path (str): relative path to AIRFLOW_HOME where to
            store the outputs locally.
        output_name_pattern (str, optional): name or regex pattern to filter
            output names to donwload.
    """
    ui_color = '#002f6c'
    ui_fgcolor = '#fff'

    def __init__(
        self,
        output_task_id,
        output_path,
        output_name_pattern=None,
        *args,
        **kwargs
    ):
        super(ValohaiDownloadExecutionOutputsOperator, self).__init__(*args, **kwargs)
        self.output_task_id = output_task_id
        self.output_path = output_path
        self.output_name_pattern = output_name_pattern

    def get_output_path(self, name):
        return os.path.join(AIRFLOW_HOME, self.output_path, name)

    def execute(self, context):
        logging.info(context['ti'])
        logging.info(self.output_task_id)
        execution_details = context['ti'].xcom_pull(task_ids=self.output_task_id)

        for output in execution_details['outputs']:
            if self.output_name_pattern and not re.match(self.output_name_pattern, output['name']):
                logging.info('Ignore ouput name {} because failed to match pattern {}'.format(
                    output['name'], self.output_name_pattern
                ))
                continue

            output_path = self.get_output_path(output['name'])
            urlretrieve(output['url'], output_path)
            logging.info('Downloaded output to: {}'.format(output_path))
