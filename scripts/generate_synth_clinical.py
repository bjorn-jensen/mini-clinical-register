import numpy as np
import pandas as pd
from datetime import datetime, timedelta

rng = np.random.default_rng(42)

N_PATIENTS = 5000
AVG_ADMISSIONS_PER_PATIENT = 2.6  # juster for flere/færre indlæggelser
READMIT_PROB = 0.22               # andel indlæggelser der får genindlæggelse < 30 dage

START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2025, 12, 31)

# --- 1) Patients ---
patient_ids = np.arange(1, N_PATIENTS + 1)

sex = rng.choice(["M", "F"], size=N_PATIENTS, p=[0.49, 0.51])
birth_year = rng.integers(1940, 2006, size=N_PATIENTS)  # 18-85ish i perioden
municipality = rng.choice(
    ["København", "Frederiksberg", "Odense", "Aarhus", "Roskilde", "Helsingør", "Hillerød"],
    size=N_PATIENTS
)

patients = pd.DataFrame({
    "patient_id": patient_ids,
    "sex": sex,
    "birth_year": birth_year,
    "municipality": municipality
})

# --- Hjælpefunktioner ---
def random_date_between(start: datetime, end: datetime) -> datetime:
    delta_days = (end - start).days
    return start + timedelta(days=int(rng.integers(0, delta_days + 1)))

def clamp_date(d: datetime) -> datetime:
    if d < START_DATE: return START_DATE
    if d > END_DATE: return END_DATE
    return d

# --- 2) Admissions ---
departments = ["Akut", "Medicin", "Kirurgi", "Ortopædi", "Kardiologi", "Neurologi"]
admission_rows = []
admission_id = 1

for pid, by in zip(patient_ids, birth_year):
    # antal indlæggelser pr patient (Poisson, min 1)
    k = max(1, int(rng.poisson(AVG_ADMISSIONS_PER_PATIENT)))
    # første indlæggelse placeres tilfældigt i perioden
    first_adm_date = random_date_between(START_DATE, END_DATE - timedelta(days=10))

    # lav en tidslinje per patient
    current_date = first_adm_date

    for i in range(k):
        # indlæggelseslængde 1-12 dage (skæv fordeling)
        length_of_stay = int(np.clip(rng.gamma(shape=2.0, scale=2.0), 1, 12))
        admit_date = clamp_date(current_date)
        discharge_date = clamp_date(admit_date + timedelta(days=length_of_stay))

        dept = rng.choice(departments)
        admission_rows.append({
            "admission_id": admission_id,
            "patient_id": pid,
            "admit_date": admit_date.date().isoformat(),
            "discharge_date": discharge_date.date().isoformat(),
            "department": dept
        })

        # beslutter om næste indlæggelse bliver en genindlæggelse (<30 dage)
        if rng.random() < READMIT_PROB:
            gap_days = int(rng.integers(1, 30))  # inden for 30 dage
        else:
            gap_days = int(rng.integers(35, 250))  # længere ude

        # næste indlæggelse starter efter udskrivelse + gap
        current_date = discharge_date + timedelta(days=gap_days)

        admission_id += 1

admissions = pd.DataFrame(admission_rows)

# Trim eventuelle indlæggelser der ender uden for perioden (pga gaps)
admissions = admissions[
    (pd.to_datetime(admissions["admit_date"]) >= pd.Timestamp(START_DATE.date())) &
    (pd.to_datetime(admissions["admit_date"]) <= pd.Timestamp(END_DATE.date()))
].copy()

# reindex admission_id til at være kompakt (valgfrit)
admissions = admissions.sort_values(["patient_id", "admit_date"]).reset_index(drop=True)
admissions["admission_id"] = np.arange(1, len(admissions) + 1)

# --- 3) Diagnoses ---
# simple “ICD-lignende” koder
diag_codes = ["I10", "E11", "J18", "K35", "S72", "I21", "G40", "N39", "A09", "M54"]

diag_rows = []
diag_id = 1

for adm_id in admissions["admission_id"].values:
    n_diag = int(rng.integers(1, 4))  # 1-3 diagnoser
    codes = rng.choice(diag_codes, size=n_diag, replace=False if n_diag <= len(diag_codes) else True)
    for c in codes:
        diag_rows.append({
            "diagnosis_id": diag_id,
            "admission_id": adm_id,
            "diagnosis_code": c
        })
        diag_id += 1

diagnoses = pd.DataFrame(diag_rows)

# --- 4) Treatments ---
treat_codes = ["LAB", "XRAY", "CT", "SURG", "MED", "PHYS"]  # simple behandlingskoder
treat_rows = []
treat_id = 1

for adm_id in admissions["admission_id"].values:
    n_treat = int(rng.integers(0, 3))  # 0-2 behandlinger
    if n_treat == 0:
        continue
    codes = rng.choice(treat_codes, size=n_treat, replace=False if n_treat <= len(treat_codes) else True)
    for c in codes:
        treat_rows.append({
            "treatment_id": treat_id,
            "admission_id": adm_id,
            "treatment_code": c
        })
        treat_id += 1

treatments = pd.DataFrame(treat_rows)

# --- 5) Save ---
patients.to_csv("patients.csv", index=False)
admissions.to_csv("admissions.csv", index=False)
diagnoses.to_csv("diagnoses.csv", index=False)
treatments.to_csv("treatments.csv", index=False)

