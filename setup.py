from setuptools import setup

setup(
    name="airflow-valohai-plugin",
    entry_points = {
        'airflow.plugins': [
            'valohai_plugin = valohai_plugin:ValohaiPlugin'
        ]
    }
)