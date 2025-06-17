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
    # No other fields! Do NOT add extras!
    return sorted(set(choices))

def answer_1_03(patient, most_interested, not_interested):
    """Please rank your selected focus areas in order of personal importance."""
    # Prioritize 'problem' areas, fill in rest, preserve order
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

def answer_2_03(patient, meals_resp):
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

def answer_2_04(patient):
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

def answer_2_05(patient, snacks_resp):
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

def answer_2_06(patient):
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

def answer_2_07(patient, eat_out_resp):
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

def answer_2_08(patient):
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

def answer_2_09(patient, protein_track_resp):
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

def answer_2_10(patient):
    """How many grams of protein do you typically consume per day?"""
    dq = patient.get('diet_quality', 'moderate')
    options = [
        "0.8-1.0g/lb",
        "<0.4g/lb",
        "0.4-0.6g/lb"
    ]
    if dq == 'good':
        weights = [1, 0, 0]
    elif dq == 'poor':
        weights = [0, 1, 0]
    else:
        weights = [0, 0, 1]
    return random.choices(options, weights=weights)[0]

def answer_2_11(patient, protein_amt_resp):
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


def answer_2_12(patient):
    """How often do you consume processed or red meat?"""
    dq = patient.get('diet_quality', 'moderate')
    options = [
        "Rarely or Never",
        "1-2 times per week",
        "3-4 times per week",
        "5 or more times per week"
    ]
    if dq == 'good':
        weights = [0.9, 0.1, 0, 0]
    elif dq == 'poor':
        weights = [0, 0, 0.7, 0.3]
    else:
        weights = [0.1, 0.7, 0.15, 0.05]
    return random.choices(options, weights=weights)[0]

def answer_2_13(patient, red_meat_resp):
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

def answer_2_14(patient):
    """How often do you eat fatty fish (e.g., salmon, sardines, mackerel) rich in omega-3s?"""
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

def answer_2_15(patient, fish_resp):
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

def answer_2_16(patient):
    """How much of your protein comes from plant-based sources in a typical week?"""
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

def answer_2_17(patient, plant_protein_resp):
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

def answer_2_18(patient):
    """How many servings of fruits and vegetables do you consume daily?"""
    options = ["0", "1-2", "3-4", "5 or more"]
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        weights = [0.01, 0.09, 0.4, 0.5]
    elif dq == 'poor':
        weights = [0.18, 0.52, 0.24, 0.06]
    else:
        weights = [0.05, 0.25, 0.4, 0.3]
    return random.choices(options, weights=weights)[0]

def answer_2_19(patient, fv_resp):
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

def answer_2_20(patient):
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

def answer_2_21(patient, whole_grain_resp):
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

def answer_2_22(patient):
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

def answer_2_23(patient, legume_resp):
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

def answer_2_24(patient):
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

def answer_2_25(patient, seed_resp):
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

def answer_2_26(patient):
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

def answer_2_27(patient, fats_resp):
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

def answer_2_28(patient):
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

def answer_2_29(patient, water_resp):
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

def answer_2_30(patient):
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

def answer_2_31(patient, caff_resp):
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

def answer_2_32(patient):
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

def answer_2_33(patient, last_caff_time):
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

def answer_2_34(patient):
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

def answer_2_35(patient, worked_with_nutritionist):
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

def answer_2_36(patient):
    """Do you have any food allergies or intolerances?"""
    options = ["Yes", "No"]
    weights = [0.35, 0.65]
    return random.choices(options, weights=weights)[0]  # returns "Yes" or "No" as string

def answer_2_37(patient, has_allergy):
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

def answer_2_38(patient):
    """Please describe your typical breakfast, lunch, and dinner, as well as the types of snacks consumed regularly"""
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        return ["Breakfast: oatmeal and fruit. Lunch: salad with lean protein. Dinner: vegetables and whole grains. Snacks: nuts, fruit."]
    elif dq == 'poor':
        return ["Breakfast: pastries or skip. Lunch: fast food or processed meal. Dinner: takeout or frozen. Snacks: chips, sweets."]
    else:
        return ["Breakfast: eggs or cereal. Lunch: sandwich or bowl. Dinner: mixed plate. Snacks: crackers, granola bars."]

