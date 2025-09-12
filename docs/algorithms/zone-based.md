# Zone-Based Algorithm (SC-ZONE-BASED)

Multi-tier scoring based on performance zones with different score values for different ranges.

## Overview

The Zone-Based algorithm defines multiple performance zones, each with specific score values. It's ideal for metrics where different ranges have different levels of optimality, rather than simple linear progression.

## Algorithm Types

### SC-ZONE-BASED-DAILY
**Purpose:** Daily zone-based evaluation  
**Pattern:** Multi-tier zones with specific scores  
**Evaluation:** Daily  
**Scoring:** Zone-specific scores (e.g., Poor=25, Good=75, Excellent=100)

### SC-ZONE-BASED-FREQUENCY
**Purpose:** Weekly frequency-based zone evaluation  
**Pattern:** Weekly evaluation with zone-based daily scoring  
**Evaluation:** Weekly  
**Scoring:** Average or frequency-based zone achievement

## Configuration Schema

```json
{
  "config_id": "SC-ZONE-BASED-SLEEP_DURATION_5_TIER",
  "scoring_method": "zone_based",
  "configuration_json": {
    "method": "zone_based",
    "formula": "score = zone.score where value in zone.range",
    "evaluation_pattern": "daily",
    "schema": {
      "measurement_type": "zone_based",
      "evaluation_period": "daily",
      "success_criteria": "zone_achievement",
      "calculation_method": "zone_mapping",
      "tracked_metrics": ["sleep_duration"],
      "zones": [
        {"min": 0, "max": 5, "score": 25, "label": "Poor"},
        {"min": 5, "max": 6.5, "score": 50, "label": "Fair"},
        {"min": 6.5, "max": 7.5, "score": 75, "label": "Good"},
        {"min": 7.5, "max": 9, "score": 100, "label": "Excellent"},
        {"min": 9, "max": 12, "score": 75, "label": "Too Much"}
      ],
      "tier_count": 5,
      "unit": "hours",
      "description": "Zone-based sleep duration scoring with optimal range"
    }
  },
  "metadata": {
    "recommendation_text": "Optimize sleep duration for quality rest",
    "recommendation_id": "REC0003.1",
    "metric_id": "sleep_duration"
  }
}
```

## Implementation

### Python Usage

```python
from algorithms import create_daily_zone_based, create_sleep_duration_zones

# Create predefined sleep duration zones
sleep_zones = create_sleep_duration_zones()
sleep_algo = create_daily_zone_based(
    zones=sleep_zones,
    unit="hours",
    description="Sleep quality scoring"
)

# Calculate scores
score_poor = sleep_algo.calculate_score(4.5)    # Returns 25 (Poor zone)
score_good = sleep_algo.calculate_score(7.0)    # Returns 75 (Good zone)  
score_excellent = sleep_algo.calculate_score(8.0) # Returns 100 (Excellent zone)
score_too_much = sleep_algo.calculate_score(10.0) # Returns 75 (Too Much zone)
```

### Custom Zone Definition

```python
from algorithms.zone_based import Zone, create_daily_zone_based

# Define custom heart rate zones
hr_zones = [
    Zone(min_val=0, max_val=60, score=25, label="Too Low"),
    Zone(min_val=60, max_val=100, score=100, label="Resting"),
    Zone(min_val=100, max_val=150, score=75, label="Active"),
    Zone(min_val=150, max_val=180, score=50, label="High"),
    Zone(min_val=180, max_val=220, score=25, label="Too High")
]

hr_algo = create_daily_zone_based(
    zones=hr_zones,
    unit="bpm",
    description="Heart rate zone scoring"
)
```

## Scoring Logic

### Zone Mapping

```python
def calculate_score(actual_value, zones):
    for zone in zones:
        if zone.min_val <= actual_value < zone.max_val:
            return zone.score
    
    # Handle edge case - value above highest zone
    if actual_value >= zones[-1].max_val:
        return zones[-1].score
    
    # Handle edge case - value below lowest zone  
    return zones[0].score
```

### Zone Definition

```python
class Zone:
    def __init__(self, min_val, max_val, score, label):
        self.min_val = min_val
        self.max_val = max_val
        self.score = score
        self.label = label
        
    def contains(self, value):
        return self.min_val <= value < self.max_val
```

## Zone Types

### 3-Tier Zones (Simple)
Basic three-level scoring for straightforward metrics:

```python
simple_zones = [
    Zone(0, 33, 25, "Low"),      # Below acceptable
    Zone(33, 67, 75, "Medium"),  # Acceptable range
    Zone(67, 100, 100, "High")   # Optimal range
]
```

### 5-Tier Zones (Detailed)
More nuanced scoring with optimal ranges and excess penalties:

```python
detailed_zones = [
    Zone(0, 20, 25, "Very Poor"),    # Critically low
    Zone(20, 40, 50, "Poor"),        # Below acceptable
    Zone(40, 70, 75, "Fair"),        # Acceptable
    Zone(70, 90, 100, "Good"),       # Optimal
    Zone(90, 100, 75, "Excessive")   # Too much of good thing
]
```

## Predefined Zone Sets

### Sleep Duration Zones
```python
sleep_zones = [
    Zone(0, 5, 25, "Insufficient"),    # < 5 hours
    Zone(5, 6.5, 50, "Poor"),          # 5-6.5 hours
    Zone(6.5, 7.5, 75, "Good"),        # 6.5-7.5 hours  
    Zone(7.5, 9, 100, "Excellent"),    # 7.5-9 hours (optimal)
    Zone(9, 12, 75, "Excessive")       # > 9 hours
]
```

