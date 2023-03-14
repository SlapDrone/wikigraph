from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from src.sparql import fetch_data
from src.data_transformer import process_data
from src.neo4j_utils import create_connection, insert_data

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "wikigraph_dag",
    default_args=default_args,
    description="Fetch and process data from Wikipedia and store it in a Neo4j database",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 3, 14),
    catchup=False,
)

def fetch_and_process_data(**kwargs):
    data = fetch_data()
    processed_data = process_data(data)
    kwargs["ti"].xcom_push(key="processed_data", value=processed_data)

def store_data_in_neo4j(**kwargs):
    processed_data = kwargs["ti"].xcom_pull(key="processed_data")
    driver = create_connection()
    insert_data(driver, processed_data)

fetch_and_process_data_task = PythonOperator(
    task_id="fetch_and_process_data",
    python_callable=fetch_and_process_data,
    provide_context=True,
    dag=dag,
)

store_data_in_neo4j_task = PythonOperator(
    task_id="store_data_in_neo4j",
    python_callable=store_data_in_neo4j,
    provide_context=True,
    dag=dag,
)

fetch_and_process_data_task >> store_data_in_neo4j_task
