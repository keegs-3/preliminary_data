import os
import pandas as pd
from datetime import datetime

# --- Load Data ---
base_dir = os.path.dirname(os.path.abspath(__file__))
patient_survey = pd.read_csv(os.path.join(base_dir, "data", "synthetic_patient_survey.csv"))
biomarker_df = pd.read_csv(os.path.join(base_dir, "data", "dummy_lab_results_full.csv"))

def clean_id(x):
    x = str(x).strip()
    if '.' in x:
        left, right = x.split('.', 1)
        return f"{int(left)}.{right.zfill(2)}"
    return x

patient_survey.columns = [clean_id(c) if c != 'patient_id' else c for c in patient_survey.columns]

# --- Custom Logic for Protein Intake (2.11) ---
def calc_protein_target(weight_lb, age):
    weight_kg = weight_lb / 2.205
    if age < 65:
        target = 1.2 * weight_kg
    else:
        target = 1.5 * weight_kg
    return round(target, 1)

def protein_intake_score(protein_g, weight_lb, age):
    try:
        protein_g = float(protein_g)
        target = calc_protein_target(weight_lb, age)
        pct = protein_g / target if target else 0
        if pct >= 1:
            return 10
        elif pct >= 0.8:
            return 8
        elif pct >= 0.6:
            return 6
        elif pct > 0:
            return 4
        else:
            return 0
    except Exception:
        return 0

# --- Custom Logic for Calories Intake (2.62) ---
def calc_calorie_target(weight_lb, age, sex):
    weight_kg = weight_lb / 2.205
    # Example: Simple Harris-Benedict BMR * 1.2 sedentary
    if sex.lower().startswith("m"):
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * 175) - (5.677 * age)  # using avg height 175cm
    else:
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * 162) - (4.330 * age)  # using avg height 162cm
    calorie_target = bmr * 1.2
    return round(calorie_target)

def calorie_intake_score(calories, weight_lb, age, sex):
    try:
        calories = float(calories)
        target = calc_calorie_target(weight_lb, age, sex)
        pct = calories / target if target else 0
        # Scoring logic, e.g. within ±15% of target = 10; ±25% = 8, ±35% = 6, else 2
        if 0.85 <= pct <= 1.15:
            return 10
        elif 0.75 <= pct < 0.85 or 1.15 < pct <= 1.25:
            return 8
        elif 0.65 <= pct < 0.75 or 1.25 < pct <= 1.35:
            return 6
        else:
            return 2
    except Exception:
        return 0

# --- Custom Logic for Movement (3.03-3.11) ---

FREQ_SCORES = {
    "": 0.0,
    "Rarely (a few times a month)": 0.4,
    "Occasionally (1–2 times per week)": 0.6,
    "Regularly (3–4 times per week)": 0.8,
    "Frequently (5 or more times per week)": 1.0
}

DUR_SCORES = {
    "": 0.0,
    "Less than 30 minutes": 0.6,
    "30–45 minutes": 0.8,
    "45–60 minutes": 0.9,
    "More than 60 minutes": 1.0
}

movement_questions = {
    "Cardio": {
        "freq_q": "3.04",
        "dur_q": "3.08",
        "pillar_weights": {"Movement": 16}
    },
    "Strength": {
        "freq_q": "3.05",
        "dur_q": "3.09",
        "pillar_weights": {"Movement": 16}
    },
    "Flexibility": {
        "freq_q": "3.06",
        "dur_q": "3.10",
        "pillar_weights": {"Movement": 13}
    },
    "HIIT": {
        "freq_q": "3.07",
        "dur_q": "3.11",
        "pillar_weights": {"Movement": 16}
    }
}

def score_movement_pillar(row, movement_questions):
    movement_scores = {}
    for move_type, cfg in movement_questions.items():
        freq_ans = row.get(cfg["freq_q"], "")
        dur_ans = row.get(cfg["dur_q"], "")
        freq = FREQ_SCORES.get(freq_ans, 0.0)
        dur = DUR_SCORES.get(dur_ans, 0.0)
        # Each pillar_weights is a dict, e.g. {"Movement": 16}
        for pillar, weight in cfg["pillar_weights"].items():
            if freq == 0 and dur == 0:
                movement_scores[(move_type, pillar)] = 0
            else:
                total = freq + dur
                if total >= 1.6:
                    movement_scores[(move_type, pillar)] = weight
                else:
                    movement_scores[(move_type, pillar)] = total * (weight / 2)
    return movement_scores

# --- Sleep Issue Config with Pillar Weights (modular for multi-pillar mapping) ---
SLEEP_ISSUES = [
    # (issue_text, frequency_qid, {"Sleep": weight, ...})
    ("Difficulty falling asleep", "4.13", {"Sleep": 5}),
    ("Difficulty staying asleep", "4.14", {"Sleep": 5}),
    ("Waking up too early", "4.15", {"Sleep": 5}),
    ("Frequent nightmares", "4.16", {"Sleep": 3}),
    ("Restless legs", "4.17", {"Sleep": 6, "Movement": 1}),
    ("Snoring", "4.18", {"Sleep": 4, "CoreCare": 2}),
    ("Sleep apnea", "4.19", {"Sleep": 7, "CoreCare": 3}),
]

SLEEP_FREQ_MAP = {
    "Always": 0.2,
    "Frequently": 0.4,
    "Occasionally": 0.6,
    "Rarely": 0.8,
    "": 1.0,  # Not selected/frequency – full credit
}

def score_sleep_issues(patient_answers):
    # patient_answers is a dict-like row from patient_survey
    sleep_issues_reported = [x.strip() for x in str(patient_answers.get("4.12", "")).split("|") if x.strip()]
    # Full credit if none reported or "None" selected
    if not sleep_issues_reported or any("none" in s.lower() for s in sleep_issues_reported):
        # Return a dict by pillar with full credit
        pillar_totals = {}
        for _, _, pillar_wts in SLEEP_ISSUES:
            for p, w in pillar_wts.items():
                pillar_totals[p] = pillar_totals.get(p, 0.0) + w
        return pillar_totals

    # Otherwise, score each reported issue
    pillar_scores = {}
    for issue, freq_qid, pillar_wts in SLEEP_ISSUES:
        if issue in sleep_issues_reported:
            freq_ans = str(patient_answers.get(freq_qid, "")).strip()
            mult = SLEEP_FREQ_MAP.get(freq_ans, 0.2)
        else:
            mult = 1.0  # Not selected = full credit
        for p, w in pillar_wts.items():
            pillar_scores[p] = pillar_scores.get(p, 0.0) + (w * mult)
    return pillar_scores

# --- Sleep Hygiene Protocols (4.07) ---
def score_sleep_protocols(answer_str):
    WEIGHT = 9.0  # Assign to pillar(s) below in config
    protocols = [x.strip() for x in (answer_str or "").split("|") if x.strip()]
    n = len(protocols)
    if n >= 7:
        score = 1.0
    elif n >= 5:
        score = 0.8
    elif n >= 3:
        score = 0.6
    elif n >= 1:
        score = 0.4
    else:
        score = 0.2
    return round(score * WEIGHT, 2)

# --- Cognitive activity count (5.08) ---
def score_cognitive_activities(answer_str):
    WEIGHT = 8.0
    activities = [x.strip() for x in (answer_str or "").split("|") if x.strip()]
    n = len(activities)
    if n >= 5:
        score = 1.0
    elif n == 4:
        score = 0.8
    elif n == 3:
        score = 0.6
    elif n == 2:
        score = 0.4
    elif n == 1:
        score = 0.2
    else:
        score = 0.0
    return round(score * WEIGHT, 2)

# --- 6.01 / 6.02 Stress score ---
def stress_score(stress_level_ans, freq_ans):
    level_map = {
        "No stress": 1.0,
        "Low stress": 0.8,
        "Moderate stress": 0.5,
        "High stress": 0.2,
        "Extreme stress": 0.0,
        "Stress levels vary from low to moderate": 0.5,
        "Stress levels vary from moderate to high": 0.5,
    }
    freq_map = {
        "Rarely": 1.0,
        "Occasionally": 0.7,
        "Frequently": 0.4,
        "Always": 0.0,
    }
    s = level_map.get(str(stress_level_ans).strip(), 0.5)
    f = freq_map.get(str(freq_ans).strip(), 0.5)
    raw_score = (s + f) / 2
    return round(raw_score * 19, 2)  # Out of 19

# --- 6.07 Coping skills score ---
COPING_WEIGHTS_6_07 = {
    "Exercise or physical activity": 1.0,
    "Meditation or mindfulness practices": 1.0,
    "Deep breathing exercises": 0.7,
    "Hobbies or recreational activities": 0.7,
    "Talking to friends or family": 0.7,
    "Professional counseling or therapy": 1.0,
    "Journaling or writing": 0.5,
    "Time management strategies": 0.5,
    "Avoiding stressful situations": 0.3,
    "Other (please specify)": 0.3,
    "None": 0.0,
}

def coping_score(answer_str, coping_weights, stress_level_ans, freq_ans):
    responses = [r.strip() for r in str(answer_str or "").split("|") if r.strip()]
    has_none = any("none" in r.lower() for r in responses)
    high_stress = (str(stress_level_ans).strip() in ["High stress", "Extreme stress"] or
                   str(freq_ans).strip() in ["Frequently", "Always"])
    
    if has_none or not responses:
        return 0.0 if high_stress else 5.5  # No coping strategies
    
    # Calculate weighted score
    total_weight = sum(coping_weights.get(response, 0.5) for response in responses)
    weighted_score = min(total_weight * 3.5, 7.0)
    
    # Adjust scoring based on stress level
    if not high_stress:
        return min(5.5 + total_weight, 7.0)  # Low stress: base 5.5 + bonus for coping
    else:
        return weighted_score  # High-stress people need good coping

# --- Custom logic for Substances ---

USE_BAND_SCORES = {
    "Heavy": 0.0,
    "Moderate": 0.25,
    "Light": 0.5,
    "Minimal": 0.75,
    "Occasional": 1.0
}
DURATION_SCORES = {
    "Less than 1 year": 1.0,
    "1-2 years": 0.8,
    "3-5 years": 0.6,
    "6-10 years": 0.4,
    "11-20 years": 0.2,
    "More than 20 years": 0.0
}