### Exercise Intensity Zones  
```python
intensity_zones = [
    Zone(0, 50, 25, "Sedentary"),      # 0-50% max HR
    Zone(50, 60, 50, "Light"),         # 50-60% max HR
    Zone(60, 70, 75, "Moderate"),      # 60-70% max HR
    Zone(70, 85, 100, "Vigorous"),     # 70-85% max HR (optimal)
    Zone(85, 100, 75, "Maximum")       # 85-100% max HR
]
```

### Blood Pressure Zones
```python
bp_zones = [
    Zone(0, 90, 25, "Hypotension"),     # < 90 systolic
    Zone(90, 120, 100, "Normal"),       # 90-120 systolic (optimal)
    Zone(120, 130, 75, "Elevated"),     # 120-130 systolic  
    Zone(130, 140, 50, "Stage 1"),      # 130-140 systolic
    Zone(140, 200, 25, "Stage 2")       # > 140 systolic
]
```

## Use Cases

### Perfect Fits for Zone-Based
- **Sleep duration:** Optimal ranges with penalties for too little/much
- **Blood pressure:** Medical categories with optimal ranges  
- **Heart rate training:** Different intensity zones
- **Body metrics:** BMI, body fat percentage with healthy ranges
- **Performance metrics:** Where "more" isn't always better

### Not Suitable For
- **Simple binary goals:** "Complete workout" → Use SC-BINARY-THRESHOLD
- **Linear progression:** "Work toward 10K steps" → Use SC-PROPORTIONAL
- **Frequency patterns:** "Exercise 3+ times/week" → Use SC-MINIMUM-FREQUENCY
- **Zero tolerance:** "No smoking" → Use SC-WEEKLY-ELIMINATION

## Validation Rules

1. **Zone Coverage:** Zones must cover expected value range
2. **No Overlaps:** Zone ranges cannot overlap
3. **Ordered Ranges:** Zones must be in ascending order by min_val
4. **Valid Scores:** All zone scores must be 0-100
5. **Label Required:** Each zone must have descriptive label

## Testing

```python
# Test zone-based algorithm
def test_zone_based():
    zones = [
        Zone(0, 5, 25, "Poor"),
        Zone(5, 7.5, 75, "Good"), 
        Zone(7.5, 9, 100, "Excellent"),
        Zone(9, 12, 75, "Too Much")
    ]
    
    algorithm = create_daily_zone_based(
        zones=zones,
        unit="hours"
    )
    
    # Test cases
    assert algorithm.calculate_score(4.0) == 25    # Poor zone
    assert algorithm.calculate_score(7.0) == 75    # Good zone
    assert algorithm.calculate_score(8.0) == 100   # Excellent zone  
    assert algorithm.calculate_score(10.0) == 75   # Too Much zone
    
    print("✅ Zone-based algorithm tests passed!")
```

## Frequency Variation

### SC-ZONE-BASED-FREQUENCY

For weekly frequency-based zone evaluation:

```json
{
  "config_id": "SC-ZONE-BASED-FREQ-EXERCISE_INTENSITY",
  "configuration_json": {
    "method": "zone_based",
    "evaluation_pattern": "frequency",
    "schema": {
      "zones": [...],
      "frequency_requirement": "achieve optimal zone 5 days per week"
    }
  }
}
```

## Real-World Examples

### Sleep Duration Optimization
```json
{
  "config_id": "SC-ZONE-BASED-SLEEP_DURATION_OPTIMAL",
  "recommendation_text": "Optimize sleep duration for quality rest",
  "zones": [
    {"min": 0, "max": 6, "score": 25, "label": "Insufficient"},
    {"min": 6, "max": 7, "score": 50, "label": "Poor"},
    {"min": 7, "max": 8, "score": 75, "label": "Good"},
    {"min": 8, "max": 9, "score": 100, "label": "Excellent"},
    {"min": 9, "max": 12, "score": 75, "label": "Excessive"}
  ]
}
```
**Results:**
- 5.5 hours = 25 points (Insufficient)
- 6.5 hours = 50 points (Poor) 
- 7.5 hours = 75 points (Good)
- 8.5 hours = 100 points (Excellent)
- 10 hours = 75 points (Excessive)

### Heart Rate Training Zones
```json
{
  "config_id": "SC-ZONE-BASED-HEART_RATE_TRAINING",
  "recommendation_text": "Train in optimal heart rate zones",
  "zones": [
    {"min": 0, "max": 114, "score": 25, "label": "Recovery"},
    {"min": 114, "max": 133, "score": 50, "label": "Aerobic Base"},
    {"min": 133, "max": 152, "score": 75, "label": "Aerobic"},
    {"min": 152, "max": 171, "score": 100, "label": "Threshold"},
    {"min": 171, "max": 190, "score": 75, "label": "VO2 Max"}
  ]
}
```

### BMI Health Categories
```json
{
  "config_id": "SC-ZONE-BASED-BMI_CATEGORIES",
  "recommendation_text": "Maintain healthy BMI range",
  "zones": [
    {"min": 0, "max": 18.5, "score": 25, "label": "Underweight"},
    {"min": 18.5, "max": 25, "score": 100, "label": "Normal"},
    {"min": 25, "max": 30, "score": 75, "label": "Overweight"}, 
    {"min": 30, "max": 35, "score": 50, "label": "Obese I"},
    {"min": 35, "max": 50, "score": 25, "label": "Obese II+"}
  ]
}
```

---

*For simple binary patterns, see [Binary Threshold](binary-threshold.md)*  
*For progressive goals, see [Proportional](proportional.md)*