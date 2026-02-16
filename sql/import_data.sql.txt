\cd ../data/raw

\copy patients   FROM 'patients.csv'   WITH (FORMAT csv, HEADER true);
\copy admissions FROM 'admissions.csv' WITH (FORMAT csv, HEADER true);
\copy diagnoses  FROM 'diagnoses.csv'  WITH (FORMAT csv, HEADER true);
\copy treatments FROM 'treatments.csv' WITH (FORMAT csv, HEADER true);
