# WellPath Survey Scoring System - Custom Logic Architecture

## Overview

This document explains the custom scoring logic architecture built for WellPath's survey system. While the current implementation is in Python, the architecture is designed to integrate with any backend system through question ID mapping and modular scoring functions.

## 🎯 Core Design Principles

### 1. **Question ID-Based Architecture**
All custom logic is mapped to specific question IDs (e.g., "2.11", "3.04", "6.07"), making it backend-agnostic:

```python
# Current Python implementation
"2.11": {
    "pillar_weights": {"Nutrition": 6, "Movement": 6},
    "score_fn": protein_intake_score
}
```

**Backend Integration Point**: The existing question ID relations can directly map to these scoring functions.

### 2. **Modular Scoring Functions**
Complex logic is encapsulated in standalone functions that accept standardized inputs:

```python
def protein_intake_score(protein_g, weight_lb, age):
    # Calculate personalized protein target
    weight_kg = weight_lb / 2.205
    target = 1.2 * weight_kg if age < 65 else 1.5 * weight_kg
    
    # Score based on percentage of target met
    pct = protein_g / target
    if pct >= 1: return 10
    elif pct >= 0.8: return 8
    # ... evidence-based scoring tiers
```

**Backend Integration**: These functions can be ported to any language or called as microservices.

## 🔧 Complete Custom Logic Implementation

### 1. **Biomarker-Dependent Personalized Scoring**

#### Protein Intake Scoring (Q2.11)
```python
def protein_intake_score(protein_g, weight_lb, age):
    weight_kg = weight_lb / 2.205
    if age < 65:
        target = 1.2 * weight_kg  # Standard adult requirement
    else:
        target = 1.5 * weight_kg  # Higher requirement for seniors
    
    pct = protein_g / target if target else 0
    if pct >= 1: return 10      # Meeting or exceeding target
    elif pct >= 0.8: return 8   # 80% of target (acceptable)
    elif pct >= 0.6: return 6   # 60% of target (needs improvement)
    elif pct > 0: return 4      # Some protein intake
    else: return 0              # No protein reported
```

**Clinical Rationale**: Age-adjusted protein requirements based on current nutritional science. Seniors need more protein to maintain muscle mass.

**Pillar Impact**: Nutrition (6 points), Movement (6 points) - protein supports both dietary goals and muscle maintenance.

#### Calorie Intake Scoring (Q2.62)
```python
def calorie_intake_score(calories, weight_lb, age, sex):
    weight_kg = weight_lb / 2.205
    # Harris-Benedict BMR calculation
    if sex.lower().startswith("m"):
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * 175) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * 162) - (4.330 * age)
    
    calorie_target = bmr * 1.2  # Sedentary activity multiplier
    pct = calories / target if target else 0
    
    # Optimal range: ±15% of calculated target
    if 0.85 <= pct <= 1.15: return 10
    elif 0.75 <= pct < 0.85 or 1.15 < pct <= 1.25: return 8
    elif 0.65 <= pct < 0.75 or 1.25 < pct <= 1.35: return 6
    else: return 2
```

**Clinical Rationale**: Personalized calorie targets using established BMR formulas with sex, age, and weight adjustments.

### 2. **Multi-Factor Movement Scoring (Q3.04-3.11)**

#### Exercise Type Configuration
```python
movement_questions = {
    "Cardio": {"freq_q": "3.04", "dur_q": "3.08", "pillar_weights": {"Movement": 16}},
    "Strength": {"freq_q": "3.05", "dur_q": "3.09", "pillar_weights": {"Movement": 16}},
    "Flexibility": {"freq_q": "3.06", "dur_q": "3.10", "pillar_weights": {"Movement": 13}},
    "HIIT": {"freq_q": "3.07", "dur_q": "3.11", "pillar_weights": {"Movement": 16}}
}

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
```

#### Composite Scoring Logic
```python
def score_movement_pillar(row, movement_questions):
    for move_type, cfg in movement_questions.items():
        freq_ans = row.get(cfg["freq_q"], "")
        dur_ans = row.get(cfg["dur_q"], "")
        freq = FREQ_SCORES.get(freq_ans, 0.0)
        dur = DUR_SCORES.get(dur_ans, 0.0)
        
        if freq == 0 and dur == 0:
            score = 0
        else:
            total = freq + dur
            if total >= 1.6:  # High frequency + good duration
                score = full_weight
            else:
                score = total * (weight / 2)  # Scaled scoring
```

