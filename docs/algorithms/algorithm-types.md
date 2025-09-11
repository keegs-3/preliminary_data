# Algorithm Types - Complete Reference

The WellPath recommendation system supports **14 distinct algorithm types** across 5 categories, each designed for specific recommendation patterns and behavioral goals.

## 🎯 Algorithm Categories Overview

| Category | Algorithm Types | Use Cases |
|----------|----------------|-----------|
| **Binary Threshold** | Daily, Frequency | Pass/fail goals, strict limits |
| **Proportional** | Daily, Frequency | Target achievement with partial credit |
| **Zone-Based** | 3-Tier, 5-Tier (Daily/Frequency) | Optimal ranges, tiered scoring |
| **Composite** | Weighted, Advanced Sleep | Multi-component recommendations |
| **Specialized** | Weekly Allowance, Categorical Filter | Complex constraints, category rules |

## 📊 Detailed Algorithm Types

### 1. Binary Threshold Algorithms

**Use Cases**: "Eliminate", "Add one daily", "No more than X", Pass/fail goals

#### 1.1 Daily Binary (`SC-BIN-DAILY-*`)
- **Pattern**: Daily compliance check
- **Scoring**: 100 points if threshold met, 0 if failed
- **Example**: "Add one daily serving of fiber" → 1 serving = 100 points, 0 servings = 0 points

#### 1.2 Frequency Binary (`SC-BIN-FREQ-*`) 
- **Pattern**: Success over 7-day rolling window
- **Scoring**: Based on compliant days (5 of 7 = success)
- **Example**: "Exercise 3 times per week" → 3+ days = 100 points

---

### 2. Proportional Algorithms

**Use Cases**: "At least X", "Target Y", Achievement-based goals with partial credit

#### 2.1 Daily Proportional (`SC-PROP-DAILY-*`)
- **Pattern**: Percentage of daily target achieved
- **Formula**: `(actual_value / target) * 100`
- **Scoring**: 1 serving of 2 target = 50%, 3 servings = 150% → capped at 100%
- **Example**: "Include at least 2 servings of whole grains daily"

#### 2.2 Frequency Proportional (`SC-PROP-FREQ-*`)
- **Pattern**: Achievement over rolling 7-day window
- **Scoring**: Average achievement across frequency period
- **Example**: "Average 10,000 steps daily over the week"

---

### 3. Zone-Based Algorithms

**Use Cases**: "Optimal range", "Between X-Y", Tiered health metrics

#### 3.1 3-Tier Zone (`SC-Z3T-DAILY-*` / `SC-Z3T-FREQ-*`)
- **Zones**: Below Target (40), On Target (100), Above Target (60)
- **Use Case**: Simple range optimization
- **Example**: Blood pressure in healthy range

#### 3.2 5-Tier Zone (`SC-Z5T-DAILY-*` / `SC-Z5T-FREQ-*`)
- **Zones**: Critical (20), Poor (40), Fair (60), **Optimal (100)**, Excessive (80)
- **Use Case**: Detailed health metric optimization
- **Example**: Sleep duration with 7-9 hours optimal
- **Zone Calculation**:
  ```
  0-5 hours: Critical (20 points)
  5-6 hours: Poor (40 points)  
  6-7 hours: Fair (60 points)
  7-9 hours: Optimal (100 points)
  9-12 hours: Excessive (80 points)
  ```

---

### 4. Composite Algorithms

**Use Cases**: Multi-component recommendations requiring weighted combinations

#### 4.1 Daily Composite (`SC-COMP-DAILY-*`)
- **Pattern**: Multiple daily components with different weights
- **Example**: "Include vegetables at every meal (70%) + 2 different types daily (30%)"
- **Components**:
  ```json
  [
    {
      "name": "Vegetable Servings at Meals",
      "weight": 0.7,
      "target": 3,
      "scoring_method": "proportional"
    },
    {
      "name": "Vegetable Variety", 
      "weight": 0.3,
      "target": 2,
      "scoring_method": "proportional"
    }
  ]
  ```

#### 4.2 Advanced Sleep Composite (`SC-COMPOSITE-SLEEP-ADVANCED`)
- **Pattern**: Sleep duration + schedule consistency
- **Weighting**: Duration (55%), Sleep Time Consistency (22.5%), Wake Time Consistency (22.5%)
- **Sleep Duration**: 5-tier zone scoring (7-9 hours optimal)
- **Consistency Method**: Rolling average tolerance
  - **Logic**: `abs(sleep_time - rolling_average) < 60 minutes`
  - **Scoring**: `(compliant_nights / 7) * 100`
  - **Examples**: 7/7 nights = 100%, 6/7 nights = 85.7%, 5/7 nights = 71.4%

