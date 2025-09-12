# Categorical Filter Threshold Algorithm (SC-CATEGORICAL-FILTER-THRESHOLD)

Category-based filtering with threshold requirements for specific food types, exercise categories, or other categorical data.

## Overview

The Categorical Filter Threshold algorithm first filters data based on specific categories, then applies threshold logic to the filtered results. It's ideal for recommendations that require specific types or categories of items.

## Algorithm Types

### SC-CATEGORICAL-FILTER-DAILY
**Purpose:** Daily categorical filtering with threshold evaluation  
**Pattern:** Filter categories → Apply threshold check  
**Evaluation:** Daily  
**Scoring:** Binary (100 or 0) or proportional based on filtered achievement

### SC-CATEGORICAL-FILTER-FREQUENCY
**Purpose:** Weekly frequency-based categorical filtering  
**Pattern:** Weekly evaluation of daily categorical achievements  
**Evaluation:** Weekly  
**Scoring:** Based on frequency of meeting categorical thresholds

## Configuration Schema

```json
{
  "config_id": "SC-CATEGORICAL-FILTER-DAILY-VEGETABLES",
  "scoring_method": "categorical_filter_threshold",
  "configuration_json": {
    "method": "categorical_filter_threshold",
    "formula": "filter_categories(data, categories) then apply_threshold(filtered_data, threshold)",
    "evaluation_pattern": "daily",
    "schema": {
      "measurement_type": "categorical_threshold",
      "evaluation_period": "daily",
      "success_criteria": "categorical_target",
      "calculation_method": "filter_then_threshold",
      "tracked_metrics": ["food_servings"],
      "categories": ["vegetables", "leafy_greens", "cruciferous"],
      "filter_type": "include",
      "threshold": 3,
      "comparison_operator": ">=",
      "success_value": 100,
      "failure_value": 0,
      "unit": "servings",
      "description": "Categorical filtering for vegetable servings"
    }
  },
  "metadata": {
    "recommendation_text": "Include at least 3 servings from vegetable categories daily",
    "recommendation_id": "REC0014.1",
    "metric_id": "food_servings"
  }
}
```

## Implementation

### Python Usage

```python
from algorithms.categorical_filter_threshold import calculate_categorical_filter_score

# Vegetable servings requirement
result = calculate_categorical_filter_score(
    daily_data=[
        {"category": "vegetables", "servings": 2},
        {"category": "fruits", "servings": 1},
        {"category": "leafy_greens", "servings": 1},
        {"category": "grains", "servings": 2}
    ],
    categories=["vegetables", "leafy_greens", "cruciferous"],
    filter_type="include",
    threshold=3,
    comparison_operator=">="
)
# Returns: {'score': 100, 'filtered_total': 3, 'threshold_met': True}
```

### Direct Function Usage

```python
from algorithms.categorical_filter_threshold import CategoricalFilterAlgorithm, CategoricalFilterConfig

config = CategoricalFilterConfig(
    categories=["vegetables", "leafy_greens", "cruciferous"],
    filter_type="include",
    threshold=3,
    comparison_operator=">=",
    success_value=100,
    failure_value=0
)

algorithm = CategoricalFilterAlgorithm(config)
result = algorithm.calculate_score(daily_food_data)
```

## Scoring Logic

### Daily Categorical Filter

```python
def calculate_categorical_filter_score(daily_data, categories, filter_type, threshold, comparison_operator):
    # Step 1: Filter data by categories
    if filter_type == "include":
        filtered_data = [item for item in daily_data if item["category"] in categories]
    else:  # exclude
        filtered_data = [item for item in daily_data if item["category"] not in categories]
    
    # Step 2: Sum filtered values
    filtered_total = sum(item.get("servings", 0) for item in filtered_data)
    
    # Step 3: Apply threshold comparison
    if comparison_operator == ">=":
        threshold_met = filtered_total >= threshold
    elif comparison_operator == "<=":
        threshold_met = filtered_total <= threshold
    elif comparison_operator == "==":
        threshold_met = filtered_total == threshold
    
    # Step 4: Return score
    return {
        'score': 100 if threshold_met else 0,
        'filtered_total': filtered_total,
        'threshold_met': threshold_met,
        'categories_found': [item["category"] for item in filtered_data]
    }
```

