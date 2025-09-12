# WellPath Algorithm System - Complete Overview

Comprehensive guide to the WellPath health recommendation algorithm system, including implementation, configuration, testing, and relationships between all components.

## System Architecture

```
WellPath Algorithm System
├── 📊 Algorithm Types (6 core types)
│   ├── Binary Threshold
│   ├── Minimum Frequency ⭐ NEW
│   ├── Weekly Elimination ⭐ NEW
│   ├── Proportional
│   ├── Zone-Based
│   └── Composite Weighted
├── 🔧 Implementation Layer
│   ├── Python Algorithms (/src/algorithms/)
│   ├── JSON Configurations (/src/generated_configs/)
│   ├── Schema Validation (/src/schemas/)
│   └── Unit Conversion (/src/core_systems/)
├── 🧪 Testing & Validation
│   ├── Algorithm Tests (/tests/)
│   ├── Config Validation (test_complex_config_validation.py)
│   └── Comprehensive Test Suite
└── 📚 Documentation
    ├── Algorithm-Specific Docs (/docs/algorithms/)
    ├── Implementation Guides (/src/algorithms/README.md)
    └── Schema References (/src/schemas/)
```

## Quick Start Guide

### 1. Choose Algorithm Type

Use the **Algorithm Selection Decision Tree**:

```
Is it a single metric?
├─ YES: Single threshold?
│  ├─ YES: Daily requirement?
│  │  ├─ YES: → SC-BINARY-DAILY
│  │  └─ NO: Zero tolerance?
│  │     ├─ YES: → SC-WEEKLY-ELIMINATION
│  │     └─ NO: → SC-MINIMUM-FREQUENCY
│  └─ NO: Gradual improvement?
│     ├─ YES: → SC-PROPORTIONAL-DAILY
│     └─ NO: Optimal ranges?
│        └─ YES: → SC-ZONE-BASED-DAILY
└─ NO: Multiple metrics? → SC-COMPOSITE-DAILY
```

### 2. Create Configuration

Generate JSON configuration using the appropriate schema:

```json
{
  "config_id": "SC-MIN-FREQ-CAFFEINE_400MG_5_DAYS",
  "scoring_method": "minimum_frequency",
  "configuration_json": {
    "method": "minimum_frequency",
    "schema": {
      "daily_threshold": 400,
      "daily_comparison": "<=",
      "required_days": 5,
      "success_value": 100,
      "failure_value": 0
    }
  }
}
```

### 3. Implement Algorithm

Use Python implementation:

```python
from algorithms.minimum_frequency import calculate_minimum_frequency_score

result = calculate_minimum_frequency_score(
    daily_values=[350, 450, 380, 420, 370, 390, 410],
    daily_threshold=400,
    daily_comparison="<=",
    required_days=5
)
# Returns: {'score': 100, 'successful_days': 6, ...}
```

### 4. Test & Validate

```bash
python test_complex_config_validation.py "path/to/config.json"
```

## Algorithm Types Deep Dive

### 1. Binary Threshold (SC-BINARY-*)

**Purpose:** Simple pass/fail scoring  
**Use Cases:** Daily completion goals, simple limits  
**Scoring:** Binary (100 or 0)

```python
# Example: Daily water intake
from algorithms import create_daily_binary_threshold

algorithm = create_daily_binary_threshold(
    threshold=8,
    success_value=100,
    failure_value=0,
    description="8 glasses water daily"
)
score = algorithm.calculate_score(9)  # Returns 100
```

### 2. Minimum Frequency (SC-MINIMUM-FREQUENCY) ⭐ NEW

**Purpose:** Must achieve threshold on ≥X days per week  
**Use Cases:** "Limit caffeine ≤400mg on ≥5 days/week"  
**Scoring:** Binary (100 if requirement met, 0 otherwise)

```python
# Example: Caffeine frequency limit
from algorithms.minimum_frequency import calculate_minimum_frequency_score

result = calculate_minimum_frequency_score(
    daily_values=[350, 450, 380, 420, 370, 390, 410],  # Weekly caffeine
    daily_threshold=400,
    daily_comparison="<=",
    required_days=5
)
# Returns: {'score': 100, 'successful_days': 6, 'threshold_met': True}
```

