-- KPI 1: Readmission rate < 30 days
WITH ordered AS (
  SELECT
    patient_id,
    admission_id,
    admit_date,
    discharge_date,
    LAG(discharge_date) OVER (
      PARTITION BY patient_id
      ORDER BY admit_date
    ) AS prev_discharge
  FROM admissions
),
flags AS (
  SELECT
    *,
    CASE
      WHEN prev_discharge IS NOT NULL
       AND (admit_date - prev_discharge) BETWEEN 1 AND 30
      THEN 1 ELSE 0
    END AS is_readmission_30d
  FROM ordered
)
SELECT
  ROUND(AVG(is_readmission_30d::numeric) * 100, 2) AS readmission_rate_pct,
  SUM(is_readmission_30d) AS readmissions_30d,
  COUNT(*) AS total_admissions
FROM flags;

-- KPI 2: Readmission rate by sex
WITH ordered AS (
  SELECT
    a.patient_id,
    a.admission_id,
    a.admit_date,
    a.discharge_date,
    p.sex,
    LAG(a.discharge_date) OVER (
      PARTITION BY a.patient_id
      ORDER BY a.admit_date
    ) AS prev_discharge
  FROM admissions a
  JOIN patients p USING (patient_id)
),
flags AS (
  SELECT
    *,
    CASE
      WHEN prev_discharge IS NOT NULL
       AND (admit_date - prev_discharge) BETWEEN 1 AND 30
      THEN 1 ELSE 0
    END AS is_readmission_30d
  FROM ordered
)
SELECT
  sex,
  ROUND(AVG(is_readmission_30d::numeric) * 100, 2) AS readmission_rate_pct,
  SUM(is_readmission_30d) AS readmissions_30d,
  COUNT(*) AS total_admissions
FROM flags
GROUP BY sex
ORDER BY sex;

-- KPI 3: Readmission rate by age group
WITH ordered AS (
  SELECT
    a.patient_id,
    a.admission_id,
    a.admit_date,
    a.discharge_date,
    p.birth_year,
    EXTRACT(YEAR FROM a.admit_date) - p.birth_year AS age,
    LAG(a.discharge_date) OVER (
      PARTITION BY a.patient_id
      ORDER BY a.admit_date
    ) AS prev_discharge
  FROM admissions a
  JOIN patients p USING (patient_id)
),
flags AS (
  SELECT *,
    CASE
      WHEN prev_discharge IS NOT NULL
       AND (admit_date - prev_discharge) BETWEEN 1 AND 30
      THEN 1 ELSE 0
    END AS is_readmission_30d
  FROM ordered
),
age_groups AS (
  SELECT *,
    CASE
      WHEN age < 30 THEN 'Under 30'
      WHEN age BETWEEN 30 AND 49 THEN '30-49'
      WHEN age BETWEEN 50 AND 69 THEN '50-69'
      ELSE '70+'
    END AS age_group
  FROM flags
)
SELECT
  age_group,
  ROUND(AVG(is_readmission_30d::numeric) * 100, 2) AS readmission_rate_pct,
  SUM(is_readmission_30d) AS readmissions_30d,
  COUNT(*) AS total_admissions
FROM age_groups
GROUP BY age_group
ORDER BY age_group;

-- KPI 4: Top 5 diagnoses among readmissions
WITH ordered AS (
  SELECT
    a.patient_id,
    a.admission_id,
    a.admit_date,
    a.discharge_date,
    LAG(a.discharge_date) OVER (
      PARTITION BY a.patient_id
      ORDER BY a.admit_date
    ) AS prev_discharge
  FROM admissions a
),
flags AS (
  SELECT *,
    CASE
      WHEN prev_discharge IS NOT NULL
       AND (admit_date - prev_discharge) BETWEEN 1 AND 30
      THEN 1 ELSE 0
    END AS is_readmission_30d
  FROM ordered
)
SELECT
  d.diagnosis_code,
  COUNT(*) AS readmission_count
FROM flags f
JOIN diagnoses d ON f.admission_id = d.admission_id
WHERE f.is_readmission_30d = 1
GROUP BY d.diagnosis_code
ORDER BY readmission_count DESC
LIMIT 5;
