# WellPath Scoring Algorithms

Comprehensive scoring algorithms for health and wellness tracking applications. This package provides production-ready algorithm implementations with full JSON configuration support.

## Overview

The WellPath scoring system uses 6 primary algorithm types to handle different recommendation patterns:

- **Binary Threshold** - Pass/fail scoring for simple goals
- **Minimum Frequency** - Must achieve threshold on ≥X days per week
- **Weekly Elimination** - Zero tolerance patterns (any violation = failure)
- **Proportional** - Percentage-based scoring relative to targets
- **Zone-Based** - Multi-tier scoring based on performance zones
- **Composite Weighted** - Weighted combinations of multiple components

## Quick Start

```python
from algorithms import *

# Binary threshold example
algorithm = create_daily_binary_threshold(
    threshold=8,
    success_value=100,
    failure_value=0,
    description="8 glasses of water daily"
)
score = algorithm.calculate_score(9)  # Returns 100

# Minimum frequency example
from algorithms.minimum_frequency import calculate_minimum_frequency_score
result = calculate_minimum_frequency_score(
    daily_values=[350, 450, 380, 500, 420, 390, 370],  # Weekly caffeine intake
    daily_threshold=400,
    daily_comparison="<=",
    required_days=5
)
# Returns {'score': 100, 'successful_days': 5, 'threshold_met': True, ...}
```

## Algorithm Types

### 1. Binary Threshold (`binary_threshold.py`)
**Purpose:** Simple pass/fail scoring based on meeting a threshold
**Pattern:** Daily or frequency-based evaluation
**Scoring:** Binary (100 or 0)

```python
# Daily binary threshold
water_algo = create_daily_binary_threshold(
    threshold=8,
    success_value=100, 
    failure_value=0,
    description="Daily water intake goal"
)

# Frequency binary threshold  
exercise_algo = create_frequency_binary_threshold(
    threshold=30,
    frequency_requirement="5 of 7 days",
    success_value=100,
    failure_value=0,
    description="Exercise 30+ minutes, 5 days/week"
)
```

### 2. Minimum Frequency (`minimum_frequency.py`) ⭐ NEW
**Purpose:** Must achieve threshold on minimum number of days
**Pattern:** Weekly evaluation with daily thresholds
**Scoring:** Binary (100 if ≥required_days, 0 otherwise)

```python
from algorithms.minimum_frequency import calculate_minimum_frequency_score

# Caffeine limit: ≤400mg on at least 5 days per week
result = calculate_minimum_frequency_score(
    daily_values=[350, 450, 380, 420, 370, 390, 410],
    daily_threshold=400,
    daily_comparison="<=", 
    required_days=5
)
# Returns: {'score': 100, 'successful_days': 6, 'threshold_met': True}
```

**Use Cases:**
- Caffeine limits (≤400mg on ≥2 days/week)
- Meal timing (finish eating by 7pm on ≥5 days/week)
- Exercise frequency (30+ min workouts on ≥3 days/week)

### 3. Weekly Elimination (`weekly_elimination.py`) ⭐ NEW
**Purpose:** Zero tolerance patterns - any violation fails entire week
**Pattern:** Weekly evaluation with daily requirements  
**Scoring:** Binary (100 if perfect week, 0 if any violation)

```python
from algorithms.weekly_elimination import calculate_weekly_elimination_score

# Complete caffeine elimination after 2pm daily
result = calculate_weekly_elimination_score(
    daily_values=["13:30", "14:00", "13:45", "15:00", "13:30", "14:00", "13:00"],
    elimination_threshold="14:00",
    elimination_comparison="<="
)
# Returns: {'score': 0, 'violations': 1, 'violation_days': [4]}
```

**Use Cases:**
- Smoking cessation (0 cigarettes every day)
- Strict eating windows (within 8 hours every day)
- Complete elimination patterns (no ultra-processed foods)

### 4. Proportional (`proportional.py`)
**Purpose:** Percentage-based scoring relative to targets
**Pattern:** Gradual scoring from 0-100% based on achievement
**Scoring:** Continuous (0-100 based on percentage of target achieved)

```python
# Steps goal with proportional scoring
steps_algo = create_daily_proportional(
    target=10000,
    unit="steps",
    maximum_cap=100,
    minimum_threshold=20,
    description="Daily step goal"
)
score = steps_algo.calculate_score(7500)  # Returns 75
```

### 5. Zone-Based (`zone_based.py`) 
**Purpose:** Multi-tier scoring based on performance zones
**Pattern:** Define zones with different score values
**Scoring:** Zone-specific scores (e.g., Poor=25, Good=75, Excellent=100)

