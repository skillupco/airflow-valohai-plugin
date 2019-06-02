import unittest
import json

from airflow import configuration
from airflow import models
from airflow.utils import db
from airflow.hooks.valohai import ValohaiHook

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
                extra=json.dumps({'token': '123456789'})
            )
        )

    def test_init(self):
        hook = ValohaiHook()

        self.assertEqual(hook.valohai_conn.conn_id, 'valohai_default')
        self.assertEqual(hook.valohai_conn.conn_type, 'HTTP')
        self.assertEqual(hook.valohai_conn.host, 'app.valohai.com')
        self.assertEqual(hook.valohai_conn.extra, '{"token": "123456789"}')

        self.assertEqual(hook.host, 'app.valohai.com')
        self.assertDictEqual(hook.headers, {'Authorization': 'Token 123456789'})


if __name__ == '__main__':
    unittest.main()
