from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "dima",
    "retries": 1,
}

with DAG(
    dag_id="govcon_pipeline",
    default_args=default_args,
    description="Extract, load, and transform GovCon contract data",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["govcon"],
) as dag:

    extract = BashOperator(
        task_id="extract_awards",
        bash_command="python /usr/local/airflow/include/src/extract/explore_api.py",
    )

    load = BashOperator(
        task_id="load_to_duckdb",
        bash_command="python /usr/local/airflow/include/src/extract/load_to_duckdb.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /usr/local/airflow/include/govcon_dbt && dbt run",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /usr/local/airflow/include/govcon_dbt && dbt test",
    )

    extract >> load >> dbt_run >> dbt_test
