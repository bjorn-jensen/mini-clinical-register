# Mini Clinical Register – SQL & KPI Analysis

## Purpose
This project demonstrates the design and analysis of a relational clinical data model using synthetic patient-level data. The objective is to simulate typical healthcare data tasks, including readmission analysis and stratified KPI reporting.

## Data Model
Tables:
- patients
- admissions
- diagnoses
- treatments

Primary/foreign keys enforce referential integrity.

## Key Analyses
- 30-day readmission rate
- Readmission rate stratified by sex and age group
- Top diagnoses associated with readmissions

## Tech Stack
- Python (synthetic data generation)
- PostgreSQL (relational data model)
- SQL (window functions, aggregation)
- Power BI (visualization layer)

## Notes
All data in this repository is synthetically generated for demonstration purposes.