# NEW: Time since quit bonus scores
QUIT_TIME_BONUS = {
    "Less than 3 years": 0.0,
    "3-5 years": 0.1,
    "6-10 years": 0.2,
    "11-20 years": 0.4,
    "More than 20 years": 0.6
}

SUBSTANCE_WEIGHTS = {
    "Tobacco": 15,
    "Nicotine": 4,
    "Alcohol": 10,
    "Recreational Drugs": 8,
    "OTC Meds": 6,
    "Other Substances": 6
}

# UPDATED: Substance questions with new time since quit questions
SUBSTANCE_QUESTIONS = {
    "Tobacco": {
        "current_band": "8.02",
        "current_years": "8.03",
        "current_trend": "8.04",
        "former_band": "8.22",
        "former_years": "8.21",
        "time_since_quit": "8.23",  # NEW
        "current_in_which": "Tobacco (cigarettes, cigars, smokeless tobacco)",
        "former_in_which": "Tobacco (cigarettes, cigars, smokeless tobacco)",
    },
    "Alcohol": {
        "current_band": "8.05",
        "current_years": "8.06",
        "current_trend": "8.07",
        "former_band": "8.25",
        "former_years": "8.24",
        "time_since_quit": "8.26",  # NEW
        "current_in_which": "Alcohol",
        "former_in_which": "Alcohol",
    },
    "Recreational Drugs": {
        "current_band": "8.08",
        "current_years": "8.09",
        "current_trend": "8.10",
        "former_band": "8.28",
        "former_years": "8.27",
        "time_since_quit": "8.29",  # NEW
        "current_in_which": "Recreational drugs (e.g., marijuana)",
        "former_in_which": "Recreational drugs (e.g., marijuana)",
    },
    "Nicotine": {
        "current_band": "8.11",
        "current_years": "8.12",
        "current_trend": "8.13",
        "former_band": "8.31",
        "former_years": "8.30",
        "time_since_quit": "8.32",  # NEW
        "current_in_which": "Nicotine",
        "former_in_which": "Nicotine",
    },
    "OTC Meds": {
        "current_band": "8.14",
        "current_years": "8.15",
        "current_trend": "8.16",
        "former_band": "8.34",
        "former_years": "8.33",
        "time_since_quit": "8.35",  # NEW
        "current_in_which": "Over-the-counter medications (e.g., sleep aids)",
        "former_in_which": "Over-the-counter medications (e.g., sleep aids)",
    },
    "Other Substances": {
        "current_band": "8.17",
        "current_years": "8.18",
        "current_trend": "8.19",
        "former_band": "8.37",
        "former_years": "8.36",
        "time_since_quit": "8.38",  # NEW
        "current_in_which": "Other",
        "former_in_which": "Other",
    }
}

# UPDATED: Enhanced substance scoring with time since quit
def score_substance_use(use_band, years_band, is_current, usage_trend=None, time_since_quit=None):
    band_level = use_band.split(":")[0].strip() if use_band else "Heavy"
    band_score = USE_BAND_SCORES.get(band_level, 0.0)
    duration_score = DURATION_SCORES.get(years_band, 0.0)
    base_score = min(band_score, duration_score)
    
    if not is_current:
        # NEW: Use graduated quit bonus based on time since quit
        if time_since_quit:
            quit_bonus = QUIT_TIME_BONUS.get(time_since_quit, 0.15)  # Default to old bonus if not found
        else:
            quit_bonus = 0.15  # Fallback to old bonus if no time data
        base_score = min(base_score + quit_bonus, 1.0)
    
    if is_current and usage_trend:
        if usage_trend == "I currently use more than I used to":
            base_score = max(base_score - 0.1, 0.0)  # Penalty for increasing use
        elif usage_trend == "I currently use less than I used to":
            base_score = min(base_score + 0.1, 1.0)  # Adjustment for past heavier use
    
    return base_score

# UPDATED: Get substance score with time since quit logic
def get_substance_score(patient_answers):
    substance_scores = {}
    for sub, qmap in SUBSTANCE_QUESTIONS.items():
        current_list = [x.strip() for x in str(patient_answers.get('8.01', '')).split('|')]
        former_list = [x.strip() for x in str(patient_answers.get('8.20', '')).split('|')]
        is_current = qmap['current_in_which'] in current_list
        is_former = (not is_current) and (qmap['former_in_which'] in former_list)
        score = 1.0  # default (never used = perfect)
        
        if is_current:
            use_band = patient_answers.get(qmap['current_band'], "")
            years_band = patient_answers.get(qmap['current_years'], "")
            usage_trend = patient_answers.get(qmap['current_trend'], "")
            score = score_substance_use(use_band, years_band, True, usage_trend)
        elif is_former:
            use_band = patient_answers.get(qmap['former_band'], "")
            years_band = patient_answers.get(qmap['former_years'], "")
            time_since_quit = patient_answers.get(qmap['time_since_quit'], "")  # NEW
            score = score_substance_use(use_band, years_band, False, time_since_quit=time_since_quit)
        
        weighted = score * SUBSTANCE_WEIGHTS[sub]
        substance_scores[sub] = weighted
    return substance_scores

# --- Screening Guidelines and Date Scoring Logic ---
screen_guidelines = {
    '10.01': 6,    # Dental exam: 6 months
    '10.02': 12,   # Skin check: 12 months
    '10.03': 12,   # Vision: 12 months
    '10.04': 120,  # Colon: 120 months (10 years)
    '10.05': 12,   # Mammogram: 12 months
    '10.06': 36,   # PAP: 36 months
    '10.07': 36,   # DEXA: 36 months
    '10.08': 36,   # PSA: 36 months
}

def score_date_response(date_str, window_months):
    if not date_str or pd.isnull(date_str):
        return 0
    try:
        exam_date = datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return 0
    today = datetime.today()
    months_ago = (today.year - exam_date.year) * 12 + (today.month - exam_date.month)
    if months_ago <= window_months:
        return 1.0
    elif months_ago <= int(window_months * 1.5):
        return 0.6
    else:
        return 0.2

# --- Pillars ---
PILLARS = [
    "Nutrition", "Movement", "Sleep", "Cognitive",
    "Stress", "Connection", "CoreCare"
]

# --- Centralized Question Map ---
# For each QID: define (score_map OR scoring_fn, pillar_weight_dict)
# If scoring_fn, it must accept the answer and return a score