## Configuration Options

### Core Parameters
- **categories** (required): List of category names to filter
- **filter_type** (required): "include" or "exclude"
- **threshold** (required): Threshold value for filtered data
- **comparison_operator** (required): ">=", "<=", or "=="
- **success_value** (default: 100): Score when threshold is met
- **failure_value** (default: 0): Score when threshold is not met

### Advanced Settings
- **unit**: Measurement unit for the filtered values
- **category_weights**: Different weights for different categories
- **minimum_categories**: Minimum number of different categories required

## Use Cases

### Perfect Fits for Categorical Filter
- **Vegetable variety**: "Include at least 3 servings from vegetable categories daily"
- **Exercise types**: "High-impact exercises 3x/week, low-impact 2x/week"
- **Supplement categories**: "Take at least 2 different vitamin categories daily"
- **Food group balance**: "Include servings from at least 4 food groups daily"

### Not Suitable For
- **Simple quantities**: "Drink 8 glasses of water" → Use SC-BINARY-THRESHOLD
- **Single category**: "Eat 5 servings of vegetables" → Use SC-PROPORTIONAL
- **Time-based patterns**: "Exercise 3+ times per week" → Use SC-MINIMUM-FREQUENCY

## Validation Rules

1. **Categories Required**: At least one category must be specified
2. **Valid Filter Type**: Must be "include" or "exclude"
3. **Valid Comparison**: Must use ">=", "<=", or "=="
4. **Positive Threshold**: Threshold must be > 0
5. **Valid Scoring**: success_value and failure_value must be 0-100

## Testing

```python
# Test categorical filter algorithm
def test_categorical_filter():
    daily_food_data = [
        {"category": "vegetables", "servings": 2},
        {"category": "fruits", "servings": 2},
        {"category": "leafy_greens", "servings": 1},
        {"category": "proteins", "servings": 1}
    ]
    
    result = calculate_categorical_filter_score(
        daily_data=daily_food_data,
        categories=["vegetables", "leafy_greens", "cruciferous"],
        filter_type="include",
        threshold=3,
        comparison_operator=">="
    )
    
    assert result['score'] == 100  # 2 + 1 = 3 servings ≥ 3
    assert result['filtered_total'] == 3
    assert result['threshold_met'] == True
    
    print("✅ Categorical filter algorithm tests passed!")
```

## Real-World Examples

### Vegetable Variety Goal
```json
{
  "config_id": "SC-CATEGORICAL-FILTER-VEGETABLES_3_SERVINGS",
  "recommendation_text": "Include at least 3 servings from vegetable categories daily",
  "schema": {
    "categories": ["vegetables", "leafy_greens", "cruciferous", "root_vegetables"],
    "filter_type": "include",
    "threshold": 3,
    "comparison_operator": ">="
  }
}
```

**Results:**
- 2 servings vegetables + 1 serving leafy greens = 100 points (meets 3 serving requirement)
- 1 serving vegetables + 1 serving fruits = 0 points (only 1 from target categories)

### Exercise Type Balance
```json
{
  "config_id": "SC-CATEGORICAL-FILTER-EXERCISE_TYPES",
  "recommendation_text": "Include both cardio and strength training weekly",
  "schema": {
    "categories": ["cardio", "strength_training"],
    "filter_type": "include", 
    "threshold": 2,
    "comparison_operator": ">=",
    "evaluation_period": "weekly"
  }
}
```

### Supplement Category Requirements
```json
{
  "config_id": "SC-CATEGORICAL-FILTER-SUPPLEMENT_VARIETY",
  "recommendation_text": "Take supplements from at least 2 different vitamin categories daily",
  "schema": {
    "categories": ["vitamin_d", "b_vitamins", "vitamin_c", "minerals"],
    "filter_type": "include",
    "threshold": 2,
    "comparison_operator": ">="
  }
}
```

---

*For simple binary patterns without categories, see [Binary Threshold](binary-threshold.md)*  
*For quantity-based goals, see [Proportional](proportional.md)*