# Getting Started with WellPath

## Quick Setup Guide

This guide will walk you through setting up your first health tracking configuration using WellPath's comprehensive data framework.

## Understanding the Data Structure

WellPath uses five key CSV files that define the entire health tracking system:

### Core Data Files

| File | Purpose | Records |
|------|---------|---------|
| **metric_types_v3.csv** | Raw metrics definitions | 88 health metrics |
| **calculated_metrics.csv** | Derived metrics formulas | 134 calculated values |
| **units_v3.csv** | Measurement units system | 151 standardized units |
| **source_options.csv** | Data input sources | Validation options |
| **screening_compliance_rules.csv** | Health screening guidelines | Age/gender-specific rules |

## Step 1: Choose Your First Metric

Let's start with a simple daily step tracking example. Looking at our metric definitions:

```csv
# From metric_types_v3.csv
step_taken,Step Taken,Individual step recorded by device,quantity,"time_start,time_end",step,"{""range"": {""min"": 1, ""max"": 1}}",HKQuantityTypeIdentifier.stepCount
```

This shows:
- **Raw Metric**: `step_taken` (individual step events)
- **Unit**: `step` 
- **HealthKit Compatible**: Yes
- **Generates**: `daily_steps` (calculated metric)

## Step 2: Understand the Data Flow

```
Raw Metric → Calculated Metric → Algorithm → Score
step_taken → daily_steps → proportional → 0-100%
```

### Raw Data Entry
```json
{
  "metric_id": "step_taken",
  "timestamp": "2025-01-15T14:30:00Z",
  "value": 1,
  "unit": "step",
  "source": "apple_watch"
}
```

### Calculated Daily Aggregation
```csv
# From calculated_metrics.csv
daily_steps,Daily Steps,"Total number of steps taken per day",SUM(step_taken) WHERE date = target_date,sum,step,step_taken
```

## Step 3: Configure Your Algorithm

Choose from 10 algorithm types. For steps, proportional scoring works well:

```json
{
  "algorithm_type": "proportional",
  "target_value": 10000,
  "unit": "step",
  "evaluation_period": "daily",
  "formula": "(actual_value / target_value) * 100"
}
```

## Step 4: Set Up Progressive Scoring

WellPath provides real-time feedback as data arrives:

```
Day 1: 3,000 steps → 30% progress
Day 2: 7,500 steps → 75% progress  
Day 3: 12,000 steps → 100% (capped)
```

## Common Metric Examples

### 1. Nutrition Tracking

**Water Intake**
```csv
# Raw: water_consumed (milliliters per instance)
# Calculated: daily_water_consumption (total mL per day)
# Algorithm: Binary threshold (2000mL daily target)
```

**Vegetable Servings**  
```csv
# Raw: vegetable_serving (0.5-3.0 servings per entry)
# Calculated: daily_vegetable_servings (total servings per day)
# Algorithm: Proportional (5 servings daily target)
```

### 2. Exercise Tracking

**Strength Training**
```csv
# Raw: strength_session (time-based sessions)
# Calculated: daily_strength_training_duration (total minutes)
# Algorithm: Minimum frequency (3 sessions per week)
```

**Zone 2 Cardio**
```csv
# Raw: zone2_cardio_session (20-90 minute sessions)
# Calculated: weekly_zone2_duration (total weekly minutes)
# Algorithm: Binary threshold (150 minutes weekly)
```

### 3. Sleep & Recovery

**Sleep Duration**
```csv
# Raw: sleep_time, wake_time (timestamps)
# Calculated: sleep_duration (hours between sleep/wake)
# Algorithm: Zone-based (7-9 hours optimal, 6-7 fair, <6 poor)
```

## Step 5: Understanding Units

WellPath uses 151 standardized units across 12 categories:

### Common Unit Types

| Category | Examples | Usage |
|----------|----------|-------|
| **Mass** | gram, kilogram, serving | Nutrition, body measurements |
| **Volume** | milliliter, liter, cup | Fluid intake, portion sizes |
| **Time** | minutes, hours, timestamp | Duration, scheduling |
| **Count** | step, session, meal | Discrete events, activities |
| **Scale** | scale_1_5, percent | Ratings, progress tracking |