def answer_2_39(patient):
    """Do you experience any digestive issues?"""
    return [random.choices(["Yes", "No"], weights=[0.3, 0.7])[0]]

def answer_2_40(patient, has_digestive_issues):
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

def answer_2_41(patient):
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

def answer_2_42(patient, goals):
    """Please rank your diet and nutrition goals in order of importance."""
    if not goals or len(goals) < 2:
        return []
    return random.sample(goals, k=len(goals))  

def answer_2_43(patient):
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

def answer_2_44(patient, followed_diet):
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

def answer_2_45(patient, followed_diet):
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

def answer_2_46(patient, followed_diet):
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

def answer_2_47(patient, followed_diet):
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


def answer_2_48(patient, followed_diet):
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

def answer_2_49(patient, followed_diet):
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

def answer_2_50(patient, followed_diet, considered_plan):
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

def answer_2_51(patient, followed_diet, considered_plan):
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

def answer_2_52(patient, followed_diet, considered_plan):
    """Which of the following dietary guidelines or principles would you be interested in exploring? (multi-select)"""
    if followed_diet != "No" or considered_plan != "Yes":
        return []
    options = [
        "Whole Food Plant-Based Diet", "Mediterranean Diet", "High-Protein Diet",
        "Low-Carb Diet (e.g., keto, Atkins)", "Vegetarian Diet", "Vegan Diet",
        "Intermittent Fasting", "Other (please specify)"
    ]
    return random.sample(options, k=random.randint(1, 4))

def answer_2_53(patient):
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

def answer_2_54(patient, changes_made):
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

def answer_2_55(patient):
    """Which of the following reasons, if any, do you feel have limited your ability to make sustainable dietary changes? (multi-select)"""
    stress = patient.get("stress_level", 5)
    busy = patient.get("busy", False)  # Added: to avoid NameError if not present
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
    if stress > 6:
        weighted_options.append("Stress or emotional eating")
    if busy:
        weighted_options.append("Lack of time to prepare meals")
    return random.sample(weighted_options, k=random.randint(2, 4))

def answer_2_56(patient):
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

def answer_2_57(patient):
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

def answer_2_58(patient, track_response):
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

def answer_2_59(patient, track_response):
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

def answer_2_60(patient, track_response):
    """How many calories do you typically consume per day?"""
    if track_response not in [
        "Yes",
        "No, but I'm generally aware of how many calories I consume each day"
    ]:
        return ""
    dq = patient.get("diet_quality", "moderate")
    options = ["<1,000", "1,000-1,500", "1,500-2,000", "2,000-2,500", "2,500-3,000", ">3,000"]
    if dq == "good":
        weights = [0.01, 0.05, 0.25, 0.4, 0.2, 0.09]
    elif dq == "poor":
        weights = [0.15, 0.3, 0.3, 0.15, 0.08, 0.02]
    else:
        weights = [0.1, 0.2, 0.3, 0.3, 0.07, 0.03]
    return random.choices(options, weights=weights)[0]

def answer_2_61(patient, track_response):
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

