# environment
export AIRFLOW_HOME=${AIRFLOW_HOME:=~}

# any argument received is overriding the default nose execution arguments:
nose_args=$@

echo "Initializing the DB"
yes | airflow initdb
yes | airflow resetdb

echo "Starting the unit tests with the following nose arguments: "$nose_args
nosetests $nose_args