### 3. Weekly Elimination (SC-WEEKLY-ELIMINATION) ⭐ NEW

**Purpose:** Zero tolerance - any violation fails entire week  
**Use Cases:** "No smoking every day", "Caffeine by 2pm daily"  
**Scoring:** Binary (100 if perfect week, 0 if any violation)

```python
# Example: Complete elimination
from algorithms.weekly_elimination import calculate_weekly_elimination_score

result = calculate_weekly_elimination_score(
    daily_values=["13:30", "14:00", "13:45", "15:00", "13:30", "14:00", "13:00"],
    elimination_threshold="14:00",
    elimination_comparison="<="
)
# Returns: {'score': 0, 'violations': 1, 'violation_days': [4]}
```

### 4. Proportional (SC-PROPORTIONAL-*)

**Purpose:** Percentage-based scoring for gradual improvement  
**Use Cases:** "Work toward 10,000 steps daily"  
**Scoring:** Continuous (0-100 based on percentage achieved)

```python
# Example: Step goal progression
from algorithms import create_daily_proportional

algorithm = create_daily_proportional(
    target=10000,
    unit="steps",
    maximum_cap=100,
    minimum_threshold=20
)
score = algorithm.calculate_score(7500)  # Returns 75
```

### 5. Zone-Based (SC-ZONE-BASED-*)

**Purpose:** Multi-tier scoring with optimal ranges  
**Use Cases:** Sleep duration, heart rate zones, BMI categories  
**Scoring:** Zone-specific (e.g., Poor=25, Good=75, Excellent=100)

```python
# Example: Sleep duration zones
from algorithms import create_sleep_duration_zones, create_daily_zone_based

zones = create_sleep_duration_zones()
algorithm = create_daily_zone_based(zones=zones, unit="hours")
score = algorithm.calculate_score(8.0)  # Returns 100 (Excellent zone)
```

### 6. Composite Weighted (SC-COMPOSITE-*)

**Purpose:** Combine multiple metrics with weights  
**Use Cases:** Overall fitness scores, comprehensive wellness  
**Scoring:** Weighted average of component scores

```python
# Example: Fitness composite
from algorithms import create_daily_composite, Component

components = [
    Component("Exercise", weight=0.4, target=30, unit="minutes"),
    Component("Steps", weight=0.3, target=10000, unit="steps"),
    Component("Sleep", weight=0.3, target=8, unit="hours")
]
algorithm = create_daily_composite(components=components)
```

## Configuration Management

### JSON Schema Structure

All configurations follow this structure:

```json
{
  "config_id": "SC-[ALGORITHM]-[DESCRIPTION]",
  "config_name": "Human readable name",
  "scoring_method": "algorithm_type",
  "configuration_json": {
    "method": "algorithm_type",
    "formula": "scoring_formula",
    "evaluation_pattern": "daily|weekly_*",
    "schema": {
      // Algorithm-specific parameters
    }
  },
  "metadata": {
    "recommendation_text": "Natural language recommendation",
    "recommendation_id": "REC####.#",
    "analysis": {
      "algorithm_type": "classification",
      "confidence": 0.9,
      "reasoning": "Why this algorithm was chosen"
    },
    "metric_id": "tracked_metric_name"
  }
}
```

### Configuration Naming Convention

| Pattern | Example | Algorithm Type |
|---------|---------|----------------|
| `SC-BINARY-DAILY-*` | `SC-BINARY-DAILY-WATER_8_GLASSES` | Binary Threshold Daily |
| `SC-MIN-FREQ-*` | `SC-MIN-FREQ-CAFFEINE_400MG_5_DAYS` | Minimum Frequency |
| `SC-WEEKLY-ELIM-*` | `SC-WEEKLY-ELIM-SMOKING_CESSATION` | Weekly Elimination |
| `SC-PROPORTIONAL-*` | `SC-PROPORTIONAL-STEPS_10000` | Proportional |
| `SC-ZONE-BASED-*` | `SC-ZONE-BASED-SLEEP_DURATION` | Zone-Based |
| `SC-COMPOSITE-*` | `SC-COMPOSITE-FITNESS_OVERALL` | Composite Weighted |

