# src/generate_biomarker_dataset_v2.py

import pandas as pd
import numpy as np
import uuid
import random
from datetime import date

# 🧬 Seed for reproducibility
np.random.seed(42)

# ------------------------
# 🎲 Random Utilities
# ------------------------

def r(low, high):
    """Random float in range [low, high], rounded to 2 decimals."""
    return round(random.uniform(low, high), 2)

def skewed_r(normal_range, low_outlier=None, high_outlier=None, p_outlier=0.2):
    """
    Bias toward outliers with probability `p_outlier`.
    Can support low or high tails.
    """
    roll = random.random()
    if roll < p_outlier / 2 and low_outlier:
        return r(*low_outlier)
    elif roll < p_outlier and high_outlier:
        return r(*high_outlier)
    return r(*normal_range)

def random_cycle_phase():
    """Return a menstrual phase."""
    return random.choice(["follicular", "ovulatory", "luteal"])

VO2_MAX = {
    "male": {
        "20s":  {"normal": (35, 50), "low": (15, 34), "high": (51, 65)},
        "30s":  {"normal": (33, 47), "low": (15, 32), "high": (48, 63)},
        "40s":  {"normal": (30, 44), "low": (13, 29), "high": (45, 60)},
        "50s":  {"normal": (28, 40), "low": (12, 27), "high": (41, 55)},
        "60s":  {"normal": (25, 36), "low": (10, 24), "high": (37, 50)},
        "70s":  {"normal": (22, 32), "low": (8, 21),  "high": (33, 45)},
    },
    "female": {
        "20s":  {"normal": (30, 45), "low": (12, 29), "high": (46, 60)},
        "30s":  {"normal": (28, 42), "low": (12, 27), "high": (43, 57)},
        "40s":  {"normal": (26, 39), "low": (10, 25), "high": (40, 54)},
        "50s":  {"normal": (24, 36), "low": (10, 23), "high": (37, 50)},
        "60s":  {"normal": (22, 32), "low": (9, 21),  "high": (33, 45)},
        "70s":  {"normal": (20, 28), "low": (8, 19),  "high": (29, 40)},
    },
}

# ------------------------
# 🧬 PATIENT GENERATION
# ------------------------

