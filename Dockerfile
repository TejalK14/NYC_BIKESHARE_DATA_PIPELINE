FROM quay.io/astronomer/astro-runtime:12.7.1-python-3.11

USER root
RUN apt-get update && apt-get install -y wget unzip
USER astro

RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-bigquery==1.8.0 && deactivate

ENV AIRFLOW_VAR_PROJECT_NAME='nyc-bike-share-de-project'   
ENV AIRFLOW_VAR_BUCKET_NAME='nyc-bike-share-2025-bucket'
ENV AIRFLOW_VAR_DATASET_NAME='NYC_BIKE_SHARE_dataset'
ENV AIRFLOW_VAR_EXTERNAL_TBL_NAME='NYC_BIKE_SHARE_data_external'