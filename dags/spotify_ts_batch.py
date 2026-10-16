from datetime import datetime
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQuery
from airflow.providers.standard.operators.bash import BashOperator

DBT_DIR = '/opt/airflow/dbt_venv/bin/dbt'
DBT_PROJECT_DIR = ''


with DAG (
    dag_id = "spotify_ts_batch",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily"
    catchup=False,
    tags=["spotify_ts","batch","dbt"]
    doc_md="__doc__"
) as DAG:
    reload_data_raw = SQLExecuteQuery(
        task_id="reload_raw"
        conn_id="snowflake_default",
        sql=COPY_RAW
        split_statements=True,
        autocommit=True,
    )

    dbt_build_code = BashOperator(
        task_id="build_dbt_core"
        bash_command="{dbt} build --project-dir {DBT_PROJECT_DIR}"
    )
