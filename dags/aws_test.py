from datetime import datetime

from airflow import DAG
from airflow.providers.amazon.aws.sensors.sqs import SqsSensor
from airflow.providers.standard.operators.bash import BashOperator

SQS_QUEUE_URL = 'https://sqs.us-east-2.amazonaws.com/047719649991/spotify-airflow-events'

with DAG(
    dag_id="aws_test",
    start_date=datetime(2024, 1, 1),
    schedule="@continuous",
    catchup=False,
    max_active_runs=1,
    tags=["aws", "test", "sqs"],
) as dag:

    wait_for_s3_event = SqsSensor(
        task_id="wait_for_s3_event",
        sqs_queue=SQS_QUEUE_URL,
        aws_conn_id="aws_default",
        region_name="us-east-2",
        max_messages=1,
        wait_time_seconds=20,
        poke_interval=30,
        timeout=604800,
)

    print_notification = BashOperator(
        task_id="print_notification",
        bash_command='echo "=== SQS notification received! S3 event sensor triggered successfully. ==="',
    )

    wait_for_s3_event >> print_notification
