# Proportional Algorithm (SC-PROPORTIONAL)

Percentage-based scoring that provides gradual improvement feedback relative to targets.

## Overview

The Proportional algorithm calculates scores as a percentage of target achievement, providing continuous feedback for progressive goals. Unlike binary algorithms, it rewards partial progress toward targets.

## Algorithm Types

### SC-PROPORTIONAL-DAILY
**Purpose:** Daily percentage-based scoring  
**Pattern:** Continuous scoring from 0-100% based on target achievement  
**Evaluation:** Daily  
**Scoring:** Continuous (0-100 with caps and minimums)

### SC-PROPORTIONAL-FREQUENCY
**Purpose:** Frequency-based proportional scoring  
**Pattern:** Weekly evaluation with proportional achievement  
**Evaluation:** Weekly  
**Scoring:** Continuous based on frequency achievement rate

## Configuration Schema

```json
{
  "config_id": "SC-PROPORTIONAL-DAILY-STEPS_10000",
  "scoring_method": "proportional",
  "configuration_json": {
    "method": "proportional",
    "formula": "(actual_value / target) * 100",
    "evaluation_pattern": "daily",
    "schema": {
      "measurement_type": "proportional",
      "evaluation_period": "daily",
      "success_criteria": "target_achievement",
      "calculation_method": "percentage_of_target",
      "tracked_metrics": ["daily_steps"],
      "target": 10000,
      "unit": "steps",
      "maximum_cap": 100,
      "minimum_threshold": 20,
      "progress_direction": "buildup",
      "description": "Proportional scoring for daily step goal"
    }
  },
  "metadata": {
    "recommendation_text": "Work toward 10,000 steps daily",
    "recommendation_id": "REC0002.1",
    "metric_id": "daily_steps"
  }
}
```

## Implementation

### Python Usage

```python
from algorithms import create_daily_proportional

# Create daily proportional algorithm
steps_algo = create_daily_proportional(
    target=10000,
    unit="steps",
    maximum_cap=100,
    minimum_threshold=20,
    description="Daily step goal"
)

# Calculate scores
score_50_percent = steps_algo.calculate_score(5000)   # Returns 50
score_100_percent = steps_algo.calculate_score(10000) # Returns 100  
score_150_percent = steps_algo.calculate_score(15000) # Returns 100 (capped)
score_low = steps_algo.calculate_score(1000)          # Returns 20 (minimum threshold)
```

### Direct Function Usage

```python
from algorithms.proportional import ProportionalAlgorithm, ProportionalConfig

config = ProportionalConfig(
    target=10000,
    unit="steps",
    maximum_cap=100,
    minimum_threshold=20,
    progress_direction="buildup"
)

algorithm = ProportionalAlgorithm(config)
result = algorithm.calculate_score(7500)  # Returns 75
```

## Scoring Logic

### Daily Proportional

```python
def calculate_score(actual_value, target, maximum_cap=100, minimum_threshold=0):
    # Calculate raw percentage
    percentage = (actual_value / target) * 100
    
    # Apply caps and minimums
    if percentage > maximum_cap:
        return maximum_cap
    elif percentage < minimum_threshold:
        return minimum_threshold
    else:
        return percentage
```

### Progress Direction

| Direction | Use Case | Example |
|-----------|----------|---------|
| `buildup` | Increasing toward target | "Work toward 10K steps daily" |
| `countdown` | Decreasing toward target | "Reduce calories to 2000 daily" |

## Configuration Options

### Core Parameters
- **target** (required): Target value for 100% score
- **unit** (required): Measurement unit
- **maximum_cap** (default: 100): Maximum score cap
- **minimum_threshold** (default: 0): Minimum score floor
- **progress_direction**: "buildup" or "countdown"

### Advanced Settings
- **scaling_factor**: Custom scaling multiplier
- **curve_type**: Linear, exponential, or logarithmic scoring curves
- **plateau_range**: Target range for 100% scoring

## Use Cases

### Perfect Fits for Proportional
- **Progressive goals:** "Work toward 10,000 steps daily"
- **Gradual improvements:** "Increase water intake toward 8 glasses"
- **Skill building:** "Build up to 30g fiber daily" 
- **Habit formation:** "Gradually increase meditation time"
- **Flexible targets:** "Improve sleep duration toward 8 hours"

