# Constrained Weekly Allowance Algorithm (SC-CONSTRAINED-WEEKLY-ALLOWANCE)

Weekly budget/allowance-based scoring with penalty systems for exceeding limits.

## Overview

The Constrained Weekly Allowance algorithm tracks weekly consumption against predefined allowances or budgets, applying penalty-based scoring when limits are exceeded. It's ideal for "treat" allowances, cheat meals, or controlled indulgences.

## Algorithm Types

### SC-CONSTRAINED-WEEKLY-ALLOWANCE
**Purpose:** Weekly budget tracking with penalty scoring  
**Pattern:** Weekly sum vs. allowance with graduated penalties  
**Evaluation:** Weekly  
**Scoring:** Penalty-based (100 down to minimum based on excess)

### SC-CONSTRAINED-MONTHLY-ALLOWANCE
**Purpose:** Monthly budget tracking for longer-term allowances  
**Pattern:** Monthly sum vs. allowance with penalty scoring  
**Evaluation:** Monthly  
**Scoring:** Similar penalty structure over monthly periods

## Configuration Schema

```json
{
  "config_id": "SC-CONSTRAINED-WEEKLY-TAKEOUT_2_MEALS",
  "scoring_method": "constrained_weekly_allowance",
  "configuration_json": {
    "method": "constrained_weekly_allowance",
    "formula": "max(minimum_score, base_score - (excess_amount × penalty_per_excess))",
    "evaluation_pattern": "weekly",
    "schema": {
      "measurement_type": "weekly_budget",
      "evaluation_period": "weekly",
      "success_criteria": "allowance_compliance",
      "calculation_method": "penalty_based_scoring",
      "tracked_metrics": ["takeout_meals"],
      "weekly_allowance": 2,
      "penalty_per_excess": 25,
      "base_score": 100,
      "minimum_score": 0,
      "unit": "meals",
      "grace_period": 0,
      "description": "Weekly takeout meal allowance with penalty scoring"
    }
  },
  "metadata": {
    "recommendation_text": "Limit takeout meals to 2 per week",
    "recommendation_id": "REC0005.2",
    "metric_id": "takeout_meals"
  }
}
```

## Implementation

### Python Usage

```python
from algorithms.constrained_weekly_allowance import calculate_weekly_allowance_score

# Takeout meal allowance example
result = calculate_weekly_allowance_score(
    daily_values=[1, 0, 1, 0, 0, 1, 1],  # 4 takeout meals this week
    weekly_allowance=2,
    penalty_per_excess=25,
    base_score=100,
    minimum_score=0
)
# Returns: {'score': 50, 'total_consumed': 4, 'allowance': 2, 'excess': 2, 'penalty_applied': 50}
```

### Direct Function Usage

```python
from algorithms.constrained_weekly_allowance import ConstrainedAllowanceAlgorithm, AllowanceConfig

config = AllowanceConfig(
    weekly_allowance=2,
    penalty_per_excess=25,
    base_score=100,
    minimum_score=0,
    unit="meals"
)

algorithm = ConstrainedAllowanceAlgorithm(config)
result = algorithm.calculate_score(weekly_consumption_data)
```

## Scoring Logic

### Weekly Allowance Scoring

```python
def calculate_weekly_allowance_score(daily_values, weekly_allowance, penalty_per_excess, base_score=100, minimum_score=0):
    # Calculate weekly total
    weekly_total = sum(daily_values)
    
    # Check if within allowance
    if weekly_total <= weekly_allowance:
        return {
            'score': base_score,
            'total_consumed': weekly_total,
            'allowance': weekly_allowance,
            'excess': 0,
            'penalty_applied': 0,
            'within_allowance': True
        }
    
    # Calculate excess and penalty
    excess = weekly_total - weekly_allowance
    total_penalty = excess * penalty_per_excess
    final_score = max(minimum_score, base_score - total_penalty)
    
    return {
        'score': final_score,
        'total_consumed': weekly_total,
        'allowance': weekly_allowance,
        'excess': excess,
        'penalty_applied': total_penalty,
        'within_allowance': False
    }
```

### Penalty Calculation Options

#### Linear Penalty
```python
penalty = excess_amount * penalty_per_excess
final_score = max(minimum_score, base_score - penalty)
```

#### Graduated Penalty
```python
def graduated_penalty(excess, penalty_rates):
    total_penalty = 0
    remaining_excess = excess
    
    for threshold, rate in penalty_rates:
        if remaining_excess <= 0:
            break
        
        penalty_amount = min(remaining_excess, threshold) * rate
        total_penalty += penalty_amount
        remaining_excess -= threshold
    
    return total_penalty
```

## Configuration Options

### Core Parameters
- **weekly_allowance** (required): Maximum allowed weekly consumption
- **penalty_per_excess** (required): Penalty points per unit over allowance
- **base_score** (default: 100): Starting score when within allowance
- **minimum_score** (default: 0): Floor score regardless of excess

### Advanced Settings
- **grace_period**: Allow small overages without penalty
- **penalty_structure**: "linear" or "graduated"
- **reset_day**: Day of week when allowance resets (default: Monday)
- **rollover_allowed**: Whether unused allowance carries forward

