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
            project_id='1234',
            step='train',
            inputs={},
            parameters={},
            environment='aws-eu-west-1-t2xlarge-no-gpu',
            valohai_conn_id='valohai_default'
        )

    @mock.patch.object(ValohaiHook, '__init__')
    @mock.patch.object(ValohaiHook, 'submit_execution')
    def test_valohai_operator_execute(self, submit_execution_mock, hook_init_mock):
        hook_init_mock.return_value = None

        self.valohai_operator.execute(None)

        submit_execution_mock.assert_called_once()
        hook_init_mock.assert_called_once_with('valohai_default')


if __name__ == '__main__':
    unittest.main()
