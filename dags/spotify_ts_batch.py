from datetime import datetime
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.standard.operators.bash import BashOperator

DBT_DIR = '/opt/airflow/dbt_venv/bin/dbt'
DBT_PROJECT_DIR = '/opt/airflow/dbt/spotify_ts'
DBT_PROFILES_DIR = '/home/airflow/.dbt'


with DAG (
    dag_id = "spotify_ts_batch",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["spotify_ts","batch","dbt"],
    doc_md="__doc__"
) as DAG:
    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=f"{DBT_DIR} build --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROFILES_DIR}"
    )

dbt_build

