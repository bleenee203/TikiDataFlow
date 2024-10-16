from airflow import DAG

from datetime import datetime,timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipelines.extract_tiki import extract_tiki_data
from pipelines.load_tiki import load_tiki_data
from pipelines.tranform_tiki import transform_tiki_data
# from pipelines.process_tiki import process_tiki_data
from pipelines.visualization_tiki import visualization_tiki_data


postgres_db = "jdbc:postgresql://postgres/airflow"
postgres_user = "airflow"
postgres_pwd = "airflow"

dag = DAG(
    dag_id="tiki_flow",
    default_args={
        'owner': "BichLy",
        'start_date': datetime(2024, 10, 1),
        'execution_timeout': timedelta(minutes=120),
    },
    schedule_interval=None,
    catchup=False
)

# extract: crawl product data from tiki
# extract_from_tiki = PythonOperator(
#     task_id = "extract_data_from_tiki",
#     python_callable= extract_tiki_data,
#     provide_context=True,
#     # op_kwargs={
#     #     "url": "https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity",
#     # },
#     dag=dag
# )
# transform
transform_tiki_data =PythonOperator(
    task_id = "transform_data_from_tiki",
    python_callable= transform_tiki_data,
    provide_context=True,
    dag=dag
)
# load 
load_tiki_data = PythonOperator (
    task_id = "load_data_from_tiki",
    python_callable= load_tiki_data,
    provide_context=True,
    dag=dag
)
# process
# process_tiki_data =PythonOperator(
#     task_id = "process_data_from_tiki",
#     python_callable= process_tiki_data,
#     provide_context=True,
#     dag=dag
# )
process_tiki_data = SparkSubmitOperator(
    task_id='process_data_from_tiki',
    application='/opt/airflow/pipelines/process_tiki.py',  # đường dẫn tới file PySpark
    conn_id='spark_default',  # Đảm bảo thiết lập kết nối Spark trong Airflow Connections
    conf={'spark.master': 'spark://spark-master:7077'},
    # jars='/opt/bitnami/spark/jars/postgresql-42.2.18.jar',
    # driver_class_path='/opt/bitnami/spark/jars/postgresql-42.2.18.jar',
    # application_args=[postgres_db,postgres_user,postgres_pwd],
    name="TikiDataProcessing",
    verbose=False,
    dag=dag
)


# visualization
visualization_tiki_data =PythonOperator(
    task_id = "visualization_data_from_tiki",
    python_callable= visualization_tiki_data,
    provide_context=True,
    dag=dag
)


# extract_from_tiki >>
transform_tiki_data >> load_tiki_data >> [visualization_tiki_data,process_tiki_data]