def generate_patient_record():
    sex = random.choice(["male", "female"])
    age = int(skewed_r((45, 70), low_outlier=(30, 44), high_outlier=(71, 85)))
    athlete = "yes" if random.random() < 0.02 else "no"
    phase = random_cycle_phase() if sex == "female" and age < 50 else None
    decade = f"{(age // 10) * 10}s"

    # 1️⃣ Height (sex-aware, bi-outlier)
    height = skewed_r((67, 71), low_outlier=(63, 66), high_outlier=(72, 76)) if sex == "male" \
        else skewed_r((62, 66), low_outlier=(58, 61), high_outlier=(67, 72))

    # 2️⃣ Body Fat %
    base_fat = skewed_r((15, 25), low_outlier=(10, 14), high_outlier=(26, 35)) if sex == "male" \
        else skewed_r((22, 35), low_outlier=(17, 21), high_outlier=(36, 42))
    fat = max(8.0, base_fat - r(3, 6)) if athlete == "yes" else base_fat
    fat = round(fat, 1)

    # 3️⃣ SMM to FFM Ratio
    if sex == "female":
        smm_to_ffm = (
            skewed_r((75, 85), high_outlier=(85, 90)) if athlete == "yes" else
            skewed_r((70, 80), low_outlier=(60, 69), high_outlier=(81, 85)) if fat < 30 else
            skewed_r((60, 70), low_outlier=(55, 59), high_outlier=(71, 75))
        )
    else:
        smm_to_ffm = (
            skewed_r((75, 85), high_outlier=(85, 95)) if athlete == "yes" else
            skewed_r((70, 80), low_outlier=(60, 69), high_outlier=(81, 85)) if fat < 30 else
            skewed_r((65, 75), low_outlier=(60, 64), high_outlier=(76, 80))
        )
    smm_to_ffm = round(smm_to_ffm, 1)

    # 4️⃣ Hip-to-Waist Ratio
    hip_to_waist = (
        skewed_r((0.85, 0.95), low_outlier=(0.75, 0.84), high_outlier=(0.96, 1.05)) if sex == "male"
        else skewed_r((0.75, 0.85), low_outlier=(0.65, 0.74), high_outlier=(0.86, 0.95))
    )
    if fat >= 30:
        hip_to_waist += r(0.01, 0.04)
    hip_to_waist = round(hip_to_waist, 2)

    # 💤 Sleep Score (required for profile)
    sleep_score = round(np.clip(np.random.normal(7.0, 1.5), 3, 10), 1)

    # 🏋️ Weight
    if athlete == "yes":
        weight = skewed_r((160, 220), low_outlier=(140, 159), high_outlier=(221, 260)) if sex == "male" \
            else skewed_r((130, 180), low_outlier=(115, 129), high_outlier=(181, 210))
    elif fat < 30:
        weight = skewed_r((150, 200), low_outlier=(130, 149), high_outlier=(201, 240)) if sex == "male" \
            else skewed_r((120, 165), low_outlier=(105, 119), high_outlier=(166, 190))
    else:
        weight = skewed_r((180, 240), low_outlier=(160, 179), high_outlier=(241, 300)) if sex == "male" \
            else skewed_r((150, 200), low_outlier=(135, 149), high_outlier=(201, 250))

    bmi = round((weight / (height ** 2)) * 703, 1)

    # 🧬 Lifestyle & Health Profile
    profile = generate_profile(age, sex, athlete, fat, sleep_score)

    # 🔍 Derived Classifications
    health_profile = profile["health_profile"]
    fitness_level = (
        "high" if athlete == "yes" or health_profile == "fit"
        else "moderate" if health_profile == "average"
        else "low"
    )
    vo2 = generate_vo2_max(sex, age, fitness_level)

    # 🧪 Full Record
    record = {
        "patient_id": str(uuid.uuid4()),
        "collection_date": str(date.today()),
        "age": age,
        "sex": sex,
        "athlete": athlete,
        "cycle_phase": phase,
        "height_in": height,
        "weight_lb": weight,
        "bmi": bmi,
        "sleep_score": sleep_score,
        "percent_body_fat_male": fat if sex == "male" else None,
        "percent_body_fat_premenopausal_female": fat if sex == "female" and age < 50 else None,
        "percent_body_fat_postmenopausal_female": fat if sex == "female" and age >= 50 else None,
        "smm_to_ffm_male": smm_to_ffm if sex == "male" else None,
        "smm_to_ffm_female": smm_to_ffm if sex == "female" else None,
        "hip_to_waist_male": hip_to_waist if sex == "male" else None,
        "hip_to_waist_female": hip_to_waist if sex == "female" else None,
        **profile,
        "fitness_level": fitness_level,
        "vo2_max": vo2,
    }

    # 🔬 Attach markers from each system
    record.update(generate_cardiovascular_markers(sex, profile))
    record.update(generate_sleep_markers(profile, athlete))
    record.update(generate_inflammation_markers(profile))
    record.update(generate_metabolism_markers(sex, fitness_level, profile))
    record.update(generate_immune_renal_markers(sex, age, fitness_level, profile))
    record.update(generate_cognition_markers(profile))
    record.update(generate_hormone_markers(sex, age, phase, profile))
    record.update(generate_recovery_markers(sex, athlete, profile))
    record.update(generate_endurance_markers(sex, athlete))
    record.update(generate_fitness_markers(sex, profile))

    return record

