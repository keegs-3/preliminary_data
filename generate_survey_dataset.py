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
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        return ["Very healthy"]
    if dq == 'poor':
        return ["Unhealthy"]
    return ["Moderately healthy"]

def answer_2_02(patient):
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        return ["3"]
    if dq == 'poor':
        return [random.choices(["≤1", "2"], weights=[0.7, 0.3])[0]]
    return ["2"]

def answer_2_03(patient, meals_resp):
    # Only shown if meals_resp in ["≤1", "2"]
    if meals_resp not in ["≤1", "2"]:
        return []
    return [random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])]

def answer_2_04(patient):
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        return ["1"]
    if dq == 'poor':
        return [random.choices(["2", "3", "4 or more"], weights=[0.3, 0.5, 0.2])[0]]
    return ["2"]

def answer_2_05(patient, snacks_resp):
    # Only shown if snacks_resp in ["3", "4 or more"]
    if snacks_resp not in ["3", "4 or more"]:
        return []
    return [random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])]

def answer_2_06(patient):
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        return ["Rarely"]
    if dq == 'poor':
        return [random.choices(["Several times a week", "Daily"], weights=[0.7, 0.3])[0]]
    return ["Once a week"]

def answer_2_07(patient, eat_out_resp):
    # Only shown if eat_out_resp in ["Daily", "Several times a week"]
    if eat_out_resp not in ["Daily", "Several times a week"]:
        return []
    return [random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])]

def answer_2_08(patient):
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        return ["Yes"]
    if dq == 'poor':
        return ["No"]
    return ["No, but I'm Generally Aware"]

def answer_2_09(patient, protein_track_resp):
    # Only shown if protein_track_resp != "Yes"
    if protein_track_resp == "Yes":
        return []
    return [random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])]

def answer_2_10(patient):
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        return ["0.8-1.0g/lb"]
    if dq == 'poor':
        return ["<0.4g/lb"]
    return ["0.4-0.6g/lb"]

def answer_2_11(patient, protein_amt_resp):
    # Only shown if protein_amt_resp in ["<0.4g/lb", "0.4-0.6g/lb", "≥1.0g/lb"]
    if protein_amt_resp not in ["<0.4g/lb", "0.4-0.6g/lb", "≥1.0g/lb"]:
        return []
    return [random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])]

def answer_2_12(patient):
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        return ["Rarely or Never"]
    if dq == 'poor':
        return [random.choices(["3-4 times per week", "5 or more times per week"], weights=[0.7, 0.3])[0]]
    return ["1-2 times per week"]

def answer_2_13(patient, red_meat_resp):
    # Only shown if red_meat_resp in ["3-4 times per week", "5 or more times per week"]
    if red_meat_resp not in ["3-4 times per week", "5 or more times per week"]:
        return []
    return [random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])]

def answer_2_14(patient):
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        return [random.choice([
            "3-4 times per week",
            "5 or more times per week"
        ])]
    if dq == 'poor':
        return ["Rarely or Never"]
    return ["1-2 times per week"]

def answer_2_15(patient, fish_resp):
    # Only shown if fish_resp in ["Rarely or Never", "Less than once a week"]
    if fish_resp not in ["Rarely or Never", "Less than once a week"]:
        return []
    return [random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])]


def answer_2_16(patient):
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
    return [random.choices(options, weights=weights)[0]]

def answer_2_17(patient, plant_protein_resp):
    # Only shown if plant_protein_resp in ["Almost none - all animal-based", "A small portion - mostly animal-based"]
    if plant_protein_resp not in ["Almost none - all animal-based", "A small portion - mostly animal-based"]:
        return []
    return [random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])]

def answer_2_18(patient):
    options = ["0", "1-2", "3-4", "5 or more"]
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        weights = [0.01, 0.09, 0.4, 0.5]
    elif dq == 'poor':
        weights = [0.18, 0.52, 0.24, 0.06]
    else:
        weights = [0.05, 0.25, 0.4, 0.3]
    return [random.choices(options, weights=weights)[0]]

def answer_2_19(patient, fv_resp):
    # Only shown if fv_resp in ["0", "1-2"]
    if fv_resp not in ["0", "1-2"]:
        return []
    return [random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])]

def answer_2_20(patient):
    options = ["Rarely or never", "Once a week", "Several times a week", "Daily"]
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        weights = [0.02, 0.08, 0.35, 0.55]
    elif dq == 'poor':
        weights = [0.56, 0.22, 0.16, 0.06]
    else:
        weights = [0.2, 0.2, 0.45, 0.15]
    return [random.choices(options, weights=weights)[0]]

