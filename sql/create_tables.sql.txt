-- PATIENTS
CREATE TABLE patients (
  patient_id   INT PRIMARY KEY,
  sex          CHAR(1) NOT NULL CHECK (sex IN ('M','F')),
  birth_year   INT NOT NULL CHECK (birth_year BETWEEN 1900 AND 2100),
  municipality TEXT
);

-- ADMISSIONS
CREATE TABLE admissions (
  admission_id   INT PRIMARY KEY,
  patient_id     INT NOT NULL REFERENCES patients(patient_id),
  admit_date     DATE NOT NULL,
  discharge_date DATE NOT NULL,
  department     TEXT,
  CHECK (discharge_date >= admit_date)
);

-- DIAGNOSES
CREATE TABLE diagnoses (
  diagnosis_id   INT PRIMARY KEY,
  admission_id   INT NOT NULL REFERENCES admissions(admission_id) ON DELETE CASCADE,
  diagnosis_code TEXT NOT NULL
);

-- TREATMENTS
CREATE TABLE treatments (
  treatment_id   INT PRIMARY KEY,
  admission_id   INT NOT NULL REFERENCES admissions(admission_id) ON DELETE CASCADE,
  treatment_code TEXT NOT NULL
);

-- Indexes (for performance on joins)
CREATE INDEX idx_admissions_patient_id ON admissions(patient_id);
CREATE INDEX idx_diagnoses_admission_id ON diagnoses(admission_id);
CREATE INDEX idx_treatments_admission_id ON treatments(admission_id);