## Use Cases

### Perfect Fits for Constrained Weekly Allowance
- **Treat allowances**: "Allow 2 desserts per week"
- **Cheat meals**: "1-2 cheat meals per week maximum"
- **Takeout limits**: "Limit restaurant meals to 3 per week"
- **Alcohol budgets**: "Maximum 4 drinks per week"
- **Screen time**: "Limit recreational screen time to 10 hours/week"

### Not Suitable For
- **Zero tolerance**: "No smoking ever" → Use SC-WEEKLY-ELIMINATION
- **Daily limits**: "≤2 cups coffee daily" → Use SC-BINARY-THRESHOLD
- **Progressive goals**: "Increase exercise gradually" → Use SC-PROPORTIONAL

## Validation Rules

1. **Positive Allowance**: weekly_allowance must be > 0
2. **Valid Penalty**: penalty_per_excess must be > 0
3. **Score Range**: base_score ≥ minimum_score
4. **Valid Unit**: unit must be specified
5. **Realistic Penalties**: Total possible penalty shouldn't exceed reasonable range

## Testing

```python
# Test constrained weekly allowance algorithm
def test_weekly_allowance():
    # Test case 1: Within allowance
    result_within = calculate_weekly_allowance_score(
        daily_values=[1, 0, 1, 0, 0, 0, 0],  # 2 meals
        weekly_allowance=2,
        penalty_per_excess=25
    )
    assert result_within['score'] == 100
    assert result_within['within_allowance'] == True
    
    # Test case 2: Exceeds allowance
    result_excess = calculate_weekly_allowance_score(
        daily_values=[1, 1, 1, 0, 1, 0, 0],  # 4 meals
        weekly_allowance=2,
        penalty_per_excess=25
    )
    assert result_excess['score'] == 50  # 100 - (2 × 25) = 50
    assert result_excess['excess'] == 2
    
    print("✅ Constrained weekly allowance tests passed!")
```

## Penalty Structure Examples

### Linear Penalty Structure
```python
# Each excess unit costs the same penalty
weekly_allowance = 2
penalty_per_excess = 25

# Examples:
# 3 meals = 100 - (1 × 25) = 75 points
# 4 meals = 100 - (2 × 25) = 50 points  
# 5 meals = 100 - (3 × 25) = 25 points
# 6+ meals = 0 points (minimum score)
```

### Graduated Penalty Structure
```python
# Increasing penalties for larger excesses
penalty_rates = [
    (1, 20),  # First excess unit: 20 points
    (1, 30),  # Second excess unit: 30 points
    (float('inf'), 40)  # Additional units: 40 points each
]

# Examples:
# 3 meals = 100 - 20 = 80 points
# 4 meals = 100 - 20 - 30 = 50 points
# 5 meals = 100 - 20 - 30 - 40 = 10 points
```

## Real-World Examples

### Takeout Meal Allowance
```json
{
  "config_id": "SC-CONSTRAINED-WEEKLY-TAKEOUT_2_MEALS",
  "recommendation_text": "Limit takeout meals to 2 per week",
  "schema": {
    "weekly_allowance": 2,
    "penalty_per_excess": 25,
    "base_score": 100,
    "minimum_score": 0,
    "unit": "meals"
  }
}
```

**Results:**
- 2 or fewer meals = 100 points
- 3 meals = 75 points (25 point penalty)
- 4 meals = 50 points (50 point penalty)
- 6+ meals = 0 points (maximum penalty reached)

### Dessert Allowance  
```json
{
  "config_id": "SC-CONSTRAINED-WEEKLY-DESSERTS_3_SERVINGS",
  "recommendation_text": "Allow up to 3 dessert servings per week",
  "schema": {
    "weekly_allowance": 3,
    "penalty_per_excess": 20,
    "base_score": 100,
    "minimum_score": 10,
    "unit": "servings"
  }
}
```

### Alcohol Budget
```json
{
  "config_id": "SC-CONSTRAINED-WEEKLY-ALCOHOL_4_DRINKS",
  "recommendation_text": "Limit alcohol consumption to 4 drinks per week",
  "schema": {
    "weekly_allowance": 4,
    "penalty_per_excess": 15,
    "base_score": 100,
    "minimum_score": 0,
    "unit": "drinks",
    "grace_period": 0.5
  }
}
```

## Advanced Features

### Rollover Allowances
```python
def calculate_with_rollover(current_week_data, unused_from_previous):
    effective_allowance = weekly_allowance + min(unused_from_previous, max_rollover)
    return calculate_weekly_allowance_score(current_week_data, effective_allowance, penalty_per_excess)
```

### Dynamic Penalties
```python
def dynamic_penalty_rate(excess_percentage):
    if excess_percentage <= 0.2:  # 20% over allowance
        return 10
    elif excess_percentage <= 0.5:  # 50% over allowance  
        return 20
    else:  # More than 50% over
        return 30
```

---

*For zero-tolerance patterns, see [Weekly Elimination](SC-WEEKLY-ELIMINATION.md)*  
*For simple binary limits, see [Binary Threshold](binary-threshold.md)*