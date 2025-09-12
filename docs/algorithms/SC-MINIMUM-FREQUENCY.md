# SC-MINIMUM-FREQUENCY Algorithm

## Overview
**SC-MINIMUM-FREQUENCY** scores based on achieving a threshold on a minimum number of days within a weekly evaluation period. Success requires meeting the criteria on at least X days per week.

## Algorithm Type
- **Pattern**: Minimum Achievement Frequency
- **Evaluation Period**: Weekly (7 days)
- **Scoring**: Binary (100 or 0)
- **Logic**: Count successful days, compare to minimum requirement

## Formula
```python
def calculate_minimum_frequency_score(daily_values, daily_threshold, daily_comparison, required_days):
    """
    Calculate score based on minimum days meeting threshold per week
    
    Args:
        daily_values: List of daily measurements for the week [day1, day2, ..., day7]
        daily_threshold: The threshold value for each day
        daily_comparison: Comparison operator ("<=", ">=", "==")
        required_days: Minimum number of days that must meet threshold
    
    Returns:
        100 if successful_days >= required_days, else 0
    """
    successful_days = 0
    
    for daily_value in daily_values:
        if daily_comparison == "<=":
            if daily_value <= daily_threshold:
                successful_days += 1
        elif daily_comparison == ">=":
            if daily_value >= daily_threshold:
                successful_days += 1
        elif daily_comparison == "==":
            if daily_value == daily_threshold:
                successful_days += 1
    
    return 100 if successful_days >= required_days else 0
```

## Use Cases

### Ultra-Processed Foods Limitation
- **Goal**: Limit ultra-processed foods to ≤1 serving on at least 2 days per week
- **Logic**: Count days where `dietary_ultraprocessed_meals <= 1`
- **Success**: If count ≥ 2 days → Score = 100
- **Failure**: If count < 2 days → Score = 0

**Example Week**:
```
Mon: 5 servings ❌  (exceeds threshold)
Tue: 0 servings ✅  (meets threshold) 
Wed: 10 servings ❌ (exceeds threshold)
Thu: 1 serving ✅   (meets threshold)
Fri: 3 servings ❌  (exceeds threshold)
Sat: 2 servings ❌  (exceeds threshold)
Sun: 1 serving ✅   (meets threshold)

Successful days: 3 (Tue, Thu, Sun)
Required days: 2
Result: 100 (success)
```

### Water Intake Goals
- **Goal**: Drink ≥8 cups of water on at least 5 days per week
- **Logic**: Count days where `dietary_water >= 1893` (mL)
- **Success**: If count ≥ 5 days → Score = 100
- **Failure**: If count < 5 days → Score = 0

## Configuration Schema

```json
{
  "method": "minimum_frequency",
  "formula": "100 if successful_days >= required_days else 0",
  "evaluation_pattern": "weekly_minimum_frequency",
  "schema": {
    "measurement_type": "minimum_frequency_achievement",
    "evaluation_period": "weekly_minimum_frequency",
    "success_criteria": "minimum_frequency_target",
    "calculation_method": "daily_threshold_frequency_count",
    "tracked_metrics": ["dietary_ultraprocessed_meals"],
    "daily_threshold": 1,
    "daily_comparison": "<=",
    "required_days": 2,
    "total_days": 7,
    "success_value": 100,
    "failure_value": 0,
    "frequency_requirement": "2 of 7 days",
    "frequency_requirement_text": "at least 2 days per week"
  }
}
```

## Key Characteristics

1. **Binary Scoring**: Only 100 (success) or 0 (failure)
2. **Weekly Evaluation**: Scores calculated per week
3. **Flexible Thresholds**: Can use <=, >=, or == comparisons
4. **Minimum Achievement**: Must meet threshold on at least X days
5. **Reset Weekly**: Fresh start every Monday

## Comparison to Other Algorithms

| Algorithm | Evaluation | Success Criteria | Example |
|-----------|------------|------------------|---------|
| **SC-MINIMUM-FREQUENCY** | Weekly | ≥X days meeting threshold | "≤1 serving on 2+ days/week" |
| **SC-PROPORTIONAL-FREQUENCY** | Weekly | Proportional to days met | "Score = (days_met / required_days) × 100" |
| **SC-BINARY-FREQUENCY** | Weekly | ALL required days met | "Meet threshold on exactly 5/7 days" |
| **SC-BINARY-DAILY** | Daily | Single day achievement | "0 servings today" |

## Implementation Notes

- **Week Definition**: Monday-Sunday cycles
- **Data Requirements**: Need all 7 daily values for weekly calculation
- **Missing Data**: Days with missing data count as "not meeting threshold"
- **Progress Direction**: Can be "buildup" (≥) or "countdown" (≤) depending on metric type

## Examples

### REC0022.1: Ultra-Processed Foods
```json
{
  "config_id": "SC-MIN-FREQ-ULTRAPROCESSED_1_SERVING_2_DAYS",
  "daily_threshold": 1,
  "daily_comparison": "<=",
  "required_days": 2,
  "description": "Limit ultra-processed foods to ≤1 serving on at least 2 days per week"
}
```

### REC0020.2: Water Intake  
```json
{
  "config_id": "SC-MIN-FREQ-WATER_8_CUPS_5_DAYS",
  "daily_threshold": 1893,
  "daily_comparison": ">=", 
  "required_days": 5,
  "description": "Drink ≥8 cups water on at least 5 days per week"
}
```

---

**SC-MINIMUM-FREQUENCY provides clear binary feedback for goals requiring consistent but not perfect adherence to healthy behaviors.**