### Not Suitable For
- **Binary compliance:** "Take medication daily" → Use SC-BINARY-THRESHOLD
- **Frequency patterns:** "Exercise 3+ times per week" → Use SC-MINIMUM-FREQUENCY
- **Zero tolerance:** "No smoking" → Use SC-WEEKLY-ELIMINATION
- **Zone-based:** "Sleep 7-9 hours optimally" → Use SC-ZONE-BASED

## Validation Rules

1. **Target Required:** Valid numeric target > 0
2. **Unit Required:** Must specify measurement unit
3. **Cap Logic:** maximum_cap ≥ minimum_threshold
4. **Direction:** progress_direction must be "buildup" or "countdown"

## Testing

```python
# Test proportional algorithm
def test_proportional():
    algorithm = create_daily_proportional(
        target=10000,
        unit="steps",
        maximum_cap=100,
        minimum_threshold=20
    )
    
    # Test cases
    assert algorithm.calculate_score(0) == 20      # Minimum threshold
    assert algorithm.calculate_score(5000) == 50   # 50% of target
    assert algorithm.calculate_score(10000) == 100 # 100% of target
    assert algorithm.calculate_score(15000) == 100 # Capped at maximum
    
    print("✅ Proportional algorithm tests passed!")
```

## Frequency Variation

### SC-PROPORTIONAL-FREQUENCY

For weekly frequency-based proportional scoring:

```json
{
  "config_id": "SC-PROPORTIONAL-FREQ-EXERCISE_5_DAYS",
  "configuration_json": {
    "method": "proportional",
    "evaluation_pattern": "frequency",
    "schema": {
      "target_frequency": 5,
      "total_days": 7,
      "frequency_requirement": "work toward 5 days per week"
    }
  }
}
```

**Scoring Logic:**
```python
score = (actual_frequency_days / target_frequency) * 100
# 3 days out of 5 target = 60 points
# 5 days out of 5 target = 100 points  
# 7 days out of 5 target = 100 points (capped)
```

## Real-World Examples

### Step Goal Progression
```json
{
  "config_id": "SC-PROPORTIONAL-DAILY-STEPS_10000",
  "recommendation_text": "Work toward 10,000 steps daily",
  "schema": {
    "target": 10000,
    "unit": "steps",
    "maximum_cap": 100,
    "minimum_threshold": 10,
    "progress_direction": "buildup"
  }
}
```
**Results:**
- 2,000 steps = 20 points
- 5,000 steps = 50 points  
- 10,000 steps = 100 points
- 12,000 steps = 100 points (capped)

### Water Intake Building
```json
{
  "config_id": "SC-PROPORTIONAL-DAILY-WATER_8_GLASSES",
  "recommendation_text": "Gradually increase water intake toward 8 glasses daily",
  "schema": {
    "target": 8,
    "unit": "glasses", 
    "maximum_cap": 100,
    "minimum_threshold": 25,
    "progress_direction": "buildup"
  }
}
```
**Results:**
- 2 glasses = 25 points (minimum threshold)
- 4 glasses = 50 points
- 6 glasses = 75 points
- 8 glasses = 100 points

### Calorie Reduction
```json
{
  "config_id": "SC-PROPORTIONAL-DAILY-CALORIES_REDUCTION",
  "recommendation_text": "Reduce daily calories toward 2000",
  "schema": {
    "target": 2000,
    "unit": "calories",
    "maximum_cap": 100, 
    "minimum_threshold": 0,
    "progress_direction": "countdown"
  }
}
```
**Results (countdown logic):**
- 3000 calories = 0 points (150% of target)
- 2500 calories = 50 points (125% of target)  
- 2000 calories = 100 points (target achieved)
- 1800 calories = 100 points (below target, capped)

---

*For binary achievement patterns, see [Binary Threshold](binary-threshold.md)*  
*For frequency-based patterns, see [SC-MINIMUM-FREQUENCY](SC-MINIMUM-FREQUENCY.md)*