def answer_2_21(patient, whole_grain_resp):
    # Only shown if whole_grain_resp in ["Rarely or never", "Once a week"]
    if whole_grain_resp not in ["Rarely or never", "Once a week"]:
        return []
    return [random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])]

def answer_2_22(patient):
    options = ["Rarely or never", "Once a week", "Several times a week", "Daily"]
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        weights = [0.04, 0.11, 0.3, 0.55]
    elif dq == 'poor':
        weights = [0.55, 0.25, 0.15, 0.05]
    else:
        weights = [0.2, 0.25, 0.45, 0.1]
    return [random.choices(options, weights=weights)[0]]

def answer_2_23(patient, legume_resp):
    # Only shown if legume_resp in ["Rarely or never", "Once a week"]
    if legume_resp not in ["Rarely or never", "Once a week"]:
        return []
    return [random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])]

def answer_2_24(patient):
    options = ["Rarely or never", "Once a week", "Several times a week", "Daily"]
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        weights = [0.05, 0.15, 0.35, 0.45]
    elif dq == 'poor':
        weights = [0.5, 0.25, 0.2, 0.05]
    else:
        weights = [0.4, 0.2, 0.3, 0.1]
    return [random.choices(options, weights=weights)[0]]

def answer_2_25(patient, seed_resp):
    # Only shown if seed_resp in ["Rarely or never", "Once a week"]
    if seed_resp not in ["Rarely or never", "Once a week"]:
        return []
    return [random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])]

def answer_2_26(patient):
    options = ["Rarely or never", "Once a week", "Several times a week", "Daily"]
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        weights = [0.03, 0.12, 0.35, 0.5]
    elif dq == 'poor':
        weights = [0.55, 0.2, 0.2, 0.05]
    else:
        weights = [0.1, 0.2, 0.5, 0.2]
    return [random.choices(options, weights=weights)[0]]


def answer_2_27(patient, fats_resp):
    # Only shown if fats_resp in ["Rarely or never", "Once a week"]
    if fats_resp not in ["Rarely or never", "Once a week"]:
        return []
    return [random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])]

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
    return [random.choices(options, weights=weights)[0]]

def answer_2_29(patient, water_resp):
    """Would you consider increasing your daily water intake in the future in support of your longevity goals?"""
    if water_resp not in [
        "Less than 1 liter (34 oz)",
        "1-2 liters (34-68 oz)"
    ]:
        return []
    return [random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])]

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
        weights = [0.25, 0.35, 0.3, 0.08, 0.02]
    else:
        weights = [0.15, 0.2, 0.35, 0.22, 0.08]
    return [random.choices(options, weights=weights)[0]]

def answer_2_31(patient, caff_resp):
    """Would you be open to adjusting your caffeine intake in the future in support of your longevity goals?"""
    if caff_resp not in [
        "201–400 mg (3–4 cups or energy drink)",
        ">400 mg (5+ cups, strong pre-workouts, etc.)"
    ]:
        return []
    return [random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])]

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
    except:
        sleep_score = 7.0

    if sleep_score >= 8:
        weights = [0.4, 0.3, 0.2, 0.07, 0.03]
    elif sleep_score <= 5:
        weights = [0.05, 0.15, 0.25, 0.3, 0.25]
    else:
        weights = [0.1, 0.2, 0.3, 0.25, 0.15]

    return [random.choices(options, weights=weights)[0]]

def answer_2_33(patient, last_caff_time):
    """Would you consider having your last caffeinated drink earlier in support of your longevity goals?"""
    if last_caff_time not in ["4:00–6:00 PM", "After 6:00 PM"]:
        return []
    return [random.choice([
        "Yes - actively working on it",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])]

def answer_2_34(patient):
    """Have you ever worked with a nutritionist or dietitian?"""
    dq = patient.get('diet_quality', 'moderate')
    if dq == 'good':
        weights = [0.7, 0.3]
    elif dq == 'poor':
        weights = [0.25, 0.75]
    else:
        weights = [0.5, 0.5]
    return [random.choices(["Yes", "No"], weights=weights)[0]]

def answer_2_35(patient, worked_with_nutritionist):
    """Would you consider working with a nutritionist or dietitian in the future in support of your longevity goals?"""
    if worked_with_nutritionist != "No":
        return []
    return [random.choice([
        "Yes - actively seeking one now",
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])]

