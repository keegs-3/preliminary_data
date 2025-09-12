# Binary Threshold Algorithm (SC-BINARY-THRESHOLD)

Simple pass/fail scoring based on meeting a threshold value.

## Overview

The Binary Threshold algorithm provides straightforward binary scoring (100 or 0) based on whether a measured value meets a defined threshold. It's the foundation of WellPath's scoring system for clear-cut goals.

## Algorithm Types

### SC-BINARY-DAILY
**Purpose:** Daily pass/fail evaluation  
**Pattern:** Single threshold check per day  
**Evaluation:** Daily  
**Scoring:** Binary (100 or 0)

### SC-BINARY-FREQUENCY [DEPRECATED]
**Status:** ⚠️ **DEPRECATED** - Use SC-MINIMUM-FREQUENCY instead

## Configuration Schema

```json
{
  "config_id": "SC-BINARY-DAILY-WATER_8_GLASSES",
  "scoring_method": "binary_threshold",
  "configuration_json": {
    "method": "binary_threshold",
    "formula": "if (actual_value >= threshold) then success_value else failure_value",
    "evaluation_pattern": "daily",
    "schema": {
      "measurement_type": "binary",
      "evaluation_period": "daily",
      "success_criteria": "simple_target",
      "calculation_method": "threshold_comparison",
      "tracked_metrics": ["daily_water_glasses"],
      "threshold": 8,
      "comparison_operator": ">=",
      "success_value": 100,
      "failure_value": 0,
      "unit": "glasses",
      "progress_direction": "buildup",
      "frequency_requirement": "daily",
      "description": "Binary threshold scoring for daily water intake goal"
    }
  },
  "metadata": {
    "recommendation_text": "Drink 8 glasses of water daily",
    "recommendation_id": "REC0001.1",
    "metric_id": "daily_water_glasses"
  }
}
```

## Implementation

### Python Usage

```python
from algorithms import create_daily_binary_threshold

# Create daily binary threshold algorithm
water_algo = create_daily_binary_threshold(
    threshold=8,
    success_value=100,
    failure_value=0,
    description="Daily water intake goal"
)

# Calculate scores
score_pass = water_algo.calculate_score(9)   # Returns 100
score_fail = water_algo.calculate_score(6)   # Returns 0
```

### Direct Function Usage

```python
from algorithms.binary_threshold import BinaryThresholdAlgorithm, BinaryThresholdConfig

config = BinaryThresholdConfig(
    threshold=8,
    success_value=100,
    failure_value=0,
    comparison_operator=">=",
    unit="glasses"
)

algorithm = BinaryThresholdAlgorithm(config)
result = algorithm.calculate_score(9)  # Returns 100
```

## Scoring Logic

### Daily Binary Threshold

```python
def calculate_score(actual_value):
    if comparison_operator == ">=":
        meets_threshold = actual_value >= threshold
    elif comparison_operator == "<=": 
        meets_threshold = actual_value <= threshold
    elif comparison_operator == "==":
        meets_threshold = actual_value == threshold
    
    return success_value if meets_threshold else failure_value
```

### Comparison Operators

| Operator | Use Case | Example |
|----------|----------|---------|
| `>=` | Minimum requirements | "≥8 glasses water daily" |
| `<=` | Maximum limits | "≤400mg caffeine daily" |
| `==` | Exact targets | "Exactly 7 hours sleep" |
| `>` | Strict minimums | ">0 workouts" |
| `<` | Strict maximums | "<2000 calories" |

## Use Cases

### Perfect Fits for Binary Threshold
- **Daily completion goals:** "Complete 30-minute workout daily"
- **Simple intake targets:** "Drink 8 glasses of water daily"
- **Habit formation:** "Take vitamins daily"
- **Compliance tracking:** "Follow medication schedule daily"
- **Basic limits:** "≤2 cups coffee daily"

### Not Suitable For
- **Frequency patterns:** "Exercise 3+ times per week" → Use SC-MINIMUM-FREQUENCY
- **Zero tolerance:** "No smoking every day" → Use SC-WEEKLY-ELIMINATION  
- **Gradual improvement:** "Work toward 10K steps" → Use SC-PROPORTIONAL
- **Range-based:** "Sleep 7-9 hours" → Use SC-ZONE-BASED

## Validation Rules

1. **Binary Scoring:** `success_value` must be 100, `failure_value` must be 0
2. **Threshold Required:** Valid numeric or time threshold required
3. **Comparison Operator:** Must be one of: `>=`, `<=`, `==`, `>`, `<`
4. **Tracked Metrics:** At least one metric must be specified

## Testing

```python
# Test binary threshold algorithm
def test_binary_threshold():
    algorithm = create_daily_binary_threshold(
        threshold=8,
        success_value=100,
        failure_value=0
    )
    
    # Test cases
    assert algorithm.calculate_score(8) == 100   # Meets threshold
    assert algorithm.calculate_score(9) == 100   # Exceeds threshold  
    assert algorithm.calculate_score(7) == 0     # Below threshold
    
    print("✅ Binary threshold tests passed!")
```

## Migration from Deprecated Patterns

### SC-BINARY-FREQUENCY → SC-MINIMUM-FREQUENCY

**Old Configuration (Deprecated):**
```json
{
  "scoring_method": "binary_threshold",
  "configuration_json": {
    "method": "binary_threshold",
    "evaluation_pattern": "weekly_frequency",
    "schema": {
      "frequency_requirement": "5 of 7 days"
    }
  }
}
```

**New Configuration:**
```json
{
  "scoring_method": "minimum_frequency", 
  "configuration_json": {
    "method": "minimum_frequency",
    "evaluation_pattern": "weekly_minimum_frequency",
    "schema": {
      "required_days": 5,
      "total_days": 7
    }
  }
}
```

## Real-World Examples

### Water Intake Goal
```json
{
  "config_id": "SC-BINARY-DAILY-WATER_8_GLASSES",
  "recommendation_text": "Drink 8 glasses of water daily",
  "schema": {
    "threshold": 8,
    "comparison_operator": ">=",
    "unit": "glasses"
  }
}
```

### Workout Completion
```json
{
  "config_id": "SC-BINARY-DAILY-WORKOUT_30_MIN",
  "recommendation_text": "Complete 30-minute workout daily",
  "schema": {
    "threshold": 30,
    "comparison_operator": ">=", 
    "unit": "minutes"
  }
}
```

### Caffeine Limit
```json
{
  "config_id": "SC-BINARY-DAILY-CAFFEINE_400MG_LIMIT",
  "recommendation_text": "Limit caffeine to ≤400mg daily",
  "schema": {
    "threshold": 400,
    "comparison_operator": "<=",
    "unit": "mg"
  }
}
```

---

*For frequency-based binary patterns, see [SC-MINIMUM-FREQUENCY](SC-MINIMUM-FREQUENCY.md)*  
*For zero-tolerance patterns, see [SC-WEEKLY-ELIMINATION](SC-WEEKLY-ELIMINATION.md)*