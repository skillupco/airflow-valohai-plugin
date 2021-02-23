import unittest

from airflow.hooks.valohai import ValohaiHook
from airflow.operators.valohai import ValohaiSubmitExecutionOperator


try:
    from unittest import mock
except ImportError:
    try:
        import mock
    except ImportError:
        mock = None


class TestValohaiSubmitExecutionOperator(unittest.TestCase):

    def setUp(self):
        self.valohai_operator = ValohaiSubmitExecutionOperator(
            task_id='test-valohai-operator',
            project_name='predict-future',
            step='train',
            inputs={},
            parameters={},
            environment='aws-eu-west-1-t2xlarge-no-gpu',
            valohai_conn_id='valohai_default'
        )

    @mock.patch.object(ValohaiHook, '__init__')
    @mock.patch.object(ValohaiHook, 'submit_execution')
    @mock.patch.object(ValohaiHook, 'get_execution_outputs')
    @mock.patch.object(ValohaiHook, 'get_output_url')
    def test_valohai_operator_execute(
        self,
        get_output_url_mock,
        get_execution_outputs_mock,
        submit_execution_mock,
        hook_init_mock
    ):
        hook_init_mock.return_value = None
        submit_execution_mock.return_value = {'id': 0}
        get_execution_outputs_mock.return_value = [{
            'name': 'output_name',
            'ctime': 'output_ctime',
            'size': 'output_size',
            'id': 'output_id',
            'uri': 'output_uri'
        }]
        get_output_url_mock.return_value = 'output_url'

        self.valohai_operator.execute(None)

        submit_execution_mock.assert_called_once()
        hook_init_mock.assert_called_once_with('valohai_default')
        get_execution_outputs_mock.assert_called_once_with(0)
        get_output_url_mock.assert_called_once_with('output_id')


if __name__ == '__main__':
    unittest.main()
