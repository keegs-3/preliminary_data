# WellPath Survey Scoring System - Complete Guide

## Overview

The WellPath survey scoring system uses multiple calculation methods beyond simple response scoring. This document explains every custom definition (`custom def`) and calculation (`calculate`) used in the survey, with specific guidance on how to display complex scores in your app.

## Scoring Architecture

### Basic Structure
- **Simple Questions**: Have direct `response_scores` mapping (e.g., "Poor" = 0.2, "Excellent" = 1.0)
- **Complex Questions**: Use custom `score_fn` functions that take patient data and return calculated scores
- **Multi-component Questions**: Combine multiple survey responses into single scores

### Score Scaling
- Raw scores > 1 are scaled down: `score_scaled = score / 10`
- Pillar weights are then applied: `weighted_score = score_scaled * pillar_weight`

## Custom Scoring Functions

### 1. Protein Intake Scoring (Question 2.11)

**Function**: `protein_intake_score(protein_g, weight_lb, age)`

**Logic**:
```python
def calc_protein_target(weight_lb, age):
    weight_kg = weight_lb / 2.205
    if age < 65:
        target = 1.2 * weight_kg
    else:
        target = 1.5 * weight_kg  # Higher needs for older adults
    return round(target, 1)

def protein_intake_score(protein_g, weight_lb, age):
    target = calc_protein_target(weight_lb, age)
    pct = protein_g / target
    if pct >= 1.0:    return 10    # Meeting or exceeding target
    elif pct >= 0.8:  return 8     # 80% of target
    elif pct >= 0.6:  return 6     # 60% of target  
    elif pct > 0:     return 4     # Some protein intake
    else:             return 0     # No protein recorded
```

**App Display Recommendation**:
```
Current Intake: 45g
Target: 68.2g (Based on your weight and age)
Progress: 66% of target
Score: 6/10
```

### 2. Calorie Intake Scoring (Question 2.62)

**Function**: `calorie_intake_score(calories, weight_lb, age, sex)`

The calorie intake scoring system creates personalized daily calorie targets based on individual metabolic needs, then evaluates how close a patient's actual intake is to their optimal range. This is more sophisticated than generic calorie recommendations because it accounts for individual differences in metabolism.

**Why Personalized Targets Matter**: A 25-year-old male athlete and a 65-year-old female have completely different caloric needs. Generic recommendations like "2000 calories for women, 2500 for men" ignore crucial individual factors like age, weight, and activity level.

**Logic**:
```python
def calc_calorie_target(weight_lb, age, sex):
    weight_kg = weight_lb / 2.205
    # Harris-Benedict BMR calculation
    if sex.lower().startswith("m"):
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * 175) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * 162) - (4.330 * age)
    
    calorie_target = bmr * 1.2  # Sedentary activity factor
    return round(calorie_target)

def calorie_intake_score(calories, weight_lb, age, sex):
    target = calc_calorie_target(weight_lb, age, sex)
    pct = calories / target
    if 0.85 <= pct <= 1.15:      return 10  # Within ±15% of target (optimal)
    elif 0.75 <= pct < 0.85 or 1.15 < pct <= 1.25:  return 8   # ±25%
    elif 0.65 <= pct < 0.75 or 1.25 < pct <= 1.35:  return 6   # ±35%
    else:                        return 2   # Outside healthy range
```

**App Display Recommendation**:
```
Current Intake: 1,650 calories
Target: 1,547 calories (Based on your BMR + activity)
Progress: 107% of target (Slightly above optimal)
Score: 10/10 - Excellent intake level
```

### 3. Movement Scoring (Questions 3.04-3.11)

**Function**: `score_movement_pillar()`

Combines frequency and duration for each exercise type:

**Logic**:
```python
FREQ_SCORES = {
    "Rarely (a few times a month)": 0.4,
    "Occasionally (1-2 times per week)": 0.6,
    "Regularly (3-4 times per week)": 0.8,
    "Frequently (5 or more times per week)": 1.0
}

DUR_SCORES = {
    "Less than 30 minutes": 0.6,
    "30-45 minutes": 0.8,
    "45-60 minutes": 0.9,
    "More than 60 minutes": 1.0
}

def score_movement_pillar():
    for each exercise type:
        total = freq_score + dur_score
        if total >= 1.6:
            final_score = max_weight
        else:
            final_score = total * (max_weight / 2)
```

**App Display Example**:
```
Cardio Assessment:
Frequency: Regularly (3-4x/week) = 0.8
Duration: 30-45 minutes = 0.8
Combined: 0.8 + 0.8 = 1.6 (exceeds 1.6 threshold)
Score: 16/16 points - Maximum cardio score!
```

### 4. Sleep Issues Scoring (Questions 4.12-4.19)

**Function**: `score_sleep_issues()`

