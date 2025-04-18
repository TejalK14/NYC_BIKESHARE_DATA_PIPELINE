BATCH PIPELINE FOR NYC BIKE SHARE DATA USING ASTRO AIRFLOW, DOCKER, COSMOS, DBT, GOOGLE CLOUD STORAGE, GCP BIG QUERY 
========

This is a batch data pipeline for NYC BIKE SHARE DATA publicly available here https://citibikenyc.com/system-data. It extracts data from 2022 - 2025 and loads the data into staging environment and then performs tranformations on the data using DBT and loads the transformed data back into GCP biquery for further analysis.

## Table of Contents

 1. [Architecture](#subheading-1)
 2. [Project Structure](#subheading-2)
 3. [Installation Guide](#subheading-3)
 4. [Data Sources](#subheading-4)
 5. [Usage](#subheading-5)
 6. [Visualizations](#subheading-6)
 7. [Technologies Used](#subheading-7)
 8. [Results](#subheading-8)

## Architecture
================
Content of the subheading 1

## Project Structure
=====================
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
=======================
## Prerequisites - you will need the following installed on your local machine
- Docker - install docker and validate it by running - docker --version
- Astro CLI - install astro cli as per instrustion here https://www.astronomer.io/docs/astro/cli/install-cli/
- Terraform - install Terraform( use hashicorp terraform from your visual studio code) and validate it by running command: terraform --version 
- GC account 

1. Clone the respository:


## Data Sources
=======================
Content of the subheading 4

## Usage
=======================
Content of the subheading 3

## Visualizations
=======================
Content of the subheading 3

## Technologies Used
=======================
Content of the subheading 3

## Results
=======================
Content of the subheading 3





Project Contents
================

This project contains the following files and folders:

- dags: This folder contains the Python files for your Airflow DAGs.
- Dockerfile: This file contains a versioned Astro Runtime Docker image that provides a differentiated Airflow experience. If you want to execute other commands or overrides at runtime, specify them here.
- include: This folder contains any additional files that you want to include as part of your project. It is empty by default.
- packages.txt: Install OS-level packages needed for your project by adding them to this file. It is empty by default.
- requirements.txt: Install Python packages needed for your project by adding them to this file. It is empty by default.
- plugins: Add custom or community plugins for your project to this file. It is empty by default.
- airflow_settings.yaml: Use this local-only file to specify Airflow Connections, Variables, and Pools instead of entering them in the Airflow UI as you develop DAGs in this project.

Deploy Your Project Locally
===========================

1. Start Airflow on your local machine by running 'astro dev start'.

This command will spin up 4 Docker containers on your machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Webserver: The Airflow component responsible for rendering the Airflow UI
- Scheduler: The Airflow component responsible for monitoring and triggering tasks
- Triggerer: The Airflow component responsible for triggering deferred tasks

2. Verify that all 4 Docker containers were created by running 'docker ps'.

Note: Running 'astro dev start' will start your project with the Airflow Webserver exposed at port 8080 and Postgres exposed at port 5432. If you already have either of those ports allocated, you can either [stop your existing Docker containers or change the port](https://www.astronomer.io/docs/astro/cli/troubleshoot-locally#ports-are-not-available-for-my-local-airflow-webserver).

3. Access the Airflow UI for your local Airflow project. To do so, go to http://localhost:8080/ and log in with 'admin' for both your Username and Password.

You should also be able to access your Postgres Database at 'localhost:5432/postgres'.