def answer_2_36(patient):
    """Do you have any food allergies or intolerances?"""
    return [random.choices(["Yes", "No"], weights=[0.35, 0.65])[0]]

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
    return random.sample(goals, k=len(goals))  # shuffled ranking

def answer_2_43(patient):
    """Have you ever followed a specific diet plan for health or weight management purposes?"""
    dq = patient.get("diet_quality", "moderate")
    if dq == "good":
        weights = [0.8, 0.2]
    elif dq == "poor":
        weights = [0.3, 0.7]
    else:
        weights = [0.6, 0.4]
    return [random.choices(["Yes", "No"], weights=weights)[0]]

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
        return []
    score = patient.get("diet_adherence", 0.5)  # fallback
    options = [
        "Less than 1 month", "1-3 months", "4-6 months",
        "7-12 months", "More than 1 year"
    ]
    weights = [0.25, 0.25, 0.2, 0.15, 0.15] if score < 0.4 else [0.05, 0.15, 0.2, 0.3, 0.3]
    return [random.choices(options, weights=weights)[0]]

def answer_2_47(patient, followed_diet):
    """How successful were you in achieving your goals with these diets?"""
    if followed_diet != "Yes":
        return []
    dq = patient.get("diet_quality", "moderate")
    if dq == "good":
        return [random.choices(["Very successful", "Somewhat successful", "Not successful"], weights=[0.6, 0.3, 0.1])[0]]
    elif dq == "poor":
        return [random.choices(["Very successful", "Somewhat successful", "Not successful"], weights=[0.1, 0.3, 0.6])[0]]
    return [random.choice(["Very successful", "Somewhat successful", "Not successful"])]

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
        return []
    stress = patient.get("stress_level", 5)
    weights = [0.7, 0.3] if stress < 5 else [0.5, 0.5]
    return [random.choices(["Yes", "No"], weights=weights)[0]]

def answer_2_50(patient, followed_diet, considered_plan):
    """Would you be willing to try a dietary plan in the future in support of your longevity goals?"""
    if followed_diet != "No" or considered_plan != "Yes":
        return []
    motivation = patient.get("diet_motivation", "moderate")
    if motivation == "high":
        weights = [0.5, 0.3, 0.1, 0.1]
    elif motivation == "low":
        weights = [0.1, 0.2, 0.3, 0.4]
    else:
        weights = [0.25, 0.35, 0.25, 0.15]
    return [random.choices([
        "Yes - open to trying", "Maybe - need more information",
        "Not now, but maybe in the future", "No"
    ], weights=weights)[0]]

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
    busy = patient.get("meals_per_day", 3) < 2
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
    if dq == "good":
        weights = [0.6, 0.3, 0.1]
    elif dq == "poor":
        weights = [0.1, 0.3, 0.6]
    else:
        weights = [0.3, 0.4, 0.3]
    return [random.choices([
        "Yes",
        "No, but I'm generally aware of how many calories I consume each day",
        "No"
    ], weights=weights)[0]]

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
        return []
    return [random.choice([
        "Yes - open to trying",
        "Maybe - need more information",
        "Not now, but maybe in the future",
        "No"
    ])]

