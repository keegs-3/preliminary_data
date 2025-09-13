# Sleep Composite Algorithm (SC-COMPOSITE-SLEEP-ADVANCED)

Advanced sleep scoring algorithm combining duration zones with schedule consistency tracking.

## Overview

The Sleep Composite algorithm provides sophisticated sleep quality assessment by evaluating both sleep duration (within optimal ranges) and schedule consistency. It uses a weighted 55/45 approach balancing sleep quantity with routine stability.

## Algorithm Types

### SC-COMPOSITE-SLEEP-ADVANCED
**Purpose:** Comprehensive sleep scoring with duration and consistency  
**Pattern:** Multi-component weighted scoring with zone-based duration and rolling average consistency  
**Evaluation:** Daily composite scoring  
**Scoring:** Weighted average (0-100)

## Configuration Schema

```json
{
  "config_id": "SC-COMP-SLEEP-ADVANCED-7TO9H_CONSISTENT",
  "scoring_method": "sleep_composite", 
  "configuration_json": {
    "method": "sleep_composite",
    "formula": "weighted_average([duration_zone_score * 0.55, sleep_consistency * 0.225, wake_consistency * 0.225])",
    "evaluation_pattern": "daily_composite",
    "schema": {
      "measurement_type": "composite",
      "evaluation_period": "daily",
      "success_criteria": "weighted_combination",
      "calculation_method": "sleep_composite_advanced",
      "tracked_metrics": ["sleep_time", "wake_time"],
      "calculated_metrics": ["sleep_duration"],
      "components": {
        "sleep_duration": {
          "weight": 55,
          "algorithm": "zone_based_5tier",
          "zones": [
            {"range": [0, 5], "score": 20, "label": "Critical"},
            {"range": [5, 6], "score": 40, "label": "Poor"},
            {"range": [6, 7], "score": 60, "label": "Fair"},
            {"range": [7, 9], "score": 100, "label": "Optimal"},
            {"range": [9, 12], "score": 80, "label": "Excessive"}
          ],
          "unit": "hours"
        },
        "sleep_time_consistency": {
          "weight": 22.5,
          "algorithm": "rolling_average_tolerance",
          "tolerance_minutes": 60,
          "evaluation_period": "weekly"
        },
        "wake_time_consistency": {
          "weight": 22.5,
          "algorithm": "rolling_average_tolerance", 
          "tolerance_minutes": 60,
          "evaluation_period": "weekly"
        }
      },
      "minimum_threshold": 0,
      "maximum_cap": 100,
      "unit": "composite_score",
      "progress_direction": "buildup",
      "description": "Advanced sleep composite: duration zones + schedule consistency"
    }
  },
  "metadata": {
    "recommendation_text": "Sleep 7-9 hours nightly with consistent sleep and wake times",
    "recommendation_id": "REC0004.3",
    "metric_id": "sleep_duration"
  }
}
```

## Implementation

### Python Usage

```python
from algorithms import create_sleep_composite

# Create sleep composite algorithm with default 55/45 weighting
sleep_algo = create_sleep_composite(
    optimal_duration_range=(7, 9),
    consistency_tolerance_minutes=60,
    description="Comprehensive sleep quality scoring"
)

# Calculate scores with sleep data
sleep_data = {
    'sleep_duration': 7.5,        # hours
    'sleep_time_consistency': 45,  # minutes variance from average
    'wake_time_consistency': 30    # minutes variance from average  
}

score = sleep_algo.calculate_score(sleep_data)  # Returns weighted composite score
```

### Direct Function Usage

```python
from algorithms.sleep_composite import SleepCompositeAlgorithm, SleepCompositeConfig

config = SleepCompositeConfig(
    optimal_duration_range=(7, 9),
    duration_weight=0.55,
    sleep_consistency_weight=0.225,
    wake_consistency_weight=0.225,
    consistency_tolerance_minutes=60
)

algorithm = SleepCompositeAlgorithm(config)
result = algorithm.calculate_score(sleep_data)
```

## Scoring Logic

### Component Breakdown

#### 1. Sleep Duration (55% Weight)
Uses 5-tier zone-based scoring for sleep duration:

```python
def score_duration(hours):
    if 0 <= hours < 5:    return 20   # Critical
    elif 5 <= hours < 6:  return 40   # Poor  
    elif 6 <= hours < 7:  return 60   # Fair
    elif 7 <= hours <= 9: return 100  # Optimal
    elif 9 < hours <= 12: return 80   # Excessive
    else:                 return 0    # Invalid
```

#### 2. Sleep Time Consistency (22.5% Weight)  
Rolling average tolerance method:

```python
def score_sleep_consistency(sleep_times, tolerance_minutes=60):
    compliant_nights = 0
    rolling_average = calculate_rolling_average(sleep_times)
    
    for night_time in sleep_times:
        variance = abs(night_time - rolling_average) 
        if variance <= tolerance_minutes:
            compliant_nights += 1
    
    return (compliant_nights / len(sleep_times)) * 100
```

#### 3. Wake Time Consistency (22.5% Weight)
Same methodology as sleep time consistency, applied to wake times.

### Rolling Average Calculation

```python
def calculate_rolling_average(time_series):
    # Progressive calculation:
    # Night 1: time1 = baseline
    # Night 2: avg = (time1 + time2) / 2  
    # Night 3: avg = (time1 + time2 + time3) / 3
    # Continue through 7 days, then use rolling 7-day window
    
    if len(time_series) <= 7:
        return sum(time_series) / len(time_series)
    else:
        # Use rolling 7-day window for weeks 2+
        recent_week = time_series[-7:]
        return sum(recent_week) / 7
```

