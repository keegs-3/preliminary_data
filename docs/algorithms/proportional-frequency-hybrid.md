# Proportional Frequency Hybrid Algorithm (SC-PROPORTIONAL-FREQUENCY-HYBRID)

Combines proportional daily scoring with frequency-based weekly evaluation for patterns like "≥X target on ≥Y days per week".

## Overview

The Proportional Frequency Hybrid algorithm solves the fundamental issue with traditional frequency patterns where partial progress gets no credit. Instead of binary daily assessment, it provides proportional daily scoring then calculates weekly scores based on the average of the top N qualifying days.

## Algorithm Types

### SC-PROPORTIONAL-FREQUENCY-HYBRID
**Purpose:** Daily proportional scoring with frequency-based weekly evaluation  
**Pattern:** Proportional daily scores averaged across top N qualifying days  
**Evaluation:** Daily scoring, weekly final calculation  
**Scoring:** Continuous (0-100) based on top qualifying days average

## Configuration Schema

```json
{
  "config_id": "SC-PROPORTIONAL-FREQUENCY-HYBRID-STEPS_5000_2_OF_7",
  "scoring_method": "proportional_frequency_hybrid",
  "configuration_json": {
    "method": "proportional_frequency_hybrid",
    "formula": "average of top N daily scores that meet minimum threshold",
    "evaluation_pattern": "weekly_proportional_frequency",
    "schema": {
      "measurement_type": "hybrid_quantity_frequency",
      "evaluation_period": "rolling_7_day",
      "success_criteria": "proportional_frequency_target",
      "calculation_method": "hybrid_proportional_frequency",
      "tracked_metrics": ["daily_steps"],
      "daily_target": 5000.0,
      "daily_minimum_threshold": 0,
      "required_qualifying_days": 2,
      "total_days": 7,
      "unit": "step",
      "minimum_threshold": 0,
      "maximum_cap": 100,
      "partial_credit": true,
      "progress_direction": "buildup",
      "description": "Proportional daily scoring, weekly score = average of top N qualifying days"
    }
  },
  "metadata": {
    "recommendation_text": "Reach at least 5,000 steps per day on at least 2 days per week",
    "recommendation_id": "REC0026.1",
    "metric_id": "daily_steps"
  }
}
```

## Implementation

### Python Usage

```python
from algorithms import create_proportional_frequency_hybrid

# Create hybrid algorithm
steps_algo = create_proportional_frequency_hybrid(
    daily_target=5000,
    required_qualifying_days=2,
    unit="steps",
    daily_minimum_threshold=0,
    description="5k steps on ≥2 days per week"
)

# Calculate weekly score with 7 days of data
daily_values = [3000, 3000, 3000, 5000, 4000, 3000, 4000]
weekly_score = steps_algo.calculate_weekly_score(daily_values)  # Returns 90.0
```

### Direct Function Usage

```python
from algorithms.proportional_frequency_hybrid import ProportionalFrequencyHybridAlgorithm, ProportionalFrequencyHybridConfig

config = ProportionalFrequencyHybridConfig(
    daily_target=5000,
    required_qualifying_days=2,
    unit="steps",
    daily_minimum_threshold=0,
    maximum_cap=100,
    progress_direction="buildup"
)

algorithm = ProportionalFrequencyHybridAlgorithm(config)
result = algorithm.calculate_weekly_score([3000, 3000, 5000, 4000, 3000, 4000, 3000])
```

## Scoring Logic

### Daily Scoring
Each day gets proportional score: `(actual_value / daily_target) * 100`
- Capped at 100% maximum
- Minimum 0% (or custom threshold)

### Weekly Scoring
1. Calculate all 7 daily proportional scores
2. Filter days meeting minimum threshold (if any)
3. Sort qualifying days by score (highest first)  
4. Take top N qualifying days (where N = required_qualifying_days)
5. If fewer than N qualifying days exist, weekly score = 0
6. Otherwise, weekly score = average of top N qualifying days

```python
def calculate_weekly_score(daily_values, daily_target, required_qualifying_days, minimum_threshold=0):
    # Calculate daily scores
    daily_scores = [(value / daily_target) * 100 for value in daily_values]
    daily_scores = [min(score, 100.0) for score in daily_scores]  # Cap at 100%
    
    # Filter qualifying days
    qualifying_data = [(score, value) for score, value in zip(daily_scores, daily_values) 
                       if value >= minimum_threshold]
    
    # Check if we have enough qualifying days
    if len(qualifying_data) < required_qualifying_days:
        return 0.0
    
    # Sort by score and take top N
    qualifying_data.sort(key=lambda x: x[0], reverse=True)
    top_scores = [score for score, _ in qualifying_data[:required_qualifying_days]]
    
    return sum(top_scores) / len(top_scores)
```

## Real-World Examples

### Water Intake Problem Resolution
**Problem:** Person drinks 4 cups daily (67% of 6 cup target) all 7 days. Traditional frequency scoring gives 0% because they never hit 6 cups on the required 2 days.

**Solution with Hybrid:**
```json
{
  "daily_target": 6.0,
  "required_qualifying_days": 2,
  "unit": "cups"
}
```

**Daily Results:**
- Day 1-7: 4 cups each → 66.7% daily score each day

**Weekly Calculation:**
- All days qualify (>0 cups)  
- Top 2 scores: 66.7% + 66.7% = 133.4%
- Weekly score: 133.4% ÷ 2 = 66.7%

