import unittest

from airflow import configuration
from airflow import models
from airflow.utils import db
from airflow_valohai_plugin.hooks.valohai_hook import ValohaiHook

try:
    from unittest import mock
except ImportError:
    try:
        import mock
    except ImportError:
        mock = None


class TestValohaiHook(unittest.TestCase):

    def setUp(self):
        configuration.load_test_config()
        db.merge_conn(
            models.Connection(
                conn_id='valohai_default',
                conn_type='HTTP',
                host='app.valohai.com',
                password='password'
            )
        )

    def test_init(self):
        hook = ValohaiHook()

        self.assertEqual(hook.valohai_conn.conn_id, 'valohai_default')
        self.assertEqual(hook.valohai_conn.conn_type, 'HTTP')
        self.assertEqual(hook.valohai_conn.host, 'app.valohai.com')
        self.assertEqual(hook.valohai_conn.password, 'password')

        self.assertEqual(hook.host, 'app.valohai.com')
        self.assertDictEqual(hook.headers, {'Authorization': 'Token password'})


if __name__ == '__main__':
    unittest.main()