## Testing Framework

### Comprehensive Config Testing

```python
# Test any configuration
python test_complex_config_validation.py "config.json"
```

**What it tests:**
- ✅ JSON structure validation
- ✅ Algorithm parameter correctness
- ✅ Functional scoring with realistic data
- ✅ Binary scoring compliance (100/0)
- ✅ Edge case handling

### Algorithm-Specific Testing

```python
# Test minimum frequency
result = calculate_minimum_frequency_score(
    daily_values=[350, 450, 380, 420, 370, 390, 410],
    daily_threshold=400,
    daily_comparison="<=",
    required_days=5
)
assert result['score'] == 100
assert result['successful_days'] == 6

# Test weekly elimination  
result = calculate_weekly_elimination_score(
    daily_values=[0, 0, 1, 0, 0, 0, 0],  # Day 3 violation
    elimination_threshold=0,
    elimination_comparison="=="
)
assert result['score'] == 0
assert result['violations'] == 1
```

## Migration Guide

### Deprecated Patterns

#### SC-BINARY-FREQUENCY → SC-MINIMUM-FREQUENCY

**Problem:** "Binary frequency" was ambiguous  
**Solution:** Use explicit minimum frequency algorithm

**Before (Deprecated):**
```json
{
  "scoring_method": "binary_threshold",
  "configuration_json": {
    "evaluation_pattern": "weekly_frequency"
  }
}
```

**After (Current):**
```json
{
  "scoring_method": "minimum_frequency",
  "configuration_json": {
    "evaluation_pattern": "weekly_minimum_frequency",
    "schema": {
      "required_days": 5,
      "total_days": 7
    }
  }
}
```

#### SC-BINARY-DAILY → SC-WEEKLY-ELIMINATION (when appropriate)

**When to migrate:**
- Recommendation says "every day" 
- Zero tolerance required
- Any single violation should fail entire week

**Before:**
```json
{
  "scoring_method": "binary_threshold",
  "evaluation_pattern": "daily"
}
```

**After:**
```json
{
  "scoring_method": "weekly_elimination",
  "evaluation_pattern": "weekly_elimination",
  "schema": {
    "tolerance_level": "zero"
  }
}
```

## Integration Examples

### Real-World Implementation Pipeline

1. **Natural Language Input:** "Limit caffeine to ≤400mg on at least 5 days per week"

2. **Algorithm Selection:** SC-MINIMUM-FREQUENCY (frequency pattern with threshold)

3. **Configuration Generation:**
```json
{
  "config_id": "SC-MIN-FREQ-CAFFEINE_400MG_5_DAYS",
  "scoring_method": "minimum_frequency",
  "schema": {
    "daily_threshold": 400,
    "daily_comparison": "<=",
    "required_days": 5,
    "total_days": 7
  }
}
```

4. **Implementation:**
```python
result = calculate_minimum_frequency_score(
    daily_values=user_caffeine_data,  # From user tracking
    daily_threshold=400,
    daily_comparison="<=", 
    required_days=5
)
```

5. **User Feedback:**
```
📊 Caffeine Limit Progress
Score: 100/100 ✅
Success: 6 out of 5 required days met limit
Details: Exceeded requirement - great job!
```

## File Organization