def answer_2_62(patient, track_response):
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
        "Sports (e.g. golf, tennis)",
        "Other (please specify)",
        "None"
    ]
    if fitness == "high":
        return random.sample(options[:-1], k=random.randint(2, 4))
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
        "Occasionally (1–2 times per week)",
        "Regularly (3–4 times per week)",
        "Frequently (5 or more times per week)"
    ]
    weights = weights_map.get(fitness, [0.3, 0.4, 0.3])
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
    "high": [0.1, 0.3, 0.6],
    "moderate": [0.3, 0.5, 0.2],
    "low": [0.7, 0.2, 0.1]
}
strength_freq_weights = {
    "high": [0.2, 0.3, 0.5],
    "moderate": [0.4, 0.4, 0.2],
    "low": [0.6, 0.3, 0.1]
}
flex_freq_weights = {
    "high": [0.3, 0.5, 0.2],
    "moderate": [0.5, 0.4, 0.1],
    "low": [0.7, 0.2, 0.1]
}
hiit_freq_weights = {
    "high": [0.3, 0.4, 0.3],
    "moderate": [0.5, 0.4, 0.1],
    "low": [0.8, 0.15, 0.05]
}
sports_freq_weights = {
    "high": [0.2, 0.5, 0.3],
    "moderate": [0.6, 0.3, 0.1],
    "low": [0.8, 0.15, 0.05]
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
sports_dur_weights = {
    "high": [0.05, 0.35, 0.4, 0.2],
    "moderate": [0.3, 0.5, 0.15, 0.05],
    "low": [0.75, 0.2, 0.04, 0.01]
}

def answer_3_14(patient, exercise_types):
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

def answer_3_15(patient, exercise_types):
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

def answer_3_16(patient, exercise_types):
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

def answer_3_17(patient, exercise_types):
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

def answer_3_18(patient, exercise_types):
    """Would you consider adding cardio training in support of your longevity goals?"""
    if "Cardio (e.g. running and cycling)" in exercise_types:
        return ""
    options = [
        "Yes",
        "Maybe",
        "No"
    ]
    return random.choice(options)

def answer_3_19(patient, exercise_types):
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

def answer_3_20(patient, exercise_types):
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

def answer_3_21(patient, exercise_types):
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

def answer_3_22(patient, exercise_types):
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

def answer_3_23(patient):
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

def answer_3_24(patient, steps_resp):
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

def answer_3_25(patient):
    """Do you use a wearable device to track steps and/or daily activity?"""
    # 70% chance "Yes", 30% "No"
    return random.choices(["Yes", "No"], weights=[0.7, 0.3])[0]

def answer_3_26(patient, wearable_resp):
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

def answer_3_27(patient, wearable_resp):
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

def answer_3_28(patient):
    """Do you have any physical restrictions or limitations that affect your physical activity choices?"""
    fitness = patient.get("fitness_level", "moderate")
    if fitness == "high":
        weights = [0.1, 0.9]  
    elif fitness == "low":
        weights = [0.5, 0.5]
    else:  
        weights = [0.25, 0.75]
    return random.choices(["Yes", "No"], weights=weights)[0]

def answer_3_29(patient, phys_lim_resp):
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


# ====================
# MAIN DRIVER AND ENTRYPOINT
# ====================

def generate_survey_responses(profile_csv, out_csv="synthetic_patient_survey.csv", seed=42):
    import random, pandas as pd
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
        ans_2_01 = answer_2_01(patient)
        meals_resp = answer_2_02(patient)
        ans_2_03 = answer_2_03(patient, meals_resp)
        snacks_resp = answer_2_04(patient)
        ans_2_05 = answer_2_05(patient, snacks_resp)
        eat_out_resp = answer_2_06(patient)
        ans_2_07 = answer_2_07(patient, eat_out_resp)
        protein_track_resp = answer_2_08(patient)
        ans_2_09 = answer_2_09(patient, protein_track_resp)
        protein_amt_resp = answer_2_10(patient)
        ans_2_11 = answer_2_11(patient, protein_amt_resp)
        red_meat_resp = answer_2_12(patient)
        ans_2_13 = answer_2_13(patient, red_meat_resp)
        fish_resp = answer_2_14(patient)
        ans_2_15 = answer_2_15(patient, fish_resp)
        plant_protein_resp = answer_2_16(patient)
        ans_2_17 = answer_2_17(patient, plant_protein_resp)
        fv_resp = answer_2_18(patient)
        ans_2_19 = answer_2_19(patient, fv_resp)
        whole_grain_resp = answer_2_20(patient)
        ans_2_21 = answer_2_21(patient, whole_grain_resp)
        legume_resp = answer_2_22(patient)
        ans_2_23 = answer_2_23(patient, legume_resp)
        seed_resp = answer_2_24(patient)
        ans_2_25 = answer_2_25(patient, seed_resp)
        fats_resp = answer_2_26(patient)
        ans_2_27 = answer_2_27(patient, fats_resp)
        water_resp = answer_2_28(patient)
        ans_2_29 = answer_2_29(patient, water_resp)
        caff_resp = answer_2_30(patient)
        ans_2_31 = answer_2_31(patient, caff_resp)
        last_caff_time = answer_2_32(patient)
        ans_2_33 = answer_2_33(patient, last_caff_time)
        nutritionist_resp = answer_2_34(patient)
        ans_2_35 = answer_2_35(patient, nutritionist_resp)
        allergies_resp = answer_2_36(patient)
        allergies_which = answer_2_37(patient, allergies_resp)
        meals_desc = answer_2_38(patient)
        dig_issues_resp = answer_2_39(patient)
        dig_which_resp = answer_2_40(patient, dig_issues_resp)
        nut_goals = answer_2_41(patient)           
        nut_goals_ranked = answer_2_42(patient, nut_goals)
        followed_diet_resp = answer_2_43(patient)
        diets_past = answer_2_44(patient, followed_diet_resp)
        diet_goals_when_start = answer_2_45(patient, followed_diet_resp)
        diet_plan_duration = answer_2_46(patient, followed_diet_resp)
        diet_plan_success = answer_2_47(patient, followed_diet_resp)
        never_diet_reasons = answer_2_48(patient, followed_diet_resp)
        considered_diet = answer_2_49(patient, followed_diet_resp)
        willing_diet = answer_2_50(patient, followed_diet_resp, considered_diet)
        factors_prevented = answer_2_51(patient, followed_diet_resp, considered_diet)
        explore_guidelines = answer_2_52(patient, followed_diet_resp, willing_diet)
        diet_changes = answer_2_53(patient)
        future_changes = answer_2_54(patient, diet_changes)
        limiting_reasons = answer_2_55(patient)
        support_needed = answer_2_56(patient)
        track_resp = answer_2_57(patient)
        ans_2_58 = answer_2_58(patient, track_resp)
        ans_2_59 = answer_2_59(patient, track_resp)
        ans_2_60 = answer_2_60(patient, track_resp)
        ans_2_61 = answer_2_61(patient, track_resp)
        ans_2_62 = answer_2_62(patient, track_resp)
        ex_freq_resp = answer_3_01(patient)
        consider_exercise_more = answer_3_02(patient, ex_freq_resp)
        exercise_types = answer_3_03(patient)
        steps_resp = answer_3_23(patient)
        wearable_resp = answer_3_25(patient)
        phys_lim_resp = answer_3_28(patient)
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


        row_data = {
            'patient_id': patient.get('patient_id'),
            '1.01': "|".join(most_interested),
            '1.02': "|".join(not_interested),
            '1.03': "|".join(ans_1_03),
            '1.04': "|".join(ans_1_04),
            '1.05': "|".join(ans_1_05),
            '1.06': ans_1_06,
            '2.01': "|".join(ans_2_01),
            '2.02': meals_resp,
            '2.03': ans_2_03,
            '2.04': snacks_resp,
            '2.05': ans_2_05,
            '2.06': eat_out_resp,
            '2.07': ans_2_07,
            '2.08': protein_track_resp,
            '2.09': ans_2_09,
            '2.10': protein_amt_resp,
            '2.11': ans_2_11,
            '2.12': red_meat_resp,
            '2.13': ans_2_13,
            '2.14': fish_resp,
            '2.15': ans_2_15,
            '2.16': plant_protein_resp,
            '2.17': ans_2_17,
            '2.18': fv_resp,
            '2.19': ans_2_19,
            '2.20': whole_grain_resp,
            '2.21': ans_2_21,
            '2.22': legume_resp,
            '2.23': ans_2_23,
            '2.24': seed_resp,
            '2.25': ans_2_25,
            '2.26': fats_resp,
            '2.27': ans_2_27,
            '2.28': water_resp,
            '2.29': ans_2_29,
            '2.30': caff_resp,
            '2.31': ans_2_31,
            '2.32': last_caff_time,
            '2.33': ans_2_33,
            '2.34': nutritionist_resp,
            '2.35': ans_2_35,
            '2.36': allergies_resp,
            '2.37': "|".join(allergies_which),
            '2.38': meals_desc,
            '2.39': dig_issues_resp,
            '2.40': "|".join(dig_which_resp),
            '2.41': "|".join(nut_goals),
            '2.42': "|".join(nut_goals_ranked),
            '2.43': followed_diet_resp,
            '2.44': "|".join(diets_past),
            '2.45': "|".join(diet_goals_when_start),
            '2.46': diet_plan_duration,
            '2.47': diet_plan_success,
            '2.48': "|".join(never_diet_reasons),
            '2.49': considered_diet,
            '2.50': willing_diet,
            '2.51': "|".join(factors_prevented),
            '2.52': "|".join(explore_guidelines),
            '2.53': "|".join(diet_changes),
            '2.54': "|".join(future_changes),
            '2.55': "|".join(limiting_reasons),
            '2.56': "|".join(support_needed),
            '2.57': track_resp,
            '2.58': "|".join(ans_2_58),
            '2.59': ans_2_59,
            '2.60': ans_2_60,
            '2.61': "|".join(ans_2_61),
            '2.62': "|".join(ans_2_62),
            '3.01': ex_freq_resp,
            '3.02': consider_exercise_more,
            '3.03': "|".join(exercise_types),
            '3.04': exercise_type_frequency(patient, exercise_types, "Cardio (e.g. running and cycling)", cardio_freq_weights),
            '3.05': exercise_type_frequency(patient, exercise_types, "Strength training (e.g. weight lifting)", strength_freq_weights),
            '3.06': exercise_type_frequency(patient, exercise_types, "Flexibility/mobility (e.g. yoga, stretching)", flex_freq_weights),
            '3.07': exercise_type_frequency(patient, exercise_types, "High-intensity interval training (HIIT)", hiit_freq_weights),
            '3.08': exercise_type_frequency(patient, exercise_types, "Sports (e.g. golf, tennis)", sports_freq_weights),
            '3.09': exercise_type_duration(patient, exercise_types, "Cardio (e.g. running and cycling)", cardio_dur_weights),
            '3.10': exercise_type_duration(patient, exercise_types, "Strength training (e.g. weight lifting)", strength_dur_weights),
            '3.11': exercise_type_duration(patient, exercise_types, "Flexibility/mobility (e.g. yoga, stretching)", flex_dur_weights),
            '3.12': exercise_type_duration(patient, exercise_types, "High-intensity interval training (HIIT)", hiit_dur_weights),
            '3.13': exercise_type_duration(patient, exercise_types, "Sports (e.g. golf, tennis)", sports_dur_weights),
            '3.14': answer_3_14(patient, exercise_types),
            '3.15': answer_3_15(patient, exercise_types),
            '3.16': answer_3_16(patient, exercise_types),
            '3.17': answer_3_17(patient, exercise_types),
            '3.18': answer_3_18(patient, exercise_types),
            '3.19': answer_3_19(patient, exercise_types),
            '3.20': answer_3_20(patient, exercise_types),
            '3.21': answer_3_21(patient, exercise_types),
            '3.22': answer_3_22(patient, exercise_types),
            '3.23': steps_resp,
            '3.24': answer_3_24(patient, steps_resp),
            '3.25': wearable_resp,
            '3.26': "|".join(answer_3_26(patient, wearable_resp)),
            '3.27': answer_3_27(patient, wearable_resp),
            '3.28': phys_lim_resp,
            '3.29': answer_3_29(patient, phys_lim_resp),
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

        }

        survey_rows.append(row_data)

    pd.DataFrame(survey_rows).to_csv(out_csv, index=False)
    print(f"✅ Survey responses generated for {len(survey_rows)} patients → {out_csv}")


if __name__ == "__main__":
    # Edit the CSV below to your real profile/patient/lab file path!
    generate_survey_responses(
        profile_csv="data/dummy_lab_results_full.csv",
        out_csv="synthetic_patient_survey.csv",
        seed=42
    )
