from setuptools import find_packages, setup


setup(
    name="airflow-valohai-plugin",
    description='Airflow plugin to integrate Airflow tasks with Valohai executions',
    author='Skillup',
    author_email='ari@skillup.co',
    license='MIT',
    packages=find_packages(include=('airflow_valohai_plugin*',)),
    entry_points={
        "airflow.plugins": [
            "valohai_plugin = airflow_valohai_plugin.valohai_plugin:ValohaiPlugin"
        ]
    }
)
