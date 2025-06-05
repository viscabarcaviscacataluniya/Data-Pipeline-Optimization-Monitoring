FROM quay.io/astronomer/astro-runtime:12.2.0

COPY requirements.txt /usr/local/airflow/requirements.txt
RUN pip install --no-cache-dir -r /usr/local/airflow/requirements.txt