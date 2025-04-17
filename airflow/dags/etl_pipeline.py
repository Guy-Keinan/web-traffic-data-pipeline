import sys
import os

sys.path.append("/opt/airflow/python/scripts")

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from generate_data import main as generate_data_main

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "web_traffic_etl_pipeline",
    default_args=default_args,
    description="Web Traffic ETL pipeline",
    schedule_interval="@daily",
    start_date=datetime(2025, 4, 11),
    catchup=False,
)

generate_data = PythonOperator(
    task_id="generate_web_traffic_data",
    python_callable=generate_data_main,
    dag=dag,
)


def upload_to_s3():
    import boto3

    s3 = boto3.client("s3")
    s3.upload_file(
        Filename="/opt/airflow/python/scripts/web_traffic_data.csv",
        Bucket="web-traffic-bucket-52fqs7r",
        Key="raw/web_traffic_data.csv",
    )


upload_data = PythonOperator(
    task_id="upload_data_to_s3",
    python_callable=upload_to_s3,
    dag=dag,
)

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

run_spark_job = BashOperator(
    task_id="run_spark_job",
    bash_command=f"docker exec -e AWS_ACCESS_KEY_ID={aws_access_key} -e AWS_SECRET_ACCESS_KEY={aws_secret_key} spark spark-submit /opt/bitnami/spark/src/job.py",
    dag=dag,
)


def generate_report():
    import pandas as pd
    import os

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    s3_path = "s3://web-traffic-bucket-52fqs7r/processed/web_traffic_data.parquet"
    output_path = "/opt/airflow/python/scripts/web_traffic_report.csv"

    df = pd.read_parquet(
        s3_path,
        engine="pyarrow",
        storage_options={
            "key": AWS_ACCESS_KEY_ID,
            "secret": AWS_SECRET_ACCESS_KEY,
        },
    )

    report = df["page"].value_counts().reset_index()
    report.columns = ["page", "visit_count"]

    report.to_csv(output_path, index=False)
    print(f"Report generated at {output_path}")


generate_report_task = PythonOperator(
    task_id="generate_web_traffic_report",
    python_callable=generate_report,
    dag=dag,
)

generate_data >> upload_data >> run_spark_job >> generate_report_task
