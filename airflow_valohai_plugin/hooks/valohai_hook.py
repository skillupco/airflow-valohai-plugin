import time
import logging

import requests

from airflow.hooks.base_hook import BaseHook
from airflow.exceptions import AirflowException

LIST_PROJECTS_ENDPOINT = 'https://{host}/api/v0/projects/'
LIST_REPOSITORIES_ENDPOINT = 'https://{host}/api/v0/repositories/'
LIST_COMMITS_ENDPOINT = 'https://{host}/api/v0/commits/'
SUBMIT_EXECUTION_ENDPOINT = 'https://{host}/api/v0/executions/'
GET_EXECUTION_DETAILS_ENDPOINT = 'https://{host}/api/v0/executions/{execution_id}/'
FETCH_REPOSITORY_ENDPOINT = 'https://{host}/api/v0/projects/{project_id}/fetch/'
SET_EXECUTION_TAGS_ENDPOINT = 'https://{host}/api/v0/executions/{execution_id}/tags/'

incomplete_execution_statuses = {
    'created',
    'queued',
    'started',
    'stopping',
}

fail_execution_statuses = {
    'error',
    'crashed',
    'stopped',
}

success_execution_statuses = {
    'complete',
}


class ValohaiHook(BaseHook):
    """
    Interact with Valohai.
    """
    def __init__(self, valohai_conn_id='valohai_default'):
        self.valohai_conn = self.get_connection(valohai_conn_id)
        self.host = self.valohai_conn.host
        self.password = self.valohai_conn.password

        self.headers = {
            'Authorization': 'Token {}'.format(self.password)
        }

    def get_project_id(self, project_name):
        response = requests.get(
            LIST_PROJECTS_ENDPOINT.format(host=self.host),
            headers=self.headers,
            params={'limit': 10000}
        )
        response.raise_for_status()

        for project in response.json()['results']:
            if project['name'] == project_name:
                return project['id']

    def get_repository_id(self, project_id):
        response = requests.get(
            LIST_REPOSITORIES_ENDPOINT.format(host=self.host),
            headers=self.headers,
            params={'limit': 10000}
        )
        response.raise_for_status()

        for repository in response.json()['results']:
            if repository['project']['id'] == project_id:
                return repository['id']

    def fetch_repository(self, project_id):
        """
        Make Valohai fetch the latest commits.
        """
        response = requests.post(
            FETCH_REPOSITORY_ENDPOINT.format(host=self.host, project_id=project_id),
            headers=self.headers,
        )
        response.raise_for_status()

        return response.json()

    def get_latest_commit(self, project_id, branch):
        repository_id = self.get_repository_id(project_id)

        response = requests.get(
            LIST_COMMITS_ENDPOINT.format(host=self.host),
            headers=self.headers,
            params={'limit': 10000, 'ordering': '-commit_time'}
        )
        response.raise_for_status()

        for commit in response.json()['results']:
            if commit['repository'] == repository_id and commit['ref'] == branch:
                return commit['identifier']

    def get_execution_details(self, execution_id):
        response = requests.get(
            GET_EXECUTION_DETAILS_ENDPOINT.format(host=self.host, execution_id=execution_id),
            headers=self.headers,
        )
        response.raise_for_status()

        return response.json()

    def add_execution_tags(self, tags, execution_id):
        response = requests.post(
            SET_EXECUTION_TAGS_ENDPOINT.format(host=self.host, execution_id=execution_id),
            headers=self.headers,
            json={'tags': tags}
        )
        response.raise_for_status()

        return response.json()

    def submit_execution(
        self,
        project_name,
        step,
        inputs,
        parameters,
        environment,
        commit,
        branch,
        tags,
        polling_period_seconds=30,
    ):
        """
        Submits an execution to valohai and checks the status until the execution succeeds or fails.

        Returns the execution details if the execution completed successfully.
        """
        self.polling_period_seconds = polling_period_seconds

        project_id = self.get_project_id(project_name)

        if not commit:
            # Use branch that defaults to master
            response = self.fetch_repository(project_id)
            logging.info('Fetched latest commits with response: {}'.format(response))

            commit = self.get_latest_commit(project_id, branch)
            logging.info('Using latest {} branch commit: {}'.format(branch, commit))

        payload = {
            'project': project_id,
            'commit': commit,
            'step': step
        }

        if inputs:
            payload['inputs'] = inputs

        if parameters:
            payload['parameters'] = parameters

        if environment:
            payload['environment'] = environment

        response = requests.post(
            SUBMIT_EXECUTION_ENDPOINT.format(host=self.host),
            json=payload,
            headers=self.headers
        )
        try:
            response.raise_for_status()
        except Exception:
            raise AirflowException('Failed to submit execution: {}'.format(response.text))

        try:
            data = response.json()
            logging.info('Got response: {}'.format(data))

            execution_id = data['id']
            execution_url = data['urls']['display']
            logging.info('Started execution: {}'.format(execution_url))
        except Exception:
            raise AirflowException('Failed to parse response: {}'.format(response.text))

        if tags:
            self.add_execution_tags(tags, execution_id)
            logging.info('Added execution tags: {}'.format(tags))

        while True:
            time.sleep(polling_period_seconds)

            execution_details = self.get_execution_details(execution_id)
            status = execution_details['status']
            if status in incomplete_execution_statuses:
                logging.info('Incomplete execution with status: {}'.format(status))
                continue
            elif status in fail_execution_statuses:
                raise AirflowException('Execution failed with status: {}'.format(status))
            elif status in success_execution_statuses:
                logging.info('Execution completed sucessfully')
                return execution_details
            else:
                raise AirflowException('Found a not handled status: {}'.format(status))
