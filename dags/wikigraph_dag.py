from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from wikigraph import settings
from wikigraph.logger import get_logger
from wikigraph.sparql import get_persons, get_relationships
from wikigraph.neo4j_utils import create_connection, insert_persons, insert_relationships
from wikigraph.config import Settings, get_settings


logger = get_logger("wikigraph_dag")

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

def fetch_and_store_persons(worker_id: int, offset: int, limit: int, **kwargs):
    persons = get_persons(offset, limit)
    if not persons:
        return f"stop_processing_persons_{worker_id}"
    driver = create_connection(settings)
    insert_persons(driver, persons)
    kwargs["ti"].xcom_push(key=f"persons_{worker_id}_{offset}_{limit}", value=persons)
    logger.info(f"Worker {worker_id}: Fetched and stored {len(persons)} persons")
    return f"fetch_and_store_relationships_{worker_id}"

def fetch_and_store_relationships(worker_id: int, offset: int, limit: int, **kwargs):
    persons = kwargs["ti"].xcom_pull(key=f"persons_{worker_id}_{offset}_{limit}")
    relationships = get_relationships(offset, limit, persons, settings.relationship_types)
    
    if not relationships:
        return f"stop_processing_relationships_{worker_id}"

    driver = create_connection(settings)
    insert_relationships(driver, relationships)
    logger.info(f"Worker {worker_id}: Fetched and stored {len(relationships)} relationships")
    return f"fetch_and_store_persons_{worker_id}"

for i in range(settings.num_workers):
    offset = i * settings.items_per_worker

    branch_fetch_and_store_persons = BranchPythonOperator(
        task_id=f"branch_fetch_and_store_persons_{i}",
        python_callable=fetch_and_store_persons,
        op_args=[i, offset, settings.items_per_worker],
        provide_context=True,
        dag=dag,
    )

    branch_fetch_and_store_relationships = BranchPythonOperator(
        task_id=f"branch_fetch_and_store_relationships_{i}",
        python_callable=fetch_and_store_relationships,
        op_args=[i, offset, settings.items_per_worker],
        provide_context=True,
        dag=dag,
    )

    stop_processing_persons = PythonOperator(
        task_id=f"stop_processing_persons_{i}",
        python_callable=lambda: None,
        dag=dag,
    )

    stop_processing_relationships = PythonOperator(
        task_id=f"stop_processing_relationships_{i}",
        python_callable=lambda: None,
        dag=dag,
    )

    branch_fetch_and_store_persons >> [branch_fetch_and_store_relationships, stop_processing_persons]
    branch_fetch_and_store_relationships >> [branch_fetch_and_store_persons, stop_processing_relationships]