**Logic Rationale**: 
- Frequency and duration both contribute to exercise effectiveness
- Different exercise types weighted by longevity impact (Strength/Cardio/HIIT > Flexibility)
- Threshold scoring rewards consistent, adequate-duration exercise

### 3. **Complex Sleep Issue Analysis (Q4.12-4.19)**

#### Sleep Issue Configuration
```python
SLEEP_ISSUES = [
    ("Difficulty falling asleep", "4.13", {"Sleep": 5}),
    ("Difficulty staying asleep", "4.14", {"Sleep": 5}),
    ("Waking up too early", "4.15", {"Sleep": 5}),
    ("Frequent nightmares", "4.16", {"Sleep": 3}),
    ("Restless legs", "4.17", {"Sleep": 6, "Movement": 1}),  # Multi-pillar
    ("Snoring", "4.18", {"Sleep": 4, "CoreCare": 2}),
    ("Sleep apnea", "4.19", {"Sleep": 7, "CoreCare": 3}),
]

SLEEP_FREQ_MAP = {
    "Always": 0.2,      # Worst case
    "Frequently": 0.4,
    "Occasionally": 0.6,
    "Rarely": 0.8,
    "": 1.0            # Not selected = full credit
}
```

#### Conditional Scoring Logic
```python
def score_sleep_issues(patient_answers):
    sleep_issues_reported = [x.strip() for x in str(patient_answers.get("4.12", "")).split("|")]
    
    # Full credit if none reported or "None" selected
    if not sleep_issues_reported or any("none" in s.lower() for s in sleep_issues_reported):
        return full_credit_for_all_pillars
    
    # Score each issue based on frequency
    for issue, freq_qid, pillar_weights in SLEEP_ISSUES:
        if issue in sleep_issues_reported:
            freq_ans = str(patient_answers.get(freq_qid, "")).strip()
            multiplier = SLEEP_FREQ_MAP.get(freq_ans, 0.2)
        else:
            multiplier = 1.0  # Not selected = no penalty
        
        for pillar, weight in pillar_weights.items():
            pillar_scores[pillar] += (weight * multiplier)
```

**Logic Rationale**:
- Different sleep issues have different severity (sleep apnea > nightmares)
- Frequency of occurrence affects scoring
- Some issues impact multiple pillars (restless legs affects sleep + movement)
- "None selected" logic prevents penalizing people without issues

#### Sleep Hygiene Protocol Scoring (Q4.07)
```python
def score_sleep_protocols(answer_str):
    protocols = [x.strip() for x in (answer_str or "").split("|")]
    n = len(protocols)
    
    if n >= 7: score = 1.0      # Comprehensive sleep hygiene
    elif n >= 5: score = 0.8    # Good practices
    elif n >= 3: score = 0.6    # Some practices
    elif n >= 1: score = 0.4    # Minimal effort
    else: score = 0.2           # No practices
    
    return round(score * 9.0, 2)  # Weight: 9 points
```

### 4. **Advanced Stress Management Scoring (Q6.01-6.07)**

#### Multi-Question Stress Assessment
```python
def stress_score(stress_level_ans, freq_ans):
    level_map = {
        "No stress": 1.0,
        "Low stress": 0.8,
        "Moderate stress": 0.5,
        "High stress": 0.2,
        "Extreme stress": 0.0,
    }
    freq_map = {
        "Rarely": 1.0,
        "Occasionally": 0.7,
        "Frequently": 0.4,
        "Always": 0.0,
    }
    
    stress_level_score = level_map.get(stress_level_ans, 0.5)
    frequency_score = freq_map.get(freq_ans, 0.5)
    raw_score = (stress_level_score + frequency_score) / 2
    return round(raw_score * 19, 2)  # Scale to pillar weight
```

