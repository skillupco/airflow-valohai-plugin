# environment
export AIRFLOW_HOME=${AIRFLOW_HOME:=~}

# any argument received is overriding the default nose execution arguments:
nose_args=$@

echo "Initializing the DB"
yes | airflow initdb
yes | airflow resetdb

# For impersonation tests running on SQLite on Travis, make the database world readable so other
# users can update it
AIRFLOW_DB="$HOME/airflow.db"

if [ -f "${AIRFLOW_DB}" ]; then
  chmod a+rw "${AIRFLOW_DB}"
  chmod g+rwx "${AIRFLOW_HOME}"
fi

# For impersonation tests on Travis, make airflow accessible to other users via the global PATH
# (which contains /usr/local/bin)
sudo ln -sf "${VIRTUAL_ENV}/bin/airflow" /usr/local/bin/

echo "Starting the unit tests with the following nose arguments: "$nose_args
nosetests $nose_args
