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
