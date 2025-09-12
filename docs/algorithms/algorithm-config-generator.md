# Algorithm Configuration Generator

*Automated generation of scoring algorithm configurations from natural language health recommendations*

This system automatically analyzes health recommendations and generates appropriate scoring algorithm configurations using your existing units and metrics data.

## Overview

The **Recommendation Algorithm Configuration Generator** takes natural language health recommendations and converts them into production-ready algorithm configurations that integrate with your WellPath scoring system.

### What It Does

1. **Analyzes recommendation text** using NLP keyword matching
2. **Selects the optimal algorithm type** from 14 available configurations
3. **Finds matching metrics** from your `metric_types_v3` database
4. **Links proper units** from your `units_v3` database  
5. **Generates complete configs** with all required schema fields
6. **Saves organized files** for immediate use

## Quick Example

**Input:**
```
"Add one daily serving of fiber-rich food (e.g., oats or beans)"
```

**Output:**
```json
{
  "config_id": "SC-BIN-DAILY-DIETARY_",
  "config_name": "Binary Threshold - dietary_fiber",
  "scoring_method": "binary_threshold",
  "configuration_json": {
    "method": "binary_threshold",
    "formula": "if (actual_value >= threshold) then success_value else failure_value",
    "evaluation_pattern": "daily",
    "schema": {
      "tracked_metrics": ["dietary_fiber"],
      "threshold": 1.0,
      "unit": "serving",
      "measurement_type": "binary",
      "success_value": 100,
      "failure_value": 0
    }
  }
}
```

## Algorithm Selection Intelligence

The system analyzes recommendations using keyword patterns to select the optimal algorithm:

### Binary Threshold (Pass/Fail)
**Triggers:** "avoid", "eliminate", "stop", "always", "never", "must", "at least", **"add one"**, **"one daily"**, **"single serving"**
**Example:** *"Add one daily serving of fiber-rich food"*
**Result:** Binary scoring - 100 points for compliance, 0 for violation
**Special Logic:** Any "one" pattern (add one, take one, one daily) automatically gets binary with target=1

### Proportional (Percentage-based)
**Triggers:** "increase", "target", "goal", "aim for", specific numbers/units
**Example:** *"Increase daily steps to 10,000"*
**Result:** Percentage scoring based on achievement vs target

### Zone-Based (Tiered Scoring)
**Triggers:** "optimal", "range", "between", "zone", "excellent/good/fair/poor"
**Example:** *"Maintain blood pressure in optimal range"*
**Result:** 3-tier or 5-tier zone scoring based on complexity

### Composite Weighted (Multi-factor)
**Triggers:** "overall", "combined", "multiple", "both", "comprehensive", "plus", "maintain", "schedule", "variation"
**Example:** *"Improve overall sleep quality through duration and consistency"*
**Result:** Weighted combination of multiple components

#### Advanced Sleep Composite
**Special Case:** Sleep recommendations with schedule consistency (e.g., "Get 7-9 hours plus maintain consistent schedule")
**Components:**
- Sleep Duration Zone (55%): 7-9 hours optimal with 5-tier scoring
- Sleep Time Consistency (22.5%): Rolling average tolerance method  
- Wake Time Consistency (22.5%): Rolling average tolerance method
**Scoring:** Daily compliance checks with percentage-based weekly scoring (6/7 nights = 85.7%)

### Categorical Filter (Category-specific)
**Triggers:** Different rules for different categories/types
**Example:** *"High-impact exercises 3x/week, low-impact 2x/week"*
**Result:** Category-specific thresholds and scoring

## Metric and Unit Linking

### Automatic Metric Detection
The system searches your `metric_types_v3` data to find the best matching metric:

1. **Direct ID match** - Looks for recommendation IDs in metric's `recommendations_v2` field
2. **Name matching** - Searches metric names for keyword matches
3. **Description analysis** - Analyzes metric descriptions for semantic matches
4. **Identifier parsing** - Breaks down metric IDs for partial matches

### Unit Resolution  
Once a metric is found, the system:

1. **Gets the unit** from the metric's `units_v3` field
2. **Validates compatibility** with the algorithm type
3. **Retrieves display info** (symbol, UI display) from `units_v3` data
4. **Sets appropriate ranges** from the metric's validation schema

