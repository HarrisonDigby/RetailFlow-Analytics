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

## Current Phase

Phase 1: Generate realistic raw source data locally.