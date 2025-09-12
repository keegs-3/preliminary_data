# Composite Weighted Algorithm (SC-COMPOSITE-WEIGHTED)

Multi-metric scoring that combines multiple health components with different importance weights.

## Overview

The Composite Weighted algorithm combines multiple individual metrics into a single unified score, with each component having a configurable weight representing its importance in the overall assessment.

## Algorithm Types

### SC-COMPOSITE-DAILY
**Purpose:** Daily multi-metric weighted evaluation  
**Pattern:** Weighted average of multiple daily component scores  
**Evaluation:** Daily  
**Scoring:** Weighted average (0-100) of all components

### SC-COMPOSITE-FREQUENCY
**Purpose:** Weekly frequency-based composite evaluation  
**Pattern:** Weekly evaluation combining multiple component frequencies  
**Evaluation:** Weekly  
**Scoring:** Weighted average of component frequency achievements

## Configuration Schema

```json
{
  "config_id": "SC-COMPOSITE-FITNESS_DAILY",
  "scoring_method": "composite_weighted",
  "configuration_json": {
    "method": "composite_weighted",
    "formula": "Σ(component_score × weight) for all components",
    "evaluation_pattern": "daily",
    "schema": {
      "measurement_type": "composite",
      "evaluation_period": "daily",
      "success_criteria": "weighted_average",
      "calculation_method": "weighted_average",
      "tracked_metrics": ["exercise_duration", "daily_steps", "active_minutes"],
      "components": [
        {
          "name": "Exercise Duration",
          "metric": "exercise_duration", 
          "weight": 0.4,
          "target": 30,
          "unit": "minutes",
          "algorithm_type": "proportional"
        },
        {
          "name": "Steps",
          "metric": "daily_steps",
          "weight": 0.3,
          "target": 10000,
          "unit": "steps",
          "algorithm_type": "proportional"
        },
        {
          "name": "Active Minutes",
          "metric": "active_minutes",
          "weight": 0.3,
          "target": 150,
          "unit": "minutes",
          "algorithm_type": "proportional"
        }
      ],
      "minimum_score": 0,
      "maximum_score": 100,
      "description": "Composite fitness scoring with weighted components"
    }
  },
  "metadata": {
    "recommendation_text": "Achieve overall fitness through exercise, steps, and activity",
    "recommendation_id": "REC0007.2",
    "metric_id": "composite_fitness"
  }
}
```

## Implementation

### Python Usage

```python
from algorithms.composite_weighted import calculate_composite_score

# Fitness composite example
components = [
    {"name": "Exercise Duration", "weight": 0.4, "target": 30, "actual": 25},
    {"name": "Steps", "weight": 0.3, "target": 10000, "actual": 8500},
    {"name": "Active Minutes", "weight": 0.3, "target": 150, "actual": 120}
]

result = calculate_composite_score(components)
# Returns: {'score': 82.5, 'component_scores': [...], 'weighted_breakdown': [...]}
```

### Direct Function Usage

```python
from algorithms.composite_weighted import CompositeWeightedAlgorithm, CompositeWeightedConfig

config = CompositeWeightedConfig(
    components=[
        Component("Exercise Duration", weight=0.4, target=30, unit="minutes"),
        Component("Steps", weight=0.3, target=10000, unit="steps"),
        Component("Active Minutes", weight=0.3, target=150, unit="minutes")
    ]
)

algorithm = CompositeWeightedAlgorithm(config)
result = algorithm.calculate_score(user_data)
```

## Scoring Logic

### Daily Composite Weighted

```python
def calculate_composite_score(components, user_data):
    total_weighted_score = 0
    total_weight = 0
    component_details = []
    
    for component in components:
        # Get actual value for this component
        actual_value = user_data.get(component.metric, 0)
        
        # Calculate component score based on its algorithm type
        if component.algorithm_type == "proportional":
            component_score = min(100, (actual_value / component.target) * 100)
        elif component.algorithm_type == "binary":
            component_score = 100 if actual_value >= component.target else 0
        elif component.algorithm_type == "zone_based":
            component_score = calculate_zone_score(actual_value, component.zones)
        
        # Apply weight
        weighted_score = component_score * component.weight
        total_weighted_score += weighted_score
        total_weight += component.weight
        
        component_details.append({
            'name': component.name,
            'score': component_score,
            'weight': component.weight,
            'weighted_contribution': weighted_score,
            'actual': actual_value,
            'target': component.target
        })
    
    # Calculate final composite score
    final_score = total_weighted_score / total_weight if total_weight > 0 else 0
    
    return {
        'score': round(final_score, 1),
        'component_scores': component_details,
        'total_weight': total_weight
    }
```

## Configuration Options

### Core Parameters
- **components** (required): List of component definitions
- **minimum_score** (default: 0): Minimum composite score
- **maximum_score** (default: 100): Maximum composite score

### Component Structure
Each component must include:
- **name**: Human-readable component name
- **metric**: Metric ID to track
- **weight**: Importance weight (0.0-1.0)
- **target**: Target value for the component
- **unit**: Measurement unit
- **algorithm_type**: "proportional", "binary", "zone_based"