# ------------------------
# 🔍 PROFILE GENERATION
# ------------------------
def generate_profile(age, sex, athlete, fat, sleep_score):
    genetic_risk_score = round(np.clip(np.random.normal(0.5 + (age - 40) / 100, 0.15), 0.1, 0.9), 2)

    diet_quality = random.choices(
        ["poor", "average", "good"],
        weights=[0.2, 0.5, 0.3] if athlete == "no" else [0.1, 0.4, 0.5]
    )[0]

    stress_level = random.choices(["low", "moderate", "high"], weights=[0.3, 0.5, 0.2])[0]

    score = 0

    # 🔹 Updated Body Fat Scoring (sex-aware, U-curve logic)
    if sex == "male":
        if 12 <= fat <= 20:
            score += 4  # optimal
        elif 9 <= fat < 12 or 20 < fat <= 25:
            score += 3
        elif 25 < fat <= 30 or fat < 9:
            score += 1
        else:
            score += 0  # outside realistic range
    else:
        if 20 <= fat <= 30:
            score += 4
        elif 18 <= fat < 20 or 30 < fat <= 35:
            score += 3
        elif 35 < fat <= 40 or fat < 18:
            score += 1
        else:
            score += 0

    # 🔹 Genetic Risk
    if genetic_risk_score < 0.3:
        score += 4
    elif genetic_risk_score < 0.5:
        score += 3
    elif genetic_risk_score < 0.7:
        score += 2
    elif genetic_risk_score < 0.85:
        score += 1

    # 🔹 Diet
    if diet_quality == "good":
        score += 4
    elif diet_quality == "average":
        score += 2

    # 🔹 Stress
    if stress_level == "low":
        score += 4
    elif stress_level == "moderate":
        score += 2

    # 🔹 Sleep
    if sleep_score >= 8.5:
        score += 4
    elif sleep_score >= 7.0:
        score += 3
    elif sleep_score >= 6.0:
        score += 2
    elif sleep_score >= 5.0:
        score += 1

    # 🎯 Final Classification
    health_profile = (
        "fit" if score >= 15 else
        "average" if score >= 9 else
        "poor"
    )

    return {
        "genetic_risk_score": genetic_risk_score,
        "diet_quality": diet_quality,
        "stress_level": stress_level,
        "sleep_score": sleep_score,
        "health_profile": health_profile,
    }

# ------------------------
# 🔬 Marker Groups
# ------------------------

def generate_cardiovascular_markers(sex, profile):
    hp = profile["health_profile"]
    dq = profile["diet_quality"]

    # HDL
    if sex == "male":
        hdl = (
            skewed_r((60, 80), low_outlier=(35, 59), high_outlier=(81, 90)) if hp == "fit" else
            skewed_r((50, 65), low_outlier=(30, 49), high_outlier=(66, 75)) if hp == "average" else
            skewed_r((35, 50), low_outlier=(20, 34), high_outlier=(51, 60))
        )
    else:
        hdl = (
            skewed_r((70, 90), low_outlier=(45, 69), high_outlier=(91, 100)) if hp == "fit" else
            skewed_r((60, 75), low_outlier=(40, 59), high_outlier=(76, 85)) if hp == "average" else
            skewed_r((45, 60), low_outlier=(30, 44), high_outlier=(61, 70))
        )

    # LDL
    ldl = (
        skewed_r((60, 100), low_outlier=(40, 59), high_outlier=(101, 120)) if hp == "fit" else
        skewed_r((90, 130), low_outlier=(70, 89), high_outlier=(131, 160)) if hp == "average" else
        skewed_r((120, 160), low_outlier=(100, 119), high_outlier=(161, 190))
    )

    # Triglycerides
    trigs = (
        skewed_r((40, 100), low_outlier=(20, 39), high_outlier=(101, 130)) if hp == "fit" else
        skewed_r((80, 150), low_outlier=(60, 79), high_outlier=(151, 200)) if hp == "average" else
        skewed_r((130, 220), low_outlier=(110, 129), high_outlier=(221, 300))
    )

    # 🧪 Diet effect
    if dq == "poor":
        ldl += 10
        trigs += 20
    elif dq == "good":
        hdl += 5

    total_chol = hdl + ldl + (0.2 * trigs)

    omega3 = (
        skewed_r((6.5, 9.0), low_outlier=(4.5, 6.4), high_outlier=(9.1, 10.5)) if dq == "good" else
        skewed_r((5.0, 7.5), low_outlier=(3.5, 4.9), high_outlier=(7.6, 8.5)) if dq == "average" else
        skewed_r((3.5, 6.0), low_outlier=(2.0, 3.4), high_outlier=(6.1, 7.0))
    )

    return {
        "hdl_male": round(hdl, 1) if sex == "male" else None,
        "hdl_female": round(hdl, 1) if sex == "female" else None,
        "ldl": round(ldl, 1),
        "triglycerides": round(trigs, 1),
        "total_cholesterol": round(total_chol, 1),
        "lp(a)": skewed_r((10, 90), low_outlier=(5, 9), high_outlier=(91, 120)),
        "apob": skewed_r((70, 110), high_outlier=(111, 140)) if hp == "fit" else skewed_r((90, 130), high_outlier=(131, 160)),
        "omega3_index": round(omega3, 1),
        "rdw": skewed_r((11, 14.5), low_outlier=(10, 10.9), high_outlier=(14.6, 16.5)),
    }