**Result:** Person gets 66.7% weekly score instead of 0%

### Step Goal Progression 
```json
{
  "daily_target": 5000.0,
  "required_qualifying_days": 2,
  "unit": "steps"
}
```

**Scenario:**
- Day 1: 3,000 steps → 60% daily score
- Day 2: 3,000 steps → 60% daily score  
- Day 3: 3,000 steps → 60% daily score
- Day 4: 5,000 steps → 100% daily score
- Day 5: 4,000 steps → 80% daily score
- Day 6: 3,000 steps → 60% daily score
- Day 7: 4,000 steps → 80% daily score

**Weekly Calculation:**
- All days qualify (>0 steps)
- Top 2 scores: 100% (day 4) + 80% (day 5 or 7)  
- Weekly score: (100 + 80) ÷ 2 = 90%

### Protein Intake Building
```json
{
  "daily_target": 120.0,
  "required_qualifying_days": 5,
  "unit": "grams"
}
```

**Scenario:**
- Day 1: 90g → 75% daily score
- Day 2: 60g → 50% daily score
- Day 3: 120g → 100% daily score
- Day 4: 100g → 83% daily score
- Day 5: 110g → 92% daily score
- Day 6: 80g → 67% daily score  
- Day 7: 105g → 88% daily score

**Weekly Calculation:**
- All days qualify (>0g)
- Need 5 qualifying days: ✓ (have 7)
- Top 5 scores: 100%, 92%, 88%, 83%, 75%
- Weekly score: (100 + 92 + 88 + 83 + 75) ÷ 5 = 87.6%

## Configuration Options

### Core Parameters
- **daily_target** (required): Target value for 100% daily score
- **required_qualifying_days** (required): Number of top days to average
- **unit** (required): Measurement unit
- **daily_minimum_threshold** (default: 0): Minimum value to qualify as a valid day
- **total_days** (default: 7): Total evaluation period length
- **maximum_cap** (default: 100): Maximum weekly score cap
- **minimum_threshold** (default: 0): Minimum weekly score floor
- **progress_direction**: "buildup" or "countdown"

### Advanced Settings
- **partial_credit** (default: true): Allow partial credit for incomplete days
- **scaling_factor**: Custom scaling multiplier for daily scores
- **qualification_threshold**: Different threshold for day qualification vs scoring

## Use Cases

### Perfect Fits for Proportional Frequency Hybrid
- **Buildup patterns with frequency:** "≥6 cups water on ≥2 days per week"
- **Progressive frequency goals:** "≥5000 steps on ≥2 days per week"  
- **Gradual habit formation:** "≥3 servings vegetables on ≥4 days per week"
- **Flexible achievement patterns:** "≥30g fiber on ≥5 days per week"
- **Partial credit scenarios:** Where some progress should count even if target isn't fully met

### Not Suitable For
- **Binary compliance:** "Take medication daily" → Use SC-BINARY-THRESHOLD
- **Zero tolerance:** "No smoking" → Use SC-WEEKLY-ELIMINATION  
- **Simple proportional:** "Work toward 10K steps daily" → Use SC-PROPORTIONAL
- **All-or-nothing frequency:** "Exercise exactly 3 times per week" → Use SC-MINIMUM-FREQUENCY

## Validation Rules

1. **Target Required:** daily_target > 0
2. **Frequency Valid:** 1 ≤ required_qualifying_days ≤ total_days
3. **Unit Required:** Must specify measurement unit
4. **Threshold Logic:** daily_minimum_threshold ≥ 0
5. **Direction:** progress_direction must be "buildup" or "countdown"

## Testing

```python
# Test proportional frequency hybrid algorithm
def test_proportional_frequency_hybrid():
    algorithm = create_proportional_frequency_hybrid(
        daily_target=5000,
        required_qualifying_days=2,
        unit="steps",
        daily_minimum_threshold=0
    )
    
    # Test case: 4 cups daily scenario
    daily_values = [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0]  # 67% each day
    weekly_score = algorithm.calculate_weekly_score(daily_values)
    assert abs(weekly_score - 66.7) < 0.1  # Should get 66.7%, not 0%
    
    # Test case: mixed performance
    daily_values = [3000, 3000, 3000, 5000, 4000, 3000, 4000] 
    weekly_score = algorithm.calculate_weekly_score(daily_values)
    assert abs(weekly_score - 90.0) < 0.1  # Should get 90%
    
    print("✅ Proportional frequency hybrid algorithm tests passed!")
```

## Comparison with Other Algorithms

| Algorithm Type | Daily 4 cups (6 cup target) | Weekly Result |
|----------------|------------------------------|---------------|
| **SC-MINIMUM-FREQUENCY** | Pass/Fail per day | 0% (never hit 6 cups on 2 days) |
| **SC-PROPORTIONAL-FREQUENCY-HYBRID** | 66.7% per day | 66.7% (average of top 2 days) |
| **SC-PROPORTIONAL** | 66.7% per day | 66.7% (average of all days) |

**Key Advantage:** Provides partial credit for consistent effort while maintaining frequency requirements.

---

*For simple proportional patterns, see [Proportional](proportional.md)*  
*For binary frequency patterns, see [SC-MINIMUM-FREQUENCY](SC-MINIMUM-FREQUENCY.md)*