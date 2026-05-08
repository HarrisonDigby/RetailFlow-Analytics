# RetailFlow Analytics Platform

End-to-end data engineering portfolio project.

## Goal

Build a realistic cloud data platform for a fake retail/e-commerce business.

The project will ingest raw business data, store it in a data lake, load it into a cloud data warehouse, transform it into analytics-ready models, validate data quality, and visualise business KPIs in Power BI.

## Planned Architecture

Raw CSV/API data  
→ AWS S3 data lake  
→ Snowflake cloud data warehouse  
→ dbt transformations  
→ fact/dimension data model  
→ data quality checks  
→ Power BI dashboard  
→ Airflow orchestration  
→ GitHub Actions CI  
→ Docker/Terraform polish

## SQL Files

The `sql/` folder contains the Snowflake SQL used to create the initial cloud warehouse structure for this project.

At this stage, the SQL is being written and run manually in Snowflake to build a proper understanding of the platform fundamentals: warehouses, databases, schemas, raw tables, and data loading.

This manual setup is intentional. Later in the project, parts of the infrastructure will be automated with tools such as Terraform, and raw file storage will be moved into AWS S3 to reflect a more production-like cloud data workflow.

The SQL files are included in the repo so the Snowflake setup is visible, documented, and version-controlled rather than only existing inside the Snowflake UI.

## Current Phase

Phase 1: Build the local-to-Snowflake foundation.

Current work includes:

- generating realistic raw retail source data locally
- validating raw data with pandas
- preparing standardised CSV files for warehouse loading
- manually creating the initial Snowflake warehouse structure with SQL
- creating raw Snowflake tables to receive the prepared data

The manual Snowflake setup is intentional at this stage to build a clear understanding of the platform before adding AWS S3, dbt, Airflow, GitHub Actions, Docker, and Terraform later.

The project currently includes the first end-to-end local-to-Snowflake data loading flow:

```
Raw generated CSVs
→ pandas validation
→ pandas preparation
→ processed CSVs
→ Snowflake internal stage
→ Snowflake RAW tables
```


The Snowflake warehouse now includes a basic analytics modelling structure:

```
RAW tables
→ STAGING views
→ MARTS fact and dimension tables
```

The MARTS layer contains reporting-ready tables such as fact_orders, fact_ad_spend, fact_refunds, dim_customers, dim_products, and dim_date. These tables are designed for BI analysis and will later be connected to Power BI.

The Snowflake marts layer now includes SQL-based data quality checks. These checks validate that reporting tables contain data, order IDs are unique, relationships between fact and dimension tables are intact, numeric business values are non-negative, and refund dates are logically valid.