def generate_sleep_markers(profile, athlete):
    sleep = profile["sleep_score"]
    diet = profile["diet_quality"]
    hp = profile["health_profile"]

    return {
        "magnesium_rbc": skewed_r(
            (5.0, 6.8),
            low_outlier=(3.5, 4.2),
            high_outlier=(6.9, 7.5)
        ) if sleep >= 7 else skewed_r(
            (4.2, 5.5),
            low_outlier=(3.5, 4.1),
            high_outlier=(5.6, 6.5)
        ),

        "vitamin_d": skewed_r(
            (45, 70),
            low_outlier=(20, 44),
            high_outlier=(71, 90)
        ) if diet == "good" else skewed_r(
            (25, 50),
            low_outlier=(10, 24),
            high_outlier=(51, 65)
        ),

        "serum_ferritin": skewed_r(
            (40, 130),
            low_outlier=(15, 39),
            high_outlier=(131, 180)
        ) if athlete == "yes" else skewed_r(
            (15, 110),
            low_outlier=(5, 14),
            high_outlier=(111, 150)
        ),

        "total_iron_binding_capacity": skewed_r(
            (250, 410),
            low_outlier=(200, 249),
            high_outlier=(411, 480)
        ),

        "transferrin_saturation": skewed_r(
            (25, 50),
            low_outlier=(10, 24),
            high_outlier=(51, 65)
        ),

        "hscrp": skewed_r(
            (0.1, 1.0),
            high_outlier=(1.1, 2.5)
        ) if hp == "fit" else skewed_r(
            (1.5, 3.0),
            low_outlier=(0.3, 1.4),
            high_outlier=(3.1, 5.0)
        ),
    }

def generate_inflammation_markers(profile):
    hp = profile["health_profile"]
    stress = profile["stress_level"]

    if hp == "fit":
        wbc = skewed_r((4.5, 6.5), low_outlier=(3.5, 4.4), high_outlier=(6.6, 8.0))
        neutrophils = skewed_r((2.0, 4.5), low_outlier=(1.2, 1.9), high_outlier=(4.6, 6.0))
        eosinophils = skewed_r((0.1, 0.3), low_outlier=(0.0, 0.09), high_outlier=(0.31, 0.5))
    elif hp == "average":
        wbc = skewed_r((5.5, 8.0), low_outlier=(4.0, 5.4), high_outlier=(8.1, 10.0))
        neutrophils = skewed_r((3.0, 5.5), low_outlier=(2.0, 2.9), high_outlier=(5.6, 7.0))
        eosinophils = skewed_r((0.1, 0.4), low_outlier=(0.0, 0.09), high_outlier=(0.41, 0.6))
    else:
        wbc = skewed_r((6.5, 9.5), low_outlier=(5.0, 6.4), high_outlier=(9.6, 12.0))
        neutrophils = skewed_r((4.5, 6.5), low_outlier=(3.5, 4.4), high_outlier=(6.6, 8.0))
        eosinophils = skewed_r((0.2, 0.5), low_outlier=(0.0, 0.19), high_outlier=(0.51, 0.7))

    lymphocytes = skewed_r((1.5, 3.5), low_outlier=(0.8, 1.4), high_outlier=(3.6, 5.0))

    # 📈 Stress bumps neutrophils slightly
    if stress == "high":
        neutrophils += r(0.2, 0.5)

    return {
        "wbc": round(wbc, 2),
        "lymphocytes": round(lymphocytes, 2),
        "neutrophils": round(neutrophils, 2),
        "eosinophils": round(eosinophils, 2),
        "lymphocyte_percent": round((lymphocytes / wbc) * 100, 2),
        "neut_lymph_ratio": round(neutrophils / lymphocytes, 2),
    }