QUESTION_CONFIG = {
    # --- Overview (Section 1) ---
    "1.01": {
        "question": "Which of the following areas are you most interested in improving right now (select all that apply)?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "1.02": {
        "question": "Which of the following areas are you NOT interested in focusing on initially?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "1.03": {
        "question": "Please rank your selected focus areas in order of personal importance.",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
    "1.04": {
        "question": "What motivates you most to prioritize your health and longevity (select all that apply)?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "1.05": {
        "question": "How do you prefer to stay motivated or held accountable (select all that apply)?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "1.06": {
        "question": "Please describe your personal health goals or longevity aspirations.",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
    # --- Healthful Nutrition (Section 2) ---
    "2.01": {
        "question": "How would you characterize your typical daily diet?",
        "pillar_weights": {"Nutrition": 0},
        "response_scores": {
            "Very healthy": 1.0,
            "Moderately healthy": 0.6,
            "Unhealthy": 0.2,
        },
        "multi_select": False,
    },
    "2.02": {
        "question": "Do you currently follow any specific dietary pattern or have any dietary restrictions?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "2.03": {
        "question": "How many full meals do you typically eat per day?",
        "pillar_weights": {"Nutrition": 6},
        "response_scores": {
            "1 or less": 0.0,
            "2": 0.5,
            "3": 1.0,
            "4 or more": 1.0,
        },
        "multi_select": False,
    },
    "2.04": {
        "question": "Would you consider adjusting your meal structure in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - actively working on it": 1.0,
            "Yes - open to trying": 0.8,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "2.05": {
        "question": "How many snacks do you typically eat per day?",
        "pillar_weights": {"Nutrition": 2},
        "response_scores": {
            "I don't typically snack": 1.0,
            "1": 0.8,
            "2": 0.6,
            "3": 0.4,
            "4 or more": 0.2,
        },
        "multi_select": False,
    },
    "2.06": {
        "question": "Would you consider adjusting your snacking habits in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - actively working on it": 1.0,
            "Yes - open to trying": 0.8,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "2.07": {
        "question": "How often do you eat out or order takeout/delivery?",
        "pillar_weights": {"Nutrition": 4},
        "response_scores": {
            "Rarely": 1.0,
            "Once a week": 0.7,
            "Several times a week": 0.4,
            "Daily": 0.2,
        },
        "multi_select": False,
    },
    "2.08": {
        "question": "Would you consider preparing more meals at home in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - actively working on it": 1.0,
            "Yes - open to trying": 0.8,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "2.09": {
        "question": "Do you track your daily protein intake?",
        "pillar_weights": {"Nutrition": 1},
        "response_scores": {
            "Yes": 1.0,
            "No, but I'm Generally Aware": 0.7,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "2.10": {
        "question": "Would you consider tracking protein more consistently in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - actively working on it": 1.0,
            "Yes - open to trying": 0.8,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    # ---- Custom protein intake logic (2.11) ----
    "2.11": {
    "pillar_weights": {"Nutrition": 6, "Movement": 6},
    "score_fn": protein_intake_score  # expects (protein_g, weight_lb, age)
    },
    "2.12": {
        "question": "Would you consider adjusting your daily protein intake in support of your longevity goals?",
        "pillar_weights": {},  # No pillar score for intent
        "response_scores": {
            "Yes - open to trying": 0.8,
            "Yes - actively working on it": 1.0,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "2.13": {
        "question": "How often do you consume processed or red meat?",
        "pillar_weights": {"Nutrition": 6, "CoreCare": 4},
        "response_scores": {
            "Rarely or Never": 1.0,
            "Less than once a week": 1.0,
            "1-2 times per week": 0.8,
            "3-4 times per week": 0.4,
            "5 or more times per week": 0.2,
        },
        "multi_select": False,
    },
    "2.14": {
        "question": "Would you consider decreasing your processed and red meat consumption in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - open to trying": 0.8,
            "Yes - actively working on it": 1.0,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "2.15": {
        "question": "How often do you eat fatty fish (e.g., salmon, sardines, mackerel) rich in omega-3s?",
        "pillar_weights": {"Nutrition": 7, "CoreCare": 5, "Cognitive": 8},
        "response_scores": {
            "Rarely or Never": 0.2,
            "Less than once a week": 0.4,
            "1-2 times per week": 0.6,
            "3-4 times per week": 1.0,
            "5 or more times per week": 1.0,
        },
        "multi_select": False,
    },
    "2.16": {
        "question": "Would you consider increasing your intake of omega-3 rich fish in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - actively working on it": 1.0,
            "Yes - open to trying": 0.8,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "2.17": {
        "question": "How much of your protein comes from plant-based sources in a typical week?",
        "pillar_weights": {"Nutrition": 5},
        "response_scores": {
            "Almost none - all animal-based": 0.2,
            "A small portion - mostly animal-based": 0.5,
            "Moderate - roughly balanced": 1.0,
            "Large portion - mostly plant-based": 1.0,
            "Almost entirely plant-based or Vegan": 1.0,
        },
        "multi_select": False,
    },
    "2.18": {
        "question": "Would you consider increasing the proportion of plant-based protein in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - actively working on it": 1.0,
            "Yes - open to trying": 0.8,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "2.19": {
        "question": "How many servings of fruits and vegetables do you consume daily?",
        "pillar_weights": {"Nutrition": 6},
        "response_scores": {
            "0": 0.2,
            "1-2": 0.4,
            "3-4": 0.7,
            "5 or more": 1.0,
        },
        "multi_select": False,
    },
    "2.20": {
        "question": "Would you consider increasing your fruit and vegetable consumption in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - actively working on it": 1.0,
            "Yes - open to trying": 0.8,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "2.21": {
        "question": "How often do you consume whole grains (e.g., oats, barley, brown rice, whole wheat)?",
        "pillar_weights": {"Nutrition": 4},
        "response_scores": {
            "Rarely or never": 0.2,
            "Once a week": 0.4,
            "Several times a week": 0.7,
            "Daily": 1.0,
        },
        "multi_select": False,
    },
    "2.22": {
        "question": "Would you consider increasing your intake of whole grains in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - actively working on it": 1.0,
            "Yes - open to trying": 0.8,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "2.23": {
        "question": "How often do you consume legumes (e.g., lentils, chickpeas, black beans)?",
        "pillar_weights": {"Nutrition": 6},
        "response_scores": {
            "Rarely or never": 0.2,
            "Once a week": 0.4,
            "Several times a week": 0.7,
            "Daily": 1.0,
        },
        "multi_select": False,
    },
    "2.24": {
        "question": "Would you consider increasing your legume consumption in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - actively working on it": 1.0,
            "Yes - open to trying": 0.8,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "2.25": {
        "question": "How often do you consume seeds such as flaxseed, chia, or hemp?",
        "pillar_weights": {"Nutrition": 4},
        "response_scores": {
            "Rarely or never": 0.2,
            "Once a week": 0.4,
            "Several times a week": 0.7,
            "Daily": 1.0,
        },
        "multi_select": False,
    },
    "2.26": {
        "question": "Would you consider increasing your intake of seeds (e.g., flax, chia) in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - actively working on it": 1.0,
            "Yes - open to trying": 0.8,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "2.27": {
        "question": "How often do you consume healthy fats such as olive oil, avocados, nuts, etc.?",
        "pillar_weights": {"Nutrition": 3},
        "response_scores": {
            "Rarely or never": 0.2,
            "Once a week": 0.4,
            "Several times a week": 0.7,
            "Daily": 1.0,
        },
        "multi_select": False,
    },
    "2.28": {
        "question": "Would you consider increasing your intake of healthy fats (olive oil, avocados, nuts, fatty fish, etc.) in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - actively working on it": 1.0,
            "Yes - open to trying": 0.8,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "2.29": {
        "question": "How much water do you drink daily?",
        "pillar_weights": {"Nutrition": 7},
        "response_scores": {
            "Less than 1 liter (34 oz)": 0.2,
            "1-2 liters (34-68 oz)": 0.5,
            "More than 2 liters (68 oz)": 1.0,
        },
        "multi_select": False,
    },
    "2.30": {
        "question": "Would you consider increasing your daily water intake in the future in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - actively working on it": 1.0,
            "Yes - open to trying": 0.8,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "2.31": {
        "question": "How much caffeine do you typically consume per day?",
        "pillar_weights": {"Nutrition": 2},
        "response_scores": {
            "None": 0.2,
            "<100 mg (e.g., 1 small coffee or tea)": 1.0,
            "100–200 mg (1–2 cups of coffee)": 1.0,
            "201–400 mg (3–4 cups or energy drink)": 0.7,
            ">400 mg (5+ cups, strong pre-workouts, etc.)": 0.2,
        },
        "multi_select": False,
    },
    "2.32": {
        "question": "Would you be open to adjusting your caffeine intake in the future in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - actively working on it": 1.0,
            "Yes - open to trying": 0.8,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "2.33": {
        "question": "What is your primary source of caffeine?",
        "pillar_weights": {"Nutrition": 3, "Sleep": 2},
        "response_scores": {
            "Coffee": 1.0,
            "Tea": 1.0,
            "Energy Drinks": 0.2,
            "Soda": 0.2,
            "Pre-Workout Supplements": 0.2,
            "Chocolate": 0.2,
            "Other": 0.2,
        },
        "multi_select": False,
    },
    "2.34": {
        "question": "What time do you typically consume your last caffeinated beverage?",
        "pillar_weights": {"Sleep": 6},
        "response_scores": {
            "Before 12:00 PM": 1.0,
            "12:00–2:00 PM": 1.0,
            "2:00–4:00 PM": 0.7,
            "4:00–6:00 PM": 0.4,
            "After 6:00 PM": 0.2,
        },
        "multi_select": False,
    },
    "2.35": {
        "question": "Would you consider having your last caffeinated drink earlier in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - actively working on it": 1.0,
            "Yes - open to trying": 0.8,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "2.36": {
        "question": "Have you ever worked with a nutritionist or dietitian?",
        "pillar_weights": {},
        "response_scores": {
            "Yes": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "2.37": {
        "question": "Would you consider working with a nutritionist or dietitian in the future in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - actively seeking one now": 1.0,
            "Yes - open to trying": 0.8,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "2.38": {
        "question": "Do you have any food allergies or intolerances?",
        "pillar_weights": {},
        "response_scores": {
            "Yes": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "2.39": {
        "question": "Which of the following are you allergic or intolerant to (select all that apply)?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "2.40": {
        "question": "Please describe your typical breakfast, lunch, and dinner, as well as the types of snacks consumed regularly",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,  # Free text
    },
    "2.41": {
        "question": "Do you experience any digestive issues?",
        "pillar_weights": {},
        "response_scores": {
            "Yes": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "2.42": {
        "question": "Which of the following digestive issues do you experience (select all that apply)?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "2.43": {
        "question": "What are your primary goals regarding diet and nutrition?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "2.44": {
        "question": "Please rank your diet and nutrition goals in order of importance.",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,  # Free text/rank
    },
    "2.45": {
        "question": "Have you ever followed a specific diet plan for health or weight management purposes?",
        "pillar_weights": {},
        "response_scores": {
            "Yes": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "2.46": {
        "question": "Which diet(s) have you followed in the past?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "2.47": {
        "question": "What were your primary goals when starting your dietary plan?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "2.48": {
        "question": "How long have you typically adhered to a dietary plan?",
        "pillar_weights": {},
        "response_scores": {
            "Less than 1 month": 0,
            "1-3 months": 0,
            "4-6 months": 0,
            "7-12 months": 0,
            "More than 1 year": 0,
        },
        "multi_select": False,
    },
    "2.49": {
        "question": "How successful were you in achieving your goals with these diets?",
        "pillar_weights": {},
        "response_scores": {
            "Not successful": 0,
            "Somewhat successful": 0,
            "Very successful": 0,
        },
        "multi_select": False,
    },
    "2.50": {
        "question": "What are the primary reasons you have never followed a specific diet plan?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "2.51": {
        "question": "Have you considered following a specific dietary plan for health or weight management purposes?",
        "pillar_weights": {},
        "response_scores": {
            "Yes": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "2.52": {
        "question": "Would you be willing to try a dietary plan in the future in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - open to trying": 0,
            "Maybe - need more information": 0,
            "Not now, but maybe in the future": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "2.53": {
        "question": "What factors have prevented you from starting or continuing a dietary plan in the past? (select all that apply)",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "2.54": {
        "question": "Which of the following dietary guidelines or principles would you be interested in exploring? (select all that apply)",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "2.55": {
        "question": "What diet changes, if any, have you made to improve your health? (select all that apply)",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "2.56": {
        "question": "Would you consider making any of the following dietary changes in the future? (select all that apply)",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "2.57": {
        "question": "Which of the following reasons, if any, do you feel have limited your ability to make sustainable dietary changes?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "2.58": {
        "question": "What kind of support, if any, do you think would be helpful in making sustainable dietary changes?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "2.59": {
        "question": "Do you track your daily caloric intake?",
        "pillar_weights": {"Nutrition": 1},
        "response_scores": {
            "Yes": 1.0,
            "No, but I'm generally aware of how many calories I consume each day": 0.8,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "2.60": {
        "question": "What are the primary reasons you do not track your caloric intake?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "2.61": {
        "question": "Would you consider tracking your caloric intake in the future?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - open to trying": 1.0,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },

    # ---- Custom calorie intake logic (2.62) ----
    "2.62": {
        "pillar_weights": {"Nutrition": 0},  # set to your actual weight if needed
        "score_fn": lambda calories, weight_lb, age, sex=None: calorie_intake_score(calories, weight_lb, age, sex),  # see function below
    },

    "2.63": {
        "question": "Which of the following tools do you use to track your caloric intake? (select all that apply)",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "2.64": {
        "question": "Which, if any, of the following methods would you consider as an alternative to calorie tracking? (select all that apply)",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    # --- Movement & Exercise (Section 3) ---
    "3.01": {
        "question": "How often do you engage in physical exercise?",
        "pillar_weights": {"Movement": 0},
        "response_scores": {
            "Rarely or Never": 0.2,
            "Occasionally (1–2 times per week)": 0.6,
            "Regularly (3–4 times per week)": 1.0,
            "Frequently (5 or more times per week)": 1.0,
        },
        "multi_select": False,
    },
    "3.02": {
        "question": "Would you consider exercising more frequently in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - open to trying": 1.0,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "3.12": {
        "question": "What are the primary reasons that strength training is not a part of your routine? (select all that apply)",
        "pillar_weights": {},  # No score/weighting for this
        "response_scores": {},
        "multi_select": True,
    },
    "3.13": {
        "question": "Would you consider adding strength training in support of your longevity goals?",
        "pillar_weights": {},  # No weighting per your source
        "response_scores": {
            "Yes - open to trying": 1.0,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "3.14": {
        "question": "What resources would help you start or optimize a strength training routine?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "3.15": {
        "question": "What are the primary reasons that cardio is not a part of your routine? (select all that apply)",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "3.16": {
        "question": "Would you consider adding cardio training in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes": 1.0,
            "Maybe": 0.6,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "3.17": {
        "question": "What resources would help you start or optimize a cardio training routine?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "3.18": {
        "question": "What are the primary reasons that high-intensity interval training (HIIT) is not a part of your routine? (select all that apply)",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "3.19": {
        "question": "Would you consider adding HIIT training in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - open to trying": 1.0,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "3.20": {
        "question": "What resources would help you start or optimize a HIIT training routine?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "3.21": {
        "question": "How many steps do you typically take per day?",
        "pillar_weights": {"Movement": 8},
        "response_scores": {
            "2,500–5,000": 0.4,
            "5,000–7,500": 0.6,
            "7,500–10,000": 0.8,
            "10,000–15,000": 1.0,
            "More than 15,000": 0.8,
            "I'm not sure": 0.2,
            "Less than 2,500": 0.2,
        },
        "multi_select": False,
    },
    "3.22": {
        "question": "Would you consider increasing your daily step count in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - open to trying": 1.0,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "3.23": {
        "question": "Do you use a wearable device to track steps and/or daily activity?",
        "pillar_weights": {},
        "response_scores": {
            "Yes": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "3.24": {
        "question": "Which of the following devices are you currently using to track steps and/or daily activity?",
        "pillar_weights": {},
        "response_scores": {},  # multi-select, no scoring
        "multi_select": True,
    },
    "3.25": {
        "question": "Would you consider using a wearable device to track your daily step count?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - open to trying": 0,
            "Maybe - need more information": 0,
            "Not now, but maybe in the future": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "3.26": {
        "question": "Do you have any physical restrictions or limitations that affect your physical activity choices?",
        "pillar_weights": {},
        "response_scores": {
            "Yes": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "3.27": {
        "question": "Please share a brief description of any current or chronic physical restrictions.",
        "pillar_weights": {},
        "response_scores": {},  # Free text, no scoring
        "multi_select": False,
    },
    # --- Restorative Sleep (Section 4) ---
    "4.01": {
        "question": "How would you rate the quality of your sleep?",
        "pillar_weights": {"Sleep": 0},
        "response_scores": {
            "Poor": 0.2,
            "Fair": 0.4,
            "Good": 0.6,
            "Very Good": 0.8,
            "Excellent": 1.0,
        },
        "multi_select": False,
    },
    "4.02": {
        "question": "How many hours of sleep do you typically get per night?",
        "pillar_weights": {"Sleep": 10},
        "response_scores": {
            "4 hours or less": 0.2,
            "5 hours": 0.4,
            "6 hours": 0.6,
            "7 hours": 1.0,
            "8 hours": 1.0,
            "9 hours": 1.0,
            "More than 9 hours": 0.6,
        },
        "multi_select": False,
    },
    "4.03": {
        "question": "How often do you feel rested and refreshed upon waking up?",
        "pillar_weights": {"Sleep": 5},
        "response_scores": {
            "Never": 0.2,
            "Rarely": 0.4,
            "Sometimes": 0.6,
            "Often": 0.8,
            "Always": 1.0,
        },
        "multi_select": False,
    },
    "4.04": {
        "question": "How consistent is your sleep schedule?",
        "pillar_weights": {"Sleep": 8},
        "response_scores": {
            "Very inconsistent": 0.2,
            "Somewhat inconsistent": 0.4,
            "Consistent on weekdays only": 0.6,
            "Consistent on weekends only": 0.6,
            "Very consistent": 1.0,
        },
        "multi_select": False,
    },
    "4.05": {
        "question": "Do you have a regular bedtime routine?",
        "pillar_weights": {"Sleep": 0},  # No weight per current table
        "response_scores": {
            "No": 0.2,
            "Sometimes (e.g., weekdays only)": 0.6,
            "Yes": 1.0,
        },
        "multi_select": False,
    },
    "4.06": {
        "question": "How is your daily functioning typically affected by a poor night's sleep?",
        "pillar_weights": {},  # No scoring
        "response_scores": {
            "Difficulty concentrating": 0,
            "Mood swings or irritability": 0,
            "Reduced physical performance": 0,
            "Increased stress or anxiety": 0,
            "Reduced energy levels": 0,
            "Other (please specify)": 0,
        },
        "multi_select": False,
    },
    "4.08": {
        "question": "Would you be willing to try new strategies or interventions to improve your sleep?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - open to trying": 1.0,
            "Maybe - need more information": 0.6,
            "Not now, but maybe in the future": 0.4,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "4.09": {
        "question": "Which, if any, of the following sleep hygiene protocols would you be willing to incorporate into your routine in the future?",
        "pillar_weights": {},
        "response_scores": {},  # Multi-select, not scored
        "multi_select": True,
    },
    "4.10": {
        "question": "How would you rate the comfort of your sleep environment?",
        "pillar_weights": {"Sleep": 0},
        "response_scores": {
            "Very comfortable": 1.0,
            "Somewhat comfortable": 0.8,
            "Neutral": 0.6,
            "Somewhat uncomfortable": 0.4,
            "Very uncomfortable": 0.2,
        },
        "multi_select": False,
    },
    "4.11": {
        "question": "Which, if any, of the following factors negatively affect your sleep environment?",
        "pillar_weights": {},
        "response_scores": {},  # Multi-select, not scored
        "multi_select": True,
    },
    "4.21": {
        "question": "Have you ever used a sleep tracking device or app to monitor your sleep?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
    "4.22": {
        "question": "Would you consider using a sleep tracking device or app to monitor your sleep in the future in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
    "4.23": {
        "question": "Are you currently using a sleep tracking device or app to monitor your sleep?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
    "4.24": {
        "question": "Which sleep tracker or app are you currently using?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "4.25": {
        "question": "How long have you been using each selected sleep tracker or app?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
    "4.26": {
        "question": "What were the primary reasons you stopped using a sleep tracker (select all that apply)?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "4.27": {
        "question": "Would you be willing to retry a device or app in the future in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
    # --- Cognitive Health (Section 5) ---
    "5.01": {
        "question": "How would you rate your current cognitive function (e.g., memory, attention, problem-solving, etc.)?",
        "pillar_weights": {"Cognitive": 8},
        "response_scores": {
            "Excellent": 1.0,
            "Good": 0.8,
            "Fair": 0.6,
            "Poor": 0.4,
            "Very poor": 0.2,
        },
        "multi_select": False,
    },
    "5.02": {
        "question": "Do you have any concerns about your current cognitive function?",
        "pillar_weights": {"Cognitive": 8},
        "response_scores": {
            "No": 1.0,
            "Yes": 0.2,
        },
        "multi_select": False,
    },
    "5.03": {
        "question": "What are your primary concerns?",
        "pillar_weights": {},  # Info only
        "response_scores": {},
        "multi_select": True,
    },
    "5.04": {
        "question": "Have you experienced any changes in your cognitive function over the past year?",
        "pillar_weights": {},
        "response_scores": {
            "No": 1.0,
            "Yes": 0.2,
        },
        "multi_select": False,
    },
    "5.05": {
        "question": "Which of the following changes have you noticed (select all that apply)?",
        "pillar_weights": {},  # Info only
        "response_scores": {},
        "multi_select": True,
    },
    "5.06": {
        "question": "How often do you engage in activities that challenge your brain (e.g. puzzles, reading, learning new skills, etc.)?",
        "pillar_weights": {"Cognitive": 8},
        "response_scores": {
            "Daily": 1.0,
            "Several times a week": 0.8,
            "Weekly": 0.6,
            "Occasionally": 0.4,
            "Rarely or Never": 0.2,
        },
        "multi_select": False,
    },
    "5.07": {
        "question": "Would you be willing to engage in more activities in the future in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - open to trying": 0,
            "Maybe - need more information": 0,
            "Not now, but maybe in the future": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "5.08": {
    "question": "...",
    "pillar_weights": {"Cognitive": 8},
    "score_fn": lambda answer, *a, **k: score_cognitive_activities(answer),
    "multi_select": True,
    },
    "5.09": {
        "question": "You previously indicated your sleep was 'poor' or 'fair.' Do you notice improved cognitive function on those nights when you are able to get better sleep?",
        "pillar_weights": {},  # Info only
        "response_scores": {},
        "multi_select": False,
    },
    "5.10": {
        "question": "You previously indicated that you exercise 'rarely' or 'occasionally.' Do you notice improved cognitive function on the days when you do engage in physical activity?",
        "pillar_weights": {},  # Info only
        "response_scores": {},
        "multi_select": False,
    },
    "5.11": {
        "question": "What are your primary goals related to cognitive health?",
        "pillar_weights": {},  # Info only
        "response_scores": {},
        "multi_select": True,
    },
    "5.12": {
        "question": "What types of support would you consider utilizing to improve or optimize cognitive health?",
        "pillar_weights": {},  # Info only
        "response_scores": {},
        "multi_select": True,
    },
    # --- Stress Management (Section 6) ---
    "6.01": {
        "question": "How would you rate your current level of stress?",
        "pillar_weights": {},  # Used in custom block below
        "response_scores": {}, # Used in custom block below
        "multi_select": False,
    },
    "6.02": {
        "question": "How often do you feel stressed?",
        "pillar_weights": {"Stress": 19},
        "score_fn": lambda ans, _, __, row=None: stress_score(
            row.get("6.01", ""), ans),
        "multi_select": False,
    },
    "6.03": {
        "question": "What are the primary sources of your stress?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "6.04": {
        "question": "What physical symptoms do you experience when you are stressed?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "6.05": {
        "question": "What emotional or psychological symptoms do you experience when you are stressed?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "6.06": {
        "question": "How does stress affect your daily life?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "6.07": {
        "question": "What methods do you currently use to manage your stress?",
        "pillar_weights": {"Stress": 7},
        "score_fn": lambda ans, _, __, row=None: coping_score(
            ans, COPING_WEIGHTS_6_07, row.get("6.01", ""), row.get("6.02", "")),
        "multi_select": True,
    },
    "6.08": {
        "question": "Which of the following methods would you consider using to manage your stress in the future?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "6.09": {
        "question": "How effective are your current stress management methods?",
        "pillar_weights": {},
        "response_scores": {
            "Extremely effective": 1.0,
            "Very effective": 0.8,
            "Moderately effective": 0.6,
            "Slightly effective": 0.4,
            "Not effective at all": 0.2,
        },
        "multi_select": False,
    },
    "6.10": {
        "question": "How important is it for you to improve your stress management skills?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
    "6.11": {
        "question": "How comfortable are you in seeking help for stress management?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
    "6.12": {
        "question": "What are your primary goals related to stress management?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "6.13": {
        "question": "What types of support would you find most helpful in managing your stress?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "6.14": {
        "question": "Do you use any apps or wearables to help with stress management?",
        "pillar_weights": {"Stress": 0},
        "response_scores": {
            "Yes": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "6.15": {
        "question": "Which apps or wearables are you currently using to help with stress management?",
        "pillar_weights": {"Stress": 0},
        "response_scores": {
            # All responses get zero (info only)
        },
        "multi_select": True,
    },
    "6.16": {
        "question": "Would you consider using an app or wearable to help with stress management in support of your longevity goals?",
        "pillar_weights": {"Stress": 0},
        "response_scores": {
            "Yes - open to trying": 0,
            "Maybe - need more information": 0,
            "Not now, but maybe in the future": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    # --- Connection & Purpose (Section 7) ---
    "7.01": {
        "question": "How would you rate the quality of your current social relationships?",
        "pillar_weights": {"Connection": 10},
        "response_scores": {
            "Very poor": 0.2,
            "Poor": 0.4,
            "Fair": 0.6,
            "Good": 0.8,
            "Excellent": 1.0,
        },
        "multi_select": False,
    },
    "7.02": {
        "question": "How often do you interact with friends and/or family?",
        "pillar_weights": {"Connection": 10},
        "response_scores": {
            "Rarely": 0.2,
            "Several times a month": 0.4,
            "Weekly": 0.6,
            "Several times a week": 0.8,
            "Daily": 1.0,
        },
        "multi_select": False,
    },
    "7.03": {
        "question": "What types of social activities do you typically engage in?",
        "pillar_weights": {"Connection": 0},
        "response_scores": {},
        "multi_select": True,
    },
    "7.04": {
        "question": "How satisfied are you with the amount of social interaction you have?",
        "pillar_weights": {"Connection": 8},
        "response_scores": {
            "Extremely dissatisfied": 0.2,
            "Somewhat dissatisfied": 0.4,
            "Neither satisfied nor dissatisfied": 0.6,
            "Somewhat satisfied": 0.8,
            "Extremely satisfied": 1.0,
        },
        "multi_select": False,
    },
    "7.05": {
        "question": "How would you describe your support network?",
        "pillar_weights": {"Connection": 0},
        "response_scores": {
            "Very weak": 0.2,
            "Weak": 0.4,
            "Moderate": 0.6,
            "Strong": 0.8,
            "Very strong": 1.0,
        },
        "multi_select": False,
    },
    "7.06": {
        "question": "Who do you rely on for emotional support?",
        "pillar_weights": {"Connection": 0},
        "response_scores": {},
        "multi_select": True,
    },
    "7.07": {
        "question": "Do you feel you have someone to talk to when you need support?",
        "pillar_weights": {"Connection": 9},
        "response_scores": {
            "Never": 0.2,
            "Rarely": 0.4,
            "Sometimes": 0.6,
            "Usually": 0.8,
            "Always": 1.0,
        },
        "multi_select": False,
    },
    "7.08": {
        "question": "What challenges do you face in maintaining social relationships?",
        "pillar_weights": {"Connection": 0},
        "response_scores": {},
        "multi_select": True,
    },
    "7.09": {
        "question": "How comfortable are you in social situations?",
        "pillar_weights": {"Connection": 3},
        "response_scores": {
            "Extremely uncomfortable": 0.2,
            "Somewhat uncomfortable": 0.4,
            "Neither comfortable nor uncomfortable": 0.6,
            "Somewhat comfortable": 0.8,
            "Extremely comfortable": 1.0,
        },
        "multi_select": False,
    },
    "7.10": {
        "question": "How important is it for you to improve your social interactions?",
        "pillar_weights": {"Connection": 0},
        "response_scores": {},
        "multi_select": False,
    },
    # --- Core Care: Substances and Hygiene (Section 8) ---
    "8.39": {
        "question": "What motivated you to quit the substance(s)?",
        "pillar_weights": {},
        "response_scores": {
            "Social reasons": 0,
            "Professional advice": 0,
            "Other": 0,
            "Personal or family reasons": 0,
            "Health concerns": -1,  # Only this answer gets a (negative) score
        },
        "multi_select": True,
    },
    "8.40": {
        "question": "How does your current substance use affect your daily life?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "8.41": {
        "question": "Would you consider reducing or quitting any substances to support your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - actively trying": 0,
            "Yes - open to trying": 0,
            "Maybe - need more information": 0,
            "Not now, but maybe in the future": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "8.42": {
        "question": "Which substance(s) would you consider reducing or quitting?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "8.43": {
        "question": "How important is it for you to address your substance use?",
        "pillar_weights": {},
        "response_scores": {
            "Extremely important": 0,
            "Very important": 0,
            "Moderately important": 0,
            "Slightly important": 0,
            "Not at all important": 0,
        },
        "multi_select": False,
    },
    "8.44": {
        "question": "Are you currently taking any dietary supplements to help meet your nutrition targets?",
        "pillar_weights": {},
        "response_scores": {
            "Yes": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "8.45": {
        "question": "Please list all dietary supplements you are currently taking.",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
    "8.46": {
        "question": "Would you consider adding dietary supplements with proven benefits to your regimen in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - open to trying": 0,
            "Maybe - need more information": 0,
            "Not now, but maybe in the future": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "8.47": {
        "question": "Are you currently taking any supplements to support your training, exercise, performance, or recovery?",
        "pillar_weights": {},
        "response_scores": {
            "Yes": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "8.48": {
        "question": "Please list all performance or recovery supplements you are currently taking.",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
    "8.49": {
        "question": "Would you consider adding performance or recovery supplements with proven benefits to your regimen in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - open to trying": 0,
            "Maybe - need more information": 0,
            "Not now, but maybe in the future": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "8.50": {
        "question": "Do you take sleep aids or medications to help you sleep?",
        "pillar_weights": {},
        "response_scores": {
            "Yes": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "8.51": {
        "question": "How often do you take sleep aids or medications to help you sleep?",
        "pillar_weights": {},
        "response_scores": {
            "Rarely": 0,
            "Occasionally": 0,
            "Frequently": 0,
            "Always": 0,
        },
        "multi_select": False,
    },
    "8.52": {
        "question": "Which of the following types of sleep aids or medications do you take to help you sleep?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "8.53": {
        "question": "Please select all natural supplements you are currently taking for sleep:",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "8.54": {
        "question": "If appropriate, would you consider taking supplements with proven sleep quality benefits in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - open to trying": 0,
            "Maybe - need more information": 0,
            "Not now, but maybe in the future": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "8.55": {
        "question": "Are you currently taking any additional supplements to support your general health or well-being (e.g., cognitive function supplements, peptides, etc.)?",
        "pillar_weights": {},
        "response_scores": {
            "Yes": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "8.56": {
        "question": "Please list any additional supplements you are taking to support your general health and well-being.",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
    "8.57": {
        "question": "If appropriate,  would you consider taking supplements with proven general health and well-being benefits in support of your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - open to trying": 0,
            "Maybe - need more information": 0,
            "Not now, but maybe in the future": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "8.58": {
        "question": "How often do you floss your teeth?",
        "pillar_weights": {"CoreCare": 6},
        "response_scores": {
            "Daily": 1.0,
            "A few times a week": 0.7,
            "Rarely": 0.4,
            "Never": 0.2,
        },
        "multi_select": False,
    },
    "8.59": {
        "question": "Would you consider flossing more often to support your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - open to trying": 0,
            "Maybe - need more information": 0,
            "Not now, but maybe in the future": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "8.60": {
        "question": "How often do you brush your teeth?",
        "pillar_weights": {"CoreCare": 7},
        "response_scores": {
            "≥2 times a day": 1.0,
            "<2 times a day": 0.2,
        },
        "multi_select": False,
    },
    "8.61": {
        "question": "Would you consider brushing more often to support your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - open to trying": 0,
            "Maybe - need more information": 0,
            "Not now, but maybe in the future": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "8.62": {
        "question": "How often do you apply sunscreen to your face and neck?",
        "pillar_weights": {"CoreCare": 4},
        "response_scores": {
            "Daily": 1.0,
            "A few times a week": 0.7,
            "Rarely": 0.4,
            "Never": 0.2,
        },
        "multi_select": False,
    },
    "8.63": {
        "question": "Would you consider applying sunscreen more often to support your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - open to trying": 0,
            "Maybe - need more information": 0,
            "Not now, but maybe in the future": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    "8.64": {
        "question": "Do you have a consistent morning and/or evening skincare routine?",
        "pillar_weights": {"CoreCare": 2},
        "response_scores": {
            "Yes": 1.0,
            "No": 0.2,
        },
        "multi_select": False,
    },
    "8.65": {
        "question": "Would you consider adding a consistent morning and/or evening skincare routine to support your longevity goals?",
        "pillar_weights": {},
        "response_scores": {
            "Yes - open to trying": 0,
            "Maybe - need more information": 0,
            "Not now, but maybe in the future": 0,
            "No": 0,
        },
        "multi_select": False,
    },
    # --- Core Care: Personal & Family History (Section 9) ---

        # -- ASCVD
    "9.01": {
        "question": "Do you have a family history of Heart Attack/ASCVD?",
        "pillar_weights": {"CoreCare": 10},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.02": {
        "question": "Which relative was diagnosed with Heart Attack/ASCVD?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "9.03": {
        "question": "Approximate age at diagnosis for your relative with Heart Attack/ASCVD?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },

        # -- Stroke
    "9.04": {
        "question": "Do you have a family history of Stroke?",
        "pillar_weights": {"CoreCare": 10},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.05": {
        "question": "Which relative was diagnosed with Stroke?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "9.06": {
        "question": "Approximate age at diagnosis for your relative with Stroke?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },

        # -- Diabetes
    "9.07": {
        "question": "Do you have a family history of Diabetes?",
        "pillar_weights": {"CoreCare": 7},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.08": {
        "question": "Which relative was diagnosed with Diabetes?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "9.09": {
        "question": "Approximate age at diagnosis for your relative with Diabetes?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },

        # -- Dementia/Alzheimer's
    "9.10": {
        "question": "Do you have a family history of Dementia/Alzheimer's?",
        "pillar_weights": {"CoreCare": 7},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.11": {
        "question": "Which relative was diagnosed with Dementia/Alzheimer's?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "9.12": {
        "question": "Approximate age at diagnosis for your relative with Dementia/Alzheimer's?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },

        # -- Breast Cancer
    "9.13": {
        "question": "Do you have a family history of Breast Cancer?",
        "pillar_weights": {"CoreCare": 7},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.14": {
        "question": "Which relative was diagnosed with Breast Cancer?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "9.15": {
        "question": "Approximate age at diagnosis for your relative with Breast Cancer?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },

        # -- Colon Cancer
    "9.16": {
        "question": "Do you have a family history of Colon Cancer?",
        "pillar_weights": {"CoreCare": 7},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.17": {
        "question": "Which relative was diagnosed with Colon Cancer?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "9.18": {
        "question": "Approximate age at diagnosis for your relative with Colon Cancer?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },

        # -- Prostate Cancer
    "9.19": {
        "question": "Do you have a family history of Prostate Cancer?",
        "pillar_weights": {"CoreCare": 5},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.20": {
        "question": "Which relative was diagnosed with Prostate Cancer?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "9.21": {
        "question": "Approximate age at diagnosis for your relative with Prostate Cancer?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },

        # -- Other Cancer
    "9.22": {
        "question": "Do you have a family history of Other Cancer?",
        "pillar_weights": {"CoreCare": 5},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.23": {
        "question": "Please specify the type of other cancer.",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
    "9.24": {
        "question": "Which relative was diagnosed with Other Cancer?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "9.25": {
        "question": "Approximate age at diagnosis for your relative with Other Cancer?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },

        # -- Osteoporosis/Osteopenia
    "9.26": {
        "question": "Do you have a family history of Osteoporosis/Osteopenia?",
        "pillar_weights": {"CoreCare": 7},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.27": {
        "question": "Which relative was diagnosed with Osteoporosis/Osteopenia?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "9.28": {
        "question": "Approximate age at diagnosis for your relative with Osteoporosis/Osteopenia?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },

        # -- Autoimmune Disease
    "9.29": {
        "question": "Do you have a family history of Autoimmune disease?",
        "pillar_weights": {"CoreCare": 7},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.30": {
        "question": "Which relative was diagnosed with Autoimmune disease?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "9.31": {
        "question": "Approximate age at diagnosis for your relative with Autoimmune disease?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },

        # -- Mental Health Issues
    "9.32": {
        "question": "Do you have a family history of Mental Health issues?",
        "pillar_weights": {"CoreCare": 5},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.33": {
        "question": "Which relative was diagnosed with Mental Health issues?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "9.34": {
        "question": "Approximate age at diagnosis for your relative with Mental Health issues?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },

        # -- Substance Use
    "9.35": {
        "question": "Do you have a family history of Substance Use?",
        "pillar_weights": {"CoreCare": 5},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.36": {
        "question": "Which relative struggled with Substance Use?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": True,
    },
    "9.37": {
        "question": "Approximate age when your relative's Substance Use became a concern (if known)?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },

        # -- Other Significant Health History
    "9.38": {
        "question": "Do you have a family history of any Other Significant Health History (e.g., liver disease, kidney disease)?",
        "pillar_weights": {"CoreCare": 5},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.39": {
        "question": "Please specify the condition(s) and which relative was affected.",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
        # --- Personal diagnosis: Heart Attack/ASCVD
    "9.40": {
        "question": "Have you been diagnosed with Heart Attack or ASCVD (Atherosclerotic Cardiovascular Disease)?",
        "pillar_weights": {"CoreCare": 10},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.41": {
        "question": "At what age were you diagnosed with Heart Attack or ASCVD?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
        # --- Personal diagnosis: Stroke
    "9.42": {
        "question": "Have you been diagnosed with Stroke?",
        "pillar_weights": {"CoreCare": 10},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.43": {
        "question": "At what age were you diagnosed with Stroke?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
        # --- Personal diagnosis: Diabetes
    "9.44": {
        "question": "Have you been diagnosed with Diabetes?",
        "pillar_weights": {"CoreCare": 10},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.45": {
        "question": "At what age were you diagnosed with Diabetes?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
        # --- Personal diagnosis: Dementia/Alzheimer's
    "9.46": {
        "question": "Have you been diagnosed with Dementia or Alzheimer's?",
        "pillar_weights": {"CoreCare": 10},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.47": {
        "question": "At what age were you diagnosed with Dementia or Alzheimer's?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
        # --- Personal diagnosis: Breast Cancer
    "9.48": {
        "question": "Have you been diagnosed with Breast Cancer?",
        "pillar_weights": {"CoreCare": 10},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.49": {
        "question": "At what age were you diagnosed with Breast Cancer?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
        # --- Personal diagnosis: Colon Cancer
    "9.50": {
        "question": "Have you been diagnosed with Colon Cancer?",
        "pillar_weights": {"CoreCare": 10},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.51": {
        "question": "At what age were you diagnosed with Colon Cancer?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
        # --- Personal diagnosis: Prostate Cancer
    "9.52": {
        "question": "Have you been diagnosed with Prostate Cancer?",
        "pillar_weights": {"CoreCare": 10},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.53": {
        "question": "At what age were you diagnosed with Prostate Cancer?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
        # --- Personal diagnosis: Other Cancer
    "9.54": {
        "question": "Have you been diagnosed with any other type of cancer?",
        "pillar_weights": {"CoreCare": 10},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.55": {
        "question": "Please specify the cancer type and age at diagnosis.",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
        # --- Personal diagnosis: Osteoporosis/Osteopenia
    "9.56": {
        "question": "Have you been diagnosed with Osteoporosis or Osteopenia?",
        "pillar_weights": {"CoreCare": 10},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.57": {
        "question": "At what age were you diagnosed with Osteoporosis or Osteopenia?",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
        # --- Personal diagnosis: Autoimmune Disease
    "9.58": {
        "question": "Have you been diagnosed with an autoimmune disease?",
        "pillar_weights": {"CoreCare": 10},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.59": {
        "question": "Please specify the autoimmune condition and age at diagnosis.",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
        # --- Personal diagnosis: Mental Health
    "9.60": {
        "question": "Have you been diagnosed with a mental health condition?",
        "pillar_weights": {"CoreCare": 10},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.61": {
        "question": "Please specify the condition and age at diagnosis.",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
        # --- Personal diagnosis: Substance Use Disorder
    "9.62": {
        "question": "Have you had any substance use disorder diagnosis?",
        "pillar_weights": {"CoreCare": 10},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.63": {
        "question": "Please describe the substance and age at diagnosis.",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
        # --- Personal diagnosis: Other Significant Health History
    "9.64": {
        "question": "Do you have any other significant health history (e.g., liver or kidney disease)?",
        "pillar_weights": {"CoreCare": 10},
        "response_scores": {"Yes": 0.2, "No": 1.0},
        "multi_select": False,
    },
    "9.65": {
        "question": "Please describe the condition and age at diagnosis.",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },

    # --- Core Care: Screening & Named Tests (Section 10) ---
    "10.01": {
        "question": "Please indicate when you last had a routine dental exam",
        "pillar_weights": {"CoreCare": 8},
        "score_fn": lambda x, *_: score_date_response(x, screen_guidelines['10.01']),
        "multi_select": False,
    },
    "10.02": {
        "question": "Please indicate when you last had a routine skin check",
        "pillar_weights": {"CoreCare": 7},
        "score_fn": lambda x, *_: score_date_response(x, screen_guidelines['10.02']),
        "multi_select": False,
    },
    "10.03": {
        "question": "Please indicate when you last had a routine vision check",
        "pillar_weights": {"CoreCare": 5},
        "score_fn": lambda x, *_: score_date_response(x, screen_guidelines['10.03']),
        "multi_select": False,
    },
    "10.04": {
        "question": "Please indicate when you last had a colon cancer screening",
        "pillar_weights": {"CoreCare": 10},
        "score_fn": lambda x, *_: score_date_response(x, screen_guidelines['10.04']),
        "multi_select": False,
    },
    "10.05": {
        "question": "Please indicate when you last had a mammogram",
        "pillar_weights": {"CoreCare": 10},
        "score_fn": lambda x, *_: score_date_response(x, screen_guidelines['10.05']),
        "multi_select": False,
    },
    "10.06": {
        "question": "Please indicate when you last had a PAP smear",
        "pillar_weights": {"CoreCare": 10},
        "score_fn": lambda x, *_: score_date_response(x, screen_guidelines['10.06']),
        "multi_select": False,
    },
    "10.07": {
        "question": "Please indicate when you last had a DEXA scan",
        "pillar_weights": {"CoreCare": 0},
        "score_fn": lambda x, *_: score_date_response(x, screen_guidelines['10.07']),
        "multi_select": False,
    },
    "10.08": {
        "question": "Please indicate when you last had a PSA screening",
        "pillar_weights": {"CoreCare": 10},
        "score_fn": lambda x, *_: score_date_response(x, screen_guidelines['10.08']),
        "multi_select": False,
    },
    "10.09": {
        "question": "Have you had any cardiac health screening, such as a stress test or coronary calcium scan?",
        "pillar_weights": {"CoreCare": 8},
        "response_scores": {"Yes": 1.0, "No": 0.2},
        "multi_select": False,
    },
    "10.10": {
        "question": "Have you ever had a sleep study test?",
        "pillar_weights": {"CoreCare": 5},
        "response_scores": {"Yes": 1.0, "No": 0.2},
        "multi_select": False,
    },
    "10.11": {
        "question": "Are you up to date on immunizations?",
        "pillar_weights": {"CoreCare": 10},
        "response_scores": {"Yes": 1.0, "No": 0.2},
        "multi_select": False,
    },
    "10.12": {
        "question": "Please list any prescription medications that you are currently taking.",
        "pillar_weights": {},
        "response_scores": {},
        "multi_select": False,
    },
        # --- Mental health symptom checks
    "10.13": {
        "question": "Over the last two weeks, how often have you been bothered by having little interest or pleasure in doing things?",
        "pillar_weights": {"Stress": 10},
        "response_scores": {
            "Not at all": 1.0,
            "Several days": 0.6,
            "More than half the days": 0.4,
            "Nearly every day": 0.2,
        },
        "multi_select": False,
    },
    "10.14": {
        "question": "Over the last two weeks, how often have you been bothered by feeling down, depressed, or hopeless?",
        "pillar_weights": {"Stress": 10},
        "response_scores": {
            "Not at all": 1.0,
            "Several days": 0.6,
            "More than half the days": 0.4,
            "Nearly every day": 0.2,
        },
        "multi_select": False,
    },
    "10.15": {
        "question": "Over the last two weeks, how often have you been bothered by feeling nervous, anxious, or on edge?",
        "pillar_weights": {"Stress": 10},
        "response_scores": {
            "Not at all": 1.0,
            "Several days": 0.6,
            "More than half the days": 0.4,
            "Nearly every day": 0.2,
        },
        "multi_select": False,
    },
    "10.16": {
        "question": "Over the last two weeks, how often have you been bothered by not being able to stop or control worrying?",
        "pillar_weights": {"Stress": 10},
        "response_scores": {
            "Not at all": 1.0,
            "Several days": 0.6,
            "More than half the days": 0.4,
            "Nearly every day": 0.2,
        },
        "multi_select": False,
    },
        # --- Optimism, life satisfaction, and coping (single-score, pillarless unless you want to map)
    "10.17": {
        "question": "Please indicate your agreement with the following statement: I feel optimistic about my future.",
        "pillar_weights": {},
        "response_scores": {
            "Strongly agree": 7,
            "Agree": 6,
            "Slightly agree": 5,
            "Neither agree nor disagree": 4,
            "Slightly disagree": 3,
            "Disagree": 2,
            "Strongly disagree": 1,
        },
        "multi_select": False,
    },
    "10.18": {
        "question": "Please indicate your agreement with the following statement: I can cope with challenges in daily life.",
        "pillar_weights": {},
        "response_scores": {
            "Strongly agree": 7,
            "Agree": 6,
            "Slightly agree": 5,
            "Neither agree nor disagree": 4,
            "Slightly disagree": 3,
            "Disagree": 2,
            "Strongly disagree": 1,
        },
        "multi_select": False,
    },
    "10.19": {
        "question": "Please indicate your agreement with the following statement: I feel that life is very rewarding.",
        "pillar_weights": {},
        "response_scores": {
            "Strongly agree": 7,
            "Agree": 6,
            "Slightly agree": 5,
            "Neither agree nor disagree": 4,
            "Slightly disagree": 3,
            "Disagree": 2,
            "Strongly disagree": 1,
        },
        "multi_select": False,
    },
    "10.20": {
        "question": "Please indicate your agreement with the following statement: I feel happy with the way I am.",
        "pillar_weights": {},
        "response_scores": {
            "Strongly agree": 7,
            "Agree": 6,
            "Slightly agree": 5,
            "Neither agree nor disagree": 4,
            "Slightly disagree": 3,
            "Disagree": 2,
            "Strongly disagree": 1,
        },
        "multi_select": False,
    },
    "10.21": {
        "question": "Please indicate your agreement with the following statement: If I could live my life over, I would change almost nothing.",
        "pillar_weights": {},
        "response_scores": {
            "Strongly agree": 7,
            "Agree": 6,
            "Slightly agree": 5,
            "Neither agree nor disagree": 4,
            "Slightly disagree": 3,
            "Disagree": 2,
            "Strongly disagree": 1,
        },
        "multi_select": False,
    },
        # --- STOPBANG Sleep Apnea Screening
    "10.22": {
        "question": "Do you snore loudly?",
        "pillar_weights": {},
        "response_scores": {"Yes": 0, "No": 1},
        "multi_select": False,
    },
    "10.23": {
        "question": "Do you often feel tired, fatigued, or sleepy during the daytime?",
        "pillar_weights": {},
        "response_scores": {"Yes": 0, "No": 1},
        "multi_select": False,
    },
    "10.24": {
        "question": "Has anyone observed you stop breathing during sleep?",
        "pillar_weights": {},
        "response_scores": {"Yes": 0, "No": 1},
        "multi_select": False,
    },
    "10.25": {
        "question": "Do you have (or are being treated for) high blood pressure?",
        "pillar_weights": {},
        "response_scores": {"Yes": 0, "No": 1},
        "multi_select": False,
    },
        # --- Epworth Sleepiness Scale
    "10.26": {
        "question": "How likely are you to nod off or fall asleep when Sitting and reading, in contrast to just feeling tired?",
        "pillar_weights": {},
        "response_scores": {
            "Would never nod off": 0,
            "Slight chance of nodding off": 1,
            "Moderate chance of nodding off": 2,
            "High chance of nodding off": 3,
        },
        "multi_select": False,
    },
    "10.27": {
        "question": "How likely are you to nod off or fall asleep when Watching TV, in contrast to just feeling tired?",
        "pillar_weights": {},
        "response_scores": {
            "Would never nod off": 0,
            "Slight chance of nodding off": 1,
            "Moderate chance of nodding off": 2,
            "High chance of nodding off": 3,
        },
        "multi_select": False,
    },
    "10.28": {
        "question": "How likely are you to nod off or fall asleep when Sitting inactive in a public place, in contrast to just feeling tired?",
        "pillar_weights": {},
        "response_scores": {
            "Would never nod off": 0,
            "Slight chance of nodding off": 1,
            "Moderate chance of nodding off": 2,
            "High chance of nodding off": 3,
        },
        "multi_select": False,
    },
    "10.29": {
        "question": "How likely are you to nod off or fall asleep when Passenger in a car for an hour without a break, in contrast to just feeling tired?",
        "pillar_weights": {},
        "response_scores": {
            "Would never nod off": 0,
            "Slight chance of nodding off": 1,
            "Moderate chance of nodding off": 2,
            "High chance of nodding off": 3,
        },
        "multi_select": False,
    },
    "10.30": {
        "question": "How likely are you to nod off or fall asleep when Lying down to rest, in contrast to just feeling tired?",
        "pillar_weights": {},
        "response_scores": {
            "Would never nod off": 0,
            "Slight chance of nodding off": 1,
            "Moderate chance of nodding off": 2,
            "High chance of nodding off": 3,
        },
        "multi_select": False,
    },
    "10.31": {
        "question": "How likely are you to nod off or fall asleep when Sitting and talking to someone, in contrast to just feeling tired?",
        "pillar_weights": {},
        "response_scores": {
            "Would never nod off": 0,
            "Slight chance of nodding off": 1,
            "Moderate chance of nodding off": 2,
            "High chance of nodding off": 3,
        },
        "multi_select": False,
    },
    "10.32": {
        "question": "How likely are you to nod off or fall asleep when Sitting quietly after a meal without alcohol, in contrast to just feeling tired?",
        "pillar_weights": {},
        "response_scores": {
            "Would never nod off": 0,
            "Slight chance of nodding off": 1,
            "Moderate chance of nodding off": 2,
            "High chance of nodding off": 3,
        },
        "multi_select": False,
    },
    "10.33": {
        "question": "How likely are you to nod off or fall asleep when In a car stopped in traffic, in contrast to just feeling tired?",
        "pillar_weights": {},
        "response_scores": {
            "Would never nod off": 0,
            "Slight chance of nodding off": 1,
            "Moderate chance of nodding off": 2,
            "High chance of nodding off": 3,
        },
        "multi_select": False,
    },
}

import inspect
import pandas as pd

# --- Constants ---
PILLARS = [
    "Nutrition", "Movement", "Sleep", "Cognitive",
    "Stress", "Connection", "CoreCare"
]

pillar_map = {
    "Nutrition": "Healthful Nutrition",
    "Movement": "Movement + Exercise",
    "Sleep": "Restorative Sleep",
    "Cognitive": "Cognitive Health",
    "Stress": "Stress Management",
    "Connection": "Connection + Purpose",
    "CoreCare": "Core Care",
}

# --- First Pass: Per-question scoring (raw + weighted + max) ---

# Use relative paths from the script location
base_dir = os.path.dirname(os.path.abspath(__file__))
survey_output_dir = os.path.join(base_dir, "WellPath_Score_Survey")

all_scores = []
for idx, row in patient_survey.iterrows():
    patient_id = row['patient_id']
    profile = biomarker_df[biomarker_df['patient_id'] == patient_id].iloc[0]
    weight_lb = profile['weight_lb']
    age = profile['age']
    sex = profile.get('sex', 'male')

    patient_result = {'patient_id': patient_id}

    for qid, config in QUESTION_CONFIG.items():
        answer = row.get(qid, "")
        
        # Calculate max possible score for this question
        max_possible_score = 0
        if "response_scores" in config and config["response_scores"]:
            max_possible_score = max(config["response_scores"].values())
        elif "score_fn" in config:
            max_possible_score = 10  # assume max raw for custom scoring fn
        
        # Scale max score same way as actual score
        max_score_scaled = max_possible_score / 10 if max_possible_score > 1 else max_possible_score
        
        # Custom date screening logic
        if qid in screen_guidelines:
            score = score_date_response(answer, screen_guidelines[qid])
        # Custom scoring functions
        elif "score_fn" in config:
            fn_args = inspect.signature(config["score_fn"]).parameters
            if 'sex' in fn_args:
                score = config["score_fn"](answer, weight_lb, age, sex)
            elif 'row' in fn_args:
                score = config["score_fn"](answer, weight_lb, age, row=row)
            else:
                score = config["score_fn"](answer, weight_lb, age)
        else:
            score = config["response_scores"].get(str(answer).strip(), 0)

        # Scale to 0-1 if >1 (assuming scale 0-10), else leave as is
        score_scaled = score / 10 if score is not None and score > 1 else score

        for pillar, wt in config.get("pillar_weights", {}).items():
            if wt:
                patient_result[f"{qid}_{pillar}_weighted"] = score_scaled * wt
                patient_result[f"{qid}_{pillar}_raw"] = score_scaled
                patient_result[f"{qid}_{pillar}_max"] = max_score_scaled * wt

    # Movement scoring (custom logic)
    move_scores = score_movement_pillar(row, movement_questions)
    for (move_type, pillar), score in move_scores.items():
        if score:
            patient_result[f"{move_type}_{pillar}_weighted"] = score
            patient_result[f"{move_type}_{pillar}_raw"] = score
            # Max for movement questions is the full weight (since they're already weighted)
            patient_result[f"{move_type}_{pillar}_max"] = movement_questions[move_type]["pillar_weights"][pillar]

    # Sleep issues scoring
    sleep_issues_scores = score_sleep_issues(row)
    for pillar, score in sleep_issues_scores.items():
        patient_result[f"4.12_{pillar}_weighted"] = score
        patient_result[f"4.12_{pillar}_raw"] = score
        # Max for sleep issues is the sum of all weights for that pillar
        max_sleep_issues_for_pillar = sum(pillar_wts.get(pillar, 0) for _, _, pillar_wts in SLEEP_ISSUES)
        patient_result[f"4.12_{pillar}_max"] = max_sleep_issues_for_pillar

    # Sleep hygiene protocols scoring
    sleep_proto_score = score_sleep_protocols(row.get("4.07", ""))
    if sleep_proto_score:
        patient_result["4.07_Sleep_weighted"] = sleep_proto_score
        patient_result["4.07_Sleep_raw"] = sleep_proto_score
        patient_result["4.07_Sleep_max"] = 9.0  # Max weight for sleep hygiene

    # Substance use scoring
    sub_scores = get_substance_score(row)
    for sub, weighted_score in sub_scores.items():
        patient_result[f"{sub}_CoreCare_weighted"] = weighted_score
        patient_result[f"{sub}_CoreCare_raw"] = weighted_score
        # Max for substances is the full weight (since scoring returns weighted values)
        patient_result[f"{sub}_CoreCare_max"] = SUBSTANCE_WEIGHTS[sub]

    all_scores.append(patient_result)

# Create DataFrame and save per-question detailed scoring
df_debug = pd.DataFrame(all_scores).fillna(0)
df_debug.to_csv(os.path.join(survey_output_dir, "per_question_scores_full_weighted.csv"), index=False)
print("✓ Per-question raw, weighted, and max scores saved to WellPath_Score_Survey/per_question_scores_full_weighted.csv")

# --- NEW: Create gap analysis export ---
gap_analysis = []
for idx, row in df_debug.iterrows():
    patient_id = row['patient_id']
    
    # Extract all weighted, max, and raw columns
    weighted_cols = [col for col in df_debug.columns if col.endswith('_weighted')]
    
    for weighted_col in weighted_cols:
        # Parse the column name to get question and pillar
        base_name = weighted_col.replace('_weighted', '')
        max_col = f"{base_name}_max"
        raw_col = f"{base_name}_raw"
        
        if max_col in df_debug.columns:
            actual_weighted = row[weighted_col]
            max_weighted = row[max_col]
            actual_raw = row.get(raw_col, 0)
            
            # Calculate gaps
            weighted_gap = max_weighted - actual_weighted
            weighted_gap_pct = (weighted_gap / max_weighted * 100) if max_weighted > 0 else 0
            
            # Determine question type and parse name
            if '_' in base_name:
                parts = base_name.split('_', 1)
                if len(parts) == 2:
                    question_id = parts[0]
                    pillar = parts[1]
                else:
                    question_id = base_name
                    pillar = "Unknown"
            else:
                question_id = base_name
                pillar = "Unknown"
            
            gap_analysis.append({
                'patient_id': patient_id,
                'question_id': question_id,
                'pillar': pillar,
                'actual_raw_score': actual_raw,
                'actual_weighted_score': actual_weighted,
                'max_weighted_score': max_weighted,
                'weighted_gap': weighted_gap,
                'weighted_gap_percent': weighted_gap_pct,
                'impact_potential': weighted_gap  # This is the direct impact if improved to max
            })

# Create gap analysis DataFrame
gap_df = pd.DataFrame(gap_analysis)

# Filter out rows with 0 gaps (already optimal)
gap_df = gap_df[gap_df['weighted_gap'] > 0]

# Sort by impact potential (descending) to show highest impact opportunities first
gap_df = gap_df.sort_values(['patient_id', 'impact_potential'], ascending=[True, False])

# Save gap analysis
gap_df.to_csv(os.path.join(survey_output_dir, "question_gap_analysis.csv"), index=False)
print("✓ Gap analysis saved to WellPath_Score_Survey/question_gap_analysis.csv")

# Optional: Create a summary by patient showing top opportunities
print("\nTop 5 improvement opportunities per patient:")
for patient_id in gap_df['patient_id'].unique()[:3]:  # Show first 3 patients as example
    patient_gaps = gap_df[gap_df['patient_id'] == patient_id].head(5)
    print(f"\nPatient {patient_id}:")
    for _, gap_row in patient_gaps.iterrows():
        print(f"  {gap_row['question_id']} ({gap_row['pillar']}): {gap_row['impact_potential']:.1f} point potential")

# --- Second Pass: Aggregate pillar scores and calculate max and percentages ---

# Aggregate pillar totals by summing all weighted columns per pillar
for pillar in PILLARS:
    col_suffix = f"_{pillar}_weighted"
    pillar_cols = [col for col in df_debug.columns if col.endswith(col_suffix)]
    if pillar_cols:
        df_debug[pillar_map[pillar]] = df_debug[pillar_cols].sum(axis=1)
    else:
        df_debug[pillar_map[pillar]] = 0

# Calculate max possible weighted scores per pillar
max_scores_per_pillar = {pillar: 0 for pillar in PILLARS}

for qid, config in QUESTION_CONFIG.items():
    for pillar, wt in config.get("pillar_weights", {}).items():
        if not wt or wt == 0:
            continue
        max_resp = 0
        if "response_scores" in config and config["response_scores"]:
            max_resp = max(config["response_scores"].values())
        elif "score_fn" in config:
            max_resp = 10  # assume max raw for custom scoring fn
        # scale max_resp same way as score_scaled above
        max_resp_scaled = max_resp / 10 if max_resp > 1 else max_resp
        max_scores_per_pillar[pillar] += max_resp_scaled * wt

# Add full weight for each movement question pillar weight
for cfg in movement_questions.values():
    for pillar, wt in cfg.get("pillar_weights", {}).items():
        max_scores_per_pillar[pillar] += wt

# Add Sleep Issues max weight total
sleep_issues_weight = sum(pillar_wts.get("Sleep", 0) for _, _, pillar_wts in SLEEP_ISSUES)
max_scores_per_pillar["Sleep"] += sleep_issues_weight

sleep_issues_corecare = sum(pillar_wts.get("CoreCare", 0) for _, _, pillar_wts in SLEEP_ISSUES)
max_scores_per_pillar["CoreCare"] += sleep_issues_corecare

sleep_issues_movement = sum(pillar_wts.get("Movement", 0) for _, _, pillar_wts in SLEEP_ISSUES)
max_scores_per_pillar["Movement"] += sleep_issues_movement

# Add Sleep Hygiene fixed weight (4.07)
max_scores_per_pillar["Sleep"] += 9.0

# Add Substance weights to CoreCare
max_scores_per_pillar["CoreCare"] += sum(SUBSTANCE_WEIGHTS.values())

# Add substance scores to individual substance columns
for idx, row_data in df_debug.iterrows():
    patient_id = row_data['patient_id']
    
    # Find the original patient survey row
    orig_row = patient_survey[patient_survey['patient_id'] == patient_id]
    if not orig_row.empty:
        orig_row = orig_row.iloc[0]
        
        # Calculate substance scores for this patient
        sub_scores = get_substance_score(orig_row)
        
        # Populate the substance columns
        for sub, weighted_score in sub_scores.items():
            df_debug.at[idx, f"Substance: {sub}"] = weighted_score
            
# Add max and percentage columns
for pillar in PILLARS:
    max_possible = max_scores_per_pillar.get(pillar, 1)  # avoid zero division
    col_name = pillar_map[pillar]
    df_debug[f"{col_name}_Max"] = max_possible
    df_debug[f"{col_name}_Pct"] = (df_debug[col_name] / max_possible) * 100

# Ensure substance columns exist
substance_cols = [
    "Substance: Tobacco",
    "Substance: Alcohol",
    "Substance: Recreational Drugs",
    "Substance: Nicotine",
    "Substance: OTC Meds",
    "Substance: Other Substances"
]
for sub in substance_cols:
    if sub not in df_debug.columns:
        df_debug[sub] = 0

# Final output columns order
final_cols = ["patient_id"] + [pillar_map[p] for p in PILLARS] + \
             [f"{pillar_map[p]}_Max" for p in PILLARS] + \
             [f"{pillar_map[p]}_Pct" for p in PILLARS] + substance_cols

scores_df = df_debug[final_cols]
scores_df.to_csv(os.path.join(survey_output_dir, "synthetic_patient_pillar_scores_survey_with_max_pct.csv"), index=False)
print("✓ Final pillar scores saved to WellPath_Score_Survey/synthetic_patient_pillar_scores_survey_with_max_pct.csv")
print("\n✅ Survey scoring complete!")
print(scores_df.head())