### Final Score Calculation

```python
def calculate_composite_score(duration_hours, sleep_consistency_variance, wake_consistency_variance):
    duration_score = score_duration(duration_hours)
    sleep_consistency_score = score_consistency(sleep_consistency_variance, tolerance=60)
    wake_consistency_score = score_consistency(wake_consistency_variance, tolerance=60)
    
    composite_score = (
        duration_score * 0.55 +
        sleep_consistency_score * 0.225 + 
        wake_consistency_score * 0.225
    )
    
    return min(100, max(0, composite_score))
```

## Use Cases

### Perfect Fits for Sleep Composite
- **Comprehensive sleep goals:** "Sleep 7-9 hours with consistent schedule"
- **Sleep optimization:** "Improve sleep quality through duration and routine"
- **Circadian rhythm support:** "Maintain regular sleep/wake times"
- **Health condition sleep requirements:** "Consistent 8-hour sleep schedule for recovery"

### Not Suitable For
- **Simple duration goals:** "Sleep 8 hours daily" → Use SC-ZONE-BASED or SC-BINARY-THRESHOLD
- **Schedule-only tracking:** "Sleep at same time daily" → Use consistency-specific algorithm
- **Sleep onset tracking:** "Fall asleep within 15 minutes" → Use SC-BINARY-THRESHOLD

## Validation Rules

1. **Weight Distribution:** All component weights must sum to 100% (55% + 22.5% + 22.5% = 100%)
2. **Duration Zones:** Must define complete range coverage (0-12+ hours)
3. **Consistency Tolerance:** Tolerance minutes must be positive integer
4. **Input Requirements:** Requires sleep_time, wake_time, and calculated sleep_duration

## Testing

```python
# Test sleep composite algorithm
def test_sleep_composite():
    algorithm = create_sleep_composite(
        optimal_duration_range=(7, 9),
        consistency_tolerance_minutes=60
    )
    
    # Test optimal sleep scenario
    optimal_data = {
        'sleep_duration': 8.0,           # Optimal range
        'sleep_time_consistency': 30,    # Within tolerance
        'wake_time_consistency': 45      # Within tolerance  
    }
    score = algorithm.calculate_score(optimal_data)
    assert 90 <= score <= 100  # Should score very high
    
    # Test poor duration scenario
    poor_duration_data = {
        'sleep_duration': 4.5,           # Critical range
        'sleep_time_consistency': 15,    # Good consistency
        'wake_time_consistency': 20      # Good consistency
    }
    score = algorithm.calculate_score(poor_duration_data)
    assert 30 <= score <= 50  # Duration heavily weighted
    
    print("✅ Sleep composite tests passed!")
```

## Progressive Scoring

Sleep Composite provides daily progressive scoring showing cumulative sleep quality:

```python
def calculate_progressive_scores(weekly_sleep_data):
    # Each day shows composite score for that specific night
    # Rolling average consistency improves over time
    progressive_scores = []
    
    for day, sleep_data in enumerate(weekly_sleep_data):
        # Use data up to current day for rolling averages
        current_data = weekly_sleep_data[:day+1]
        score = calculate_daily_composite(sleep_data, current_data)
        progressive_scores.append(score)
    
    return progressive_scores
```

## Real-World Examples

### Comprehensive Sleep Optimization
```json
{
  "config_id": "SC-COMP-SLEEP-ADVANCED-7TO9H_CONSISTENT",
  "recommendation_text": "Sleep 7-9 hours nightly with consistent sleep and wake times",
  "schema": {
    "optimal_duration_range": [7, 9],
    "consistency_tolerance_minutes": 60,
    "duration_weight": 55,
    "sleep_consistency_weight": 22.5,
    "wake_consistency_weight": 22.5
  }
}
```

### Recovery-Focused Sleep
```json
{
  "config_id": "SC-COMP-SLEEP-RECOVERY-8H_STRICT",
  "recommendation_text": "Maintain 8-hour sleep schedule with strict consistency for recovery",
  "schema": {
    "optimal_duration_range": [7.5, 8.5],
    "consistency_tolerance_minutes": 30,
    "duration_weight": 60,
    "consistency_weight_combined": 40
  }
}
```

### Sleep Routine Establishment  
```json
{
  "config_id": "SC-COMP-SLEEP-ROUTINE-FOCUS",
  "recommendation_text": "Focus on consistent sleep/wake times while improving duration",
  "schema": {
    "optimal_duration_range": [6.5, 9],
    "consistency_tolerance_minutes": 45,
    "duration_weight": 40,
    "consistency_weight_combined": 60
  }
}
```

## Advanced Features

### Circadian Rhythm Support
- **Rolling average adaptation:** Gradually adjusts to patient's natural patterns
- **Tolerance flexibility:** Allows reasonable variance while maintaining routine
- **Progressive improvement:** Tracks consistency gains over time

### Clinical Integration
- **Sleep disorder monitoring:** Tracks both quantity and quality metrics
- **Treatment compliance:** Monitors adherence to sleep hygiene recommendations  
- **Recovery tracking:** Assesses sleep pattern improvements during treatment

---

*For simple duration tracking, see [SC-ZONE-BASED](zone-based.md)*  
*For basic sleep goals, see [SC-BINARY-THRESHOLD](binary-threshold.md)*