def generate_metabolism_markers(sex, fitness_level, profile):
    hp = profile["health_profile"]

    if fitness_level == "high":
        glucose = skewed_r((75, 88), low_outlier=(65, 74), high_outlier=(89, 95))
        insulin = skewed_r((2.0, 6.0), low_outlier=(1.0, 1.9), high_outlier=(6.1, 9.0))
    elif fitness_level == "moderate":
        glucose = skewed_r((85, 95), low_outlier=(75, 84), high_outlier=(96, 105))
        insulin = skewed_r((6.0, 12.0), low_outlier=(3.5, 5.9), high_outlier=(12.1, 18.0))
    else:
        glucose = skewed_r((90, 110), low_outlier=(80, 89), high_outlier=(111, 130))
        insulin = skewed_r((12.0, 25.0), low_outlier=(8.0, 11.9), high_outlier=(25.1, 35.0))

    homa_ir = round((glucose * insulin) / 405, 2)
    hba1c = skewed_r((4.8, 5.6), high_outlier=(5.7, 6.4)) if hp != "poor" else skewed_r((5.7, 6.4), high_outlier=(6.5, 7.0))

    # ALT / Uric Acid trend higher in poor profiles
    alt = skewed_r((15, 40), high_outlier=(41, 60)) if sex == "male" else skewed_r((10, 35), high_outlier=(36, 50))
    uric = skewed_r((3.5, 6.5), high_outlier=(6.6, 8.0)) if sex == "male" else skewed_r((2.5, 5.5), high_outlier=(5.6, 7.0))

    if hp == "poor":
        alt += r(2, 6)
        uric += r(0.2, 0.6)

    test = r(400, 900) if sex == "male" and hp != "poor" else \
           r(200, 450) if sex == "male" else \
           r(20, 70)

    return {
        "fasting_glucose": round(glucose, 1),
        "fasting_insulin": round(insulin, 1),
        "homa_ir": homa_ir,
        "hba1c": round(hba1c, 2),
        "alt_male": round(alt, 1) if sex == "male" else None,
        "alt_female": round(alt, 1) if sex == "female" else None,
        "uric_acid_male": round(uric, 2) if sex == "male" else None,
        "uric_acid_female": round(uric, 2) if sex == "female" else None,
        "alkaline_phosphatase": r(40, 110),
        "testosterone_male": round(test, 1) if sex == "male" else None,
        "testosterone_female": round(test, 1) if sex == "female" else None,
    }

def generate_immune_renal_markers(sex, age, fitness_level, profile):
    hp = profile["health_profile"]

    # 🩸 Hemoglobin / Hematocrit
    if sex == "male":
        hgb = skewed_r((14.0, 17.0), low_outlier=(12.0, 13.9), high_outlier=(17.1, 18.5))
        hct = skewed_r((41.0, 50.0), low_outlier=(35.0, 40.9), high_outlier=(50.1, 54.0))
    else:
        hgb = skewed_r((12.0, 15.0), low_outlier=(10.0, 11.9), high_outlier=(15.1, 16.5))
        hct = skewed_r((36.0, 44.0), low_outlier=(30.0, 35.9), high_outlier=(44.1, 47.0))

    hgb_ckd = skewed_r((10.0, 12.0), low_outlier=(8.5, 9.9))
    hct_ckd = skewed_r((30.0, 39.0), low_outlier=(25.0, 29.9))

    # 💧 Renal function
    egfr = skewed_r((90, 120), low_outlier=(60, 89)) if hp == "fit" else skewed_r((60, 90), low_outlier=(30, 59))
    cystatin_c = skewed_r((0.6, 1.0), high_outlier=(1.1, 1.5)) if hp == "fit" else skewed_r((1.0, 1.4), high_outlier=(1.5, 2.0))
    bun = skewed_r((7, 18), high_outlier=(19, 25)) if hp == "fit" else skewed_r((15, 25), high_outlier=(26, 35))

    # 🧬 Protein status
    albumin = skewed_r((4.0, 5.0), low_outlier=(3.2, 3.9)) if hp == "fit" else skewed_r((3.5, 4.5), low_outlier=(2.8, 3.4))
    serum_protein = skewed_r((6.5, 8.0), low_outlier=(5.5, 6.4))

    # 🔬 Micronutrients
    b12 = skewed_r((350, 900), low_outlier=(150, 349)) if profile["diet_quality"] != "poor" else skewed_r((200, 500), low_outlier=(100, 199))
    folate_serum = skewed_r((8.0, 20.0), low_outlier=(4.0, 7.9)) if profile["diet_quality"] != "poor" else skewed_r((5.0, 12.0), low_outlier=(2.0, 4.9))
    folate_rbc = skewed_r((400, 790), low_outlier=(250, 399)) if profile["diet_quality"] != "poor" else skewed_r((280, 500), low_outlier=(150, 279))

    return {
        "albumin": round(albumin, 2),
        "serum_protein": round(serum_protein, 2),
        "hemoglobin_men": round(hgb, 1) if sex == "male" else None,
        "hemoglobin_women": round(hgb, 1) if sex == "female" else None,
        "hgb_ckd": round(hgb_ckd, 1),
        "hematocrit_men": round(hct, 1) if sex == "male" else None,
        "hematocrit_women": round(hct, 1) if sex == "female" else None,
        "hct_ckd": round(hct_ckd, 1),
        "egfr": round(egfr, 1),
        "cystatin_c": round(cystatin_c, 2),
        "bun": round(bun, 1),
        "vitamin_b12": round(b12, 1),
        "folate_serum": round(folate_serum, 1),
        "folate_rbc": round(folate_rbc, 1),
    }