## File Organization

Generated configurations are saved in an organized structure:

```
src/generated_configs/
├── all_generated_configs.json          # Master list of all configs
├── SC-BIN-DAILY-DIETARY_.json          # Individual config files
├── SC-PROP-DAILY-STEPS_.json
├── SC-Z5T-DAILY-SLEEP_.json
└── ...
```

### Master List Benefits
- **Single source** of all generated configurations
- **Easy import** into your main system
- **Version tracking** with timestamps
- **Duplicate prevention** with automatic updates

## Usage

### Python API

```python
from recommendation_config_generator import process_recommendation

# Process a single recommendation
recommendation = "Add one daily serving of fiber-rich food"
config, filepath = process_recommendation(recommendation, "REC001")

print(f"Config saved to: {filepath}")
print(f"Algorithm type: {config['metadata']['analysis']['algorithm_type']}")
```

### Batch Processing

```python
from recommendation_config_generator import RecommendationConfigGenerator

generator = RecommendationConfigGenerator()

recommendations = [
    "Add one daily serving of fiber-rich food",
    "Take at least 10,000 steps daily", 
    "Maintain optimal sleep duration of 7-9 hours"
]

for rec in recommendations:
    config = generator.generate_config(rec)
    filepath = generator.save_config(config)
    print(f"Generated: {config['config_id']}")
```

## Configuration Schema

Each generated configuration follows this structure:

### Core Configuration
```json
{
  "config_id": "SC-{TYPE}-{PATTERN}-{METRIC}",
  "config_name": "Human readable name",
  "scoring_method": "algorithm_type",
  "configuration_json": {
    "method": "algorithm_type",
    "formula": "mathematical formula",
    "evaluation_pattern": "daily|frequency",
    "schema": {
      "measurement_type": "quantity|binary|composite",
      "evaluation_period": "daily|rolling_7_day",
      "success_criteria": "simple_target|frequency_target",
      "calculation_method": "sum|average|exists|weighted_average",
      "tracked_metrics": ["metric_id"],
      "target": 100,
      "unit": "serving",
      "description": "Generated description"
    }
  }
}
```

### Metadata
```json
{
  "metadata": {
    "recommendation_text": "Original recommendation",
    "recommendation_id": "REC001",
    "analysis": {
      "algorithm_type": "binary_threshold",
      "confidence": 0.9,
      "reasoning": "Binary/threshold language detected (binary score: 10)"
    },
    "metric_id": "dietary_fiber",
    "generated_at": "2025-09-10T16:57:52.440658"
  }
}
```

## Algorithm Types Generated

### 1. Binary Threshold Configurations
- **Daily Binary** (`SC-BIN-DAILY-*`) - Pass/fail daily goals
- **Frequency Binary** (`SC-BIN-FREQ-*`) - Pass/fail over time windows

### 2. Proportional Configurations  
- **Daily Proportional** (`SC-PROP-DAILY-*`) - Percentage achievement daily
- **Frequency Proportional** (`SC-PROP-FREQ-*`) - Percentage achievement over time

### 3. Zone-Based Configurations
- **3-Tier Daily** (`SC-Z3T-DAILY-*`) - Simple zone scoring
- **5-Tier Daily** (`SC-Z5T-DAILY-*`) - Detailed zone scoring
- **3-Tier Frequency** (`SC-Z3T-FREQ-*`) - Simple zone frequency
- **5-Tier Frequency** (`SC-Z5T-FREQ-*`) - Detailed zone frequency

### 4. Composite Configurations
- **Daily Composite** (`SC-COMP-DAILY-*`) - Multi-factor daily scoring
- **Frequency Composite** (`SC-COMP-FREQ-*`) - Multi-factor frequency scoring
- **Advanced Composite** (`SC-COMP-ADV-*`) - Complex specialized scoring

### 5. Specialized Configurations
- **Weekly Allowance** (`SC-ALLOW-WEEKLY-*`) - Constrained weekly budgets
- **Categorical Filter** (`SC-CAT-*`) - Category-specific rules

## Integration with WellPath System