---

### 5. Specialized Algorithms

#### 5.1 Constrained Weekly Allowance (`SC-ALLOW-WEEKLY-*`)
- **Pattern**: Dual constraint system (total limit + day frequency)
- **Use Case**: "No more than X drinks per week across Y days"
- **Logic**: `weekly_total <= allowance AND days_with_consumption <= max_days`
- **Example**: "3 drinks across 2 days" 
  - ✅ Pass: Day 1: 2 drinks, Day 2: 1 drink = 3 total, 2 days
  - ❌ Fail: Day 1: 1 drink, Day 2: 1 drink, Day 3: 1 drink = 3 total, 3 days

#### 5.2 Categorical Filter (`SC-CAT-*`)
- **Pattern**: Different rules for different categories
- **Use Case**: "High-impact exercises 3x/week, low-impact 2x/week"
- **Logic**: Category-specific thresholds with separate scoring

---

## 🎯 Algorithm Selection Intelligence

The system uses **weighted keyword analysis** to automatically select the optimal algorithm:

### High-Priority Binary Patterns (5x weight)
```
"add one", "take one", "one daily", "eliminate", "no more than"
```

### Proportional Triggers
```
"at least", "target", "goal", "increase", specific numbers
```

### Zone-Based Triggers  
```
"optimal", "range", "between", "zone", "excellent/good/fair/poor"
```

### Composite Triggers
```
"overall", "combined", "multiple", "plus", "with at least", "different sources"
```

## 📋 Algorithm Configuration Schema

### Standard Fields (All Types)
```json
{
  "config_id": "SC-{TYPE}-{PATTERN}-{METRIC}",
  "config_name": "Human readable name",
  "scoring_method": "algorithm_type",
  "configuration_json": {
    "method": "algorithm_type",
    "formula": "mathematical description",
    "evaluation_pattern": "daily|frequency|weekly",
    "schema": {
      "measurement_type": "binary|quantity|composite",
      "tracked_metrics": ["metric_id"],
      "unit": "serving|step|hour|etc",
      "progress_direction": "buildup|countdown|measurement"
    }
  }
}
```

### Progress Direction Types
- **`"buildup"`**: Progress builds from 0 towards target (steps, meals, exercise, nutrients)
- **`"countdown"`**: Progress counts down from 100% as limits are approached (alcohol, sugar, calorie limits) 
- **`"measurement"`**: Retrospective evaluation after period ends (sleep quality, time-restricted eating, weight checks)

### Algorithm-Specific Fields

**Binary Threshold**:
```json
{
  "threshold": 1.0,
  "success_value": 100,
  "failure_value": 0
}
```

**Proportional**:
```json
{
  "target": 2.0,
  "maximum_cap": 100,
  "partial_credit": true
}
```

**Zone-Based**:
```json
{
  "zones": [
    {"range": [7, 9], "score": 100, "label": "Optimal"},
    {"range": [6, 7], "score": 60, "label": "Fair"}
  ]
}
```

**Composite**:
```json
{
  "components": [
    {
      "name": "Component Name",
      "weight": 0.7,
      "target": 3,
      "scoring_method": "proportional"
    }
  ]
}
```

## 🔄 Integration with WellPath System

### Automatic Metric Linking
1. **Direct ID match** in metric's `recommendations_v2` field
2. **Name matching** for keyword searches
3. **Unit resolution** from `units_v3` database
4. **Validation** against metric schemas

### Generated Output Structure
```
src/generated_configs/
├── REC0001.1-BINARY-THRESHOLD.json
├── REC0007.2-COMPOSITE-WEIGHTED.json  
├── REC0008.3-COMPOSITE-WEIGHTED.json
└── all_generated_configs.json
```

## 🎮 Usage Examples

### Binary Threshold
```python
# REC0009.3: "Eliminate processed sugar"
threshold = 0  # Zero tolerance
score = 100 if actual_servings <= threshold else 0
```

### Proportional
```python  
# REC0011.1: "At least 2 servings whole grains daily"
target = 2.0
score = min((actual_servings / target) * 100, 100)
```

### Zone-Based 5-Tier
```python
# REC0004.1: "7-9 hours sleep nightly"  
if 7 <= hours <= 9:
    score = 100  # Optimal
elif 6 <= hours < 7:
    score = 60   # Fair
# ... other zones
```

### Composite
```python
# REC0007.2: "1 serving at each meal + 2 variety"
meal_score = (actual_meals / 3) * 100
variety_score = (actual_variety / 2) * 100
final_score = (meal_score * 0.7) + (variety_score * 0.3)
```

---

**This flexible algorithm framework enables precise behavioral targeting while maintaining clinical relevance and user engagement through appropriate scoring methods.**