def generate_cognition_markers(profile):
    stress = profile["stress_level"]
    sleep = profile["sleep_score"]
    diet = profile["diet_quality"]

    # 🔹 Homocysteine (higher with poor methylation / B vitamin status)
    if diet == "good":
        homocysteine = skewed_r((6.0, 9.0), high_outlier=(9.1, 12.0))
    elif diet == "average":
        homocysteine = skewed_r((9.0, 12.0), high_outlier=(12.1, 15.0))
    else:
        homocysteine = skewed_r((12.0, 16.0), high_outlier=(16.1, 20.0))

    # 🔹 Cortisol Patterns (by stress & sleep)
    if stress == "low" and sleep >= 7:
        morning = skewed_r((10, 18), low_outlier=(6, 9))
        afternoon = skewed_r((4, 8), low_outlier=(2, 3))
        night = skewed_r((1, 5), low_outlier=(0.2, 0.9))
    elif stress == "moderate":
        morning = skewed_r((15, 22), high_outlier=(23, 28))
        afternoon = skewed_r((6, 12), high_outlier=(13, 16))
        night = skewed_r((2, 6), high_outlier=(6.1, 9))
    else:  # High stress
        morning = skewed_r((18, 30), high_outlier=(31, 40))
        afternoon = skewed_r((10, 20), high_outlier=(21, 30))
        night = skewed_r((5, 12), high_outlier=(13, 20))

    cortisol_24hr = round(morning + afternoon + night + r(5, 15), 1)

    return {
        "homocysteine": round(homocysteine, 1),
        "cortisol_morning": round(morning, 1),
        "cortisol_afternoon": round(afternoon, 1),
        "cortisol_night": round(night, 1),
        "cortisol_24hr_urine": cortisol_24hr,
    }