### Direct Integration
Generated configurations can be directly imported into your existing algorithm system:

```python
# Load generated config
with open('generated_configs/SC-BIN-DAILY-DIETARY_.json') as f:
    config = json.load(f)

# Create algorithm instance
from algorithms import create_binary_threshold
algo = create_binary_threshold(
    threshold=config['configuration_json']['schema']['threshold'],
    unit=config['configuration_json']['schema']['unit']
)

# Use for scoring
score = algo.calculate_score(1)  # User had 1 serving of fiber -> 100 points
```

### Batch Import
```python
# Import all generated configs
with open('generated_configs/all_generated_configs.json') as f:
    all_configs = json.load(f)

algorithms = {}
for config in all_configs:
    config_id = config['config_id']
    # Create appropriate algorithm instance based on config
    algorithms[config_id] = create_algorithm_from_config(config)
```

## Quality and Validation

### Automatic Validation
- **Schema compliance** - All configs match required schema
- **Unit compatibility** - Units validated against metrics database
- **Algorithm suitability** - Algorithms matched to recommendation patterns
- **Completeness** - All required fields populated

### Confidence Scoring
Each configuration includes a confidence score (0.0-1.0):
- **0.9+** - High confidence, clear pattern match
- **0.7-0.9** - Good confidence, solid keyword matches  
- **0.5-0.7** - Medium confidence, some uncertainty
- **<0.5** - Low confidence, defaulted or unclear

### Manual Review Flags
Configurations with confidence < 0.7 should be manually reviewed for:
- Algorithm type appropriateness
- Target value accuracy
- Metric matching correctness
- Unit compatibility

## Example Generations

### Fiber Recommendation (Fixed)
**Input:** "Add one daily serving of fiber-rich food (e.g., oats or beans)"
- **Algorithm:** Binary threshold (one = pass/fail, not proportional)
- **Metric:** dietary_fiber  
- **Unit:** serving
- **Target:** 1 serving (not 5 from database)
- **Confidence:** 0.9 (high confidence due to clear "one" pattern)

### Steps Recommendation  
**Input:** "Take at least 10,000 steps daily"
- **Algorithm:** Proportional (target-based)
- **Metric:** daily_steps
- **Unit:** step
- **Target:** 10,000 steps
- **Confidence:** 0.8 (clear target pattern)

### Sleep Recommendation
**Input:** "Maintain optimal sleep duration between 7-9 hours nightly"
- **Algorithm:** Zone-based 5-tier (range-based)
- **Metric:** sleep_duration
- **Unit:** hour  
- **Zones:** 5 tiers around optimal range
- **Confidence:** 0.8 (clear zone language)

## Key Algorithm Selection Logic

### Priority Pattern Matching
The system uses weighted scoring for algorithm selection:

1. **High-priority binary patterns** get 5x weight:
   - "add one", "take one", "one daily", "single serving"
   
2. **Standard keyword matching** for other algorithms:
   - Binary: avoid, eliminate, stop, never, always, must
   - Proportional: increase, target, goal, specific numbers
   - Zone: optimal, range, between, excellent/good/fair/poor
   
3. **Threshold extraction** with special handling:
   - "One" patterns always return 1.0
   - Numeric extraction for other patterns
   - Fallback to metric database defaults

### Example Selection Process

For "Add one daily serving of fiber-rich food":
1. **Binary score**: 1 (daily) + 5 (add one priority) = 6
2. **Proportional score**: 1 (serving)
3. **Zone score**: 0
4. **Winner**: Binary threshold with confidence 0.9

## Future Enhancements

### Planned Features
- **Machine learning** improvement of algorithm selection
- **A/B testing** of algorithm effectiveness 
- **User feedback** integration for algorithm tuning
- **Recommendation clustering** for pattern discovery
- **Auto-optimization** of targets and thresholds

### Integration Opportunities
- **Real-time generation** during recommendation creation
- **Bulk import** from recommendation databases
- **API endpoints** for external system integration
- **UI integration** for manual configuration review

This system bridges the gap between human-readable health recommendations and machine-executable scoring algorithms, enabling rapid deployment of new recommendations with proper algorithmic backing.