### Advanced Settings
- **normalization**: Weight normalization method
- **floor_score**: Minimum score per component
- **ceiling_score**: Maximum score per component

## Use Cases

### Perfect Fits for Composite Weighted
- **Overall fitness**: Exercise duration + steps + active minutes
- **Sleep quality**: Duration + consistency + timing
- **Nutrition balance**: Protein + vegetables + hydration + fiber
- **Wellness assessment**: Physical + mental + social metrics
- **Lifestyle scoring**: Activity + nutrition + sleep + stress

### Not Suitable For
- **Simple single metrics**: "Walk 10,000 steps" → Use SC-PROPORTIONAL
- **Binary compliance**: "Take medication daily" → Use SC-BINARY-THRESHOLD
- **Zero tolerance**: "No smoking" → Use SC-WEEKLY-ELIMINATION

## Validation Rules

1. **Components Required**: At least 2 components must be specified
2. **Weight Validation**: All weights must be > 0 and sum should be reasonable
3. **Valid Targets**: All component targets must be > 0
4. **Algorithm Types**: Each component must have valid algorithm type
5. **Metric Mapping**: Each component metric must exist in tracked_metrics

## Testing

```python
# Test composite weighted algorithm
def test_composite_weighted():
    components = [
        {"name": "Exercise", "weight": 0.5, "target": 30, "actual": 30},
        {"name": "Steps", "weight": 0.3, "target": 10000, "actual": 5000},  
        {"name": "Sleep", "weight": 0.2, "target": 8, "actual": 7}
    ]
    
    result = calculate_composite_score(components)
    
    # Exercise: 100 * 0.5 = 50
    # Steps: 50 * 0.3 = 15  
    # Sleep: 87.5 * 0.2 = 17.5
    # Total: 50 + 15 + 17.5 = 82.5
    
    assert result['score'] == 82.5
    assert len(result['component_scores']) == 3
    
    print("✅ Composite weighted algorithm tests passed!")
```

## Real-World Examples

### Comprehensive Fitness Scoring
```json
{
  "config_id": "SC-COMPOSITE-FITNESS_COMPREHENSIVE",
  "recommendation_text": "Achieve overall fitness through balanced activity",
  "components": [
    {
      "name": "Cardio Exercise",
      "weight": 0.3,
      "target": 150,
      "unit": "minutes_per_week",
      "algorithm_type": "proportional"
    },
    {
      "name": "Strength Training", 
      "weight": 0.25,
      "target": 2,
      "unit": "sessions_per_week",
      "algorithm_type": "proportional"
    },
    {
      "name": "Daily Steps",
      "weight": 0.25,
      "target": 10000,
      "unit": "steps",
      "algorithm_type": "proportional"
    },
    {
      "name": "Sleep Quality",
      "weight": 0.2,
      "target": 8,
      "unit": "hours",
      "algorithm_type": "zone_based"
    }
  ]
}
```

### Nutrition Balance Assessment
```json
{
  "config_id": "SC-COMPOSITE-NUTRITION_BALANCE",
  "recommendation_text": "Maintain balanced nutrition across key areas",
  "components": [
    {
      "name": "Protein Intake",
      "weight": 0.3,
      "target": 100,
      "unit": "grams",
      "algorithm_type": "proportional"
    },
    {
      "name": "Vegetable Servings",
      "weight": 0.25,
      "target": 5,
      "unit": "servings",
      "algorithm_type": "proportional"
    },
    {
      "name": "Water Intake",
      "weight": 0.25, 
      "target": 8,
      "unit": "glasses",
      "algorithm_type": "binary"
    },
    {
      "name": "Fiber Intake",
      "weight": 0.2,
      "target": 25,
      "unit": "grams", 
      "algorithm_type": "proportional"
    }
  ]
}
```

### Sleep Quality Composite
```json
{
  "config_id": "SC-COMPOSITE-SLEEP_QUALITY",
  "recommendation_text": "Optimize sleep through duration, timing, and consistency",
  "components": [
    {
      "name": "Sleep Duration",
      "weight": 0.5,
      "target": 8,
      "unit": "hours",
      "algorithm_type": "zone_based",
      "zones": [
        {"range": [7, 9], "score": 100, "label": "Optimal"},
        {"range": [6, 7], "score": 75, "label": "Good"}
      ]
    },
    {
      "name": "Bedtime Consistency",
      "weight": 0.3,
      "target": 30,
      "unit": "minutes_variance",
      "algorithm_type": "proportional"
    },
    {
      "name": "Sleep Efficiency",
      "weight": 0.2,
      "target": 85,
      "unit": "percentage",
      "algorithm_type": "proportional"
    }
  ]
}
```

## Component Scoring Methods

### Proportional Components
```python
component_score = min(100, (actual / target) * 100)
```

### Binary Components  
```python
component_score = 100 if actual >= target else 0
```

### Zone-Based Components
```python
component_score = get_zone_score(actual, component.zones)
```

---

*For single-metric patterns, see [Proportional](proportional.md)*  
*For simple binary goals, see [Binary Threshold](binary-threshold.md)*