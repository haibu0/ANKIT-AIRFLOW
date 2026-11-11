from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.amazon.aws.sensors.sqs import SqsSensor

DBT_DIR = '/opt/airflow/dbt_venv/bin/dbt'
DBT_PROJECT_DIR = '/opt/airflow/dbt/spotify_ts'
DBT_PROFILES_DIR = '/home/airflow/.dbt'


with DAG (
    dag_id = "spotify_ts_batch",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["spotify_ts","batch","dbt"],
    max_active_runs=1,
    doc_md="__doc__"
) as DAG:
    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=f"{DBT_DIR} build --exclude tag:ai --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROFILES_DIR}"
    )
    
    enrich_tracks = BashOperator(
        task_id="enrich_tracks",
        bash_command=f"python opt/airflow/ai/enrich_reviews.py"
    )

    dbt_build_ai = BashOperator(
        task_id="dbt_build_ai",
        bash_command=f"{DBT_DIR} build --select tag:ai --project-dir {DBT_DIR} --profiles-dir {DBT_PROFILES_DIR}"
    )

dbt_build >> enrich_tracks >> dbt_build_ai


