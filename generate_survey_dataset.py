import os
import pandas as pd
import random

# ====================
# ANSWER LOGIC FOR OVERVIEW (SECTION 1)
# ====================
def answer_1_01(patient):
    """Which of the following areas are you most interested in improving right now (select all that apply)?"""
    choices = []
    if patient.get('diet_quality', '') == 'poor':
        choices.append("Healthful Nutrition")
    if float(patient.get('sleep_score', 7)) < 6.5:
        choices.append("Restorative Sleep")
    if patient.get('stress_level', '') == 'high':
        choices.append("Stress Management")
    if patient.get('health_profile', '') == 'poor' or patient.get('fitness_level', '') == 'low':
        choices.append("Movement and Exercise")
    # No other fields! Do NOT add extras!
    return sorted(set(choices))

def answer_1_02(patient):
    """Which areas NOT interested in focusing on initially (select all that apply)?"""
    choices = []
    if patient.get('diet_quality', '') == 'good':
        choices.append("Healthful Nutrition")
    if float(patient.get('sleep_score', 7)) > 8.5:
        choices.append("Restorative Sleep")
    if patient.get('stress_level', '') == 'low':
        choices.append("Stress Management")
    if patient.get('health_profile', '') == 'fit' or patient.get('fitness_level', '') == 'high':
        choices.append("Movement and Exercise")
    return sorted(set(choices))

def answer_1_03(patient, most_interested, not_interested):
    """Please rank your selected focus areas in order of personal importance."""
    areas = most_interested + [a for a in not_interested if a not in most_interested]
    problem_areas = []
    if "Healthful Nutrition" in areas and patient.get('diet_quality', '') == 'poor':
        problem_areas.append("Healthful Nutrition")
    if "Restorative Sleep" in areas and float(patient.get('sleep_score', 7)) < 6.5:
        problem_areas.append("Restorative Sleep")
    if "Stress Management" in areas and patient.get('stress_level', '') == 'high':
        problem_areas.append("Stress Management")
    if "Movement and Exercise" in areas and (
        patient.get('health_profile', '') == 'poor' or patient.get('fitness_level', '') == 'low'
    ):
        problem_areas.append("Movement and Exercise")
    # Add the rest (excluding already included)
    other_areas = [a for a in areas if a not in problem_areas]
    # Could shuffle or keep order—up to you
    ranking = problem_areas + other_areas
    return ranking

def answer_1_04(patient):
    """What motivates you most to prioritize health/longevity? (select all)"""
    choices = []
    if int(patient.get('age', 50)) < 35:
        choices.append("Athletic performance")
    if patient.get('family_history', False):
        choices.append("Prevent disease")
    if patient.get('stress_level', '') == 'high':
        choices.append("Reduce stress")
    # Default motivator if nothing above
    if not choices:
        choices.append("General well-being")
    return sorted(set(choices))

def answer_1_05(patient):
    """How do you prefer to stay motivated/accountable? (select all)"""
    choices = []
    if patient.get('athlete', '') == 'yes':
        choices.append("Tracking")
    if int(patient.get('age', 50)) > 50:
        choices.append("Support group")
    # Always give at least one, if none
    if not choices:
        choices.append("Apps")
    return sorted(set(choices))

def answer_1_06(patient):
    """Please describe your personal health goals or longevity aspirations (free text)"""
    parts = []
    if patient.get('diet_quality', '') == 'poor':
        parts.append("improve my diet")
    if float(patient.get('sleep_score', 7)) < 6.5:
        parts.append("sleep better")
    if patient.get('stress_level', '') == 'high':
        parts.append("manage my stress")
    if patient.get('health_profile', '') == 'poor' or patient.get('fitness_level', '') == 'low':
        parts.append("get in better shape")
    if not parts:
        parts.append("maintain my current good health")
    return "I want to " + " and ".join(parts) + " to support my longevity."


# ====================
# ANSWER LOGIC FOR NUTRITION AND DIET (SECTION 2)
# ====================



def answer_2_01(patient):
    """How would you characterize your typical daily diet?"""
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        return ["Very healthy"]
    if dq == 'poor':
        return ["Unhealthy"]
    return ["Moderately healthy"]

def answer_2_02(patient):
    base_options = [
        "Vegan (no animal products)",
        "Vegetarian (no meat, may include dairy/eggs)",
        "Pescatarian (includes fish, no other meat)",
        "No Restrictions"
    ]
    stackable = [
        "Gluten-free",
        "Dairy-free",
        "Kosher",
        "Halal",
        "Low-carb-Keto",
        "Paleo",
        "Intermittent Fasting"
    ]
    base_weights = [0.02, 0.06, 0.05, 0.43]  # Prevalence from above

    base = random.choices(base_options, weights=base_weights)[0]

    # If "No Restrictions" just return that
    if base == "No Restrictions":
        return [base]
    # Otherwise, add 0–2 stackable restrictions (weighted)
    k = random.choices([0,1,2], [0.65,0.25,0.10])[0]
    restrictions = random.sample(stackable, k=k)
    return [base] + restrictions

def answer_2_03(patient):
    """How many full meals do you typically eat per day?"""
    dq = patient.get('diet_quality', 'moderate')
    options = [
        "≤1",
        "2",
        "3",
        "4 or more"
    ]
    if dq == "good":
        weights = [0.01, 0.09, 0.55, 0.35]
    elif dq == "poor":
        weights = [0.25, 0.55, 0.15, 0.05]
    else:
        weights = [0.1, 0.3, 0.4, 0.2]
    return random.choices(options, weights=weights)[0]

def answer_2_04(patient, meals_resp):
    """Would you consider adjusting your meal structure in support of your longevity goals?"""
    if meals_resp not in ["≤1", "2"]:
        return ""
    return random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])

def answer_2_05(patient):
    """How many snacks do you typically eat per day?"""
    dq = patient.get('diet_quality', 'moderate')
    options = [
        "≤1",
        "2",
        "3",
        "4 or more"
    ]
    if dq == "good":
        weights = [0.01, 0.09, 0.55, 0.35]
    elif dq == "poor":
        weights = [0.25, 0.55, 0.15, 0.05]
    else:
        weights = [0.1, 0.3, 0.4, 0.2]
    return random.choices(options, weights=weights)[0]

def answer_2_06(patient, snacks_resp):
    """Would you consider adjusting your snacking habits in support of your longevity goals?"""
    if snacks_resp not in ["3", "4 or more"]:
        return ""
    return random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])

def answer_2_07(patient):
    """How often do you eat out or order takeout/delivery?"""
    dq = patient.get('diet_quality', 'moderate')
    options = [
        "Rarely",
        "Once a week",
        "Several times a week",
        "Daily"
    ]
    if dq == "good":
        weights = [0.65, 0.25, 0.08, 0.02]
    elif dq == "poor":
        weights = [0.1, 0.2, 0.4, 0.3]
    else:
        weights = [0.1, 0.4, 0.4, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_2_08(patient, eat_out_resp):
    """Would you consider preparing more meals at home in support of your longevity goals?"""
    if eat_out_resp not in ["Daily", "Several times a week"]:
        return ""
    return random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])

def answer_2_09(patient):
    """Do you track your daily protein intake?"""
    dq = patient.get('diet_quality', 'moderate')
    options = [
        "Yes",
        "No",
        "No, but I'm Generally Aware"
    ]
    if dq == 'good':
        weights = [0.4, 0, 0.6]
    elif dq == 'poor':
        weights = [0.1, 0.7, 0.2]
    else:
        weights = [0.2, 0.6, 0.2]
    return random.choices(options, weights=weights)[0]

