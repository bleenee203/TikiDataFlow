#!/bin/bash
set -e


# Tạo thư mục và cấp quyền cho thư mục /opt/airflow/data
if [ ! -d "/opt/airflow/data" ]; then
  echo "Creating /opt/airflow/data directory..."
  mkdir -p /opt/airflow/data
  mkdir -p /opt/airflow/data/output_data

fi


$(command -v pip) install --upgrade pip

if [ -e "/opt/airflow/requirements.txt" ]; then
    $(command -v pip) install --user -r requirements.txt
fi

# chown -R airflow:root /opt/airflow/data

# Initialize the database if it hasn't been initialized yet
if [ ! -f "/opt/airflow/airflow.db" ]; then
  airflow db init && \
  airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@airscholar.com \
    --password admin
fi

$(command -v airflow) db upgrade

exec airflow webserver