def answer_2_60(patient, track_response):
    """How many calories do you typically consume per day?"""
    if track_response != "Yes":
        return []
    dq = patient.get("diet_quality", "moderate")
    options = ["<1,000", "1,000-1,500", "1,500-2,000", "2,000-2,500", "2,500-3,000", ">3,000"]
    if dq == "good":
        weights = [0.01, 0.05, 0.25, 0.4, 0.2, 0.09]
    elif dq == "poor":
        weights = [0.15, 0.3, 0.3, 0.15, 0.08, 0.02]
    else:
        weights = [0.1, 0.2, 0.3, 0.3, 0.07, 0.03]
    return [random.choices(options, weights=weights)[0]]

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
# END SECTION 2
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
        meals_resp = answer_2_02(patient)[0]
        snacks_resp = answer_2_04(patient)[0]
        eat_out_resp = answer_2_06(patient)[0]
        protein_track_resp = answer_2_08(patient)[0]
        protein_amt_resp = answer_2_10(patient)[0]
        red_meat_resp = answer_2_12(patient)[0]
        fish_resp = answer_2_14(patient)[0]
        plant_protein_resp = answer_2_16(patient)[0]
        fv_resp = answer_2_18(patient)[0]
        whole_grain_resp = answer_2_20(patient)[0]
        legume_resp = answer_2_22(patient)[0]
        seed_resp = answer_2_24(patient)[0]
        fats_resp = answer_2_26(patient)[0]
        water_resp = answer_2_28(patient)[0]
        caff_resp = answer_2_30(patient)[0]
        last_caff_time = answer_2_32(patient)[0]
        nutritionist_resp = answer_2_34(patient)[0]
        allergies_resp = answer_2_36(patient)[0]
        meals_desc = answer_2_38(patient)[0]
        dig_issues_resp = answer_2_39(patient)[0]
        dig_which_resp = answer_2_40(patient, dig_issues_resp)
        nut_goals = answer_2_41(patient)
        nut_goals_ranked = answer_2_42(patient, nut_goals)
        followed_diet_resp = answer_2_43(patient)[0]
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
        track_resp = answer_2_57(patient)[0]

        row_data = {
            'patient_id': patient.get('patient_id'),
            '1.01': "|".join(most_interested),
            '1.02': "|".join(not_interested),
            '1.03': "|".join(answer_1_03(patient, most_interested, not_interested)),
            '1.04': "|".join(answer_1_04(patient)),
            '1.05': "|".join(answer_1_05(patient)),
            '1.06': answer_1_06(patient),
            '2.01': "|".join(answer_2_01(patient)),
            '2.02': meals_resp,
            '2.03': "|".join(answer_2_03(patient, meals_resp)),
            '2.04': snacks_resp,
            '2.05': "|".join(answer_2_05(patient, snacks_resp)),
            '2.06': eat_out_resp,
            '2.07': "|".join(answer_2_07(patient, eat_out_resp)),
            '2.08': protein_track_resp,
            '2.09': "|".join(answer_2_09(patient, protein_track_resp)),
            '2.10': protein_amt_resp,
            '2.11': "|".join(answer_2_11(patient, protein_amt_resp)),
            '2.12': red_meat_resp,
            '2.13': "|".join(answer_2_13(patient, red_meat_resp)),
            '2.14': fish_resp,
            '2.15': "|".join(answer_2_15(patient, fish_resp)),
            '2.16': plant_protein_resp,
            '2.17': "|".join(answer_2_17(patient, plant_protein_resp)),
            '2.18': fv_resp,
            '2.19': "|".join(answer_2_19(patient, fv_resp)),
            '2.20': whole_grain_resp,
            '2.21': "|".join(answer_2_21(patient, whole_grain_resp)),
            '2.22': legume_resp,
            '2.23': "|".join(answer_2_23(patient, legume_resp)),
            '2.24': seed_resp,
            '2.25': "|".join(answer_2_25(patient, seed_resp)),
            '2.26': fats_resp,
            '2.27': "|".join(answer_2_27(patient, fats_resp)),
            '2.28': water_resp,
            '2.29': "|".join(answer_2_29(patient, water_resp)),
            '2.30': caff_resp,
            '2.31': "|".join(answer_2_31(patient, caff_resp)),
            '2.32': last_caff_time,
            '2.33': "|".join(answer_2_33(patient, last_caff_time)),
            '2.34': nutritionist_resp,
            '2.35': "|".join(answer_2_35(patient, nutritionist_resp)),
            '2.36': allergies_resp,
            '2.37': "|".join(answer_2_37(patient, allergies_resp)),
            '2.38': meals_desc,
            '2.39': dig_issues_resp,
            '2.40': "|".join(dig_which_resp),
            '2.41': "|".join(nut_goals),
            '2.42': "|".join(nut_goals_ranked),
            '2.43': followed_diet_resp,
            '2.44': "|".join(diets_past),
            '2.53': "|".join(diet_changes),
            '2.54': "|".join(future_changes),
            '2.55': "|".join(limiting_reasons),
            '2.56': "|".join(support_needed),
            '2.57': track_resp,
            '2.58': "|".join(answer_2_58(patient, track_resp)),
            '2.59': "|".join(answer_2_59(patient, track_resp)),
            '2.60': "|".join(answer_2_60(patient, track_resp)),
            '2.61': "|".join(answer_2_61(patient, track_resp)),
            '2.62': "|".join(answer_2_62(patient, track_resp)),
        }

        if followed_diet_resp == "Yes":
            row_data.update({
                '2.45': "|".join(diet_goals_when_start),
                '2.46': diet_plan_duration,
                '2.47': diet_plan_success,
            })
        if followed_diet_resp == "No":
            row_data.update({
                '2.48': "|".join(never_diet_reasons),
                '2.49': "|".join(considered_diet),
                '2.50': "|".join(willing_diet),
                '2.51': "|".join(factors_prevented),
            })
            if explore_guidelines:
                row_data['2.52'] = "|".join(explore_guidelines)

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