Multi-pillar impact based on reported issues and their frequency:

**Issues & Weights**:
```python
SLEEP_ISSUES = [
    ("Difficulty falling asleep", {"Sleep": 5}),
    ("Difficulty staying asleep", {"Sleep": 5}),
    ("Waking up too early", {"Sleep": 5}),
    ("Frequent nightmares", {"Sleep": 3}),
    ("Restless legs", {"Sleep": 6, "Movement": 1}),
    ("Snoring", {"Sleep": 4, "Core Care": 2}),
    ("Sleep apnea", {"Sleep": 7, "Core Care": 3}),
]
```

### 5. Sleep Hygiene Protocols (Question 4.07)

**Function**: `score_sleep_protocols()`

**Logic**: Simple count-based scoring:
```python
def score_sleep_protocols(answer_str):
    protocols = answer_str.split("|")  # Multi-select
    n = len(protocols)
    if n >= 7:    score = 1.0
    elif n >= 5:  score = 0.8
    elif n >= 3:  score = 0.6
    elif n >= 1:  score = 0.4
    else:         score = 0.2
    return score * 9.0  # Weight of 9 points
```

### 6. Stress Scoring (Questions 6.01 & 6.02)

**Function**: `stress_score(stress_level_ans, freq_ans)`

**Logic**: Combines stress level and frequency:
```python
level_map = {
    "No stress": 1.0,
    "Low stress": 0.8,
    "Moderate stress": 0.5,
    "High stress": 0.2,
    "Extreme stress": 0.0
}

freq_map = {
    "Rarely": 1.0,
    "Occasionally": 0.7,
    "Frequently": 0.4,
    "Always": 0.0
}

raw_score = (level_score + freq_score) / 2
final_score = raw_score * 19  # Out of 19 points
```

**App Display Recommendation**:
```
Stress Assessment:
Level: Moderate stress (0.5)
Frequency: Occasionally (0.7)
Combined: (0.5 + 0.7) ÷ 2 = 0.6
Score: 0.6 × 19 = 11.4/19 points
```

## Enhanced Substance Scoring System

### 7. Substance Use Scoring (Questions 8.01-8.38) - UPDATED WITH TIME-SINCE-QUIT BONUSES

This is your most complex scoring system with enhanced former user bonuses.

**Function**: `get_substance_score()`

**Substance Types & Weights**:
```python
SUBSTANCE_WEIGHTS = {
    "Tobacco": 15,          # Highest impact
    "Alcohol": 10,
    "Recreational Drugs": 8,
    "Nicotine": 4,
    "OTC Meds": 6,
    "Other Substances": 6
}
```

**Scoring Bands**:
```python
USE_BAND_SCORES = {
    "Heavy": 0.0,      # Worst score
    "Moderate": 0.25,
    "Light": 0.5,
    "Minimal": 0.75,
    "Occasional": 1.0   # Best score
}

DURATION_SCORES = {
    "Less than 1 year": 1.0,
    "1-2 years": 0.8,
    "3-5 years": 0.6,
    "6-10 years": 0.4,
    "11-20 years": 0.2,
    "More than 20 years": 0.0
}
```

**NEW: Enhanced Time-Since-Quit Bonuses**:
```python
QUIT_TIME_BONUS = {
    "Less than 3 years": 0.0,        # No bonus yet
    "3-5 years": 0.1,                # Small bonus
    "6-10 years": 0.2,               # Moderate bonus  
    "11-20 years": 0.4,              # Large bonus
    "More than 20 years": 0.6        # Maximum bonus
}
```

**Enhanced Scoring Logic**:
```python
def score_substance_use(use_band, years_band, is_current, usage_trend=None, time_since_quit=None):
    band_score = USE_BAND_SCORES.get(use_band, 0.0)
    duration_score = DURATION_SCORES.get(years_band, 0.0)
    base_score = min(band_score, duration_score)  # Take worse of the two
    
    if not is_current:
        # NEW: Graduated bonus based on time since quitting
        if time_since_quit:
            quit_bonus = QUIT_TIME_BONUS.get(time_since_quit, 0.15)
        else:
            quit_bonus = 0.15  # Fallback for missing data
        base_score = min(base_score + quit_bonus, 1.0)
    
    if is_current and usage_trend:
        if "more than I used to":
            base_score = max(base_score - 0.1, 0.0)  # Penalty for increasing use
        elif "less than I used to":
            base_score = min(base_score + 0.1, 1.0)  # Bonus for reducing use
    
    return base_score
```

### How to Display Enhanced Substance Scores in Your App

**For Tobacco (Smoking) Example**:

