Airflow ETL Pipeline with PySpark and Google Cloud Dataproc
This project implements an ETL pipeline using Apache Airflow to automate data processing workflows on Google Cloud Platform (GCP). The pipeline performs daily analyses of vehicle data, intelligently differentiating between weekday and weekend processing by leveraging Google Cloud Dataproc clusters and storing the results in Google Cloud Storage (GCS). The workflow uploads PySpark scripts to GCS, creates and manages Dataproc clusters, executes day-specific data processing jobs, and cleans up resources after completion.

Table of Contents
Overview

Key Features

Key Components

Pipeline Structure

Prerequisites

Usage

Overview
This pipeline automates the ingestion and processing of vehicle data within GCP, utilizing Airflow's scheduling and orchestration features alongside GCP services like Dataproc and GCS. It incorporates branching logic to execute different Spark jobs depending on whether the day is a weekday or weekend.

Key Features
Dynamic Scheduling: Runs daily with tasks that adjust based on the day of the week.

PySpark Workflows: Executes tailored PySpark scripts for distinct weekday and weekend analyses.

Seamless Google Cloud Integration: Utilizes GCS for script storage and output, and Dataproc for running Spark jobs efficiently.

Key Components
Airflow DAG: Defines the ETL workflow, including tasks for uploading scripts, cluster creation, job submission, and cleanup.

Branching Logic: Uses a BranchPythonOperator to determine day type (weekday/weekend) and route execution accordingly.

Dataproc Clusters: Created and deleted dynamically to optimize resource use and cost.

Google Cloud Storage: Stores PySpark scripts and job output data.

Pipeline Structure
Upload Tasks: Transfers all local PySpark scripts from the specified directory to a GCS bucket.

Cluster Creation: Provisions a Dataproc cluster for running Spark jobs.

Branching: Identifies if the current day is a weekday or weekend and directs processing accordingly.

Data Processing:

Weekday Jobs: Runs multiple PySpark scripts analyzing metrics such as average speed, temperature, and tire pressure.

Weekend Job: Performs gas composition analysis.

Cluster Deletion: Terminates the Dataproc cluster after job completion to free up resources.

Prerequisites
A Google Cloud Project with Dataproc, GCS, and IAM permissions enabled.

An Apache Airflow environment configured with GCP connections.

Python version 3.7 or higher.

Airflow Connections
Ensure the following connections are configured in your Airflow environment:

gcp_default: Connection to GCP for accessing Dataproc and GCS.

airflow-bigquery-project: GCS bucket used for storing PySpark scripts and output data.

Usage
Place your PySpark scripts into the local directory specified (e.g., /usr/local/airflow/include/data/pyspark).

Deploy the DAG file into your Airflow environment.

Trigger the DAG manually or schedule it to run automatically.

Monitor execution logs and review output data in the Airflow UI and the configured GCS bucket.
