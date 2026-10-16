"""Batch load Spotify time-series data into Snowflake, then run dbt."""
from datetime import datetime

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.standard.operators.bash import BashOperator

# Paths inside the Airflow container (adjust to where you mount dbt)
DBT_BIN = "/opt/airflow/dbt_venv/bin/dbt"
DBT_PROJECT_DIR = "/opt/airflow/dbt/spotify_ts"
DBT_PROFILES_DIR = "/home/airflow/.dbt"


with DAG(
    dag_id="spotify_ts_batch",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["spotify_ts", "batch", "dbt"],
    doc_md=__doc__,
) as dag:

    dbt_build = BashOperator(
        task_id="build_dbt_core",
        bash_command=(
            f"{DBT_BIN} build "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROFILES_DIR}"
        ),
    )

dbt_build