#### Context-Aware Coping Skills Scoring
```python
COPING_WEIGHTS = {
    "Exercise or physical activity": 1.0,           # Most effective
    "Meditation or mindfulness practices": 1.0,     # Most effective
    "Professional counseling or therapy": 1.0,      # Most effective
    "Deep breathing exercises": 0.7,
    "Hobbies or recreational activities": 0.7,
    "Talking to friends or family": 0.7,
    "Journaling or writing": 0.5,
    "Time management strategies": 0.5,
    "Avoiding stressful situations": 0.3,           # Less effective
    "None": 0.0,
}

def coping_score(answer_str, stress_level_ans, freq_ans):
    responses = [r.strip() for r in str(answer_str or "").split("|")]
    has_none = any("none" in r.lower() for r in responses)
    n_coping = sum([1 for r in responses if r.lower() not in ("none", "")])
    
    # High stress individuals need coping strategies
    high_stress = (stress_level_ans in ["High stress", "Extreme stress"] or
                   freq_ans in ["Frequently", "Always"])
    
    if not n_coping or has_none:
        if high_stress:
            return 0.0  # High stress + no coping = major concern
        else:
            return 5.5  # Low stress + no coping = acceptable
    elif n_coping >= 1:
        return 7.0  # Has coping strategies
```

**Logic Rationale**: 
- Stress assessment considers both intensity and frequency
- Coping strategies weighted by evidence-based effectiveness
- Context-aware: High stress individuals penalized more for lacking coping skills

### 5. **Sophisticated Substance Use Scoring (Q8.01-8.32)**

#### Multi-Substance Tracking System
```python
SUBSTANCE_QUESTIONS = {
    "Tobacco": {
        "current_band": "8.02",     # Usage intensity
        "current_years": "8.03",    # Duration of use
        "current_trend": "8.04",    # Increasing/decreasing
        "former_band": "8.22",      # Past usage if quit
        "former_years": "8.21",     # Duration when used
    },
    # ... similar for Alcohol, Recreational Drugs, Nicotine, OTC Meds, Other
}

USE_BAND_SCORES = {
    "Heavy": 0.0,      # Worst health impact
    "Moderate": 0.25,
    "Light": 0.5,
    "Minimal": 0.75,
    "Occasional": 1.0   # Best score for current users
}

DURATION_SCORES = {
    "Less than 1 year": 1.0,      # Short exposure
    "1-2 years": 0.8,
    "3-5 years": 0.6,
    "6-10 years": 0.4,
    "11-20 years": 0.2,
    "More than 20 years": 0.0     # Long exposure = more damage
}
```

#### Complex Substance Scoring Logic
```python
def score_substance_use(use_band, years_band, is_current, usage_trend=None):
    band_score = USE_BAND_SCORES.get(use_band, 0.0)
    duration_score = DURATION_SCORES.get(years_band, 0.0)
    base_score = min(band_score, duration_score)  # Worst of both factors
    
    if not is_current:
        base_score = min(base_score + 0.15, 1.0)  # Quit bonus
    
    if is_current and usage_trend:
        if usage_trend == "I currently use more than I used to":
            base_score = max(base_score - 0.1, 0.0)  # Penalty for increasing
        elif usage_trend == "I currently use less than I used to":
            base_score = min(base_score + 0.1, 1.0)  # Bonus for decreasing
    
    return base_score
```

**Logic Rationale**:
- Tracks 6 different substance categories with different health impacts
- Considers usage intensity, duration, and trends
- Rewards quitting and reducing usage
- Penalizes heavy/long-term use patterns

### 6. **Evidence-Based Screening Compliance (Q10.01-10.08)**

#### Screening Guidelines Database
```python
screen_guidelines = {
    '10.01': 6,     # Dental exam: Every 6 months
    '10.02': 12,    # Skin check: Annual
    '10.03': 12,    # Vision: Annual
    '10.04': 120,   # Colon: Every 10 years (120 months)
    '10.05': 12,    # Mammogram: Annual
    '10.06': 36,    # PAP: Every 3 years
    '10.07': 36,    # DEXA: Every 3 years
    '10.08': 36,    # PSA: Every 3 years
}
```

#### Time-Based Compliance Scoring
```python
def score_date_response(date_str, window_months):
    exam_date = datetime.strptime(date_str, "%Y-%m-%d")
    today = datetime.today()
    months_ago = (today.year - exam_date.year) * 12 + (today.month - exam_date.month)
    
    if months_ago <= window_months:
        return 1.0              # Within guidelines
    elif months_ago <= int(window_months * 1.5):
        return 0.6              # Slightly overdue
    else:
        return 0.2              # Significantly overdue
```

**Logic Rationale**: Evidence-based screening intervals with grace periods for scheduling challenges.

