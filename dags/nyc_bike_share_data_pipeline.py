import os
import pyarrow.parquet as pq
import pyarrow.csv as pv
import pyarrow as pa
import requests
import json
import pandas as pd
from airflow import DAG
from airflow.decorators import dag, task
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from  astro import sql as aql
from  astro.files import File
from  astro.sql.table import Table, Metadata
from  astro.constants import FileType
from include.dbt.cosmos_config import DBT_PROJECT_CONFIG, DBT_CONFIG
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.constants import LoadMode
from cosmos.config import RenderConfig


data_folder = "/usr/local/airflow/data"
PROJECTNAME = os.getenv("AIRFLOW_VAR_PROJECT_NAME")
BUCKETNAME = os.getenv("AIRFLOW_VAR_BUCKET_NAME")
DATASETNAME = os.getenv("AIRFLOW_VAR_DATASET_NAME")
EXTERNALTBLNAME = os.getenv("AIRFLOW_VAR_EXTERNAL_TBL_NAME")


# upload csv files to google cloud storage
def upload_to_gcs(data_folder, gcs_path,**kwargs):
    data_folder = data_folder
    gcs_conn_id = 'gcp'
    # List all csv files in the data folder
    csv_files = [file for file in os.listdir(data_folder) if file.endswith('.csv')]

    # Upload each CSV file to GCS
    for csv_file in csv_files:
        local_file_path = os.path.join(data_folder, csv_file)
        gcs_file_path = f"{gcs_path}/{csv_file}"
        upload_task = LocalFilesystemToGCSOperator(
            task_id=f'upload_to_gcs',
            src=local_file_path,
            dst=gcs_file_path,
            bucket=BUCKETNAME,
            gcp_conn_id=gcs_conn_id,
        )
        upload_task.execute(context=kwargs)

#extract station_info
def extract_stn_info():
    url = "https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_information.json"
    response = requests.get(url)
    if response.status_code == 200:
        stn_info = response.text
    else:
        print(f"Error:{response.status_code}")
    stn_info_json = json.loads(stn_info)
    stn_info_parsed = pd.json_normalize(stn_info_json["data"], "stations")
    stn_info_parsed.drop(['rental_uris.ios','rental_uris.android'],axis=1, inplace=True)
    stn_info_parsed.to_csv(f'{data_folder}/station_info.csv',index=False)

#extract region lookup
def extract_rgn_info():
    url = "https://gbfs.lyft.com/gbfs/2.3/bkn/en/system_regions.json"
    response = requests.get(url)
    if response.status_code == 200:
        rgn_info = response.text
    else:
        print(f"Error:{response.status_code}")
    rgn_info_json = json.loads(rgn_info)
    rgn_info_parsed = pd.json_normalize(rgn_info_json["data"], "regions")
    rgn_info_parsed.to_csv(f'{data_folder}/region_lookup.csv',index=False)

# create external table
CREATE_EXTERNAL_TABLES_SQL = f"""
CREATE OR REPLACE EXTERNAL TABLE `{PROJECTNAME}.{DATASETNAME}.{EXTERNALTBLNAME}`
                            OPTIONS (
                            format = 'CSV',
                            uris = ['gs://{BUCKETNAME}/raw/JC*.csv'],
                            skip_leading_rows = 1
                            );"""
 
with DAG(
    "nyc_bike_share_data_pipeline",
    start_date=datetime(2025, 4, 6),
    schedule_interval=None,
    catchup=False,
    ) as dag:
    download_and_unzip_22_24 = BashOperator(
        task_id="download_and_unzip_22_24",
        bash_command=f""" mkdir -p {data_folder} && echo https://s3.amazonaws.com/tripdata/JC-{{2022..2024}}{{01..12}}-citibike-tripdata.csv.zip | xargs -n 1 -P 2 wget -P {data_folder}/ || true"""  # && unzip '{data_folder}/*.zip' -d {data_folder}"""
    )
    download_and_unzip_25 = BashOperator(
        task_id="download_and_unzip_25",
        bash_command=f""" echo https://s3.amazonaws.com/tripdata/JC-2025{{01..03}}-citibike-tripdata.csv.zip | xargs -n 1 -P 2 wget -P {data_folder}/ || true && unzip '{data_folder}/*.zip' -d {data_folder}"""
    )
    remove_zip_file = BashOperator(
        task_id ="remove_zip_and_csv_file",
        bash_command = f"rm {data_folder}/*.zip"
    )
    extract_station_info = PythonOperator(
        task_id="extract_station_info",
        python_callable=extract_stn_info,
    )
    extract_region_info = PythonOperator(
        task_id="extract_region_info",
        python_callable=extract_rgn_info,
    )
    upload_raw_data_to_gcs = PythonOperator(
        task_id="upload_raw_data_to_gcs",
        python_callable=upload_to_gcs,
        op_args=[data_folder, 'raw'],
        provide_context=True
    )
    create_external_tables = BigQueryInsertJobOperator(
        task_id="create_external_table",
        configuration={
            "query": {
                "query": CREATE_EXTERNAL_TABLES_SQL,
                "useLegacySql":False,
            }
        },
        location="US",
        gcp_conn_id='gcp'
    )
    load_station_info_gcs_to_bigquery = GCSToBigQueryOperator(
        task_id="load_station_info_gcs_to_bigquery",
        source_objects=['raw/station_info.csv'],
        source_format="CSV",
        skip_leading_rows=1,
        destination_project_dataset_table=f"{DATASETNAME}.station_info",
        write_disposition="WRITE_TRUNCATE",
        bucket=BUCKETNAME,
        gcp_conn_id='gcp',
    )
    load_region_lookup_gcs_to_bigquery = GCSToBigQueryOperator(
        task_id="load_region_lookup_gcs_to_bigquery",
        source_objects=['raw/region_lookup.csv'],
        source_format="CSV",
        skip_leading_rows=1,
        destination_project_dataset_table=f"{DATASETNAME}.region_lookup",
        write_disposition="WRITE_TRUNCATE",
        bucket=BUCKETNAME,
        gcp_conn_id='gcp',
    )
    transform = DbtTaskGroup(
        group_id="transform",
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/transform']
        )
    )
    remove_all_files_from_local_folder = BashOperator(
        task_id ="remove_all_files_from_local_folder",
        bash_command = f"rm {data_folder}/*.csv"
    )
    download_and_unzip_22_24 >> download_and_unzip_25 >> remove_zip_file >> extract_station_info >> extract_region_info >> upload_raw_data_to_gcs  >> create_external_tables >> load_station_info_gcs_to_bigquery >> load_region_lookup_gcs_to_bigquery >> transform >> remove_all_files_from_local_folder