def generate_hormone_markers(sex, age, phase, profile):
    hp = profile["health_profile"]

    # 🔹 TSH (thyroid stimulating hormone)
    tsh = (
        skewed_r((0.4, 2.5), high_outlier=(2.6, 4.5)) if hp == "fit"
        else skewed_r((2.5, 4.5), low_outlier=(0.2, 0.3), high_outlier=(4.6, 7.0))
    )

    calcium_serum = skewed_r((9.0, 10.2), low_outlier=(8.5, 8.9), high_outlier=(10.3, 10.8))
    calcium_ionized = skewed_r((4.6, 5.2), low_outlier=(4.3, 4.5), high_outlier=(5.3, 5.6))

    markers = {
        "tsh_general": round(tsh, 2),
        "tsh_elderly": round(tsh, 2) if age >= 65 else None,
        "tsh_pregnancy": None,  # 🔒 Not simulating pregnancy
        "calcium_serum": round(calcium_serum, 2),
        "calcium_ionized": round(calcium_ionized, 2),
    }

    # 🔹 DHEA-S
    if sex == "male":
        dhea = skewed_r((200, 560), low_outlier=(80, 199)) if hp == "fit" else skewed_r((80, 300), low_outlier=(40, 79))
        markers["dhea_s_men"] = round(dhea, 1)
    else:
        dhea = skewed_r((100, 400), low_outlier=(35, 99)) if hp != "poor" else skewed_r((35, 200), low_outlier=(15, 34))
        markers["dhea_s_women"] = round(dhea, 1)

        # 🔹 Female Hormones (phase-specific)
        if age < 50:
            if phase == "follicular":
                markers.update({
                    "estradiol_follicular_premenopausal_women": round(skewed_r((50, 120), high_outlier=(121, 150)), 1),
                    "progesterone_follicular_premenopausal": round(skewed_r((0.1, 0.5), high_outlier=(0.6, 1.0)), 2),
                })
            elif phase == "ovulatory":
                markers.update({
                    "estradiol_ovulatory_premenopausal": round(skewed_r((200, 350), high_outlier=(351, 450)), 1),
                    "progesterone_ovulatory_premenopausal": round(skewed_r((0.5, 2.0), high_outlier=(2.1, 3.0)), 2),
                })
            elif phase == "luteal":
                markers.update({
                    "estradiol_luteal_premenopausal": round(skewed_r((100, 200), high_outlier=(201, 280)), 1),
                    "progesterone_luteal_premenopausal": round(skewed_r((10.0, 20.0), high_outlier=(20.1, 30.0)), 2),
                })
        else:
            markers.update({
                "estradiol_postmenopausal": round(skewed_r((5, 30), low_outlier=(1, 4)), 1),
                "progesterone_postmenopausal": round(skewed_r((0.1, 1.2), high_outlier=(1.3, 2.5)), 2),
            })

    if sex == "male":
        markers["estradiol_men"] = round(skewed_r((10, 35), high_outlier=(36, 45)), 1)

    return markers

def generate_recovery_markers(sex, athlete, profile):
    hp = profile["health_profile"]

    # 🔹 AST / GGT (sex-based)
    ast = (
        skewed_r((15, 40), low_outlier=(10, 14), high_outlier=(41, 60)) if sex == "male"
        else skewed_r((10, 35), low_outlier=(8, 9), high_outlier=(36, 50))
    )
    ggt = (
        skewed_r((15, 60), high_outlier=(61, 90)) if sex == "male"
        else skewed_r((10, 45), high_outlier=(46, 70))
    )

    # 🔹 Creatine Kinase (CK) — higher in athletes
    if athlete == "yes":
        ck = skewed_r((150, 800), high_outlier=(801, 1200))
        ck_field = "ck_athlete"
    else:
        ck = skewed_r((70, 350), high_outlier=(351, 500)) if sex == "male" else skewed_r((50, 250), high_outlier=(251, 400))
        ck_field = "ck_male" if sex == "male" else "ck_female"

    # 🔹 Electrolytes
    sodium = skewed_r((136, 144), low_outlier=(130, 135), high_outlier=(145, 150)) if hp == "fit" \
        else skewed_r((134, 142), low_outlier=(128, 133), high_outlier=(143, 150))

    potassium = skewed_r((3.8, 4.8), low_outlier=(3.2, 3.7), high_outlier=(4.9, 5.5)) if hp == "fit" \
        else skewed_r((3.5, 5.0), low_outlier=(3.0, 3.4), high_outlier=(5.1, 5.6))

    return {
        "ast_male": round(ast, 1) if sex == "male" else None,
        "ast_female": round(ast, 1) if sex == "female" else None,
        "ggt_male": round(ggt, 1) if sex == "male" else None,
        "ggt_female": round(ggt, 1) if sex == "female" else None,
        "sodium": round(sodium, 1),
        "potassium": round(potassium, 2),
        ck_field: round(ck, 1),
    }

