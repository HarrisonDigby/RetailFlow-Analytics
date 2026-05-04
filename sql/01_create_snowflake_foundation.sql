-- Create the compute warehouse used to run queries and load data.
CREATE WAREHOUSE IF NOT EXISTS retailflow_wh
    WAREHOUSE_SIZE = XSMALL
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE;

-- Create the main project database.
CREATE DATABASE IF NOT EXISTS retailflow_db;

-- Set the active database before creating schemas inside it.
USE DATABASE retailflow_db;

-- Create the raw schema for source-like loaded data.
CREATE SCHEMA IF NOT EXISTS raw;

-- Create the staging schema for cleaned and standardised SQL models.
CREATE SCHEMA IF NOT EXISTS staging;

-- Create the marts schema for business-ready reporting tables.
CREATE SCHEMA IF NOT EXISTS marts;

-- Set the active warehouse for this session.
USE WAREHOUSE retailflow_wh;

-- Confirm the active Snowflake context.
SELECT
    CURRENT_ROLE(),
    CURRENT_DATABASE(),
    CURRENT_SCHEMA(),
    CURRENT_WAREHOUSE();