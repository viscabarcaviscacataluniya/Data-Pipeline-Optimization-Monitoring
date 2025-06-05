from airflow.decorators import dag, task
from datetime import datetime
import os
from include.pipeline.etl import assess_day
from airflow.operators.python import PythonOperator
from airflow.operators.python import BranchPythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateClusterOperator,
    DataprocDeleteClusterOperator,
    DataprocSubmitJobOperator,
)

@dag(
    tags = ['etl', 'spark_jobs', 'pipeline'],
    schedule_interval = "0 15 * * *",
    default_args = {
        "owner": "Ahmed Ayodele",
        "start_date": datetime(2024, 10, 30),
        "retries": 1,
    },
    catchup = False,
    max_active_runs = 1, 
)

def spark_job():

    local_directory = "/usr/local/airflow/include/data/pyspark"  # Folder to upload  
    upload_tasks = []

    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(local_directory):
        for file in files:
            file_path = os.path.join(root, file)

            # Create the destination path in GCS, preserving the subdirectory structure
            relative_path = os.path.relpath(file_path, local_directory)
            gcs_destination_path = f"pyspark/{relative_path}"  # For example: pyspark/subdir/file.py

            # Create an upload task for each file
            upload_to_gcs = LocalFilesystemToGCSOperator(
                task_id = f"load_{relative_path.replace('/', '_')}_to_gcs", 
                src = file_path,
                dst = gcs_destination_path,
                bucket = "airflow-bigquery-project",
                gcp_conn_id = "gcp_default",
                mime_type = "application/octet-stream",  # General MIME type for binary files
                gzip = False,
            )
            upload_tasks.append(upload_to_gcs)

    cluster_config = {
        "master_config": {"num_instances": 1, "machine_type_uri": "n1-standard-2", "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 100}},
        "worker_config": {"num_instances": 2, "machine_type_uri": "n1-standard-2", "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 100}},
        "gce_cluster_config": {
            "internal_ip_only": False},
        "config_bucket": 'airflow-bigquery-project'
    }

    create_cluster = DataprocCreateClusterOperator(
        task_id = 'create_cluster',
        project_id = 'test-project-439910',
        cluster_name = f"spark-cluster-{{{{ ds_nodash }}}}", #time
        cluster_config = cluster_config,
        region = 'europe-west2',
        gcp_conn_id = 'gcp_default'
    )

    weekday_or_weekend = BranchPythonOperator(
        task_id = 'weekday_to_weekend',
        python_callable = assess_day,
        op_kwargs = {
            "execution_date" : "{{ ds }}",
        },
    )

    weekend_analytics = DataprocSubmitJobOperator(
        task_id = 'submit_weekend_job',
        job = {
            "reference": {"project_id": "test-project-439910"},
            "placement": {"cluster_name": f"spark-cluster-{{{{ ds_nodash }}}}"},
            "pyspark_job": {"main_python_file_uri": "gs://airflow-bigquery-project/pyspark/weekend/gas_composition_count.py"},
        },
        project_id = 'test-project-439910',
        region = 'europe-west2',
        gcp_conn_id = 'gcp_default'
    )

    weekday_scripts = [
        "gs://airflow-bigquery-project/pyspark/weekday/avg_speed.py",
        "gs://airflow-bigquery-project/pyspark/weekday/avg_temperature.py",
        "gs://airflow-bigquery-project/pyspark/weekday/avg_tire_pressure.py",
    ]

    # Loop to create DataprocSubmitJobOperator for each script
    weekday_tasks = []
    for i, script_path in enumerate(weekday_scripts, start = 1):
        weekday_task = DataprocSubmitJobOperator(
            task_id = f'submit_weekday_job_{i}',
            job = {
                "reference": {"project_id": "test-project-439910"},
                "placement": {"cluster_name": f"spark-cluster-{{{{ ds_nodash }}}}"},
                "pyspark_job": {"main_python_file_uri": script_path},
            },
            region='europe-west2',
            project_id='test-project-439910',
            gcp_conn_id='gcp_default'
        )
        weekday_tasks.append(weekday_task)

    delete_cluster = DataprocDeleteClusterOperator(
        task_id = "delete_cluster",
        project_id = "test-project-439910",
        cluster_name = f"spark-cluster-{{{{ ds_nodash }}}}",
        region = "europe-west2",
        trigger_rule = "all_done",
        gcp_conn_id = 'gcp_default'
    )

    upload_tasks >> create_cluster >> weekday_or_weekend
    weekday_or_weekend >> weekday_tasks >> delete_cluster
    weekday_or_weekend >> weekend_analytics >> delete_cluster


dag = spark_job()