def answer_2_10(patient, protein_track_resp):
    """Would you consider tracking protein more consistently in support of your longevity goals?"""
    if protein_track_resp == "Yes":
        return ""
    options = [
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    weights = [0.3, 0.3, 0.2, 0.1, 0.1]
    return random.choices(options, weights=weights)[0]

def calc_protein_target(weight_lb, age):
    weight_kg = weight_lb / 2.205
    if age < 65:
        target = 1.2 * weight_kg
    else:
        target = 1.5 * weight_kg
    return round(target, 1)

def answer_2_11(patient, protein_track_resp):
    """
    How many grams of protein do you typically consume per day?
    Only fill if protein_track_resp is "Yes" or "No, but I'm Generally Aware".
    Use diet_quality to bias under/over/at target.
    """
    if protein_track_resp == "No":
        return ""  # leave blank
    weight_lb = float(patient.get('weight', 170))
    age = int(patient.get('age', 45))
    protein_target = calc_protein_target(weight_lb, age)
    dq = patient.get('diet_quality', 'moderate')
    # Good: meet/exceed target, Moderate: ~80–100%, Poor: 50–80%
    if dq == "good":
        val = round(random.uniform(protein_target, protein_target * 1.2), 1)
    elif dq == "poor":
        val = round(random.uniform(protein_target * 0.5, protein_target * 0.8), 1)
    else:
        val = round(random.uniform(protein_target * 0.8, protein_target), 1)
    return val

def answer_2_12(patient, protein_amt_resp):
    """Would you consider adjusting your daily protein intake in support of your longevity goals?"""
    if protein_amt_resp not in ["<0.4g/lb", "0.4-0.6g/lb", "≥1.0g/lb"]:
        return ""
    options = [
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    weights = [0.3, 0.3, 0.2, 0.1, 0.1]
    return random.choices(options, weights=weights)[0]


def answer_2_13(patient, dietary_restrictions):
    """
    How often do you consume processed or red meat?
    - If vegan, vegetarian, or pescatarian: always 'Rarely or Never'
    - If only 'No Restrictions', or only stackable restrictions (e.g. intermittent fasting, paleo): use normal diet_quality logic
    """
    if isinstance(dietary_restrictions, str):
        dietary_restrictions = [s.strip() for s in dietary_restrictions.split("|")]
    restrictions = [r.lower() for r in dietary_restrictions]
    if any(
        kw in r for r in restrictions for kw in ["vegan", "vegetarian", "pescatarian"]
    ):
        return "Rarely or Never"
    dq = patient.get('diet_quality', 'moderate')
    options = [
        "Rarely or Never",
        "1-2 times per week",
        "3-4 times per week",
        "5 or more times per week"
    ]
    if dq == "good":
        weights = [0.9, 0.1, 0, 0]
    elif dq == "poor":
        weights = [0, 0, 0.7, 0.3]
    else:
        weights = [0.1, 0.7, 0.15, 0.05]
    return random.choices(options, weights=weights)[0]

def answer_2_14(patient, red_meat_resp):
    """Would you consider decreasing your processed and red meat consumption in support of your longevity goals?"""
    if red_meat_resp not in ["3-4 times per week", "5 or more times per week"]:
        return ""
    options = [
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    weights = [0.3, 0.3, 0.2, 0.1, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_2_15(patient, dietary_restrictions):
    """
    How often do you eat fatty fish (e.g., salmon, sardines, mackerel) rich in omega-3s?
    - Pescatarian: always "5 or more times per week"
    - Vegan or Vegetarian: always "Rarely or Never"
    - Else: standard logic
    """
    if isinstance(dietary_restrictions, str):
        dietary_restrictions = [s.strip() for s in dietary_restrictions.split("|")]
    restrictions = [r.lower() for r in dietary_restrictions]
    
    if any("pescatarian" in r for r in restrictions):
        return "5 or more times per week"
    if any(kw in r for r in restrictions for kw in ["vegan", "vegetarian"]):
        return "Rarely or Never"
    
    dq = patient.get('diet_quality', 'moderate')
    options = [
        "Rarely or Never",
        "Less than once a week",
        "1-2 times per week",
        "3-4 times per week",
        "5 or more times per week"
    ]
    if dq == 'good':
        weights = [0, 0, 0.15, 0.45, 0.4]
    elif dq == 'poor':
        weights = [0.8, 0.1, 0.1, 0, 0]
    else:
        weights = [0.15, 0.3, 0.4, 0.1, 0.05]
    return random.choices(options, weights=weights)[0]

def answer_2_16(patient, fish_resp):
    """Would you consider increasing your intake of omega-3 rich fish in support of your longevity goals?"""
    if fish_resp not in ["Rarely or Never", "Less than once a week"]:
        return ""
    options = [
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    weights = [0.3, 0.3, 0.2, 0.1, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_2_17(patient, dietary_restrictions):
    """
    How much of your protein comes from plant-based sources in a typical week?
    - Vegan or Vegetarian: always 'Almost entirely plant-based or Vegan'
    - Else: weighted random
    """
    # Handle pipe-separated string or list
    if isinstance(dietary_restrictions, str):
        dietary_restrictions = [s.strip() for s in dietary_restrictions.split("|")]
    restrictions = [r.lower() for r in dietary_restrictions]

    if any(kw in r for r in restrictions for kw in ["vegan", "vegetarian"]):
        return "Almost entirely plant-based or Vegan"

    options = [
        "Almost none - all animal-based",
        "A small portion - mostly animal-based",
        "Moderate - roughly balanced",
        "Large portion - mostly plant-based",
        "Almost entirely plant-based or Vegan"
    ]
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        weights = [0.05, 0.1, 0.2, 0.4, 0.25]
    elif dq == 'poor':
        weights = [0.5, 0.3, 0.15, 0.04, 0.01]
    else:
        weights = [0.1, 0.2, 0.4, 0.2, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_2_18(patient, plant_protein_resp):
    """Would you consider increasing the proportion of plant-based protein in support of your longevity goals?"""
    if plant_protein_resp not in ["Almost none - all animal-based", "A small portion - mostly animal-based"]:
        return ""
    options = [
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    weights = [0.3, 0.3, 0.2, 0.1, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_2_19(patient, dietary_restrictions):
    """
    How many servings of fruits and vegetables do you consume daily?
    - Vegan or Vegetarian: almost always '3-4' or '5 or more'
    - Else: weighted random
    """
    if isinstance(dietary_restrictions, str):
        dietary_restrictions = [s.strip() for s in dietary_restrictions.split("|")]
    restrictions = [r.lower() for r in dietary_restrictions]
    
    options = ["0", "1-2", "3-4", "5 or more"]

    if any(kw in r for r in restrictions for kw in ["vegan", "vegetarian"]):
        weights = [0, 0, 0.3, 0.7]
        return random.choices(options, weights=weights)[0]
    
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        weights = [0.01, 0.09, 0.4, 0.5]
    elif dq == 'poor':
        weights = [0.18, 0.52, 0.24, 0.06]
    else:
        weights = [0.05, 0.25, 0.4, 0.3]
    return random.choices(options, weights=weights)[0]

def answer_2_20(patient, fv_resp):
    """Would you consider increasing your fruit and vegetable consumption in support of your longevity goals?"""
    if fv_resp not in ["0", "1-2"]:
        return ""
    options = [
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    weights = [0.3, 0.3, 0.2, 0.1, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_2_21(patient):
    """How often do you consume whole grains (e.g., oats, barley, brown rice, whole wheat)?"""
    options = ["Rarely or never", "Once a week", "Several times a week", "Daily"]
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        weights = [0.02, 0.08, 0.35, 0.55]
    elif dq == 'poor':
        weights = [0.56, 0.22, 0.16, 0.06]
    else:
        weights = [0.2, 0.2, 0.45, 0.15]
    return random.choices(options, weights=weights)[0]

def answer_2_22(patient, whole_grain_resp):
    """Would you consider increasing your intake of whole grains in support of your longevity goals?"""
    if whole_grain_resp not in ["Rarely or never", "Once a week"]:
        return ""
    options = [
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    weights = [0.3, 0.3, 0.2, 0.1, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_2_23(patient):
    """How often do you consume legumes (e.g., lentils, chickpeas, black beans)?"""
    options = ["Rarely or never", "Once a week", "Several times a week", "Daily"]
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        weights = [0.04, 0.11, 0.3, 0.55]
    elif dq == 'poor':
        weights = [0.55, 0.25, 0.15, 0.05]
    else:
        weights = [0.2, 0.25, 0.45, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_2_24(patient, legume_resp):
    """Would you consider increasing your legume consumption in support of your longevity goals?"""
    if legume_resp not in ["Rarely or never", "Once a week"]:
        return ""
    options = [
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    weights = [0.3, 0.3, 0.2, 0.1, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_2_25(patient):
    """How often do you consume seeds such as flaxseed, chia, or hemp?"""
    options = ["Rarely or never", "Once a week", "Several times a week", "Daily"]
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        weights = [0.05, 0.15, 0.35, 0.45]
    elif dq == 'poor':
        weights = [0.5, 0.25, 0.2, 0.05]
    else:
        weights = [0.4, 0.2, 0.3, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_2_26(patient, seed_resp):
    """Would you consider increasing your intake of seeds (e.g., flax, chia) in support of your longevity goals?"""
    if seed_resp not in ["Rarely or never", "Once a week"]:
        return ""
    options = [
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    weights = [0.3, 0.3, 0.2, 0.1, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_2_27(patient):
    """How often do you consume healthy fats such as olive oil, avocados, nuts, fatty fish, etc.?"""
    options = ["Rarely or never", "Once a week", "Several times a week", "Daily"]
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        weights = [0.03, 0.12, 0.35, 0.5]
    elif dq == 'poor':
        weights = [0.55, 0.2, 0.2, 0.05]
    else:
        weights = [0.1, 0.2, 0.5, 0.2]
    return random.choices(options, weights=weights)[0]

def answer_2_28(patient, fats_resp):
    """Would you consider increasing your intake of healthy fats (olive oil, avocados, nuts, fatty fish, etc.) in support of your longevity goals?"""
    if fats_resp not in ["Rarely or never", "Once a week"]:
        return ""
    options = [
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    weights = [0.3, 0.3, 0.2, 0.1, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_2_29(patient):
    """How much water do you drink daily?"""
    options = [
        "Less than 1 liter (34 oz)",
        "1-2 liters (34-68 oz)",
        "More than 2 liters (68 oz)"
    ]
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        weights = [0.05, 0.3, 0.65]
    elif dq == 'poor':
        weights = [0.6, 0.35, 0.05]
    else:
        weights = [0.2, 0.6, 0.2]
    return random.choices(options, weights=weights)[0]

def answer_2_30(patient, water_resp):
    """Would you consider increasing your daily water intake in the future in support of your longevity goals?"""
    if water_resp not in [
        "Less than 1 liter (34 oz)",
        "1-2 liters (34-68 oz)"
    ]:
        return ""
    options = [
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    weights = [0.3, 0.3, 0.2, 0.1, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_2_31(patient):
    """How much caffeine do you typically consume per day?"""
    options = [
        "None",
        "<100 mg (e.g., 1 small coffee or tea)",
        "100–200 mg (1–2 cups of coffee)",
        "201–400 mg (3–4 cups or energy drink)",
        ">400 mg (5+ cups, strong pre-workouts, etc.)"
    ]
    stress = patient.get('stress_level', 'moderate')
    if stress == 'high':
        weights = [0.05, 0.15, 0.35, 0.3, 0.15]
    elif stress == 'low':
        weights = [0.15, 0.45, 0.3, 0.08, 0.02]
    else:
        weights = [0.05, 0.25, 0.4, 0.22, 0.08]
    return random.choices(options, weights=weights)[0]

def answer_2_32(patient, caff_resp):
    """Would you be open to adjusting your caffeine intake in the future in support of your longevity goals?"""
    if caff_resp not in [
        "201–400 mg (3–4 cups or energy drink)",
        ">400 mg (5+ cups, strong pre-workouts, etc.)"
    ]:
        return ""
    options = [
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    weights = [0.3, 0.3, 0.2, 0.1, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_2_33(patient):
    """What is your primary source of caffeine"""
    options = [
        "Coffee",
        "Tea",
        "Energy Drinks",
        "Soda",
        "Pre-Workout Supplements",
        "Chocolate",
        "Other"

    ]
    weights = [0.5, 0.1, 0.1, 0.15, 0.05, 0.05, 0.05]
    return random.choices(options, weights=weights)[0]

def answer_2_34(patient):
    """What time do you typically consume your last caffeinated beverage?"""
    options = [
        "Before 12:00 PM",
        "12:00–2:00 PM",
        "2:00–4:00 PM",
        "4:00–6:00 PM",
        "After 6:00 PM"
    ]
    sleep_score = patient.get('sleep_score', 7.0)
    try:
        sleep_score = float(sleep_score)
    except Exception:
        sleep_score = 7.0

    if sleep_score >= 8:
        weights = [0.4, 0.3, 0.2, 0.07, 0.03]
    elif sleep_score <= 5:
        weights = [0.05, 0.15, 0.25, 0.3, 0.25]
    else:
        weights = [0.1, 0.2, 0.3, 0.25, 0.15]

    return random.choices(options, weights=weights)[0]

def answer_2_35(patient, last_caff_time):
    """Would you consider having your last caffeinated drink earlier in support of your longevity goals?"""
    if last_caff_time not in ["4:00–6:00 PM", "After 6:00 PM"]:
        return ""
    options = [
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    weights = [0.3, 0.3, 0.2, 0.1, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_2_36(patient):
    """Have you ever worked with a nutritionist or dietitian?"""
    dq = patient.get('diet_quality', 'moderate')
    options = ["Yes", "No"]
    if dq == 'good':
        weights = [0.7, 0.3]
    elif dq == 'poor':
        weights = [0.25, 0.75]
    else:
        weights = [0.5, 0.5]
    return random.choices(options, weights=weights)[0]

def answer_2_37(patient, worked_with_nutritionist):
    """Would you consider working with a nutritionist or dietitian in the future in support of your longevity goals?"""
    if worked_with_nutritionist != "No":
        return ""
    options = [
        "Yes - actively seeking one now",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    weights = [0.1, 0.4, 0.2, 0.2, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_2_38(patient):
    """Do you have any food allergies or intolerances?"""
    options = ["Yes", "No"]
    weights = [0.35, 0.65]
    return random.choices(options, weights=weights)[0]  # returns "Yes" or "No" as string

def answer_2_39(patient, has_allergy):
    """Which of the following are you allergic or intolerant to? (select all that apply)"""
    if has_allergy != "Yes":
        return []  
    options = [
        "Gluten",
        "Dairy",
        "Peanuts",
        "Tree nuts",
        "Shellfish",
        "Other (please specify)"
    ]
    k = random.randint(1, 3)
    return random.sample(options, k)  

def answer_2_40(patient):
    """Please describe your typical breakfast, lunch, and dinner, as well as the types of snacks consumed regularly"""
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        return ["Breakfast: oatmeal and fruit. Lunch: salad with lean protein. Dinner: vegetables and whole grains. Snacks: nuts, fruit."]
    elif dq == 'poor':
        return ["Breakfast: pastries or skip. Lunch: fast food or processed meal. Dinner: takeout or frozen. Snacks: chips, sweets."]
    else:
        return ["Breakfast: eggs or cereal. Lunch: sandwich or bowl. Dinner: mixed plate. Snacks: crackers, granola bars."]

def answer_2_41(patient):
    """Do you experience any digestive issues?"""
    return [random.choices(["Yes", "No"], weights=[0.3, 0.7])[0]]

def answer_2_42(patient, has_digestive_issues):
    """Which of the following digestive issues do you experience? (select all that apply)"""
    if has_digestive_issues != "Yes":
        return []
    options = [
        "Bloating",
        "Constipation",
        "Diarrhea",
        "Acid reflux",
        "Other (please specify)"
    ]
    return random.sample(options, k=random.randint(1, 3))

def answer_2_43(patient):
    """What are your primary goals regarding diet and nutrition? (multi-select)"""
    options = [
        "Improve overall health",
        "Increase energy levels",
        "Enhance mental clarity",
        "Improve digestion",
        "Improve physical appearance (e.g., skin health)",
        "Longevity and healthy aging",
        "Reduce inflammation",
        "Manage a chronic condition (e.g., diabetes, hypertension)",
        "Weight loss",
        "Weight gain",
        "Other (please specify)"
    ]
    # Select 2 to 4 goals randomly
    return random.sample(options, k=random.randint(2, 4))  

def answer_2_44(patient, goals):
    """Please rank your diet and nutrition goals in order of importance."""
    if not goals or len(goals) < 2:
        return []
    return random.sample(goals, k=len(goals))  

def answer_2_45(patient):
    """Have you ever followed a specific diet plan for health or weight management purposes?"""
    dq = patient.get("diet_quality", "moderate")
    options = ["Yes", "No"]
    if dq == "good":
        weights = [0.8, 0.2]
    elif dq == "poor":
        weights = [0.3, 0.7]
    else:
        weights = [0.6, 0.4]
    return random.choices(options, weights=weights)[0]

def answer_2_46(patient, followed_diet):
    """Which diet(s) have you followed in the past? (multi-select)"""
    if followed_diet != "Yes":
        return []
    options = [
        "Whole Food Plant-Based Diet", "Mediterranean Diet", "High-Protein Diet",
        "Low-Carb Diet (e.g., keto, Atkins)", "Vegetarian Diet", "Vegan Diet",
        "Intermittent Fasting", "Low-Fat Diet", "Paleo Diet", "Whole30",
        "DASH Diet", "Other (please specify)"
    ]
    return random.sample(options, k=random.randint(1, 4))

def answer_2_47(patient, followed_diet):
    """What were your primary goals when starting your dietary plan? (multi-select)"""
    if followed_diet != "Yes":
        return []
    goals = [
        "Improve overall health", "Increase energy levels", "Enhance mental clarity",
        "Improve digestion", "Improve physical appearance (e.g., skin health)",
        "Longevity and healthy aging", "Reduce inflammation",
        "Manage a chronic condition (e.g., diabetes, hypertension)",
        "Weight loss", "Weight gain", "Other (please specify)"
    ]
    return random.sample(goals, k=random.randint(1, 4))

def answer_2_48(patient, followed_diet):
    """How long have you typically adhered to a dietary plan?"""
    if followed_diet != "Yes":
        return ""
    dq = patient.get("diet_quality", "moderate") 
    options = [
        "Less than 1 month", "1-3 months", "4-6 months",
        "7-12 months", "More than 1 year"
    ]
    if dq == "good": 
        weights = [0.05, 0.15, 0.25, 0.35, 0.2]
    elif dq == "poor":
        weights = [0.35, 0.25, 0.2, 0.15, 0.05]
    else:
        weights = [0.15, 0.45, 0.2, 0.1, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_2_49(patient, followed_diet):
    """How successful were you in achieving your goals with these diets?"""
    if followed_diet != "Yes":
        return ""
    dq = patient.get("diet_quality", "moderate")
    options = ["Very successful", "Somewhat successful", "Not successful"]
    if dq == "good":
        weights = [0.6, 0.3, 0.1]
    elif dq == "poor":
        weights = [0.1, 0.3, 0.6]
    else:
        weights = [0.3, 0.5, 0.2]
    return random.choices(options, weights=weights)[0]


def answer_2_50(patient, followed_diet):
    """What are the primary reasons you have never followed a specific diet plan? (multi-select)"""
    if followed_diet != "No":
        return []
    options = [
        "Satisfied with current eating habits", "Lack of interest",
        "Uncertainty about which diet to follow",
        "Concern about potential health effects",
        "Perceived difficulty or inconvenience",
        "Other (please specify)"
    ]
    return random.sample(options, k=random.randint(1, 3))

def answer_2_51(patient, followed_diet):
    """Have you considered following a specific dietary plan for health or weight management purposes?"""
    if followed_diet != "No":
        return ""
    dq = patient.get("diet_quality", "moderate")
    options = ["Yes", "No"]
    if dq == "good":
        weights = [0.6, 0.4]  
    elif dq == "poor":
        weights = [0.4, 0.6]  
    else:
        weights = [0.5, 0.5]  
    return random.choices(options, weights=weights)[0]

def answer_2_52(patient, followed_diet, considered_plan):
    """Would you be willing to try a dietary plan in the future in support of your longevity goals?"""
    if followed_diet != "No" or considered_plan != "Yes":
        return ""
    motivation = patient.get("diet_motivation", "moderate")
    options = [
        "Yes - open to trying", "Maybe - need more information",
        "Not now, but maybe in the future", "No"
    ]
    if motivation == "high":
        weights = [0.5, 0.3, 0.1, 0.1]
    elif motivation == "low":
        weights = [0.1, 0.2, 0.3, 0.4]
    else:
        weights = [0.25, 0.35, 0.25, 0.15]
    return random.choices(options, weights=weights)[0]

def answer_2_53(patient, followed_diet, considered_plan):
    """What factors have prevented you from starting or continuing a dietary plan in the past? (multi-select)"""
    if followed_diet != "No" or considered_plan != "Yes":
        return []
    options = [
        "Lack of time to prepare meals",
        "Conflicting information about nutrition",
        "Social or family commitments",
        "Uncertainty about effectiveness",
        "Other (please specify)"
    ]
    return random.sample(options, k=random.randint(1, 3))

def answer_2_54(patient, followed_diet, considered_plan):
    """Which of the following dietary guidelines or principles would you be interested in exploring? (multi-select)"""
    if followed_diet != "No" or considered_plan != "Yes":
        return []
    options = [
        "Whole Food Plant-Based Diet", "Mediterranean Diet", "High-Protein Diet",
        "Low-Carb Diet (e.g., keto, Atkins)", "Vegetarian Diet", "Vegan Diet",
        "Intermittent Fasting", "Other (please specify)"
    ]
    return random.sample(options, k=random.randint(1, 4))

def answer_2_55(patient):
    """What diet changes, if any, have you made to improve your health? (multi-select)"""
    dq = patient.get("diet_quality", "moderate")
    options = [
        "Increased fruit and vegetable consumption", "Reduced sugar intake",
        "Limited processed foods", "Increased water intake",
        "Reduced processed and red meat intake", "Reduced portion sizes",
        "Other (please specify)", "None"
    ]
    if dq == "good":
        sample_pool = options[:-1]  # skip "None"
        return random.sample(sample_pool, k=random.randint(2, 4))
    elif dq == "poor":
        return ["None"]
    return random.sample(options, k=random.randint(1, 3))

def answer_2_56(patient, changes_made):
    """Would you consider making any of the following dietary changes in the future? (multi-select)"""
    all_options = [
        "Increased fruit and vegetable consumption", "Reduced sugar intake",
        "Limited processed foods", "Increased water intake",
        "Reduced processed and red meat intake", "Reduced portion sizes",
        "Other (please specify)", "None"
    ]
    available = [opt for opt in all_options if opt not in changes_made and opt != "None"]
    if not available:
        return ["None"]
    return random.sample(available, k=min(len(available), random.randint(1, 3)))

def answer_2_57(patient):
    """Which of the following reasons, if any, do you feel have limited your ability to make sustainable dietary changes? (multi-select)"""
    stress = patient.get("stress_level", "moderate")
    options = [
        "Lack of time to prepare meals",
        "Difficulty in following the plan consistently",
        "Social events or peer pressure",
        "Lack of variety and enjoyment in meals",
        "Insufficient results or slow progress",
        "Cravings for restricted foods",
        "Stress or emotional eating",
        "Lack of support or guidance",
        "Health issue or adverse effects",
        "Other (please specify)"
    ]
    weighted_options = options[:]
    if stress == "high":
        weighted_options.append("Stress or emotional eating")
    return random.sample(weighted_options, k=random.randint(2, 4))

def answer_2_58(patient):
    """What kind of support, if any, do you think would be helpful in making sustainable dietary changes? (multi-select)"""
    dq = patient.get("diet_quality", "moderate")
    support_options = [
        "Assistance with meal preparation",
        "Regular check-ins with a nutritionist or dietitian",
        "Access to easy and quick recipes",
        "Meal planning and preparation tips",
        "Mobile app or online tracking tool",
        "Accountability partner",
        "Other (please specify)", "None"
    ]
    if dq == "poor":
        return random.sample(support_options[:-1], k=random.randint(2, 4))
    if dq == "good":
        return random.sample(support_options[:-1], k=1)
    return random.sample(support_options[:-1], k=random.randint(1, 3))

def answer_2_59(patient):
    """Do you track your daily caloric intake?"""
    dq = patient.get("diet_quality", "moderate")
    options = [
        "Yes",
        "No, but I'm generally aware of how many calories I consume each day",
        "No"
    ]
    if dq == "good":
        weights = [0.6, 0.3, 0.1]
    elif dq == "poor":
        weights = [0.1, 0.3, 0.6]
    else:
        weights = [0.3, 0.4, 0.3]
    return random.choices(options, weights=weights)[0]

def answer_2_60(patient, track_response):
    """If no, what are the primary reasons you do not track your caloric intake? (multi-select)"""
    if track_response == "Yes":
        return []
    reasons = [
        "Too time consuming",
        "Feels restrictive or obsessive",
        "Lack of knowledge regarding how to track calories",
        "Difficult to estimate portion sizes correctly",
        "Does not fit into my lifestyle",
        "Prefer to eat intuitively",
        "Have had negative experiences with calorie tracking",
        "Believe it is unnecessary for my goals",
        "Concern about developing an unhealthy relationship with food",
        "Other (please specify)"
    ]
    return random.sample(reasons, k=random.randint(1, 3))

def answer_2_61(patient, track_response):
    """Would you consider tracking your caloric intake in the future?"""
    if track_response == "Yes":
        return ""
    options = [
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    return random.choice(options)

def calc_calorie_target(weight_lb, age, sex, activity_level="moderate"):
    weight_kg = weight_lb / 2.205
    if sex and isinstance(sex, str) and sex.lower().startswith("m"):
        bmr = 10 * weight_kg + 6.25 * 170 - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * 160 - 5 * age - 161
    multiplier = 1.55 if activity_level == "moderate" else 1.3
    return int(bmr * multiplier)

def answer_2_62(patient, calorie_track_resp):
    """
    How many calories do you typically consume per day?
    Only fill if calorie_track_resp is "Yes" or "No, but I'm Generally Aware..."
    Use diet_quality to bias under/over/at target.
    """
    if calorie_track_resp == "No":
        return ""  # leave blank
    weight_lb = float(patient.get('weight', 170))
    age = int(patient.get('age', 45))
    sex = patient.get('sex', 'female')
    calorie_target = calc_calorie_target(weight_lb, age, sex)
    dq = patient.get('diet_quality', 'moderate')
    # Good: within or slightly under target, Poor: over/under target, Moderate: ±10–15%
    if dq == "good":
        val = int(random.uniform(calorie_target * 0.9, calorie_target))
    elif dq == "poor":
        # Could be over OR under, but more variance
        val = int(random.uniform(calorie_target * 0.7, calorie_target * 1.2))
    else:
        val = int(random.uniform(calorie_target * 0.85, calorie_target * 1.05))
    return val

def answer_2_63(patient, track_response):
    """Which of the following tools do you use to track your caloric intake? (multi-select)"""
    if track_response != "Yes":
        return []
    options = [
        "Food scale",
        "Mobile app (e.g. MyFitnessPal, Cronometer)",
        "Written food diary or journal",
        "Online calorie tracking tools",
        "Pre-packaged meal plans with calorie counts"
    ]
    return random.sample(options, k=random.randint(1, 3))

def answer_2_64(patient, track_response):
    """Which, if any, of the following methods would you consider as an alternative to calorie tracking? (multi-select)"""
    if track_response == "Yes":
        return []
    options = [
        "Caloric restriction (e.g. portion control)",
        "Dietary restriction (e.g. avoiding sugar, gluten, etc.)",
        "Time restriction (e.g. intermittent fasting)",
        "Eating more whole foods and less processed foods",
        "Listening to hunger and fullness cues",
        "Focusing on macronutrient balance",
        "Regular consultations with a nutritionist or dietitian",
        "Other (please specify)",
        "None"
    ]
    return random.sample(options, k=random.randint(1, 3))

# ====================
# ANSWER LOGIC FOR EXERCISE AND NUTRITION (SECTION 3)
# ====================

def answer_3_01(patient):
    """How often do you engage in physical exercise?"""
    fitness = patient.get("fitness_level", "moderate")
    options = [
        "Rarely or Never",
        "Occasionally (1–2 times per week)",
        "Regularly (3–4 times per week)",
        "Frequently (5 or more times per week)"
    ]
    if fitness == "high":
        weights = [0.01, 0.09, 0.35, 0.55]
    elif fitness == "low":
        weights = [0.55, 0.35, 0.09, 0.01]
    else:  # moderate
        weights = [0.15, 0.35, 0.35, 0.15]
    return random.choices(options, weights=weights)[0]

def answer_3_02(patient, ex_freq_resp):
    """Would you consider exercising more frequently in support of your longevity goals?"""
    if ex_freq_resp in [
        "Frequently (5 or more times per week)",
        "Regularly (3–4 times per week)"
    ]:
        return ""
    options = [
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    return random.choice(options)

def answer_3_03(patient):
    """What types of exercise do you typically engage in? (multi-select)"""
    fitness = patient.get("fitness_level", "moderate")
    options = [
        "Cardio (e.g. running and cycling)",
        "Strength training (e.g. weight lifting)",
        "Flexibility/mobility (e.g. yoga, stretching)",
        "High-intensity interval training (HIIT)",
        "None"
    ]
    if fitness == "high":
        return random.sample(options[:-1], k=random.randint(3, 4))
    if fitness == "low":
        return ["None"] if random.random() < 0.5 else random.sample(options[:-1], k=1)
    # moderate
    return random.sample(options[:-1], k=random.randint(1, 3))

def exercise_type_frequency(patient, exercise_types, type_name, weights_map):
    """Generic frequency picker for any exercise type."""
    if type_name not in exercise_types:
        return ""
    fitness = patient.get("fitness_level", "moderate")
    options = [
        "Rarely (a few times a month)",
        "Occasionally (1–2 times per week)",
        "Regularly (3–4 times per week)",
        "Frequently (5 or more times per week)"
    ]
    weights = weights_map.get(fitness, [0.2, 0.3, 0.3, 0.2])
    return random.choices(options, weights=weights)[0]

def exercise_type_duration(patient, exercise_types, type_name, weights_map):
    """Generic duration picker for any exercise type."""
    if type_name not in exercise_types:
        return ""
    fitness = patient.get("fitness_level", "moderate")
    options = [
        "Less than 30 minutes",
        "30–45 minutes",
        "45–60 minutes",
        "More than 60 minutes"
    ]
    weights = weights_map.get(fitness, [0.2, 0.4, 0.3, 0.1])
    return random.choices(options, weights=weights)[0]

# Frequency Weights
cardio_freq_weights = {
    "high":     [0.05, 0.15, 0.3, 0.5],
    "moderate": [0.2, 0.3, 0.3, 0.2],
    "low":      [0.5, 0.3, 0.15, 0.05]
}

strength_freq_weights = {
    "high": [0.1, 0.2, 0.3, 0.4],
    "moderate": [0.3, 0.3, 0.3, 0.1],
    "low": [0.6, 0.2, 0.15, 0.05]
}

flex_freq_weights = {
    "high": [0.15, 0.2, 0.3, 0.35],
    "moderate": [0.4, 0.3, 0.2, 0.1],
    "low": [0.65, 0.2, 0.1, 0.05]
}

hiit_freq_weights = {
    "high": [0.1, 0.2, 0.3, 0.4],
    "moderate": [0.45, 0.3, 0.2, 0.05],
    "low": [0.75, 0.15, 0.08, 0.02]
}

# Duration Weights
cardio_dur_weights = {
    "high": [0.05, 0.3, 0.4, 0.25],
    "moderate": [0.2, 0.5, 0.25, 0.05],
    "low": [0.5, 0.4, 0.09, 0.01]
}
strength_dur_weights = {
    "high": [0.1, 0.25, 0.35, 0.3],
    "moderate": [0.2, 0.5, 0.25, 0.05],
    "low": [0.6, 0.3, 0.08, 0.02]
}
flex_dur_weights = {
    "high": [0.1, 0.3, 0.4, 0.2],
    "moderate": [0.3, 0.5, 0.15, 0.05],
    "low": [0.7, 0.2, 0.08, 0.02]
}
hiit_dur_weights = {
    "high": [0.2, 0.5, 0.25, 0.05],
    "moderate": [0.3, 0.5, 0.15, 0.05],
    "low": [0.8, 0.15, 0.04, 0.01]
}

def answer_3_12(patient, exercise_types):
    """What are the primary reasons that strength training is not a part of your routine? (multi-select)"""
    if "Strength training (e.g. weight lifting)" in exercise_types:
        return ""
    options = [
        "Lack of knowledge about strength training",
        "Lack of access to equipment",
        "Preference for other types of exercise",
        "Concern about injury",
        "Perception that it is not necessary for my goals",
        "Disinterest in strength training",
        "Intimidation or discomfort in the gym environment",
        "Physical limitations or medical conditions",
        "Other (please specify)"
    ]
    return "|".join(random.sample(options, k=random.randint(1, 3)))

def answer_3_13(patient, exercise_types):
    """Would you consider adding strength training in support of your longevity goals?"""
    if "Strength training (e.g. weight lifting)" in exercise_types:
        return ""
    options = [
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    return random.choice(options)

def answer_3_14(patient, exercise_types):
    """What resources would help you start or optimize a strength training routine? (multi-select)"""
    if "Strength training (e.g. weight lifting)" in exercise_types:
        return ""
    options = [
        "Professional guidance (e.g., personal trainer)",
        "Online tutorials or videos",
        "Detailed workout plans",
        "Gym membership with strength training facilities",
        "Support from friends or workout partners",
        "Home workout equipment",
        "Educational articles or books",
        "Group fitness classes",
        "None",
        "Other (please specify)"
    ]
    picks = random.sample(options[:-2], k=random.randint(1, 4))
    if random.random() < 0.1:
        picks.append("Other (please specify)")
    if not picks or random.random() < 0.1:
        picks = ["None"]
    return "|".join(picks)

def answer_3_15(patient, exercise_types):
    """What are the primary reasons that cardio is not a part of your routine? (multi-select)"""
    if "Cardio (e.g. running and cycling)" in exercise_types:
        return ""
    options = [
        "Lack of interest in cardio exercises",
        "Preference for other types of exercise",
        "Concern about injury",
        "Lack of time",
        "Perception that it is not necessary for my goals",
        "Discomfort with cardio activities",
        "Boredom with cardio activities",
        "Lack of access to facilities or equipment",
        "Physical limitations or medical conditions",
        "Other (please specify)"
    ]
    return "|".join(random.sample(options, k=random.randint(1, 3)))

def answer_3_16(patient, exercise_types):
    """Would you consider adding cardio training in support of your longevity goals?"""
    if "Cardio (e.g. running and cycling)" in exercise_types:
        return ""
    options = [
        "Yes",
        "Maybe",
        "No"
    ]
    return random.choice(options)

def answer_3_17(patient, exercise_types):
    """What resources would help you start or optimize a cardio training routine? (multi-select)"""
    if "Cardio (e.g. running and cycling)" in exercise_types:
        return ""
    options = [
        "Professional guidance (e.g., a personal trainer)",
        "Online tutorials or videos",
        "Detailed workout plans",
        "Access to cardio equipment (e.g., a treadmill, stationary bike, etc.)",
        "Support from friends or workout partners",
        "Educational articles or books",
        "Group fitness classes",
        "None",
        "Other (please specify)"
    ]
    picks = random.sample(options[:-2], k=random.randint(1, 4))
    if random.random() < 0.1:
        picks.append("Other (please specify)")
    if not picks or random.random() < 0.1:
        picks = ["None"]
    return "|".join(picks)

def answer_3_18(patient, exercise_types):
    """What are the primary reasons that high-intensity interval training (HIIT) is not a part of your routine? (multi-select)"""
    if "High-intensity interval training (HIIT)" in exercise_types:
        return ""
    options = [
        "Lack of knowledge about HIIT",
        "Preference for other types of exercise",
        "Concern about injury or physical strain",
        "Perception that HIIT is too intense or difficult",
        "Lack of time",
        "Disinterest in HIIT",
        "Lack of access to facilities or equipment",
        "Physical limitations or medical conditions",
        "Other (please specify)"
    ]
    return "|".join(random.sample(options, k=random.randint(1, 3)))

def answer_3_19(patient, exercise_types):
    """Would you consider adding HIIT training in support of your longevity goals?"""
    if "High-intensity interval training (HIIT)" in exercise_types:
        return ""
    options = [
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    return random.choice(options)

def answer_3_20(patient, exercise_types):
    """What resources would help you start or optimize a HIIT training routine? (multi-select)"""
    if "High-intensity interval training (HIIT)" in exercise_types:
        return ""
    options = [
        "Professional guidance (e.g., personal trainer)",
        "Online tutorials or videos",
        "Detailed workout plans",
        "Support from friends or workout partners",
        "Educational articles or books",
        "Group fitness classes",
        "Mobile apps or online programs",
        "None",
        "Other (please specify)"
    ]
    picks = random.sample(options[:-2], k=random.randint(1, 4))
    if random.random() < 0.1:
        picks.append("Other (please specify)")
    if not picks or random.random() < 0.1:
        picks = ["None"]
    return "|".join(picks)

def answer_3_21(patient):
    """How many steps do you typically take per day?"""
    fitness = patient.get("fitness_level", "moderate")
    options = [
        "Less than 2,500",
        "2,500–5,000",
        "5,000–7,500",
        "7,500–10,000",
        "10,000–15,000",
        "More than 15,000",
        "I'm not sure"
    ]
    if fitness == "high":
        weights = [0.01, 0.04, 0.1, 0.25, 0.4, 0.15, 0.05]
    elif fitness == "low":
        weights = [0.35, 0.3, 0.2, 0.1, 0.03, 0.01, 0.01]
    else:  # moderate
        weights = [0.07, 0.15, 0.25, 0.32, 0.15, 0.03, 0.03]
    return random.choices(options, weights=weights)[0]

def answer_3_22(patient, steps_resp):
    """Would you consider increasing your daily step count in support of your longevity goals?"""
    if steps_resp in ["7,500-10,000", "10,000–15,000", "More than 15,000"]:
        return ""
    options = [
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    return random.choice(options)

def answer_3_23(patient):
    """Do you use a wearable device to track steps and/or daily activity?"""
    # 70% chance "Yes", 30% "No"
    return random.choices(["Yes", "No"], weights=[0.7, 0.3])[0]

def answer_3_24(patient, wearable_resp):
    """Which of the following devices are you currently using to track steps and/or daily activity? (multi-select)"""
    if wearable_resp != "Yes":
        return []
    options = [
        "Apple Watch",  # Most prominent
        "Fitbit",
        "Garmin",
        "Samsung Galaxy",
        "Whoop",
        "Oura Ring",
        "Other (please specify)"
    ]
    # 60% Apple Watch + another, 30% Apple Watch only, 10% something else
    rand_val = random.random()
    if rand_val < 0.9:
        second = random.choice([d for d in options[1:]])  # Not Apple Watch
        return ["Apple Watch", second]
    elif rand_val < 0.6:
        return ["Apple Watch",]
    else:
        return [random.choice(options[1:])]

def answer_3_25(patient, wearable_resp):
    """Would you consider using a wearable device to track your daily step count?"""
    if wearable_resp == "Yes":
        return ""
    options = [
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    return random.choice(options)

def answer_3_26(patient):
    """Do you have any physical restrictions or limitations that affect your physical activity choices?"""
    fitness = patient.get("fitness_level", "moderate")
    if fitness == "high":
        weights = [0.1, 0.9]  
    elif fitness == "low":
        weights = [0.5, 0.5]
    else:  
        weights = [0.25, 0.75]
    return random.choices(["Yes", "No"], weights=weights)[0]

def answer_3_27(patient, phys_lim_resp):
    """Please share a brief description of any current or chronic physical restrictions."""
    if phys_lim_resp != "Yes":
        return ""
    sample_restrictions = [
        "Knee pain limits running or jumping activities.",
        "Chronic back issues; avoid heavy lifting.",
        "Arthritis in hands and wrists; limit grip exercises.",
        "Asthma restricts intense cardio.",
        "Hip replacement; restricted range of motion.",
        "Recovering from recent surgery; doctor recommends low-impact only."
    ]
    return random.choice(sample_restrictions)


# ====================
# ANSWER LOGIC FOR RESTORATIVE SLEEP (SECTION 4)
# ====================

def answer_4_01(patient):
    """How would you rate the quality of your sleep?"""
    score = float(patient.get("sleep_score", 7.0))
    if score >= 8.5:
        return "Excellent"
    elif score >= 7.0:
        return "Very Good"
    elif score >= 6.0:
        return "Good"
    elif score >= 5.0:
        return "Fair"
    else:
        return "Poor"

def answer_4_02(patient):
    """How many hours of sleep do you typically get per night?"""
    score = float(patient.get("sleep_score", 7.0))
    if score >= 9.0:
        return "More than 9 hours"
    elif score >= 8.0:
        return "9 hours"
    elif score >= 7.0:
        return "8 hours"
    elif score >= 6.0:
        return "7 hours"
    elif score >= 5.0:
        return "6 hours"
    elif score >= 4.5:
        return "5 hours"
    else:
        return "4 hours or less"

def answer_4_03(patient):
    """How often do you feel rested and refreshed upon waking up?"""
    score = float(patient.get("sleep_score", 7.0))
    if score >= 8.5:
        return "Always"
    elif score >= 7.0:
        return "Often"
    elif score >= 6.0:
        return "Sometimes"
    elif score >= 5.0:
        return "Rarely"
    else:
        return "Never"

def answer_4_04(patient):
    """How consistent is your sleep schedule?"""
    score = float(patient.get("sleep_score", 7.0))
    if score >= 8.5:
        return "Very consistent"
    elif score >= 7.0:
        return "Consistent on weekdays only"
    elif score >= 6.0:
        return "Somewhat inconsistent"
    elif score >= 5.0:
        return "Very inconsistent"
    else:
        return "Very inconsistent"

def answer_4_05(patient):
    """Do you have a regular bedtime routine?"""
    score = float(patient.get("sleep_score", 7.0))
    if score >= 8.0:
        return "Yes"
    elif score >= 6.0:
        return "Sometimes (e.g., weekdays only)"
    else:
        return "No"

def answer_4_06(patient):
    """How is your daily functioning typically affected by a poor night's sleep? (multi-select)"""
    options = [
        "Reduced energy levels",
        "Difficulty concentrating",
        "Mood swings or irritability",
        "Reduced physical performance",
        "Increased stress or anxiety",
        "Other (please specify)"
    ]
    return random.sample(options, k=random.randint(1, 4))

def answer_4_07(patient):
    """Which, if any, of the following sleep hygiene protocols do you follow? (multi-select, higher score = more protocols)"""
    options = [
        "Having a consistent sleep and wake schedule throughout the week",
        "Getting sunlight exposure by going outside within 30–60 minutes of waking/sunrise",
        "Avoiding caffeine within 8–10 hours of bedtime",
        "Keeping your bedroom cool, dark, and quiet",
        "Following a regular, relaxing bedtime routine",
        "Avoiding bright screens and overhead lights before bed",
        "Limiting alcohol consumption",
        "Avoiding fluids close to bedtime",
        "Avoiding eating within 2–3 hours of bedtime",
        "Avoiding long naps during the day",
        "Other (please specify)"
    ]
    score = float(patient.get("sleep_score", 7.0))
    # Higher sleep score → more protocols followed
    if score >= 8.5:
        k = random.randint(4, 6)
    elif score >= 7.5:
        k = random.randint(3, 5)
    elif score >= 6.5:
        k = random.randint(2, 4)
    else:
        k = random.randint(1, 2)
    return random.sample(options, k=k)

def answer_4_08(patient):
    """Would you be willing to try new strategies or interventions to improve your sleep?"""
    options = [
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    # Lean toward "Yes" for lower sleep scores, otherwise random.
    score = float(patient.get("sleep_score", 7.0))
    if score < 6:
        weights = [0.6, 0.2, 0.15, 0.05]
    elif score > 8.5:
        weights = [0.15, 0.3, 0.3, 0.25]
    else:
        weights = [0.4, 0.3, 0.2, 0.1]
    return random.choices(options, weights=weights)[0]


def answer_4_09(patient, already_followed, willing_to_try):
    """Which sleep hygiene protocols would you be willing to incorporate in the future? (multi-select, only if 4.08 is Yes/Maybe, only those not already followed)"""
    if willing_to_try not in [
        "Yes - open to trying", "Maybe - need more information"
    ]:
        return []
    options = [
        "Having a consistent sleep and wake schedule throughout the week",
        "Getting sunlight exposure by going outside within 30–60 minutes of waking/sunrise",
        "Avoiding caffeine within 8–10 hours of bedtime",
        "Keeping your bedroom cool, dark, and quiet",
        "Following a regular, relaxing bedtime routine",
        "Avoiding bright screens and overhead lights before bed",
        "Limiting alcohol consumption",
        "Avoiding fluids close to bedtime",
        "Avoiding eating within 2–3 hours of bedtime",
        "Avoiding long naps during the day",
        "Other (please specify)"
    ]
    available = [opt for opt in options if opt not in already_followed]
    score = float(patient.get("sleep_score", 7.0))
    if not available:
        return []
    if score < 6.0:
        k = min(len(available), random.randint(3, 5))
    elif score < 7.0:
        k = min(len(available), random.randint(2, 4))
    else:
        k = min(len(available), random.randint(1, 2))
    return random.sample(available, k=k)

def answer_4_10(patient):
    """How would you rate the comfort of your sleep environment?"""
    score = float(patient.get("sleep_score", 7.0))
    options = [
        "Very uncomfortable",
        "Somewhat uncomfortable",
        "Neutral",
        "Somewhat comfortable",
        "Very comfortable"
    ]
    if score >= 8.5:
        weights = [0.01, 0.04, 0.10, 0.35, 0.50]
    elif score >= 7.0:
        weights = [0.03, 0.10, 0.22, 0.40, 0.25]
    elif score >= 6.0:
        weights = [0.10, 0.20, 0.30, 0.25, 0.15]
    else:
        weights = [0.25, 0.25, 0.30, 0.15, 0.05]
    return random.choices(options, weights=weights)[0]

def answer_4_11(patient, env_comfort_resp):
    """Which, if any, of the following factors negatively affect your sleep environment? (multi-select)"""
    options = [
        "Noise",
        "Light",
        "Temperature",
        "Mattress comfort",
        "Pillow comfort",
        "Bed partner (e.g., snoring)",
        "Pets",
        "Other (please specify)"
    ]
    score = float(patient.get("sleep_score", 7.0))

    if env_comfort_resp == "Very comfortable" and score >= 8.5:
        return random.sample(options, k=1)
    if score >= 7.0:
        return random.sample(options, k=random.randint(1, 2))
    elif score >= 6.0:
        return random.sample(options, k=random.randint(2, 3))
    else:
        return random.sample(options, k=random.randint(3, 5))

def answer_4_12(patient):
    """Multi-select: Do you experience any of the following sleep issues?"""
    sleep_score = float(patient.get("sleep_score", 7.0))
    options = [
        "Difficulty falling asleep", "Difficulty staying asleep", "Waking up too early",
        "Frequent nightmares", "Restless legs", "Snoring", "Sleep apnea", "Other (please specify)"
    ]
    # Lower sleep_score → more issues
    if sleep_score >= 8.5:
        return []
    if sleep_score >= 7.0:
        return random.sample(options[:-1], k=random.choices([0, 1], [0.6, 0.4])[0])
    if sleep_score >= 6.0:
        return random.sample(options[:-1], k=random.randint(1, 2))
    if sleep_score >= 5.0:
        return random.sample(options[:-1], k=random.randint(1, 3))
    return random.sample(options, k=random.randint(2, 4))

def sleep_issue_frequency(patient, has_issue):
    """Return frequency for a selected sleep issue."""
    sleep_score = float(patient.get("sleep_score", 7.0))
    options = ["Rarely", "Occasionally", "Frequently", "Always"]
    # Lower score → more frequent
    if not has_issue:
        return ""
    if sleep_score >= 8.5:
        weights = [0.9, 0.09, 0.009, 0.001]
    elif sleep_score >= 7.0:
        weights = [0.7, 0.2, 0.09, 0.01]
    elif sleep_score >= 6.0:
        weights = [0.5, 0.3, 0.15, 0.05]
    elif sleep_score >= 5.0:
        weights = [0.3, 0.4, 0.2, 0.1]
    else:
        weights = [0.05, 0.2, 0.4, 0.35]
    return random.choices(options, weights=weights)[0]

def answer_4_21(patient):
    """Have you ever used a sleep tracking device or app to monitor your sleep?"""
    # 65% chance Yes if sleep_score < 8, else 40%
    sleep_score = float(patient.get("sleep_score", 7.0))
    p_yes = 0.65 if sleep_score < 8 else 0.4
    return "Yes" if random.random() < p_yes else "No"

def answer_4_22(patient, used_tracker):
    """Would you consider using a sleep tracker in the future? (if never used)"""
    if used_tracker == "Yes":
        return ""
    return random.choices(
        ["Yes", "Maybe", "No"],
        weights=[0.5, 0.3, 0.2]
    )[0]

def answer_4_23(patient, used_tracker):
    """Are you currently using a sleep tracker?"""
    if used_tracker != "Yes":
        return ""
    # If previously used, 55% currently use, else 45%
    return "Yes" if random.random() < 0.55 else "No"

def answer_4_24(patient, currently_using):
    """Which sleep tracker or app are you currently using? (multi-select)"""
    if currently_using != "Yes":
        return []
    options = [
        "Apple Watch", "Oura Ring", "Garmin", "Fitbit", "Whoop", "8 Sleep",
        "Sleeptracker AI", "Withings", "Other (please specify)"
    ]
    weights = [0.35, 0.18, 0.12, 0.15, 0.08, 0.04, 0.03, 0.03, 0.02]
    n = random.randint(1, 2)
    return random.choices(options, weights=weights, k=n)

def answer_4_25(patient, tracker_list):
    """How long have you been using each selected sleep tracker/app?"""
    if not tracker_list:
        return ""
    options = [
        "Less than 1 month", "1–3 months", "4–6 months", "7–12 months", "More than 1 year"
    ]
    return "|".join(random.choices(options, k=len(tracker_list)))

def answer_4_26(patient, used_tracker, currently_using):
    """Why did you stop using a sleep tracker? (multi-select)"""
    if used_tracker != "Yes" or currently_using != "No":
        return ""
    options = [
        "It was not providing useful information", "It was difficult to use or understand",
        "It was too time consuming to maintain", "I did not see any improvement in my sleep",
        "I found it uncomfortable or intrusive", "The data was inaccurate or inconsistent",
        "It increased my anxiety or stress about sleep", "I lost interest or motivation",
        "It did not fit well with my routine", "Technical issues with the app or device",
        "Other (please specify)"
    ]
    return "|".join(random.sample(options, k=random.randint(1, 3)))

def answer_4_27(patient, used_tracker, currently_using):
    """Would you be willing to retry a device or app in the future?"""
    if used_tracker != "Yes" or currently_using != "No":
        return ""
    options = [
        "Yes - open to trying", "Maybe - need more information",
        "Not now, but maybe in the future", "No"
    ]
    return random.choice(options)

# ====================
# ANSWER LOGIC FOR COGNITIVE HEALTH (SECTION 5)
# ====================

def answer_5_01(patient):
    """Rate current cognitive function."""
    profile = patient.get("health_profile", "average")
    options = ["Very poor", "Poor", "Fair", "Good", "Excellent"]
    if profile == "fit":
        weights = [0.01, 0.05, 0.15, 0.45, 0.34]
    elif profile == "poor":
        weights = [0.25, 0.35, 0.25, 0.12, 0.03]
    else:  # average
        weights = [0.08, 0.18, 0.35, 0.30, 0.09]
    return random.choices(options, weights=weights)[0]

def answer_5_02(patient):
    """Do you have concerns about cognitive function?"""
    profile = patient.get("health_profile", "average")
    if profile == "poor":
        p_yes = 0.8
    elif profile == "fit":
        p_yes = 0.18
    else:
        p_yes = 0.45
    return "Yes" if random.random() < p_yes else "No"

def answer_5_03(patient, has_concerns):
    """Primary cognitive concerns (multi-select)"""
    if has_concerns != "Yes":
        return []
    options = [
        "Memory loss",
        "Difficulty concentrating",
        "Trouble with problem solving or decision-making",
        "Difficulty finding words or speaking clearly",
        "Slower thinking or processing speed",
        "Other (please specify)"
    ]
    return random.sample(options, k=random.randint(1, 3))

def answer_5_04(patient):
    """Changes in cognitive function over past year?"""
    profile = patient.get("health_profile", "average")
    p_yes = 0.5 if profile == "poor" else (0.3 if profile == "average" else 0.12)
    return "Yes" if random.random() < p_yes else "No"

def answer_5_05(patient, had_changes):
    """Which changes noticed (multi-select)?"""
    if had_changes != "Yes":
        return []
    options = [
        "Increased forgetfulness",
        "More frequent confusion",
        "Difficulty learning new things",
        "Decreased ability to focus",
        "Other (please specify)"
    ]
    return random.sample(options, k=random.randint(1, 3))

def answer_5_06(patient):
    """How often do you challenge your brain?"""
    profile = patient.get("health_profile", "average")
    options = [
        "Daily",
        "Several times a week",
        "Weekly",
        "Occasionally",
        "Rarely or Never"
    ]
    if profile == "fit":
        weights = [0.5, 0.3, 0.12, 0.06, 0.02]
    elif profile == "poor":
        weights = [0.05, 0.12, 0.15, 0.23, 0.45]
    else:
        weights = [0.2, 0.3, 0.25, 0.15, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_5_07(patient, challenge_freq):
    """Willing to engage in more cognitive activities?"""
    # If already daily/several times, less likely
    if challenge_freq in ["Daily", "Several times a week"]:
        weights = [0.05, 0.2, 0.4, 0.35]
    else:
        weights = [0.5, 0.3, 0.15, 0.05]
    options = [
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    return random.choices(options, weights=weights)[0]

def answer_5_08(patient):
    """Types of cognitive activities (multi-select)"""
    profile = patient.get("health_profile", "average")
    options = [
        "Reading books or articles",
        "Engaging in hobbies (e.g., music, sports)",
        "Socializing with friends and family",
        "Learning a new language or skill",
        "Playing brain games or puzzles",
        "Other (please specify)"
    ]
    if profile == "fit":
        return random.sample(options, k=random.randint(2, 4))
    if profile == "poor":
        return random.sample(options, k=random.randint(1, 2))
    return random.sample(options, k=random.randint(2, 3))

def answer_5_09(patient):
    """Improved cognitive function with better sleep? Only relevant for 'poor'/'fair' sleep."""
    sleep_score = float(patient.get("sleep_score", 7.0))
    if sleep_score >= 6.0:
        return ""
    options = ["Yes", "No", "I'm not sure"]
    weights = [0.65, 0.1, 0.25]
    return random.choices(options, weights=weights)[0]

def answer_5_10(patient):
    """Improved cognitive function with better exercise? Only relevant for 'rarely'/'occasionally' exercise."""
    fitness_level = patient.get("fitness_level", "moderate")
    if fitness_level != "low":
        return ""
    options = ["Yes", "No", "I'm not sure"]
    weights = [0.65, 0.1, 0.25]
    return random.choices(options, weights=weights)[0]

def answer_5_11(patient):
    """What are your primary goals related to cognitive health? (multi-select)"""
    # Slightly more goals if 'fit', fewer if 'poor'
    profile = patient.get("health_profile", "average")
    options = [
        "Enhancing memory",
        "Improving focus and concentration",
        "Boosting problem-solving skills",
        "Increasing mental processing speed",
        "Preventing cognitive decline",
        "Other (please specify)"
    ]
    if profile == "fit":
        return random.sample(options, k=random.randint(2, 4))
    if profile == "poor":
        return random.sample(options, k=random.randint(1, 2))
    # average
    return random.sample(options, k=random.randint(1, 3))

def answer_5_12(patient):
    """What types of support would you consider utilizing to improve or optimize cognitive health? (multi-select)"""
    profile = patient.get("health_profile", "average")
    options = [
        "Cognitive training programs or apps",
        "Educational resources (e.g. books, articles)",
        "Professional guidance (e.g., neurologist, phychologist)",
        "Social activities or support groups",
        "Nutritional advice or supplements",
        "Physical exercise programs",
        "Other (please specify)"
    ]
    if profile == "fit":
        return random.sample(options, k=random.randint(2, 4))
    if profile == "poor":
        return random.sample(options, k=random.randint(1, 2))
    # average
    return random.sample(options, k=random.randint(1, 3))


# ====================
# ANSWER LOGIC FOR STRESS MANAGEMENT (SECTION 6)
# ====================

def answer_6_01(patient):
    """How would you rate your current level of stress?"""
    level = patient.get("stress_level", "moderate")
    options = [
        "No stress",
        "Low stress",
        "Moderate stress",
        "High stress",
        "Extreme stress",
        "Stress levels vary from low to moderate",
        "Stress levels vary from moderate to high"
    ]
    if level == "low":
        weights = [0.25, 0.6, 0.1, 0.01, 0.01, 0.03, 0.0]
    elif level == "high":
        weights = [0.01, 0.05, 0.15, 0.5, 0.15, 0.02, 0.12]
    else:  
        weights = [0.02, 0.08, 0.6, 0.2, 0.04, 0.04, 0.02]
    return random.choices(options, weights=weights)[0]

def answer_6_02(patient):
    """How often do you feel stressed?"""
    level = patient.get("stress_level", "moderate")
    options = ["Rarely", "Occasionally", "Frequently", "Always"]
    if level == "low":
        weights = [0.7, 0.25, 0.04, 0.01]
    elif level == "high":
        weights = [0.01, 0.09, 0.5, 0.4]
    else:  
        weights = [0.05, 0.35, 0.5, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_6_03(patient):
    """What are the primary sources of your stress? (multi-select)"""
    level = patient.get("stress_level", "moderate")
    options = [
        "Work", "Family or relationships", "Financial concerns", "Health issues",
        "Time management", "Major life changes",
        "Environmental factors (e.g., noise, commute)", "Other (please specify)"
    ]
    if level == "low":
        return random.sample(options, k=random.randint(1, 2))
    elif level == "high":
        return random.sample(options, k=random.randint(3, 5))
    else:  
        return random.sample(options, k=random.randint(2, 3))

def answer_6_04(patient):
    """What physical symptoms do you experience when you are stressed? (multi-select)"""
    level = patient.get("stress_level", "moderate")
    options = [
        "Headaches", "Muscle tension or pain", "Fatigue", "Upset stomach",
        "Rapid heartbeat", "Difficulty sleeping", "Other (please specify)",
        "I don't notice any physical effects"
    ]
    if level == "low":
        if random.random() < 0.7:
            return ["I don't notice any physical effects"]
        else:
            return random.sample(options[:-1], k=random.randint(0, 1))
    elif level == "high":
        return random.sample(options[:-1], k=random.randint(3, 6))
    else:  
        return random.sample(options[:-1], k=random.randint(1, 3))

def answer_6_05(patient):
    """Multi-select: What emotional or psychological symptoms do you experience when you are stressed?"""
    stress = patient.get("stress_level", "moderate")
    options = [
        "Anxiety", "Irritability or anger", "Sadness or depression",
        "Feeling overwhelmed", "Difficulty concentrating", "Restlessness",
        "Other (please specify)", "I don't experience any emotional or psychological symptoms"
    ]
    if stress == "low":
        if random.random() < 0.7:
            return ["I don't experience any emotional or psychological symptoms"]
        return random.sample(options[:-2], k=random.choices([0,1], [0.6,0.4])[0])
    if stress == "high":
        return random.sample(options[:-1], k=random.randint(3, 5))
    else:
        return random.sample(options[:-1], k=random.randint(1, 3))

def answer_6_06(patient):
    """Multi-select: How does stress affect your daily life?"""
    stress = patient.get("stress_level", "moderate")
    options = [
        "Decreased productivity", "Interference with personal relationships",
        "Reduced motivation", "Impact on physical health",
        "Changes in eating habits", "Changes in sleeping patterns",
        "Other (please specify)", "Stress does not affect my daily life"
    ]
    if stress == "low":
        if random.random() < 0.8:
            return ["Stress does not affect my daily life"]
        return random.sample(options[:-1], k=1)
    if stress == "high":
        return random.sample(options[:-1], k=random.randint(3, 6))
    else:
        return random.sample(options[:-1], k=random.randint(1, 3))

def answer_6_07(patient):
    """Multi-select: What methods do you currently use to manage your stress?"""
    stress = patient.get("stress_level", "moderate")
    options = [
        "Exercise or physical activity",
        "Meditation or mindfulness practices",
        "Deep breathing exercises",
        "Hobbies or recreational activities",
        "Talking to friends or family",
        "Professional counseling or therapy",
        "Journaling or writing",
        "Time management strategies",
        "Avoiding stressful situations",
        "Other (please specify)",
        "None"
    ]
    if stress == "low":
        if random.random() < 0.1:  
            return ["None"]
        return random.sample(options[:-1], k=random.randint(2, 4))
    elif stress == "high":
        if random.random() < 0.5: 
            return ["None"]
        return random.sample(options[:-1], k=1)
    else:  
        if random.random() < 0.15:  
            return ["None"]
        return random.sample(options[:-1], k=random.randint(1, 3))


def answer_6_08(patient, stress_methods_now):
    """Multi-select: Future methods, only show those not already selected (except 'None').
    If only 'None' was previously picked, offer all (including 'None') as available."""
    options = [
        "Exercise or physical activity",
        "Meditation or mindfulness practices",
        "Deep breathing exercises",
        "Hobbies or recreational activities",
        "Talking to friends or family",
        "Professional counseling or therapy",
        "Journaling or writing",
        "Time management strategies",
        "Avoiding stressful situations",
        "Other (please specify)",
        "None"
    ]
    if stress_methods_now == ["None"]:
        available = options
    else:
        available = [opt for opt in options if opt not in stress_methods_now and opt != "None"]

    if not available:
        return ["None"]
    k = min(len(available), random.randint(1, 3))
    return random.sample(available, k=k)

def answer_6_09(patient):
    """How effective are your current stress management methods?"""
    stress = patient.get("stress_level", "moderate")
    options = [
        "Not effective at all",
        "Slightly effective",
        "Moderately effective",
        "Very effective",
        "Extremely effective"
    ]
    if stress == "low":
        weights = [0.01, 0.09, 0.2, 0.4, 0.3]
    elif stress == "high":
        weights = [0.3, 0.3, 0.2, 0.1, 0.1]
    else:
        weights = [0.1, 0.25, 0.35, 0.2, 0.1]
    return random.choices(options, weights=weights)[0]

def answer_6_10(patient):
    """How important is it for you to improve your stress management skills?"""
    stress = patient.get("stress_level", "moderate")
    options = [
        "Not at all important",
        "Slightly important",
        "Moderately important",
        "Very important",
        "Extremely important"
    ]
    if stress == "low":
        weights = [0.4, 0.35, 0.2, 0.04, 0.01]
    elif stress == "high":
        weights = [0.01, 0.05, 0.15, 0.39, 0.4]
    else:
        weights = [0.05, 0.2, 0.35, 0.25, 0.15]
    return random.choices(options, weights=weights)[0]

def answer_6_11(patient):
    """How comfortable are you in seeking help for stress management?"""
    stress = patient.get("stress_level", "moderate")
    options = [
        "Extremely uncomfortable",
        "Somewhat uncomfortable",
        "Neither comfortable nor uncomfortable",
        "Somewhat comfortable",
        "Extremely comfortable"
    ]
    if stress == "high":
        weights = [0.3, 0.3, 0.2, 0.15, 0.05]
    elif stress == "low":
        weights = [0.05, 0.1, 0.2, 0.3, 0.35]
    else:  # moderate
        weights = [0.15, 0.2, 0.25, 0.25, 0.15]
    return random.choices(options, weights=weights)[0]

def answer_6_12(patient):
    """Multi-select: What are your primary goals related to stress management?"""
    options = [
        "Reduce overall stress",
        "Improve physical health",
        "Improve mental health",
        "Enhance work performance",
        "Improve personal relationships",
        "Increase overall well-being",
        "Other (please specify)"
    ]
    return random.sample(options, k=random.randint(1, 3))

def answer_6_13(patient):
    """Multi-select: What types of support would you find most helpful in managing your stress?"""
    options = [
        "Professional counseling or therapy",
        "Stress management workshops or classes",
        "Support groups",
        "Online resources or apps",
        "Books or educational materials",
        "Relaxation techniques (e.g. yoga, meditation)",
        "Time management tools or strategies",
        "Other (please specify)"
    ]
    return random.sample(options, k=random.randint(1, 3))

def answer_6_14(patient):
    """Do you use any apps or wearables to help with stress management?"""
    return random.choices(["Yes", "No"], weights=[0.3, 0.7])[0]

def answer_6_15(patient, uses_wearable):
    """Multi-select: Which apps or wearables?"""
    if uses_wearable != "Yes":
        return []
    options = [
        "Apple Watch", "Fitbit", "Garmin", "Oura Ring", "Samsung Watch",
        "Calm App", "Headspace App", "Other (please specify)"
    ]
    always = []
    if random.random() < 0.5:
        always = ["Apple Watch"]
        sample = random.sample([o for o in options if o != "Apple Watch"], k=random.randint(0, 2))
        return always + sample
    else:
        return random.sample(options, k=random.randint(1, 3))
    
def answer_6_16(patient, uses_wearable):
    """Single-select: If not currently using, would you consider app/wearable for managing stress?"""
    if uses_wearable == "No":
        return ""
    options = [
        "Yes - open to trying", "Maybe - need more information",
        "Not now, but maybe in the future", "No"
    ]
    return random.choice(options)
    
# ====================
# ANSWER LOGIC FOR CONNECTION + PURPOSE (SECTION 7)
# ====================

def answer_7_01(patient):
    """How would you rate the quality of your current social relationships?"""
    options = [
        "Very poor", "Poor", "Fair", "Good", "Excellent"
    ]
    weights = [0.05, 0.1, 0.3, 0.4, 0.15]  
    return random.choices(options, weights=weights)[0]

def answer_7_02(patient):
    """How often do you interact with friends and/or family?"""
    options = [
        "Daily", "Several times a week", "Weekly", "Several times a month", "Rarely"
    ]
    weights = [0.3, 0.25, 0.2, 0.15, 0.1]  
    return random.choices(options, weights=weights)[0]

def answer_7_03(patient):
    """What types of social activities do you typically engage in? (multi-select)"""
    options = [
        "In-person gatherings",
        "Phone calls",
        "Video calls",
        "Text messaging or social media",
        "Group activities (e.g., sports, clubs)",
        "Volunteering",
        "Other (please specify)"
    ]
    k = random.choices([1,2,3,4], [0.1,0.2,0.4,0.3])[0]
    return random.sample(options, k=k)

def answer_7_04(patient):
    """How satisfied are you with the amount of social interaction you have?"""
    options = [
        "Extremely dissatisfied",
        "Somewhat dissatisfied",
        "Neither satisfied nor dissatisfied",
        "Somewhat satisfied",
        "Extremely satisfied"
    ]
    weights = [0.05, 0.1, 0.3, 0.4, 0.15]  
    return random.choices(options, weights=weights)[0]

def answer_7_05(patient):
    """How would you describe your support network?"""
    options = [
        "Very weak", "Weak", "Moderate", "Strong", "Very strong"
    ]
    weights = [0.06, 0.12, 0.35, 0.35, 0.12]
    return random.choices(options, weights=weights)[0]

def answer_7_06(patient):
    """Who do you rely on for emotional support? (multi-select)"""
    options = [
        "Family", "Friends", "Colleagues", "Support groups", "Professional counselor or therapist", "Other (please specify)"
    ]
    k = random.choices([1,2,3], [0.3,0.45,0.25])[0]
    return random.sample(options, k=k)

def answer_7_07(patient):
    """Do you feel you have someone to talk to when you need support?"""
    options = [
        "Always", "Usually", "Sometimes", "Rarely", "Never"
    ]
    weights = [0.4, 0.25, 0.2, 0.1, 0.05]
    return random.choices(options, weights=weights)[0]

def answer_7_08(patient):
    """What challenges do you face in maintaining social relationships? (multi-select)"""
    options = [
        "Lack of time", "Geographical distance", "Personal or family obligations",
        "Health issues", "Social anxiety or shyness", "Lack of interest", "Other (please specify)"
    ]
    if random.random() < 0.2:
        return []
    k = random.choices([1,2], [0.7,0.3])[0]
    return random.sample(options, k=k)

def answer_7_09(patient):
    """How comfortable are you in social situations?"""
    options = [
        "Extremely uncomfortable", "Somewhat uncomfortable", "Neither comfortable nor uncomfortable",
        "Somewhat comfortable", "Extremely comfortable"
    ]
    weights = [0.06, 0.16, 0.2, 0.38, 0.2]
    return random.choices(options, weights=weights)[0]

def answer_7_10(patient):
    """How important is it for you to improve your social interactions?"""
    options = [
        "Not at all important", "Slightly important", "Moderately important", "Very important", "Extremely important"
    ]
    weights = [0.05, 0.14, 0.26, 0.37, 0.18]
    return random.choices(options, weights=weights)[0]

# ====================
# ANSWER LOGIC FOR CORE CARE - SUBSTANCES/SUPPLEMENTS/HYGIENE (SECTION 8)
# ====================

# For each substance, map question tags to relevant options.
SUBSTANCE_QS = {
    "Tobacco (cigarettes, cigars, smokeless tobacco)": {
        "freq": [
            "Heavy: 2+ packs per day (or equivalent heavy vape/smokeless)",
            "Moderate: 1 pack per day (or moderate vape/smokeless)",
            "Light: Less than 1 pack per day / occasional use",
            "Minimal: A few times a month or less",
            "Occasional: Only rarely or on special occasions"
        ],
        "years": [
            "Less than 1 year", "1-2 years", "3-5 years", "6-10 years", "11-20 years", "More than 20 years"
        ],
        "pattern": [
            "I currently use more than I used to",
            "My current use is about the same as its been overall",
            "I currently use less than I used to"
        ],
        "past_freq": [
            "Heavy: 2+ packs per day (or equivalent heavy vape/smokeless)",
            "Moderate: 1 pack per day (or moderate vape/smokeless)",
            "Light: Less than 1 pack per day / occasional use",
            "Minimal: A few times a month or less",
            "Occasional: Only rarely or on special occasions"
        ]
    },
    "Alcohol": {
        "freq": [
            "Heavy: 5+ drinks per day / heavy daily use",
            "Moderate: 2–4 drinks per day / frequent use",
            "Light: 1 drink per day or most days",
            "Minimal: A few drinks per month or less",
            "Occasional: Only rarely/special occasions"
        ],
        "years": [
            "Less than 1 year", "1-2 years", "3-5 years", "6-10 years", "11-20 years", "More than 20 years"
        ],
        "pattern": [
            "I currently use more than I used to",
            "My current use is about the same as its been overall",
            "I currently use less than I used to"
        ],
        "past_freq": [
            "Heavy: 5+ drinks per day / heavy daily use",
            "Moderate: 2–4 drinks per day / frequent use",
            "Light: 1 drink per day or most days",
            "Minimal: A few drinks per month or less",
            "Occasional: Only rarely/special occasions"
        ]
    },
    "Recreational drugs (e.g., marijuana)": {
        "freq": [
            "Heavy: Daily or almost daily use",
            "Moderate: Weekly use (1–2x/week)",
            "Light: Monthly or less",
            "Minimal: A few times a year",
            "Occasional: Only a handful of times ever"
        ],
        "years": [
            "Less than 1 year", "1-2 years", "3-5 years", "6-10 years", "11-20 years", "More than 20 years"
        ],
        "pattern": [
            "I currently use more than I used to",
            "My current use is about the same as its been overall",
            "I currently use less than I used to"
        ],
        "past_freq": [
            "Heavy: Daily or almost daily use",
            "Moderate: Weekly use (1–2x/week)",
            "Light: Monthly or less",
            "Minimal: A few times a year",
            "Occasional: Only a handful of times ever"
        ]
    },
    "Nicotine": {
        "freq": [
            "Heavy: All-day or equivalent to 2+ packs/day",
            "Moderate: Most of the day/equivalent to 1 pack/day",
            "Light: Less than daily or only in specific situations",
            "Minimal: A few times a month or less",
            "Occasional: Only rarely or on special occasions"
        ],
        "years": [
            "Less than 1 year", "1-2 years", "3-5 years", "6-10 years", "11-20 years", "More than 20 years"
        ],
        "pattern": [
            "I currently use more than I used to",
            "My current use is about the same as its been overall",
            "I currently use less than I used to"
        ],
        "past_freq": [
            "Heavy: All-day or equivalent to 2+ packs/day",
            "Moderate: Most of the day/equivalent to 1 pack/day",
            "Light: Less than daily or only in specific situations",
            "Minimal: A few times a month or less",
            "Occasional: Only rarely or on special occasions"
        ]
    },
    "Over-the-counter medications (e.g., sleep aids)": {
        "freq": [
            "Heavy: Daily or nightly use for months",
            "Moderate: Several times per week",
            "Light: A few times per month",
            "Minimal: Less than monthly",
            "Occasional: Only rarely or on special occasions"
        ],
        "years": [
            "Less than 1 year", "1-2 years", "3-5 years", "6-10 years", "11-20 years", "More than 20 years"
        ],
        "pattern": [
            "I currently use more than I used to",
            "My current use is about the same as its been overall",
            "I currently use less than I used to"
        ],
        "past_freq": [
            "Heavy: Daily or nightly use for months",
            "Moderate: Several times per week",
            "Light: A few times per month",
            "Minimal: Less than monthly",
            "Occasional: Only rarely or on special occasions"
        ]
    },
    "Other": {
        "freq": [
            "Heavy: Daily or almost daily use",
            "Moderate: Weekly use (1–2x/week)",
            "Light: Monthly or less",
            "Minimal: A few times a year",
            "Occasional: Only a handful of times ever"
        ],
        "years": [
            "Less than 1 year", "1-2 years", "3-5 years", "6-10 years", "11-20 years", "More than 20 years"
        ],
        "pattern": [
            "I currently use more than I used to",
            "My current use is about the same as its been overall",
            "I currently use less than I used to"
        ],
        "past_freq": [
            "Heavy: Daily or almost daily use",
            "Moderate: Weekly use (1–2x/week)",
            "Light: Monthly or less",
            "Minimal: A few times a year",
            "Occasional: Only a handful of times ever"
        ]
    }
}

SUBSTANCE_META = [
    {
        "name": "Tobacco (cigarettes, cigars, smokeless tobacco)",
        "current": {"freq": "8.02", "years": "8.03", "pattern": "8.04"},
        "past": {"years": "8.21", "freq": "8.22"}
    },
    {
        "name": "Alcohol",
        "current": {"freq": "8.05", "years": "8.06", "pattern": "8.07"},
        "past": {"years": "8.23", "freq": "8.24"}
    },
    {
        "name": "Recreational drugs (e.g., marijuana)",
        "current": {"freq": "8.08", "years": "8.09", "pattern": "8.10"},
        "past": {"years": "8.25", "freq": "8.26"}
    },
    {
        "name": "Nicotine",
        "current": {"freq": "8.11", "years": "8.12", "pattern": "8.13"},
        "past": {"years": "8.27", "freq": "8.28"}
    },
    {
        "name": "Over-the-counter medications (e.g., sleep aids)",
        "current": {"freq": "8.14", "years": "8.15", "pattern": "8.16"},
        "past": {"years": "8.29", "freq": "8.30"}
    },
    {
        "name": "Other",
        "current": {"freq": "8.17", "years": "8.18", "pattern": "8.19"},
        "past": {"years": "8.31", "freq": "8.32"}
    }
]

def random_substance_answer(subst, qtype):
    """Randomly select an option for substance Q."""
    if qtype == "freq" or qtype == "past_freq":
        return random.choice(SUBSTANCE_QS[subst]["freq"])
    elif qtype == "years":
        return random.choice(SUBSTANCE_QS[subst]["years"])
    elif qtype == "pattern":
        return random.choice(SUBSTANCE_QS[subst]["pattern"])
    return ""

def answer_8_01(patient):
    """Multi-select: Which, if any, of the following substances do you currently use?"""
    options = [s["name"] for s in SUBSTANCE_META] + ["None"]
    if random.random() < 0.2:
        return ["None"]
    k = random.choices([1, 2, 3], [0.7, 0.2, 0.1])[0]
    return random.sample(options[:-1], k=k)

def current_use_rowdata(substances):
    rowdata = {}
    for meta in SUBSTANCE_META:
        if meta["name"] not in substances:
            continue
        tags = meta["current"]
        rowdata[tags["freq"]] = random.choice(SUBSTANCE_QS[meta["name"]]["freq"])
        rowdata[tags["years"]] = random.choice(SUBSTANCE_QS[meta["name"]]["years"])
        rowdata[tags["pattern"]] = random.choice(SUBSTANCE_QS[meta["name"]]["pattern"])
    return rowdata

def past_use_rowdata(substances):
    all_names = [s["name"] for s in SUBSTANCE_META]
    not_current = [name for name in all_names if name not in substances]
    if not_current and random.random() < 0.7:
        n = random.randint(1, min(2, len(not_current)))
        used_past = random.sample(not_current, n)
    else:
        used_past = ["None"]
    rowdata = {}
    rowdata["8.20"] = "|".join(used_past)
    for meta in SUBSTANCE_META:
        if meta["name"] not in used_past or used_past == ["None"]:
            continue
        tags = meta["past"]
        rowdata[tags["years"]] = random.choice(SUBSTANCE_QS[meta["name"]]["years"])
        rowdata[tags["freq"]] = random.choice(SUBSTANCE_QS[meta["name"]]["past_freq"])
    return rowdata

# --- Generate all substance use rowdata ---

def answer_8_33(patient, substances, past_substances):
    """Reasons for quitting (multi-select, if any past use)"""
    options = [
        "Health concerns", "Personal or family reasons", "Social reasons",
        "Professional advice", "Other"
    ]
    if not past_substances or "None" in past_substances:
        return []
    k = random.randint(1, min(3, len(options)))
    return random.sample(options, k=k)

def answer_8_34(patient, substances):
    """Impact on daily life (multi-select, if any current use)"""
    options = [
        "No impact", "Reduced physical health", "Reduced mental health",
        "Strained personal relationships", "Impaired work performance", "Other"
    ]
    if not substances or "None" in substances:
        return ["No impact"]
    k = random.randint(1, min(3, len(options)))
    return random.sample(options, k=k)

def answer_8_35(patient, substances):
    """Readiness to reduce/quit (if any current use)"""
    options = [
        "Yes - actively trying", "Yes - open to trying", "Maybe - need more information",
        "Not now, but maybe in the future", "No"
    ]
    if not substances or "None" in substances:
        return "No"
    return random.choice(options)

def answer_8_36(patient, substances):
    """Which would you consider quitting (multi, from current)"""
    if not substances or "None" in substances:
        return []
    k = random.randint(1, len(substances))
    return random.sample([s for s in substances if s != "None"], k=k)

def answer_8_37(patient, substances):
    """Importance of addressing substance use"""
    options = [
        "Not at all important", "Slightly important", "Moderately important",
        "Very important", "Extremely important"
    ]
    if not substances or "None" in substances:
        return "Not at all important"
    return random.choice(options)

def answer_8_38(patient):
    """Are you currently taking dietary supplements?"""
    return random.choices(["Yes", "No"], weights=[0.7, 0.3])[0]

def answer_8_39(patient, takes_dietary_supps):
    """Free text listing of dietary supplements."""
    if takes_dietary_supps != "Yes":
        return ""
    options = [
        "Vitamin D", "Omega-3", "Multivitamin", "Probiotic", "Magnesium", "Collagen", "Zinc", "B12"
    ]
    n = random.randint(1, 4)
    return ", ".join(random.sample(options, n))

def answer_8_40(patient, takes_dietary_supps):
    """Consider dietary supplements?"""
    if takes_dietary_supps == "Yes":
        return ""
    options = [
        "Yes - open to trying", 
        "Maybe - need more information", 
        "Not now, but maybe in the future", 
        "No"
    ]
    return random.choice(options)

def answer_8_41(patient):
    """Are you currently taking performance supplements"""
    return random.choices(["Yes", "No"], weights=[0.7, 0.3])[0]

def answer_8_42(patient, takes_performance_supps):
    """Free text listing of performance supplements"""
    if takes_performance_supps != "Yes":
            return ""
    options = [
        "Creatine Monohydrate",
        "Beta-Alanine",
        "Citrulline Malate",
        "Branched-Chain Amino Acids (BCAAs)",
        "Essential Amino Acids (EAAs)",
        "Whey Protein",
        "Casein Protein",
        "Electrolytes (e.g., sodium, potassium, magnesium)",
        "Tart Cherry Extract",
        "Beetroot Juice/Nitrates",
        "Ashwagandha",
        "Rhodiola Rosea",
        "Caffeine",
        "L-Theanine",
        "NAC (N-Acetyl Cysteine)",
        "Vitamin D",
        "Omega-3 (EPA/DHA)",
        "Magnesium",
        "Zinc",
        "CoQ10 (Ubiquinol)"
    ]
    n = random.randint(1, 4)
    return ", ".join(random.sample(options, n))

def answer_8_43(patient, takes_performance_supps):
    """Consider performance supplements?"""
    options = [
        "Yes - open to trying", 
        "Maybe - need more information", 
        "Not now, but maybe in the future", 
        "No"
    ]
    if takes_performance_supps != "Yes":
        return ""
    return random.choice(options)

def answer_8_44(patient):
    """Do you take sleep aids/medications"""
    return random.choices(["Yes", "No"], weights=[0.6, 0.4])[0]

def answer_8_45(patient,takes_sleep_supps):
    """Frequency of sleep aid use."""
    if takes_sleep_supps != "Yes":
        return ""  
    options = ["Rarely", "Occasionally", "Frequently", "Always"]
    weights = [0.65, 0.2, 0.1, 0.05]
    return random.choices(options, weights=weights)[0]

def answer_8_46(patient, sleep_aid_freq):
    """Which types of sleep aids do you take?"""
    options = [
        "Prescription medication",
        "Over-the-counter medications",
        "Natural supplements",
        "Other"
    ]
    if sleep_aid_freq == "Rarely":
        return []
    n = random.randint(1, 2)
    return random.sample(options, n)

def answer_8_47(patient, aid_types):
    """Which natural supplements for sleep (if applicable)?"""
    options = [
        "Magnesium threonate / Magnesium Bisglycinate",
        "Apigenin", "Theanine", "Glycine", "GABA", "Melatonin", "Other"
    ]
    if "Natural supplements" not in aid_types:
        return []
    n = random.randint(1, 3)
    return random.sample(options, n)

def answer_8_48(patient, sleep_aid_freq, aid_types):
    """Would you consider supplements for sleep longevity goals?"""
    options = [
        "Yes - open to trying", 
        "Maybe - need more information", 
        "Not now, but maybe in the future", 
        "No"
    ]
    if sleep_aid_freq == "Rarely" and not aid_types:
        return "No"
    return random.choice(options)

def answer_8_49(patient):
    """Currently taking additional health supplements?"""
    return random.choices(["Yes", "No"], weights=[0.5, 0.5])[0]

def answer_8_50(patient, takes_more):
    """List additional health supplements (free text)"""
    if takes_more != "Yes":
        return ""
    options = [
        "NAC", "Creatine", "Ashwagandha", "CoQ10", "Lion's Mane", "Bacopa", "Fish Oil", "Vitamin K2"
    ]
    n = random.randint(1, 3)
    return ", ".join(random.sample(options, n))

def answer_8_51(patient, takes_more):
    """Consider more for longevity (general health)"""
    options = [
        "Yes - open to trying", "Maybe - need more information",
        "Not now, but maybe in the future", "No"
    ]
    if takes_more == "No":
        return random.choices(options, weights=[0.15, 0.35, 0.4, 0.1])[0]
    return random.choice(options)

import random

def answer_8_52(patient):
    """How often do you floss?"""
    return random.choices(
        ["Daily", "A few times a week", "Rarely", "Never"],
        weights=[0.5, 0.3, 0.15, 0.05]
    )[0]

def answer_8_53(patient, floss_freq):
    """Would you consider flossing more?"""
    options = [
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    if floss_freq == "Daily":
        # Less likely to consider more
        return random.choices(options, weights=[0.05,0.1,0.35,0.5])[0]
    return random.choices(options, weights=[0.5,0.2,0.2,0.1])[0]

def answer_8_54(patient):
    """How often do you brush?"""
    return random.choices(
        ["≥2 times a day", "<2 times a day"],
        weights=[0.8, 0.2]
    )[0]

def answer_8_55(patient, brush_freq):
    """Would you consider brushing more?"""
    options = [
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    if brush_freq == "≥2 times a day":
        return random.choices(options, weights=[0.02,0.08,0.3,0.6])[0]
    return random.choices(options, weights=[0.5,0.2,0.2,0.1])[0]

def answer_8_56(patient):
    """How often sunscreen?"""
    return random.choices(
        ["Daily", "A few times a week", "Rarely", "Never"],
        weights=[0.3, 0.3, 0.3, 0.1]
    )[0]

def answer_8_57(patient, sunscreen_freq):
    """Consider more sunscreen?"""
    options = [
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    if sunscreen_freq == "Daily":
        return random.choices(options, weights=[0.05,0.1,0.3,0.55])[0]
    return random.choices(options, weights=[0.45,0.25,0.2,0.1])[0]

def answer_8_58(patient):
    """Consistent skincare routine?"""
    return random.choices(["Yes", "No"], weights=[0.45, 0.55])[0]

def answer_8_59(patient, skincare):
    """Consider adding routine?"""
    options = [
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ]
    if skincare == "Yes":
        return ""
    return random.choices(options, weights=[0.4,0.25,0.25,0.1])[0]

# ====================
# ANSWER LOGIC FOR CORE CARE - PERSONAL/FAMILY HISTORY (SECTION 9)
# ====================

# ========== Family History Section ==========

FAMILY_HISTORY = [
    # name, yesno_col, rel_col, age_col, [special_text_cols]
    ('Heart Attack/ASCVD', '9.01', '9.02', '9.03', []),
    ('Stroke', '9.04', '9.05', '9.06', []),
    ('Diabetes', '9.07', '9.08', '9.09', []),
    ('Dementia/Alzheimer\'s', '9.10', '9.11', '9.12', []),
    ('Breast Cancer', '9.13', '9.14', '9.15', []),
    ('Colon Cancer', '9.16', '9.17', '9.18', []),
    ('Prostate Cancer', '9.19', '9.20', '9.21', []),
    ('Other Cancer', '9.22', '9.24', '9.25', ['9.23']),
    ('Osteoporosis/Osteopenia', '9.26', '9.27', '9.28', []),
    ('Autoimmune disease', '9.29', '9.30', '9.31', []),
    ('Mental Health issues', '9.32', '9.33', '9.34', []),
    ('Substance Use', '9.35', '9.36', '9.37', []),
    ('Other Significant Health History', '9.38', None, None, ['9.39']),
]
RELATIVES = ['Parent', 'Sibling', 'Grandparent', 'Other']

def rand_yesno(p=0.2):
    """Random Yes/No with given probability for 'Yes'."""
    return 'Yes' if random.random() < p else 'No'

def rand_relatives():
    k = random.choices([1, 2], [0.8, 0.2])[0]
    return '|'.join(random.sample(RELATIVES, k=k))

def rand_age(min_age=35, max_age=80):
    return str(random.randint(min_age, max_age))

def rand_text(candidates):
    return random.choice(candidates)

def answer_family_history():
    rowdata = {}
    for name, yesno_col, rel_col, age_col, special_cols in FAMILY_HISTORY:
        rowdata[yesno_col] = rand_yesno(0.25)
        if rel_col:
            rowdata[rel_col] = ''
        if age_col:
            rowdata[age_col] = ''
        for c in special_cols:
            rowdata[c] = ''
        if rowdata[yesno_col] == 'Yes':
            if rel_col:
                rel = rand_relatives()
                rowdata[rel_col] = rel
            if age_col and rowdata[rel_col]:
                relatives = rowdata[rel_col].split('|')
                ages = [rand_age() for _ in relatives]
                rowdata[age_col] = '|'.join(ages)
            for c in special_cols:
                if c == '9.23':
                    rowdata[c] = rand_text([
                        'Lung Cancer', 'Skin Cancer', 'Leukemia', 'Pancreatic Cancer', 'Other'
                    ])
                elif c == '9.39':
                    rowdata[c] = rand_text([
                        'Liver disease (Parent)', 'Kidney disease (Sibling)', 'Rare disease (Other)'
                    ])
    return rowdata

def answer_personal_history():
    import random

    conditions = [
        # (Yes/No col, Age col, Free text col)
        ('9.40', '9.41', None),           # Heart Attack/ASCVD
        ('9.42', '9.43', None),           # Stroke
        ('9.44', '9.45', None),           # Diabetes
        ('9.46', '9.47', None),           # Dementia/Alzheimer's
        ('9.48', '9.49', None),           # Breast Cancer
        ('9.50', '9.51', None),           # Colon Cancer
        ('9.52', '9.53', None),           # Prostate Cancer
        ('9.54', None,   '9.55'),         # Other cancer
        ('9.56', '9.57', None),           # Osteoporosis/Osteopenia
        ('9.58', None,   '9.59'),         # Autoimmune
        ('9.60', None,   '9.61'),         # Mental Health
        ('9.62', None,   '9.63'),         # Substance Use Dx
        ('9.64', None,   '9.65'),         # Other significant history
    ]

    # Text examples for free text
    other_cancer_types = ['Skin cancer age 49', 'Thyroid cancer age 33', 'Bladder cancer age 62']
    autoimmune_types = ['Rheumatoid arthritis age 40', 'Lupus age 35', 'Celiac disease age 29']
    mental_health_types = ['Major depression age 27', 'Bipolar disorder age 30', 'PTSD age 41']
    substance_types = ['Alcohol use disorder age 32', 'Opioid use disorder age 25']
    other_conditions = ['Kidney disease age 55', 'Liver disease age 60', 'Hypertension age 37']

    row = {}

    for idx, (yn_col, age_col, text_col) in enumerate(conditions):
        yes = random.random() < 0.15  # ~15% chance diagnosed

        # Yes/No column
        row[yn_col] = 'Yes' if yes else 'No'

        # Age or free text
        if yes:
            if age_col:
                # Random plausible age, younger for autoimmune, mental, etc.
                row[age_col] = str(random.randint(18, 70))
            if text_col:
                if text_col == '9.55':
                    row[text_col] = random.choice(other_cancer_types)
                elif text_col == '9.59':
                    row[text_col] = random.choice(autoimmune_types)
                elif text_col == '9.61':
                    row[text_col] = random.choice(mental_health_types)
                elif text_col == '9.63':
                    row[text_col] = random.choice(substance_types)
                elif text_col == '9.65':
                    row[text_col] = random.choice(other_conditions)
        else:
            # No diagnosis: blank age/text
            if age_col:
                row[age_col] = ''
            if text_col:
                row[text_col] = ''

    return row


# ====================
# ANSWER LOGIC FOR CORE CARE - SCREENINGS + NAMED TESTS (SECTION 10)
# ====================

# screenings

from datetime import datetime, timedelta
import random

def months_ago(months):
    """Return an ISO date string N months ago."""
    dt = datetime.today() - timedelta(days=months*30)
    return dt.strftime('%Y-%m-%d')

def years_ago(years):
    """Return an ISO date string N years ago."""
    dt = datetime.today() - timedelta(days=years*365)
    return dt.strftime('%Y-%m-%d')

def answer_screenings(patient):
    hp = patient.get('health_profile', 'average')
    sex = patient.get('sex', 'female').lower()
    age = int(patient.get('age', 40))
    row = {}

    # Ranges
    ranges = {
        "dental": 6,        # months
        "skin": 12,         # months
        "vision": 12,       # months
        "colon": 120,       # months
        "mammo": 12,        # months (assume annual)
        "pap": 36,          # months (3 years)
        "dexa": 6,          # months
        "psa": 36,          # months (3 years)
    }

    # For each, logic: fit (in range), average (mostly), poor (mostly out)
    def gen_date(period_months, mostly_in_range=True):
        if mostly_in_range:
            offset = random.randint(0, int(period_months*1.25))
        else:
            offset = random.randint(int(period_months*1.5), int(period_months*2.5))
        return months_ago(offset)

    # Dental (all)
    row['10.01'] = gen_date(ranges['dental'],
                            hp == 'fit' or (hp == 'average' and random.random() < 0.7))
    # Skin check (all)
    row['10.02'] = gen_date(ranges['skin'],
                            hp == 'fit' or (hp == 'average' and random.random() < 0.7))

    # Vision (all)
    row['10.03'] = gen_date(ranges['vision'],
                            hp == 'fit' or (hp == 'average' and random.random() < 0.7))

    # Colon (only 50+)
    if age >= 50:
        row['10.04'] = years_ago(random.randint(0, 10) if (hp == 'fit' or (hp == 'average' and random.random() < 0.7)) else random.randint(11, 25))
    else:
        row['10.04'] = ''

    # Mammogram (females only)
    if sex == 'female':
        row['10.05'] = gen_date(ranges['mammo'],
                                hp == 'fit' or (hp == 'average' and random.random() < 0.7))
        row['10.06'] = gen_date(ranges['pap'],
                                hp == 'fit' or (hp == 'average' and random.random() < 0.7))
    else:
        row['10.05'] = ''
        row['10.06'] = ''

    # DEXA (all)
    row['10.07'] = gen_date(ranges['dexa'],
                            hp == 'fit' or (hp == 'average' and random.random() < 0.7))

    # PSA (males only)
    if sex == 'male':
        row['10.08'] = gen_date(ranges['psa'],
                                hp == 'fit' or (hp == 'average' and random.random() < 0.7))
    else:
        row['10.08'] = ''

    return row

def answer_10_09(patient):
    """Cardiac screening (random yes/no)"""
    return random.choice(['Yes', 'No'])

def answer_10_10(patient):
    """Sleep study (random yes/no)"""
    return random.choice(['Yes', 'No'])

def answer_10_11(patient):
    """Up to date on immunizations? (random yes/no)"""
    return random.choice(['Yes', 'No'])

def answer_10_12(patient):
    """Prescription meds: blank or random meds"""
    example_meds = [
        "Atorvastatin 20mg", "Lisinopril 10mg", "Metformin 500mg", 
        "Levothyroxine 50mcg", "Amlodipine 5mg", "Omeprazole 20mg",
        "Vitamin D3", "None"
    ]
    # 30% chance no meds, else 1-3 random meds (comma separated)
    if random.random() < 0.3:
        return ''
    meds = random.sample(example_meds[:-1], k=random.randint(1, 3))
    return ", ".join(meds)


# ====================
# NAMED TESTS SECTION (PHQ-2, GAD-2, BRHS, STOP-BANG, Epworth)
# ====================

PHQ2_OPTIONS = [
    "Not at all",
    "Several days",
    "More than half the days",
    "Nearly every day"
]

GAD2_OPTIONS = PHQ2_OPTIONS  # Same options

BRHS_OPTIONS = [
    "Strongly agree", "Agree", "Slightly agree", "Neither agree nor disagree",
    "Slightly disagree", "Disagree", "Strongly disagree"
]

YN_OPTIONS = ["Yes", "No"]

EPWORTH_OPTIONS = [
    "Would never nod off",
    "Slight chance of nodding off",
    "Moderate chance of nodding off",
    "High chance of nodding off"
]

def bias_pick(options, profile, positive_idx=0):
    n = len(options)
    if profile == 'fit':
        if n == 2:
            weights = [0.65 if i == positive_idx else 0.35 for i in range(n)]
        elif n > 2:
            weights = [0.65 if i == positive_idx else 0.25 if i == positive_idx+1 else (0.1/(n-2)) for i in range(n)]
    elif profile == 'average':
        # Distribute for n options
        if n == 2:
            weights = [0.55, 0.45]
        else:
            # Spread somewhat evenly
            base = 1.0 - 0.25 - 0.22 - 0.09
            rest = base/(n-3) if n > 3 else 0
            weights = [0.25 if i==positive_idx else 0.22 if i==positive_idx+1 else 0.09 if i==n-1 else rest for i in range(n)]
    else:  # poor
        if n == 2:
            weights = [0.35 if i == positive_idx else 0.65 for i in range(n)]
        else:
            # Heavier bias to last items
            base = 1.0 - 0.1 - 0.25 - 0.25
            rest = base/(n-3) if n > 3 else 0
            weights = [0.1 if i==positive_idx else 0.25 if i>=n-2 else rest for i in range(n)]
    # Normalize weights just in case
    s = sum(weights)
    weights = [w/s for w in weights]
    return random.choices(options, weights=weights, k=1)[0]


def answer_named_tests(patient):
    profile = patient.get("health_profile", "average")
    row = {}

    # PHQ-2 (Depression)
    row['10.13'] = bias_pick(PHQ2_OPTIONS, profile, positive_idx=0)
    row['10.14'] = bias_pick(PHQ2_OPTIONS, profile, positive_idx=0)

    # GAD-2 (Anxiety)
    row['10.15'] = bias_pick(GAD2_OPTIONS, profile, positive_idx=0)
    row['10.16'] = bias_pick(GAD2_OPTIONS, profile, positive_idx=0)

    # BRHS (Wellbeing/Happiness)
    for q in ['10.17', '10.18', '10.19', '10.20', '10.21']:
        row[q] = bias_pick(BRHS_OPTIONS, profile, positive_idx=0)

    # STOP-BANG (Sleep Apnea Risk: Yes/No)
    for q in ['10.22', '10.23', '10.24', '10.25']:
        # For "fit", bias to "No" (index 1), for "poor" bias to "Yes" (index 0)
        pos_idx = 1  # "No"
        row[q] = bias_pick(YN_OPTIONS, profile, positive_idx=pos_idx)

    # Epworth Sleepiness Scale (8 situations)
    for i, q in enumerate([f'10.{26+i}' for i in range(8)]):
        row[q] = bias_pick(EPWORTH_OPTIONS, profile, positive_idx=0)

    return row


# ====================
# MAIN DRIVER AND ENTRYPOINT
# ====================

def generate_survey_responses(profile_csv, out_csv=None, seed=42):
    # Add file existence check
    if not os.path.exists(profile_csv):
        print(f"⚠️  Profile data file not found: {profile_csv}")
        print("Please run generate_biomarker_dataset.py first to create the biomarker data.")
        return
    
    # Handle default output path
    if out_csv is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        out_csv = os.path.join(base_dir, "synthetic_patient_survey.csv")
    
    random.seed(seed)
    df_profiles = pd.read_csv(profile_csv)
    survey_rows = []

    for _, row in df_profiles.iterrows():
        patient = row.to_dict()
        most_interested = answer_1_01(patient)
        not_interested = answer_1_02(patient)
        ans_1_03 = answer_1_03(patient, most_interested, not_interested)
        ans_1_04 = answer_1_04(patient)
        ans_1_05 = answer_1_05(patient)
        ans_1_06 = answer_1_06(patient)
        dietary_restrictions = answer_2_02(patient)
        ans_2_01 = answer_2_01(patient)
        meals_resp = answer_2_03(patient)
        ans_2_04 = answer_2_04(patient, meals_resp)
        snacks_resp = answer_2_05(patient)
        ans_2_06 = answer_2_06(patient, snacks_resp)
        eat_out_resp = answer_2_07(patient)
        ans_2_08 = answer_2_08(patient, eat_out_resp)
        protein_track_resp = answer_2_09(patient)
        ans_2_10 = answer_2_10(patient, protein_track_resp)
        protein_amt_resp = answer_2_11(patient, protein_track_resp)
        ans_2_12 = answer_2_12(patient, protein_amt_resp)
        red_meat_resp = answer_2_13(patient, dietary_restrictions)
        ans_2_14 = answer_2_14(patient, red_meat_resp)
        fish_resp = answer_2_15(patient, dietary_restrictions)
        ans_2_16 = answer_2_16(patient, fish_resp)
        plant_protein_resp = answer_2_17(patient, dietary_restrictions)
        ans_2_18 = answer_2_18(patient, plant_protein_resp)
        fv_resp = answer_2_19(patient, dietary_restrictions)
        ans_2_20 = answer_2_20(patient, fv_resp)
        whole_grain_resp = answer_2_21(patient)
        ans_2_22 = answer_2_22(patient, whole_grain_resp)
        legume_resp = answer_2_23(patient)
        ans_2_24 = answer_2_24(patient, legume_resp)
        seed_resp = answer_2_25(patient)
        ans_2_26 = answer_2_26(patient, seed_resp)
        fats_resp = answer_2_27(patient)
        ans_2_28 = answer_2_28(patient, fats_resp)
        water_resp = answer_2_29(patient)
        ans_2_30 = answer_2_30(patient, water_resp)
        caff_resp = answer_2_31(patient)
        ans_2_32 = answer_2_32(patient, caff_resp)
        primary_caff_source = answer_2_33(patient)
        last_caff_time = answer_2_34(patient)
        ans_2_35 = answer_2_35(patient, last_caff_time)
        nutritionist_resp = answer_2_36(patient)
        ans_2_37 = answer_2_37(patient, nutritionist_resp)
        allergies_resp = answer_2_38(patient)
        allergies_which = answer_2_39(patient, allergies_resp)
        meals_desc = answer_2_40(patient)
        dig_issues_resp = answer_2_41(patient)
        dig_which_resp = answer_2_42(patient, dig_issues_resp)
        nut_goals = answer_2_43(patient)           
        nut_goals_ranked = answer_2_44(patient, nut_goals)
        followed_diet_resp = answer_2_45(patient)
        diets_past = answer_2_46(patient, followed_diet_resp)
        diet_goals_when_start = answer_2_47(patient, followed_diet_resp)
        diet_plan_duration = answer_2_48(patient, followed_diet_resp)
        diet_plan_success = answer_2_49(patient, followed_diet_resp)
        never_diet_reasons = answer_2_50(patient, followed_diet_resp)
        considered_diet = answer_2_51(patient, followed_diet_resp)
        willing_diet = answer_2_52(patient, followed_diet_resp, considered_diet)
        factors_prevented = answer_2_53(patient, followed_diet_resp, considered_diet)
        explore_guidelines = answer_2_54(patient, followed_diet_resp, willing_diet)
        diet_changes = answer_2_55(patient)
        future_changes = answer_2_56(patient, diet_changes)
        limiting_reasons = answer_2_57(patient)
        support_needed = answer_2_58(patient)
        track_resp = answer_2_59(patient)
        ans_2_60 = answer_2_60(patient, track_resp)
        ans_2_61 = answer_2_61(patient, track_resp)
        ans_2_62 = answer_2_62(patient, track_resp)
        ans_2_63 = answer_2_63(patient, track_resp)
        ans_2_64 = answer_2_64(patient, track_resp)
        ex_freq_resp = answer_3_01(patient)
        consider_exercise_more = answer_3_02(patient, ex_freq_resp)
        exercise_types = answer_3_03(patient)
        steps_resp = answer_3_21(patient)
        wearable_resp = answer_3_23(patient)
        phys_lim_resp = answer_3_26(patient)
        sleep_protocols_now = answer_4_07(patient)
        willing_to_try = answer_4_08(patient)
        future_protocols = answer_4_09(patient, sleep_protocols_now, willing_to_try)
        sleep_env_comf = answer_4_10(patient)
        sleep_issues = answer_4_12(patient)
        used_sleep_tracker = answer_4_21(patient)
        consider_future_tracker = answer_4_22(patient, used_sleep_tracker)
        currently_using_tracker = answer_4_23(patient, used_sleep_tracker)
        tracker_list = answer_4_24(patient, currently_using_tracker)
        tracker_duration = answer_4_25(patient, tracker_list)
        stopped_reasons = answer_4_26(patient, used_sleep_tracker, currently_using_tracker)
        retry_device = answer_4_27(patient, used_sleep_tracker, currently_using_tracker)
        cognitive_func = answer_5_01(patient)
        cog_concerns = answer_5_02(patient)
        cog_primary_concerns = answer_5_03(patient, cog_concerns)
        cog_change = answer_5_04(patient)
        cog_change_types = answer_5_05(patient, cog_change)
        cog_challenge_freq = answer_5_06(patient)
        cog_challenge_more = answer_5_07(patient, cog_challenge_freq)
        cog_activities = answer_5_08(patient)
        cog_sleep_benefit = answer_5_09(patient)
        cog_exercise_benefit = answer_5_10(patient)
        stress_methods_now = answer_6_07(patient)
        uses_stress_wearable = answer_6_14(patient)
        substances = answer_8_01(patient)
        substance_rowdata = {"8.01": "|".join(substances)}
        substance_rowdata.update(current_use_rowdata(substances))
        substance_rowdata.update(past_use_rowdata(substances))
        past_substances = substance_rowdata["8.20"].split("|") if "8.20" in substance_rowdata else []
        takes_dietary_supps = answer_8_38(patient)
        dietary_supps_list = answer_8_39(patient, takes_dietary_supps)
        consider_dietary_supps = answer_8_40(patient, takes_dietary_supps)
        takes_performance_supps = answer_8_41(patient)
        performance_supps_list = answer_8_42(patient, takes_performance_supps)
        consider_performance_supps = answer_8_43(patient, takes_performance_supps)
        takes_sleep_supps = answer_8_44(patient)
        sleep_aid_freq = answer_8_45(patient, takes_sleep_supps)
        sleep_aid_types = answer_8_46(patient, sleep_aid_freq)
        sleep_nat_supps = answer_8_47(patient, sleep_aid_types)
        consider_sleep_supps = answer_8_48(patient, sleep_aid_freq, sleep_aid_types)
        takes_more = answer_8_49(patient)
        more_supps_list = answer_8_50(patient, takes_more)
        consider_more = answer_8_51(patient, takes_more)
        floss_freq = answer_8_52(patient)
        brush_freq = answer_8_54(patient)
        sunscreen_freq = answer_8_56(patient)
        skincare = answer_8_58(patient)
        family_history_rowdata = answer_family_history()    
        personal_history_rowdata = answer_personal_history()
        named_tests_rowdata = answer_named_tests(patient)
        screenings_rowdata = answer_screenings(patient)
  

        


        row_data = {
            'patient_id': patient.get('patient_id'),
            '1.01': "|".join(most_interested),
            '1.02': "|".join(not_interested),
            '1.03': "|".join(ans_1_03),
            '1.04': "|".join(ans_1_04),
            '1.05': "|".join(ans_1_05),
            '1.06': ans_1_06,
            '2.01': "|".join(ans_2_01),
            '2.02': "|".join(dietary_restrictions),
            '2.03': meals_resp,
            '2.04': ans_2_04,
            '2.05': snacks_resp,
            '2.06': ans_2_06,
            '2.07': eat_out_resp,
            '2.08': ans_2_08,
            '2.09': protein_track_resp,
            '2.10': ans_2_10,
            '2.11': protein_amt_resp,
            '2.12': ans_2_12,
            '2.13': red_meat_resp,
            '2.14': ans_2_14,
            '2.15': fish_resp,
            '2.16': ans_2_16,
            '2.17': plant_protein_resp,
            '2.18': ans_2_18,
            '2.19': fv_resp,
            '2.20': ans_2_20,
            '2.21': whole_grain_resp,
            '2.22': ans_2_22,
            '2.23': legume_resp,
            '2.24': ans_2_24,
            '2.25': seed_resp,
            '2.26': ans_2_26,
            '2.27': fats_resp,
            '2.28': ans_2_28,
            '2.29': water_resp,
            '2.30': ans_2_30,
            '2.31': caff_resp,
            '2.32': ans_2_32,
            '2.33': primary_caff_source,
            '2.34': last_caff_time,
            '2.35': ans_2_35,
            '2.36': nutritionist_resp,
            '2.37': ans_2_37,
            '2.38': allergies_resp,
            '2.39': "|".join(allergies_which),
            '2.40': meals_desc,
            '2.41': dig_issues_resp,
            '2.42': "|".join(dig_which_resp),
            '2.43': "|".join(nut_goals),
            '2.44': "|".join(nut_goals_ranked),
            '2.45': followed_diet_resp,
            '2.46': "|".join(diets_past),
            '2.47': "|".join(diet_goals_when_start),
            '2.48': diet_plan_duration,
            '2.49': diet_plan_success,
            '2.50': "|".join(never_diet_reasons),
            '2.51': considered_diet,
            '2.52': willing_diet,
            '2.53': "|".join(factors_prevented),
            '2.54': "|".join(explore_guidelines),
            '2.55': "|".join(diet_changes),
            '2.56': "|".join(future_changes),
            '2.57': "|".join(limiting_reasons),
            '2.58': "|".join(support_needed),
            '2.59': track_resp,
            '2.60': "|".join(ans_2_60),
            '2.61': ans_2_61,
            '2.62': ans_2_62,
            '2.63': "|".join(ans_2_63),
            '2.64': "|".join(ans_2_64),
            '3.01': ex_freq_resp,
            '3.02': consider_exercise_more,
            '3.03': "|".join(exercise_types),
            '3.04': exercise_type_frequency(patient, exercise_types, "Cardio (e.g. running and cycling)", cardio_freq_weights),
            '3.05': exercise_type_frequency(patient, exercise_types, "Strength training (e.g. weight lifting)", strength_freq_weights),
            '3.06': exercise_type_frequency(patient, exercise_types, "Flexibility/mobility (e.g. yoga, stretching)", flex_freq_weights),
            '3.07': exercise_type_frequency(patient, exercise_types, "High-intensity interval training (HIIT)", hiit_freq_weights),
            '3.08': exercise_type_duration(patient, exercise_types, "Cardio (e.g. running and cycling)", cardio_dur_weights),
            '3.09': exercise_type_duration(patient, exercise_types, "Strength training (e.g. weight lifting)", strength_dur_weights),
            '3.10': exercise_type_duration(patient, exercise_types, "Flexibility/mobility (e.g. yoga, stretching)", flex_dur_weights),
            '3.11': exercise_type_duration(patient, exercise_types, "High-intensity interval training (HIIT)", hiit_dur_weights),
            '3.12': answer_3_12(patient, exercise_types),
            '3.13': answer_3_13(patient, exercise_types),
            '3.14': answer_3_14(patient, exercise_types),
            '3.15': answer_3_15(patient, exercise_types),
            '3.16': answer_3_16(patient, exercise_types),
            '3.17': answer_3_17(patient, exercise_types),
            '3.18': answer_3_18(patient, exercise_types),
            '3.19': answer_3_19(patient, exercise_types),
            '3.20': answer_3_20(patient, exercise_types),
            '3.21': steps_resp,
            '3.22': answer_3_22(patient, steps_resp),
            '3.23': wearable_resp,
            '3.24': "|".join(answer_3_24(patient, wearable_resp)),
            '3.25': answer_3_25(patient, wearable_resp),
            '3.26': phys_lim_resp,
            '3.27': answer_3_27(patient, phys_lim_resp),
            '4.01': answer_4_01(patient),
            '4.02': answer_4_02(patient),
            '4.03': answer_4_03(patient),
            '4.04': answer_4_04(patient),
            '4.05': answer_4_05(patient),
            '4.06': "|".join(answer_4_06(patient)),
            '4.07': "|".join(sleep_protocols_now),
            '4.08': willing_to_try,
            '4.09': "|".join(future_protocols),
            '4.10': sleep_env_comf,
            '4.11': "|".join(answer_4_11(patient, sleep_env_comf)),
            '4.12': "|".join(sleep_issues),
            '4.13': sleep_issue_frequency(patient, "Difficulty falling asleep" in sleep_issues),
            '4.14': sleep_issue_frequency(patient, "Difficulty staying asleep" in sleep_issues),
            '4.15': sleep_issue_frequency(patient, "Waking up too early" in sleep_issues),
            '4.16': sleep_issue_frequency(patient, "Frequent nightmares" in sleep_issues),
            '4.17': sleep_issue_frequency(patient, "Restless legs" in sleep_issues),
            '4.18': sleep_issue_frequency(patient, "Snoring" in sleep_issues),
            '4.19': sleep_issue_frequency(patient, "Sleep apnea" in sleep_issues),
            '4.20': sleep_issue_frequency(patient, "Other (please specify)" in sleep_issues),
            '4.21': used_sleep_tracker,
            '4.22': consider_future_tracker,
            '4.23': currently_using_tracker,
            '4.24': "|".join(tracker_list),
            '4.25': tracker_duration,
            '4.26': stopped_reasons,
            '4.27': retry_device,
            '5.01': cognitive_func,
            '5.02': cog_concerns,
            '5.03': "|".join(cog_primary_concerns),
            '5.04': cog_change,
            '5.05': "|".join(cog_change_types),
            '5.06': cog_challenge_freq,
            '5.07': cog_challenge_more,
            '5.08': "|".join(cog_activities),
            '5.09': cog_sleep_benefit,
            '5.10': cog_exercise_benefit,
            '5.11': "|".join(answer_5_11(patient)),
            '5.12': "|".join(answer_5_12(patient)),
            '6.01': answer_6_01(patient),
            '6.02': answer_6_02(patient),
            '6.03': "|".join(answer_6_03(patient)),
            '6.04': "|".join(answer_6_04(patient)),
            '6.05': "|".join(answer_6_05(patient)),
            '6.06': "|".join(answer_6_06(patient)),
            '6.07': "|".join(stress_methods_now),
            '6.08': "|".join(answer_6_08(patient, stress_methods_now)),
            '6.09': answer_6_09(patient),
            '6.10': answer_6_10(patient),
            '6.11': answer_6_11(patient),
            '6.12': "|".join(answer_6_12(patient)),
            '6.13': "|".join(answer_6_13(patient)),
            '6.14': uses_stress_wearable,
            '6.15': "|".join(answer_6_15(patient, uses_stress_wearable)),
            '6.16': answer_6_16(patient,uses_stress_wearable),
            '7.01': answer_7_01(patient),
            '7.02': answer_7_02(patient),
            '7.03': "|".join(answer_7_03(patient)),
            '7.04': answer_7_04(patient),
            '7.05': answer_7_05(patient),
            '7.06': "|".join(answer_7_06(patient)),
            '7.07': answer_7_07(patient),
            '7.08': "|".join(answer_7_08(patient)),
            '7.09': answer_7_09(patient),
            '7.10': answer_7_10(patient),
            **substance_rowdata,
            '8.33': "|".join(answer_8_33(patient, substances, past_substances)),
            '8.34': "|".join(answer_8_34(patient, substances)),
            '8.35': answer_8_35(patient, substances),
            '8.36': "|".join(answer_8_36(patient, substances)),
            '8.37': answer_8_37(patient, substances),
            '8.38': takes_dietary_supps,
            '8.39': dietary_supps_list,
            '8.40': consider_dietary_supps,
            '8.41': takes_performance_supps,
            '8.42': performance_supps_list,
            '8.43': consider_performance_supps,
            '8.44': takes_sleep_supps,
            '8.45': sleep_aid_freq,
            '8.46': "|".join(sleep_aid_types),
            '8.47': "|".join(sleep_nat_supps),
            '8.48': consider_sleep_supps,
            '8.49': takes_more,
            '8.50': more_supps_list,
            '8.51': consider_more,
            '8.52': floss_freq,
            '8.53': answer_8_53(patient, floss_freq),
            '8.54': brush_freq,
            '8.55': answer_8_55(patient, brush_freq),
            '8.56': sunscreen_freq,
            '8.57': answer_8_57(patient, sunscreen_freq),
            '8.58': skincare,
            '8.59': answer_8_59(patient, skincare),
            '10.09': answer_10_09(patient),
            '10.10': answer_10_10(patient),
            '10.11': answer_10_11(patient),
            '10.12': answer_10_12(patient),
            **family_history_rowdata,
            **personal_history_rowdata,
            **named_tests_rowdata,
            **screenings_rowdata


        }

        survey_rows.append(row_data)

    pd.DataFrame(survey_rows).to_csv(out_csv, index=False, encoding="utf-8")
    print(f"✅ Survey responses generated for {len(survey_rows)} patients → {out_csv}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    profile_csv = os.path.join(base_dir, "data", "dummy_lab_results_full.csv")
    out_csv = os.path.join(base_dir, "data", "synthetic_patient_survey.csv")
    
    generate_survey_responses(
        profile_csv=profile_csv,
        out_csv=out_csv,
        seed=42
    )


