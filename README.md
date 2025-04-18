BATCH DATA PIPELINE FOR NYC BIKE SHARE
========
## Overview
This is a batch data pipeline for NYC BIKE SHARE DATA publicly available here https://citibikenyc.com/system-data. It extracts data from 2022 - 2025 and loads the data into staging environment and then performs tranformations on the data using DBT and loads the transformed data back into GCP biquery for further analysis.

## Key Features

- **Cloud-based Infrastructure**: Uses Google Cloud Platform (GCP cloud storage and big query) 
- **Terraform** - To define, build and manage Infrastructure as Code.
- **Workflow Orchestration**: Data ingestion, transformation, and visualization automated via DAG workflows using Astro Airflow.
- **Optimized Storage**: Data is partitioned for efficient querying.
- **Transformation with dbt**: Data cleaning and tranformation using dbt managed by cosmos in Astro airflow.
- **Data Visualization with Looker Studio**: Interactive dashboards for insights.


## Table of Contents

 1. [Architecture](#Architecture)
 2. [Project Structure](#Project-Structure)
 3. [Installation Guide](#Installation-Guide)
 4. [Data Sources](#Data-Sources)
 5. [Usage](#Usage)
 6. [Visualizations](#Vizualizations)
 7. [Technologies Used](#Technologies-Used)
 8. [Results](#Results)

## Architecture


## Project Structure

This project contains the following files and folders:
```
    /NYC_BIKE_SHARE_DE_PROJECT
    ├── .astro                  # Compiled files (alternatively `dist`)
    ├── dags                    # This folder contains the Python files for your Airflow DAGs.
    ├── include                 # This folder contains any additional files that you want to include as part of your project.
        ├── dbt                 # dbt transformations   
        ├── gcp                 # gcp folder to store service-account information
            ├── keys            # service account credentials(json file)
        ├──Terraform            # Terraform .tf files
    ├── requirements.txt        # list of required packages
    ├── packages.txt            # Install OS-level packages needed for your project by adding them to this file. 
    ├── Dockerfile              # This file contains a versioned Astro Runtime Docker image
    ├── plugins                 # Add custom or community plugins for your project to this file. It is empty by default.
    ├── airflow_settings.yaml   # Use this local-only file to specify Airflow Connections, Variables, and Pools.
    └── README.md               # project overview and instructions
```
## Installation Guide

Prerequisites - you will need the following installed on your local machine
- Docker - install docker and validate it by running - docker --version
- Astro CLI - install astro cli as per instrustion here https://www.astronomer.io/docs/astro/cli/install-cli/
- Terraform - install Terraform( use hashicorp terraform from your visual studio code) and validate it by running command: terraform --version 
- GC account 

1. **Clone the respository**:
```
git clone https://github.com/TejalK14/NYC_BIKESHARE_DATA_PIPELINE.git
```
2. Create GCS account and create a new project
3. Create a new service account for the project you created in step 2 (with BigQuery Admin and Storage Admin permissions)
4. Create key for your service account and save it as my-creds.json in the gcp/keys folder
5. Update the Terraform file variable.tf with your project name, region, location, dataset name and bucket name and run the following commands to create the gcp resources.
```
terraform init
terraform plan
terraform apply
```
  
6. Update the following environment variables in the dockerfile 
```
AIRFLOW_VAR_PROJECT_NAME
AIRFLOW_VAR_BUCKET_NAME
AIRFLOW_VAR_DATASET_NAME
AIRFLOW_VAR_EXTERNAL_TBL_NAME
```
7. Update the profiles.yml file in the include/dbt/ folder with your key file path, project name and dataset name
8. **Deploy Your Project Locally**
  -  Start Airflow on your local machine by running 'astro dev start'.

This command will spin up 4 Docker containers on your machine, each for a different Airflow component:

        - Postgres: Airflow's Metadata Database
        - Webserver: The Airflow component responsible for rendering the Airflow UI
        - Scheduler: The Airflow component responsible for monitoring and triggering tasks
        - Triggerer: The Airflow component responsible for triggering deferred tasks

  -  Verify that all 4 Docker containers were created by running 'docker ps'.

Note: Running 'astro dev start' will start your project with the Airflow Webserver exposed at port 8080 and Postgres exposed at port 5432. If you already have either of those ports allocated, you can either [stop your existing Docker containers or change the port](https://www.astronomer.io/docs/astro/cli/troubleshoot-locally#ports-are-not-available-for-my-local-airflow-webserver).

  -  Access the Airflow UI for your local Airflow project. To do so, go to http://localhost:8080/ and log in with 'admin' for both your Username and Password.
9. Run the nyc_bike_share_data_pipeline DAG on Airflow UI. It runs the following 
    - Downloads the the JC*.csv.zip files from https://s3.amazonaws.com/tripdata/index.html
    - Extracts the station information from https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_information.json
    - Extracts the region information from https://gbfs.lyft.com/gbfs/2.3/bkn/en/system_regions.json
    - Unzips the files
    - Uploads the files gcs bucket
    - loads the station information and region lookup files to big query 
    - creates external table for the main bike share data files
    - run transformations using dbt on the external table and creates a fnl_nyc_bike_share_data table with tranformed data
10. connect to looker studio using your gcp credentials and run vizualizations
11. Stop the pipeline
    ```
    astro dev stop
    ```
12. Destroy the gcp resources when done with project.
   ```
   terraform destroy
   ```

   

## Visualizations
Content of the subheading 3

## Technologies Used
Content of the subheading 3
USING ASTRO AIRFLOW, DOCKER, COSMOS, DBT, GOOGLE CLOUD STORAGE, GCP BIG QUERY

## Results
Content of the subheading 3