### 7. **Cognitive Activity Engagement (Q5.08)**
```python
def score_cognitive_activities(answer_str):
    activities = [x.strip() for x in (answer_str or "").split("|")]
    n = len(activities)
    
    if n >= 5: score = 1.0      # Highly engaged
    elif n == 4: score = 0.8    # Well engaged
    elif n == 3: score = 0.6    # Moderately engaged
    elif n == 2: score = 0.4    # Some engagement
    elif n == 1: score = 0.2    # Minimal engagement
    else: score = 0.0           # No engagement
    
    return round(score * 8.0, 2)  # Weight: 8 points
```

### 8. **Multi-Pillar Impact Logic**

Several questions impact multiple health pillars with different weights:

```python
# Protein impacts both nutrition and muscle maintenance
"2.11": {"Nutrition": 6, "Movement": 6}

# Caffeine timing affects both nutrition choices and sleep quality  
"2.34": {"Sleep": 6}
"2.33": {"Nutrition": 3, "Sleep": 2}

# Restless legs affects sleep quality and movement disorders
"Restless legs": {"Sleep": 6, "Movement": 1}

# Sleep apnea affects sleep and requires medical care
"Sleep apnea": {"Sleep": 7, "CoreCare": 3}
```

**Architecture Benefit**: Single questions can appropriately impact multiple aspects of health, reflecting real-world interconnections.

## 🏛️ Backend Integration Strategy

### 1. **Database Schema Considerations**

The existing question relations should support:
```sql
-- Question metadata table
questions (
    id VARCHAR,  -- "2.11", "3.04", etc.
    scoring_type ENUM('simple', 'custom_function', 'multi_factor'),
    requires_biomarkers BOOLEAN,
    dependent_questions JSON  -- For multi-question logic
)

-- Scoring parameters table  
question_scoring (
    question_id VARCHAR,
    pillar VARCHAR,
    weight DECIMAL,
    response_value VARCHAR,
    score_value DECIMAL
)
```

### 2. **API Design Pattern**

```javascript
// Scoring service endpoint
POST /api/scoring/calculate-survey-scores
{
    "patient_id": "123",
    "responses": {
        "2.11": "85",  // protein grams
        "3.04": "Regularly (3-4 times per week)"
    },
    "biomarkers": {  // For biomarker-dependent questions
        "weight_lb": 150,
        "age": 35,
        "sex": "female"
    }
}
```

### 3. **Scoring Engine Architecture**

```python
class SurveyScorer:
    def __init__(self, question_config, biomarker_data):
        self.config = question_config
        self.biomarkers = biomarker_data
    
    def score_question(self, question_id, response):
        config = self.config[question_id]
        
        if config.get('score_fn'):
            # Custom function scoring
            return self._call_custom_function(config['score_fn'], response)
        else:
            # Simple response mapping
            return config['response_scores'].get(response, 0)
    
    def _call_custom_function(self, func_name, response):
        # Route to appropriate custom scoring function
        # Can be local functions, microservices, or external APIs
```

## 🔄 Migration Path from Current Python

### Phase 1: API Wrapper
Wrap existing Python logic as REST APIs that the backend can call

### Phase 2: Function Translation  
Port individual scoring functions to the backend language (Node.js, Java, etc.)

### Phase 3: Native Integration
Fully integrate logic into the existing scoring service architecture

## 💡 Key Benefits for Backend Integration

1. **Question ID Mapping**: Seamless integration with existing question relations
2. **Modular Functions**: Each scoring algorithm is self-contained
3. **Language Agnostic**: Logic can be ported to any backend technology
4. **Incremental Migration**: Can implement custom scoring gradually by question ID
5. **Testable**: Each function has clear inputs/outputs for unit testing

## 🎛️ Configuration Management

The scoring logic is highly configurable through the question mapping structure:

```python
"2.11": {
    "pillar_weights": {"Nutrition": 6, "Movement": 6},  # Multi-pillar impact
    "score_fn": "protein_intake_score",                  # Custom function name
    "requires": ["weight_lb", "age"]                     # Required biomarker fields
}
```

This allows the backend to:
- Dynamically load scoring configurations
- Update scoring weights without code changes  
- A/B test different scoring algorithms
- Maintain audit trails of scoring logic changes

## 🚀 Next Steps for Integration

1. **Map existing question IDs** to the custom logic requirements
2. **Identify biomarker dependencies** for questions requiring patient data
3. **Choose integration approach** (API wrapper vs. native implementation)
4. **Set up scoring configuration** management in your backend
5. **Implement incremental migration** starting with highest-impact custom logic

The architecture is designed to be flexible and backend-agnostic while preserving the sophisticated health scoring logic that makes WellPath's assessments clinically meaningful.