```
🚬 Tobacco Assessment
Status: Current User
Usage Level: Moderate (0.25 base score)
Duration: 6-10 years (0.4 base score)
Final Base: min(0.25, 0.4) = 0.25
Trend: Using less than before (+0.1)
Final Score: min(0.25 + 0.1, 1.0) = 0.35
Weighted Score: 0.35 × 15 = 5.25/15 points

Impact: High Risk - This is significantly affecting your Core Care score
```

**For Never Used Substances**:
```
✅ Alcohol Assessment  
Status: Never Used
Score: 1.0 (Perfect)
Weighted Score: 1.0 × 10 = 10/10 points
Impact: No negative impact on Core Care
```

**For Former Users - UPDATED Examples**:

```
🎯 Nicotine Assessment - Recent Quit (2 years ago)
Status: Former User
Previous Usage: Light use (0.5 base)
Duration Used: 1-2 years (0.8 base)
Base Score: min(0.5, 0.8) = 0.5
Quit Bonus: +0.0 (Less than 3 years - no bonus yet)
Final Score: min(0.5 + 0.0, 1.0) = 0.5
Weighted Score: 0.5 × 4 = 2.0/4 points
Impact: Good progress from quitting, bonus will increase over time
```

```
🎯 Tobacco Assessment - Long-term Quit (8 years ago)
Status: Former User
Previous Usage: Heavy use (0.0 base)
Duration Used: 11-20 years (0.2 base)
Base Score: min(0.0, 0.2) = 0.0
Quit Bonus: +0.2 (6-10 years category)
Final Score: min(0.0 + 0.2, 1.0) = 0.2
Weighted Score: 0.2 × 15 = 3.0/15 points
Impact: Great improvement from quitting despite heavy past use
```

```
🎯 Alcohol Assessment - Decades Clean (25 years ago)
Status: Former User
Previous Usage: Moderate use (0.25 base)
Duration Used: 6-10 years (0.4 base)
Base Score: min(0.25, 0.4) = 0.25
Quit Bonus: +0.6 (More than 20 years - maximum bonus)
Final Score: min(0.25 + 0.6, 1.0) = 0.85
Weighted Score: 0.85 × 10 = 8.5/10 points
Impact: Excellent long-term recovery, minimal current health impact
```

**Former User Examples by Time Since Quit**:
```
🕐 Recent Quit (2 years ago): Base score + 0.0 bonus
🕑 Medium-term (4 years ago): Base score + 0.1 bonus  
🕒 Long-term (8 years ago): Base score + 0.2 bonus
🕓 Very long-term (15 years ago): Base score + 0.4 bonus
🕔 Decades ago (25 years ago): Base score + 0.6 bonus
```

### 8. Cognitive Activities (Question 5.08)

**Function**: `score_cognitive_activities()`

**Logic**: Simple count-based scoring:
```python
def score_cognitive_activities(answer_str):
    activities = answer_str.split("|")  # Multi-select
    n = len(activities)
    if n >= 5:    score = 1.0
    elif n == 4:  score = 0.8
    elif n == 3:  score = 0.6
    elif n == 2:  score = 0.4
    elif n == 1:  score = 0.2
    else:         score = 0.0
    return score * 8.0  # Weight of 8 points
```

### 9. Coping Skills Scoring (Question 6.07)

**Function**: `coping_score()`

**Logic**: Context-aware scoring based on stress level:
```python
def coping_score(answer_str, stress_level_ans, freq_ans):
    responses = answer_str.split("|")
    n_coping = count_non_none_responses(responses)
    high_stress = is_high_stress_situation(stress_level_ans, freq_ans)
    
    if n_coping == 0:
        if high_stress:
            return 0.0  # Critical: No coping skills under high stress
        else:
            return 5.5  # Acceptable: Low stress, no specific coping needed
    elif n_coping >= 1:
        return 7.0  # Good: Has coping strategies
    else:
        return min(n_coping / 2 * 7.0, 7.0)
```

### 10. Date-Based Screening Guidelines (Questions 10.01-10.08)

**Function**: `score_date_response()`

**Logic**: Time-sensitive scoring based on medical guidelines:
```python
def score_date_response(date_str, window_months):
    months_ago = calculate_months_since(date_str)
    if months_ago <= window_months:
        return 1.0  # Up to date
    elif months_ago <= int(window_months * 1.5):
        return 0.6  # Slightly overdue
    else:
        return 0.2  # Significantly overdue
```

**Screening Guidelines**:
- Dental exam: 6 months
- Skin check: 12 months  
- Vision: 12 months
- Colon screening: 120 months (10 years)
- Mammogram: 12 months
- PAP smear: 36 months
- DEXA scan: 36 months
- PSA screening: 36 months

## Summary

This enhanced scoring system provides personalized, evidence-based health assessments that account for individual circumstances, medical history, and behavior change over time. The new time-since-quit bonuses particularly recognize and reward long-term substance cessation, providing more accurate health risk assessments for former users.