```python
# Sleep duration zones
sleep_zones = create_sleep_duration_zones()
sleep_algo = create_daily_zone_based(
    zones=sleep_zones,
    unit="hours",
    description="Sleep quality scoring"
)
score = sleep_algo.calculate_score(7.5)  # Returns zone-appropriate score
```

### 6. Composite Weighted (`composite_weighted.py`)
**Purpose:** Weighted combination of multiple components
**Pattern:** Combine multiple metrics with different weights
**Scoring:** Weighted average of component scores

```python
# Fitness composite score
fitness_algo = create_daily_composite(
    components=[
        Component("Exercise Duration", weight=0.4, target=30, unit="minutes"),
        Component("Steps", weight=0.3, target=10000, unit="steps"), 
        Component("Active Minutes", weight=0.3, target=150, unit="minutes")
    ],
    description="Overall fitness score"
)
```

## Configuration Integration

All algorithms integrate with JSON configuration files:

```json
{
  "config_id": "SC-MIN-FREQ-CAFFEINE_400MG_2_DAYS",
  "scoring_method": "minimum_frequency",
  "configuration_json": {
    "method": "minimum_frequency",
    "formula": "100 if days_meeting_threshold >= required_days else 0",
    "schema": {
      "daily_threshold": 400,
      "daily_comparison": "<=",
      "required_days": 2,
      "total_days": 7,
      "success_value": 100,
      "failure_value": 0
    }
  }
}
```

## Testing

Comprehensive test suite available:

```bash
# Test individual algorithm functions
python -m pytest tests/test_algorithms.py

# Test JSON configurations
python test_complex_config_validation.py "path/to/config.json"

# Test all generated configurations
python tests/test_with_csv_configs.py
```

## Support Functions

### Validation Functions
- `validate_minimum_frequency_config(config)` - Validate minimum frequency configurations
- `validate_weekly_elimination_config(config)` - Validate weekly elimination configurations

### Single Day Functions  
- `calculate_single_day_minimum_frequency_score()` - Daily contribution to minimum frequency
- `calculate_single_day_elimination_score()` - Daily contribution to weekly elimination

### Specialized Functions
- `calculate_weekly_limit_score()` - Weekly sum limits (e.g., ≤2 takeout meals/week)
- `calculate_monthly_limit_score()` - Monthly sum limits

## File Structure

```
src/algorithms/
├── __init__.py                    # Main exports
├── binary_threshold.py           # Binary threshold algorithms
├── minimum_frequency.py          # Minimum frequency algorithms ⭐
├── weekly_elimination.py         # Weekly elimination algorithms ⭐
├── proportional.py               # Proportional algorithms
├── zone_based.py                 # Zone-based algorithms
├── composite_weighted.py         # Composite weighted algorithms
├── constrained_weekly_allowance.py
├── categorical_filter_threshold.py
└── README.md                     # This file
```

## Algorithm Selection Guide

| Recommendation Pattern | Algorithm Type | Example |
|------------------------|----------------|---------|
| "Complete X daily" | Binary Threshold | "Complete 30min workout daily" |
| "X on at least Y days/week" | Minimum Frequency | "≤400mg caffeine on ≥5 days/week" |
| "X every single day" | Weekly Elimination | "No smoking every day" |
| "Gradually improve X" | Proportional | "Increase steps toward 10,000" |
| "Different levels of X" | Zone-Based | "Sleep 7-9 hours (zones)" |
| "Balance multiple Xs" | Composite | "Overall fitness (exercise + steps + sleep)" |

## Production Usage

1. **Generate Configurations:** Use the recommendation algorithm generator
2. **Load JSON Configs:** Parse generated configuration files  
3. **Create Algorithm Instances:** Use factory functions or direct imports
4. **Calculate Scores:** Call appropriate scoring functions with user data
5. **Handle Results:** Process returned score objects with detailed breakdowns

## Recent Updates (2024-01-15)

- ✅ **Added SC-MINIMUM-FREQUENCY algorithm** - Handle "at least X days per week" patterns
- ✅ **Added SC-WEEKLY-ELIMINATION algorithm** - Handle zero tolerance patterns  
- ✅ **Updated all algorithm exports** in `__init__.py`
- ✅ **Added comprehensive validation functions**
- ✅ **Enhanced JSON configuration support**
- ✅ **Added single-day scoring functions for real-time feedback**

---

*For detailed algorithm-specific documentation, see `/docs/algorithms/` directory.*