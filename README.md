<h1>Airflow ETL Pipeline with PySpark and Google Cloud Dataproc</h1>

<p>This project is an ETL pipeline using <strong>Apache Airflow</strong> to automate data processing tasks on <strong>Google Cloud Platform (GCP)</strong>. The pipeline performs daily analyses on vehicle data, dynamically handling weekday and weekend processing using Google Cloud Dataproc clusters and storing results in Google Cloud Storage (GCS). The DAG uploads PySpark scripts to GCS, creates a Dataproc cluster, processes data based on the day type, and cleans up resources post-processing.</p>

<h2>Table of Contents</h2>
<ul>
    <li><a href="#overview">Overview</a></li>
    <li><a href="#key-components">Key Components</a></li>
    <li><a href="#pipeline-structure">Pipeline Structure</a></li>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#usage">Usage</a></li>
</ul>

<h2 id="overview">Overview</h2>
<p>The pipeline automates data ingestion and processing tasks in GCP, leveraging Airflow's scheduling capabilities and GCP services such as Dataproc and GCS. The pipeline branches based on whether it's a weekday or weekend, running separate Spark jobs accordingly.</p>

<h3>Key Features</h3>
<ul>
    <li><strong>Dynamic Task Scheduling</strong>: Configured to run daily, adjusting tasks based on the day of the week.</li>
    <li><strong>PySpark Workflows</strong>: Processes data with specific PySpark scripts for weekend and weekday analyses.</li>
    <li><strong>Google Cloud Integration</strong>: Utilizes GCS for storage and Dataproc for Spark job execution.</li>
</ul>

<h2 id="key-components">Key Components</h2>
<ul>
    <li><strong>Airflow DAG</strong>: Defines the workflow, with tasks including file upload, Dataproc cluster management, and job submission.</li>
    <li><strong>Branching Logic</strong>: A BranchPythonOperator determines if it’s a weekday or weekend, allowing for targeted analyses.</li>
    <li><strong>Dataproc</strong>: Dynamically created and deleted for job execution, optimized for cost efficiency.</li>
    <li><strong>GCS</strong>: Stores input scripts and job outputs.</li>
</ul>

<h2 id="pipeline-structure">Pipeline Structure</h2>
<ul>
    <li><strong>Upload Tasks</strong>: Uploads all local PySpark scripts from the specified directory to a GCS bucket.</li>
    <li><strong>Cluster Creation</strong>: Creates a Dataproc cluster to run PySpark jobs.</li>
    <li><strong>Branching</strong>: Uses a BranchPythonOperator to identify weekday/weekend, routing to the appropriate jobs.</li>
    <li><strong>Data Processing</strong>: Executes PySpark jobs based on day type:
        <ul>
            <li><strong>Weekday Jobs</strong>: Runs multiple scripts for metrics like average speed, temperature, and tire pressure.</li>
            <li><strong>Weekend Job</strong>: Analyzes gas composition data.</li>
        </ul>
    </li>
    <li><strong>Cluster Deletion</strong>: Deletes the Dataproc cluster post-job completion, freeing resources.</li>
</ul>

<h2 id="prerequisites">Prerequisites</h2>
<ul>
    <li><strong>Google Cloud Project</strong> with enabled Dataproc, GCS, and IAM permissions.</li>
    <li><strong>Apache Airflow</strong> environment configured with GCP connections.</li>
    <li><strong>Python 3.7+</strong></li>
</ul>

<h3>Airflow Connections</h3>
<p>Set up the following connections in your Airflow environment:</p>
<ul>
    <li><code>gcp_default</code>: Connection to GCP for Dataproc and GCS.</li>
    <li><code>airflow-bigquery-project</code>: Bucket for storing PySpark scripts and output data.</li>
</ul>

<h2 id="usage">Usage</h2>
<ul>
    <li>Place PySpark scripts in the local directory specified (<code>/usr/local/airflow/include/data/pyspark</code>).</li>
    <li>Deploy the DAG file to your Airflow environment.</li>
    <li>Trigger the DAG or set it to run on a schedule.</li>
    <li>Review logs and outputs in the Airflow UI and GCS bucket.</li>
</ul>
