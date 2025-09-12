# SC-WEEKLY-ELIMINATION Algorithm

## Overview
**SC-WEEKLY-ELIMINATION** scores based on complete elimination of unwanted behaviors across an entire week. Any violation during the week results in failure for the entire weekly period.

## Algorithm Type
- **Pattern**: Weekly Elimination Block
- **Evaluation Period**: Weekly (7 days)
- **Scoring**: Binary (100 or 0)
- **Logic**: Zero tolerance - any violation fails the entire week

## Formula
```python
def calculate_weekly_elimination_score(daily_values, elimination_threshold, comparison_operator):
    """
    Calculate score based on complete elimination across entire week
    
    Args:
        daily_values: List of daily measurements for the week [day1, day2, ..., day7]
        elimination_threshold: The threshold for elimination (usually 0)
        comparison_operator: Usually "==" for exact match or "<=" for at-or-below
    
    Returns:
        100 if ALL days meet elimination criteria, else 0
    """
    for daily_value in daily_values:
        if comparison_operator == "==":
            if daily_value != elimination_threshold:
                return 0  # Any violation = failure for entire week
        elif comparison_operator == "<=":
            if daily_value > elimination_threshold:
                return 0  # Any violation = failure for entire week
        elif comparison_operator == ">=":
            if daily_value < elimination_threshold:
                return 0  # Any violation = failure for entire week
    
    return 100  # All days met elimination criteria
```

## Use Cases

### Complete Ultra-Processed Food Elimination
- **Goal**: Eliminate ultra-processed foods entirely, every day of the week
- **Logic**: Check if `dietary_ultraprocessed_meals == 0` for ALL 7 days
- **Success**: All days = 0 → Score = 100 for the week
- **Failure**: Any day > 0 → Score = 0 for the entire week

**Example Week**:
```
Mon: 0 servings ✅
Tue: 0 servings ✅  
Wed: 1 serving ❌  <-- VIOLATION
Thu: 0 servings ✅
Fri: 0 servings ✅
Sat: 0 servings ✅
Sun: 0 servings ✅

Result: 0 (entire week failed due to Wednesday violation)
```

### Takeout Meal Strict Limits
- **Goal**: Limit takeout meals to ≤1 per week
- **Logic**: Check if weekly sum ≤ 1
- **Success**: Weekly total ≤ 1 → Score = 100
- **Failure**: Weekly total > 1 → Score = 0

### Complete Smoking Cessation
- **Goal**: No smoking whatsoever
- **Logic**: Check if `daily_smoking == 0` for ALL 7 days
- **Success**: All days smoke-free → Score = 100
- **Failure**: Any smoking day → Score = 0 for entire week

## Configuration Schema

```json
{
  "method": "weekly_elimination",
  "formula": "100 if all_days_meet_elimination_criteria else 0",
  "evaluation_pattern": "weekly_elimination",
  "schema": {
    "measurement_type": "weekly_elimination_achievement",
    "evaluation_period": "weekly_elimination",
    "success_criteria": "weekly_elimination_target",
    "calculation_method": "weekly_zero_tolerance",
    "tracked_metrics": ["dietary_ultraprocessed_meals"],
    "elimination_threshold": 0,
    "elimination_comparison": "==",
    "total_days": 7,
    "success_value": 100,
    "failure_value": 0,
    "tolerance_level": "zero",
    "evaluation_text": "eliminate entirely every day of the week"
  }
}
```

## Variant: Weekly Limit (Not Daily Elimination)

For recommendations like "≤1 takeout meal per week":

```json
{
  "method": "weekly_elimination",
  "evaluation_pattern": "weekly_limit",
  "schema": {
    "calculation_method": "weekly_sum_limit",
    "weekly_limit": 1,
    "weekly_comparison": "<=",
    "description": "Weekly sum must not exceed limit"
  }
}
```

```python
def calculate_weekly_limit_score(daily_values, weekly_limit):
    """
    Calculate score based on weekly sum not exceeding limit
    
    Args:
        daily_values: List of daily measurements for the week
        weekly_limit: Maximum allowed for entire week
    
    Returns:
        100 if weekly_sum <= weekly_limit, else 0
    """
    weekly_sum = sum(daily_values)
    return 100 if weekly_sum <= weekly_limit else 0
```

## Key Characteristics

1. **Zero Tolerance**: Any violation fails the entire week
2. **Binary Scoring**: Only 100 (success) or 0 (failure)
3. **Weekly Blocks**: Evaluation and scoring per week
4. **Fresh Start**: Reset every Monday regardless of previous week
5. **High Standard**: Designed for elimination/cessation goals

## Comparison to Other Algorithms

| Algorithm | Tolerance | Evaluation | Example |
|-----------|-----------|------------|---------|
| **SC-WEEKLY-ELIMINATION** | Zero | Weekly block | "0 ultra-processed foods all week" |
| **SC-DAILY-ELIMINATION** | Zero | Daily reset | "0 ultra-processed foods today, fresh start tomorrow" |
| **SC-MINIMUM-FREQUENCY** | Partial | Weekly count | "≤1 serving on at least 2 days/week" |
| **SC-BINARY-FREQUENCY** | Specific | Weekly pattern | "Meet goal exactly 5/7 days" |

## Implementation Variants

### Type 1: Daily Elimination (Most Strict)
Every single day must meet elimination criteria:
```python
# All days must equal 0
for day in week:
    if day != 0: return 0
return 100
```

### Type 2: Weekly Limit
Weekly sum must not exceed limit:
```python
# Weekly total must be ≤ limit
weekly_total = sum(week)
return 100 if weekly_total <= limit else 0
```

### Type 3: Monthly Elimination
Same logic but over 30-day periods (for very strict goals):
```python
# All 30 days must meet criteria
for day in month:
    if day != 0: return 0
return 100
```

## Examples

### REC0022.3: Ultra-Processed Elimination
```json
{
  "config_id": "SC-WEEKLY-ELIM-ULTRAPROCESSED_COMPLETE",
  "elimination_threshold": 0,
  "elimination_comparison": "==",
  "description": "Eliminate ultra-processed foods entirely, every day of the week"
}
```

### REC0023.1: Weekly Takeout Limit
```json
{
  "config_id": "SC-WEEKLY-ELIM-TAKEOUT_1_PER_WEEK",
  "weekly_limit": 1,
  "weekly_comparison": "<=",
  "calculation_method": "weekly_sum_limit",
  "description": "Limit takeout meals to ≤1 per week"
}
```

### REC0055.3: Complete Smoking Cessation
```json
{
  "config_id": "SC-WEEKLY-ELIM-SMOKING_COMPLETE",
  "elimination_threshold": 0, 
  "elimination_comparison": "==",
  "description": "Complete smoking cessation - zero cigarettes"
}
```

## Psychological Impact

**Advantages**:
- Clear, unambiguous goals
- Strong motivation for consistency
- Builds elimination habits

**Challenges**:
- All-or-nothing can be demotivating
- One slip ruins entire week
- May discourage users with perfectionist tendencies

**Mitigation**:
- Use for appropriate elimination goals only
- Provide supportive messaging around "fresh start next week"
- Consider offering "streak" tracking in UI for motivation

---

**SC-WEEKLY-ELIMINATION provides strict binary feedback for behaviors that require complete elimination or very strict limits, with weekly accountability blocks.**