### HealthKit Compatibility

Many units map directly to Apple HealthKit:

```csv
# From units_v3.csv
step,Steps,steps,count,,,HKUnit.count(),checked
kilogram,Kilograms,kg,mass,gram,1000,HKUnit.kilogram(),checked
```

## Step 6: Data Validation

All metrics include validation schemas:

```json
{
  "step_taken": {
    "range": {"min": 1, "max": 1},
    "type": "quantity",
    "required_fields": ["timestamp", "value"]
  },
  "water_consumed": {
    "range": {"min": 50, "max": 1000},
    "unit": "milliliter",
    "validation": "positive_number"
  }
}
```

## Step 7: Health Screening Integration

For users over certain ages, WellPath tracks health screening compliance:

```csv
# Calculated metrics for screening intervals
years_since_physical,Years Since Last Physical,DATEDIF(physical_exam_date, TODAY(), 'YEARS')
mammogram_compliance_status,Mammogram Compliance Status,"IF(gender=female AND age>21, calculate_compliance(...))"
```

## Implementation Example

Here's a complete configuration for daily step tracking:

```json
{
  "config_id": "daily_steps_10k",
  "recommendation": "Walk 10,000 steps daily",
  "data_pipeline": {
    "raw_metric": {
      "identifier": "step_taken",
      "unit": "step", 
      "source": "wearable_device",
      "validation": {"range": {"min": 1, "max": 1}}
    },
    "calculated_metric": {
      "identifier": "daily_steps",
      "formula": "SUM(step_taken) WHERE date = target_date",
      "unit": "step",
      "calculation_type": "sum"
    },
    "algorithm": {
      "type": "proportional",
      "target_value": 10000,
      "unit": "step",
      "evaluation_period": "daily",
      "score_formula": "(actual_value / target_value) * 100"
    }
  },
  "progressive_scoring": true,
  "healthkit_integration": "HKQuantityTypeIdentifier.stepCount"
}
```

## Testing Your Configuration

Use the built-in testing framework to validate your setup:

```python
from src.algorithms.proportional import ProportionalAlgorithm
from src.config_generator import validate_config

# Test with sample data
test_data = [3000, 7500, 12000, 8500, 9200, 6800, 11000]
config = load_config("daily_steps_10k.json")
algorithm = ProportionalAlgorithm.from_config(config)

# Validate progressive scores
progressive_scores = algorithm.calculate_progressive_scores(test_data)
print(f"Daily progress: {progressive_scores}")
# Output: [30.0, 75.0, 100.0, 85.0, 92.0, 68.0, 100.0]
```

## Next Steps

### For Developers
- **[Algorithm Implementation Guide](../guides/algorithm-implementation.md)** - Build custom scoring algorithms
- **[Data Modeling Guide](../guides/data-modeling.md)** - Design new metric types
- **[API Reference](../api-reference/algorithms.md)** - Integration documentation

### For Health Professionals  
- **[Metric Types Catalog](../reference/metric-types/)** - Complete health metrics reference
- **[Compliance Rules](../reference/compliance/)** - Health screening guidelines
- **[Units System](../reference/units/)** - Measurement standards

### For Researchers
- **[Data Architecture](data-architecture.md)** - System design principles  
- **[Algorithm Research](../../WellPath-Adherence-Scoring-Implementation-Guide.md)** - Scoring methodology

## Common Questions

**Q: Can I track custom metrics not in the CSV files?**
A: Yes! Follow the data modeling guide to extend the metric_types_v3.csv with your custom definitions.

**Q: How do I handle missing data?**
A: WellPath includes data quality scoring and graceful degradation for incomplete datasets.

**Q: Is real-time scoring required?**
A: No, you can configure batch processing for weekly or monthly scoring instead of daily updates.

**Q: Can I modify existing algorithms?**
A: Yes, all algorithms support parameter customization. See the configuration schema guide for details.

---

**Ready to implement?** Start with the [Algorithm Implementation Guide](../guides/algorithm-implementation.md) or explore the [Metric Types Catalog](../reference/metric-types/) for comprehensive metric definitions.