# Mini Clinical Register – SQL & KPI Analysis

## Purpose
This project demonstrates the design and analysis of a relational clinical data model using synthetically generated patient-level data. The objective is to simulate analytical workflows typical in healthcare data environments, including 30-day readmission analysis and stratified KPI reporting.

All data is synthetically generated for demonstration purposes.

## Data Model
The database consists of four relational tables:
- patients
- admissions
- diagnoses
- treatments

The schema enforces:
- Primary key constraints
- Foreign key relationships
- Referential integrity
- Basic data validation checks
- Indexes are applied to support efficient joins and aggregation queries.

## Analytical Focus
The project includes SQL-based analyses covering:
- 30-day readmission rate
- Stratification by sex
- Stratification by age group
- Diagnosis-level breakdown of readmissions
- Window functions (LAG), aggregation logic, and CASE-based stratification are used to define and compute KPIs.

## KPI Definition

### 30-Day Readmission Rate

A 30-day readmission is defined as any admission occurring within 30 days of a previous discharge for the same patient.

Formally:

For each admission of a given patient:

- Let `PrevDischarge` be the previous discharge date.
- If the difference between admit_date and PrevDischarge is greater than 0 and less than or equal to 30 days, the admission is classified as a readmission.

The 30-day readmission rate is computed as:

Readmission Rate = (Number of readmissions within 30 days)/(Total number of eligible admissions)



## Technical Stack
- Python (synthetic data generation)
- PostgreSQL (relational database)
- SQL (window functions, joins, aggregation)
- Git (version control)

## Reproducibility
The repository contains:
- SQL scripts for table creation
- Import scripts for CSV data
- KPI query scripts
- Structured folder hierarchy separating raw data and analysis logic
- The project can be reproduced locally using PostgreSQL and the included SQL scripts.