def generate_endurance_markers(sex, athlete):
    # 🔹 Iron & Ferritin (higher in athletes)
    iron = skewed_r((70, 150), low_outlier=(40, 69), high_outlier=(151, 180)) if athlete == "yes" \
        else skewed_r((50, 120), low_outlier=(30, 49), high_outlier=(121, 150))

    ferritin = (
        skewed_r((30, 200), low_outlier=(15, 29), high_outlier=(201, 250)) if athlete == "yes" else
        skewed_r((15, 200), low_outlier=(5, 14), high_outlier=(201, 250)) if sex == "male" else
        skewed_r((10, 150), low_outlier=(5, 9), high_outlier=(151, 200))
    )

    # 🔹 Red cell indices
    mch = skewed_r((27, 33), low_outlier=(24, 26.9), high_outlier=(33.1, 35))
    mchc = skewed_r((32, 36), low_outlier=(30, 31.9), high_outlier=(36.1, 38))
    mcv = skewed_r((80, 100), low_outlier=(70, 79), high_outlier=(101, 110))

    # 🔹 RBC & Platelet
    rbc = (
        skewed_r((4.7, 6.1), low_outlier=(4.2, 4.6), high_outlier=(6.2, 6.8)) if sex == "male"
        else skewed_r((4.2, 5.4), low_outlier=(3.8, 4.1), high_outlier=(5.5, 6.0))
    )

    platelet = skewed_r((150, 400), low_outlier=(125, 149), high_outlier=(401, 500))

    return {
        "iron": round(iron, 1),
        "mch": round(mch, 1),
        "mchc": round(mchc, 1),
        "mcv": round(mcv, 1),
        "rbc_male": round(rbc, 2) if sex == "male" else None,
        "rbc_female": round(rbc, 2) if sex == "female" else None,
        "platelet": round(platelet, 0),
        "ferritin_athlete": round(ferritin, 1) if athlete == "yes" else None,
        "ferritin_male": round(ferritin, 1) if sex == "male" and athlete == "no" else None,
        "ferritin_female": round(ferritin, 1) if sex == "female" and athlete == "no" else None,
    }

def generate_fitness_markers(sex, profile):
    hp = profile["health_profile"]

    # 🔹 Free Testosterone
    if sex == "male":
        free_testosterone = skewed_r(
            (15, 25), low_outlier=(7, 14), high_outlier=(26, 35)
        ) if hp == "fit" else skewed_r(
            (10, 18), low_outlier=(5, 9), high_outlier=(19, 24)
        ) if hp == "average" else skewed_r(
            (5, 10), low_outlier=(2, 4), high_outlier=(11, 14)
        )
    else:
        free_testosterone = skewed_r(
            (3.5, 5.0), low_outlier=(2.0, 3.4), high_outlier=(5.1, 6.5)
        ) if hp == "fit" else skewed_r(
            (2.0, 3.5), low_outlier=(1.0, 1.9), high_outlier=(3.6, 4.5)
        ) if hp == "average" else skewed_r(
            (0.5, 2.0), low_outlier=(0.2, 0.4), high_outlier=(2.1, 3.0)
        )

    # 🔹 SHBG
    if sex == "male":
        shbg = skewed_r((20, 40), low_outlier=(10, 19), high_outlier=(41, 55)) if hp == "fit" \
            else skewed_r((30, 60), low_outlier=(15, 29), high_outlier=(61, 75))
    else:
        shbg = skewed_r((30, 70), low_outlier=(20, 29), high_outlier=(71, 85)) if hp == "fit" \
            else skewed_r((40, 90), low_outlier=(30, 39), high_outlier=(91, 110))

    return {
        "free_testosterone_male": round(free_testosterone, 2) if sex == "male" else None,
        "free_testosterone_female": round(free_testosterone, 2) if sex == "female" else None,
        "shbg_male": round(shbg, 1) if sex == "male" else None,
        "shbg_female": round(shbg, 1) if sex == "female" else None,
    }

def generate_vo2_max(sex, age, fitness_level):
    decade = f"{(age // 10) * 10}s"
    ranges = VO2_MAX[sex][decade]

    if fitness_level == "high":
        p_high, p_low = 0.25, 0.05
    elif fitness_level == "moderate":
        p_high, p_low = 0.1, 0.1
    else:
        p_high, p_low = 0.02, 0.3

    roll = random.random()
    if roll < p_low:
        return round(r(*ranges["low"]), 1)
    elif roll < p_low + p_high:
        return round(r(*ranges["high"]), 1)
    else:
        return round(r(*ranges["normal"]), 1)


# ------------------------
# 🎯 Generate Dataset
# ------------------------
def generate_patients(n=50, outfile="data/dummy_lab_results_full.csv"):
    patients = [generate_patient_record() for _ in range(n)]
    df = pd.DataFrame(patients)
    df.to_csv(outfile, index=False)
    print(f"✅ Generated {n} patients -> {outfile}")

# ------------------------
# 🚀 Execute Script
# ------------------------
if __name__ == "__main__":
    generate_patients()
