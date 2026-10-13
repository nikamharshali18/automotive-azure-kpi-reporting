# Azure Data Factory pipeline

Pipeline name: `pl_automotive_kpi_reporting`.

1. Create an ADLS Gen2 account and `bronze`, `silver`, `gold` containers.
2. Create linked service `ls_adls_gen2` using managed identity where supported.
3. Create linked service `ls_azure_databricks`.
4. Create Copy activities for `production.csv`, `sales.csv`, and `quality.csv` into `bronze/automotive/`.
5. After all three Copy activities succeed, run notebook `01_bronze_to_silver.py`.
6. On success, run `02_silver_to_gold.py`.
7. On success, run `03_data_quality_checks.py`.
8. Configure monitoring, retry policy, failure alerts, and audit logging.

Do not put storage keys or tokens in notebook source or Git. Grant only the required permissions. This file is a setup guide, not an exported ADF pipeline JSON.
