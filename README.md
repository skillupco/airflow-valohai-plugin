GPL dependency

One of the dependencies of Apache Airflow by default pulls in a GPL library (‘unidecode’). In case this is a concern you can force a non GPL library by issuing export SLUGIFY_USES_TEXT_UNIDECODE=yes and then proceed with the normal installation. Please note that this needs to be specified at every upgrade. Also note that if unidecode is already present on the system the dependency will still be used.

For Airflow 1.10.2 we can distribute airflow plugins with setuptools https://airflow.apache.org/plugins.html#plugins-as-python-packages
For the rest write doc of how to copy paste the code in plugins folder.

Create venv

Install dependencies
SLUGIFY_USES_TEXT_UNIDECODE=yes pip install -r tests/requirements.txt

Run tests

```nosetests tests```