```
WellPath Algorithm System
├── src/
│   ├── algorithms/
│   │   ├── __init__.py                    # Main exports
│   │   ├── binary_threshold.py           # SC-BINARY-*
│   │   ├── minimum_frequency.py          # SC-MINIMUM-FREQUENCY ⭐
│   │   ├── weekly_elimination.py         # SC-WEEKLY-ELIMINATION ⭐  
│   │   ├── proportional.py               # SC-PROPORTIONAL-*
│   │   ├── zone_based.py                 # SC-ZONE-BASED-*
│   │   ├── composite_weighted.py         # SC-COMPOSITE-*
│   │   └── README.md                     # Implementation guide
│   ├── generated_configs/                # JSON configurations
│   │   ├── REC0001.1-BINARY-THRESHOLD.json
│   │   ├── REC0013.1-BINARY-FREQUENCY.json  # → Fixed to MIN-FREQ
│   │   ├── REC0013.3-BINARY-DAILY.json      # → Fixed to WEEKLY-ELIM
│   │   └── ...
│   ├── schemas/
│   │   └── algorithm_schemas.json        # JSON validation schemas
│   └── core_systems/
│       └── unit_conversion_service.py    # Unit standardization
├── docs/
│   ├── algorithms/
│   │   ├── README.md                     # Algorithm overview
│   │   ├── algorithm-types.md            # Complete type reference
│   │   ├── SC-MINIMUM-FREQUENCY.md       # Detailed docs ⭐
│   │   ├── SC-WEEKLY-ELIMINATION.md      # Detailed docs ⭐
│   │   ├── binary-threshold.md           # Detailed docs
│   │   ├── proportional.md               # Detailed docs
│   │   └── zone-based.md                 # Detailed docs
│   └── WellPath-Algorithm-System-Overview.md  # This file
├── tests/
│   ├── test_algorithms.py               # Unit tests
│   ├── test_with_csv_configs.py        # Config integration tests
│   └── test_complex_config_validation.py # Comprehensive testing ⭐
└── test_complex_config_validation.py    # Standalone config tester ⭐
```

## Production Deployment Checklist

### Pre-Deployment Validation

- [ ] All algorithm implementations tested
- [ ] JSON configurations validated with schemas
- [ ] Migration from deprecated patterns completed
- [ ] Unit conversion system tested
- [ ] Integration tests passing
- [ ] Documentation updated

### Algorithm Completeness Check

- [ ] **Binary Threshold:** ✅ Complete & tested
- [ ] **Minimum Frequency:** ✅ Complete & tested ⭐
- [ ] **Weekly Elimination:** ✅ Complete & tested ⭐
- [ ] **Proportional:** ✅ Complete & tested
- [ ] **Zone-Based:** ✅ Complete & tested
- [ ] **Composite Weighted:** ✅ Complete & tested

### Configuration Status

- [ ] **REC0013.1-REC0013.3:** ✅ Fixed (caffeine timing)
- [ ] **REC0015.1-REC0015.3:** ✅ Fixed (caffeine cutoff)
- [ ] **REC0017.1-REC0017.3:** ✅ Fixed (eating window)
- [ ] **REC0018.1-REC0018.3:** ✅ Fixed (first meal timing)
- [ ] **REC0019.1-REC0019.3:** ✅ Fixed (last meal timing)
- [ ] **REC0021.1-REC0021.3:** ✅ Fixed (whole food meals)
- [ ] **All binary failure values:** ✅ Updated to 0

## Future Enhancements

### Planned Improvements
- **Advanced Zone Types:** Non-linear zone scoring
- **Dynamic Thresholds:** User-adaptive threshold adjustment
- **Composite Improvements:** Advanced weighting strategies
- **Real-time Scoring:** Single-day contribution functions
- **Performance Optimization:** Caching and batch processing

### Research Areas
- **Machine Learning Integration:** Pattern-based algorithm selection
- **Behavioral Analytics:** Success prediction modeling
- **Personalization:** Individual algorithm parameter tuning

---

## Quick Reference

### Most Common Patterns
1. **"Do X daily"** → `SC-BINARY-DAILY`
2. **"Do X on ≥Y days/week"** → `SC-MINIMUM-FREQUENCY`
3. **"Do X every single day"** → `SC-WEEKLY-ELIMINATION`
4. **"Work toward X"** → `SC-PROPORTIONAL`
5. **"Optimize X range"** → `SC-ZONE-BASED`

### Key Testing Commands
```bash
# Test single config
python test_complex_config_validation.py "config.json"

# Test all algorithms  
python -m pytest tests/test_algorithms.py

# Test all CSV configs
python tests/test_with_csv_configs.py
```

### Critical Implementation Notes
- ✅ **Binary scoring must be 100/0** (never partial credit)
- ✅ **All frequency algorithms require required_days parameter**
- ✅ **Weekly elimination has zero tolerance** (any violation = 0)
- ✅ **Use exact tracked_metrics names** from database

---

*Last Updated: 2025-01-15 - Added SC-MINIMUM-FREQUENCY and SC-WEEKLY-ELIMINATION algorithms*