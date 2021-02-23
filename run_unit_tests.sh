# environment
export AIRFLOW_HOME=${AIRFLOW_HOME:=~}

# any argument received is overriding the default nose execution arguments:
nose_args=$@

echo "Clean up environment"
rm tests/airflow.cfg tests/airflow.db tests/unittests.cfg tests/webserver_config.py

echo "Initializing the DB"
yes | airflow db init
yes | airflow db reset

echo "Starting the unit tests with the following nose arguments: "$nose_args
nosetests $nose_args
