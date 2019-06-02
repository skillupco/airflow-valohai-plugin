from setuptools import setup, find_packages

setup(
    name="airflow-valohai-plugin",
    # TODO: remove tests from package
    packages=find_packages(),
    entry_points = {
        'airflow.plugins': [
            'valohai_plugin = airflow_valohai_plugin.valohai_plugin:ValohaiPlugin'
        ]
    }
)