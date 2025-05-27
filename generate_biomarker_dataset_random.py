# src/generate_biomarker_dataset_v2.py

import pandas as pd
import numpy as np
import uuid
import random
from datetime import date

np.random.seed(42)

def r(low, high):
    return round(random.uniform(low, high), 2)

VO2_MAX = {
    "male": {
        "20s": (35, 50), "30s": (33, 47), "40s": (30, 44),
        "50s": (28, 40), "60s": (25, 36), "70s": (22, 32),
    },
    "female": {
        "20s": (30, 45), "30s": (28, 42), "40s": (26, 39),
        "50s": (24, 36), "60s": (22, 32), "70s": (20, 28),
    },
}

def random_cycle_phase():
    return random.choice(["follicular", "ovulatory", "luteal"])

def generate_patient_record():
    sex = random.choice(["male", "female"])
    age = random.randint(20, 75)
    athlete = random.choice(["yes","no"])
    decade = f"{(age // 10) * 10}s"
    phase = random_cycle_phase() if sex == "female" else None

    record = {
        "patient_id": str(uuid.uuid4()),
        "collection_date": str(date.today()),
        "age": age,
        "sex": sex,
        "athlete": athlete,
    }

    # --- Cardiovascular Health ---
    hdl = r(40, 60) if sex == "male" else r(50, 70)
    ldl = r(80, 130)
    triglycerides = r(60, 180)
    total_cholesterol = hdl + ldl + (0.2 * triglycerides)
    record.update({
        "hdl_male": hdl if sex == "male" else None,
        "hdl_female": hdl if sex == "female" else None,
        "ldl": ldl,
        "triglycerides": triglycerides,
        "total_cholesterol": total_cholesterol,
        "lp(a)": r(10, 90),
        "apob": r(60, 120),
        "omega3_index": r(4, 8),
        "rdw": r(11, 14.5),
    })

    # --- Sleep ---
    record.update({
        "magnesium_rbc": r(4.2, 6.8),
        "vitamin_d": r(25, 70),
        "serum_ferritin": r(15, 150),
        "total_iron_binding_capacity": r(250, 450),
        "transferrin_saturation": r(20, 50),
        "hscrp": r(0.1, 3.0),
    })

    # --- Inflammation ---
    wbc = r(4.5, 9.5)
    lymphocytes = r(1.0, 3.5)
    neutrophils = r(2.0, 6.5)
    eosinophils = r(0.1, 0.5)
    record.update({
        "wbc": wbc,
        "lymphocytes": lymphocytes,
        "neutrophils": neutrophils,
        "eosinophils": eosinophils,
        "lymphocyte_percent": round((lymphocytes / wbc) * 100, 2),
        "neut_lymph_ratio": round(neutrophils / lymphocytes, 2),
    })

    # --- Metabolism ---
    glucose = r(75, 100)
    insulin = r(2.0, 15.0)
    record.update({
        "fasting_glucose": glucose,
        "fasting_insulin": insulin,
        "homa_ir": round((glucose * insulin) / 405, 2),
        "hba1c": r(4.8, 5.6),
        "alt_male": r(10, 50) if sex == "male" else None,
        "alt_female": r(7, 40) if sex == "female" else None,
        "uric_acid_male": r(3.5, 7.2) if sex == "male" else None,
        "uric_acid_female": r(2.5, 6.0) if sex == "female" else None,
        "alkaline_phosphatase": r(40, 130),
        "testosterone_male": r(200, 1500) if sex == "male" else None,
        "testosterone_female": r(2, 80) if sex == "female" else None,
    })

    # --- Immune/Renal ---
    record.update({
        "albumin": r(3.5, 5.0),
        "serum_protein": r(6.0, 8.3),
        "hemoglobin_men": r(13.5, 17.5) if sex == "male" else None,
        "hemoglobin_women": r(12.0, 15.5) if sex == "female" else None,
        "hgb_ckd": r(10.0, 12.0),
        "hematocrit_men": r(38.8, 50.0) if sex == "male" else None,
        "hematocrit_women": r(34.9, 44.5) if sex == "female" else None,
        "hct_ckd": r(30.0, 39.0),
        "egfr": r(60, 120),
        "cystatin_c": r(0.6, 1.3),
        "bun": r(7, 20),
        "vitamin_b12": r(200, 900),
        "folate_serum": r(5.0, 20.0),
        "folate_rbc": r(280, 790),
    })

    # --- Cognition ---
    record.update({
        "homocysteine": r(4, 15),
        "cortisol_morning": r(5, 25),
        "cortisol_afternoon": r(2, 15),
        "cortisol_night": r(1, 10),
        "cortisol_24hr_urine": r(10, 100),
    })

    # --- Hormone Balance ---
    record.update({
        "tsh_general": r(0.4, 4.0),
        "tsh_elderly": r(0.5, 5.0) if age > 65 else None,
        "tsh_pregnancy": None,  # Not simulating pregnancy
        "calcium_serum": r(8.5, 10.5),
        "calcium_ionized": r(4.4, 5.4),
        "dhea_s_men": r(80, 560) if sex == "male" else None,
        "dhea_s_women": r(35, 430) if sex == "female" else None,
    })

    if sex == "female":
        if age < 50:
            record.update({
                "estradiol_follicular_premenopausal_women": r(20, 150) if phase == "follicular" else None,
                "estradiol_ovulatory_premenopausal": r(100, 400) if phase == "ovulatory" else None,
                "estradiol_luteal_premenopausal": r(50, 250) if phase == "luteal" else None,
                "progesterone_follicular_premenopausal": r(0.1, 0.3) if phase == "follicular" else None,
                "progesterone_ovulatory_premenopausal": r(0.5, 1.5) if phase == "ovulatory" else None,
                "progesterone_luteal_premenopausal": r(5.0, 20.0) if phase == "luteal" else None,
            })
        else:
            record.update({
                "estradiol_postmenopausal": r(5, 40),
                "progesterone_postmenopausal": r(0.1, 1.5),
            })
    else:
        record.update({
            "estradiol_men": r(10, 50)
        })

    # --- Recovery ---
    record.update({
        "ast_male": r(10, 40) if sex == "male" else None,
        "ast_female": r(7, 35) if sex == "female" else None,
        "ggt_male": r(10, 65) if sex == "male" else None,
        "ggt_female": r(7, 50) if sex == "female" else None,
        "sodium": r(135, 145),
        "potassium": r(3.5, 5.0),
        })
    
    if athlete == "yes":
        record.update({
            "ck_athlete": r(100, 800) if athlete == "yes" else None,    
        })
    else:
        record.update({
            "ck_male": r(50, 350) if sex == "male" else None,
            "ck_female": r(30, 250) if sex == "female" else None,
        })

    # --- Endurance ---
    record.update({
        "iron": r(50, 170),
        "mch": r(27, 33),
        "mchc": r(32, 36),
        "mcv": r(80, 100),
        "rbc_male": r(4.7, 6.1) if sex == "male" else None,
        "rbc_female": r(4.2, 5.4) if sex == "female" else None,
        "platelet": r(150, 400),
        })
  
    if athlete == "yes":
        record.update({
            "ferritin_athlete": r(20, 200) if athlete == "yes" else None,    
        })
    else:
        record.update({
            "ferritin_male": r(15, 200) if sex == "male" else None,
            "ferritin_female": r(10, 150) if sex == "female" else None,
        })


    # --- Fitness ---
    record.update({
        "free_testosterone_male": r(5, 25) if sex == "male" else None,
        "free_testosterone_female": r(0.5, 5.0) if sex == "female" else None,
        "shbg_male": r(10, 60) if sex == "male" else None,
        "shbg_female": r(20, 90) if sex == "female" else None,
    })

    for field in [
        f"vo2_max_{sex}_{d}" 
        for d in ["20s", "30s", "40s", "50s", "60s", "70s"]
    ]:
        record[field] = r(*VO2_MAX[sex][decade]) if field.endswith(decade) else None

    # --- Body Composition ---
    fat = r(15, 25) if sex == "male" else r(22, 35)
    record.update({
        "percent_body_fat_male": fat if sex == "male" else None,
        "percent_body_fat_premenopausal_female": fat if sex == "female" and age < 50 else None,
        "percent_body_fat_postmenopausal_female": fat if sex == "female" and age >= 50 else None,
        "SMM_to_FFM_male": r(65, 85) if sex == "male" else None,
        "SMM_to_FFM_female": r(60, 80) if sex == "female" else None,
        "hip_to_waist_male": r(0.85, 0.95) if sex == "male" else None,
        "hip_to_waist_female": r(0.75, 0.9) if sex == "female" else None,
        "bmi": r(18.5, 27.5),
    })

    return record

# ---------- File Generation Logic ----------
def generate_patients(n=50, outfile="data/dummy_lab_results_full.csv"):
    patients = [generate_patient_record() for _ in range(n)]
    df = pd.DataFrame(patients)
    df.to_csv(outfile, index=False)
    print(f"✅ Generated {n} patients -> {outfile}")

# ---------- Main ----------
if __name__ == "__main__":
    generate_patients()
