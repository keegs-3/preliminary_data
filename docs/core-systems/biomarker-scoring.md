# Biomarker Scoring System

The WellPath biomarker scoring system processes laboratory values and biometric data through reference range analysis and pillar allocation to generate normalized health scores.

## 🎯 Overview

The biomarker scoring engine:
- **Processes raw lab values** against established reference ranges
- **Normalizes scores** to 0-100 scale for consistency
- **Allocates scores** across health pillars with evidence-based weighting
- **Handles missing data** gracefully with configurable defaults
- **Supports gender-specific** reference ranges and calculations

## 📊 Processing Pipeline

```
Raw Lab Values → Reference Range Check → Raw Score (0-1) → Pillar Weight Allocation → Pillar Normalization → Final Scores
     ↓                    ↓                     ↓                    ↓                      ↓                    ↓
   125 mg/dL        Normal Range          Raw: 0.85        Weight × Raw: 8.5        Norm: 3.53/4.15      Final: 85.1%
                    (65-99 mg/dL)                          (weight=10)               (pillar norm)
```

**Example Calculation:**
- Raw score: 0.85 (out of 1.0, not 100)
- Pillar weight: 10 → Raw weighted: 8.5
- Movement pillar max: 130, marker weight: 54%
- **Normalized value**: `(100/130) × 0.54 × 8.5 = 3.53`
- **Max possible**: `(100/130) × 0.54 × 10 = 4.15`
- **Final percentage**: 3.53/4.15 = 85.1%

## 🧮 Scoring Methods

### 1. Linear Scoring
For continuous biomarkers with optimal ranges:
```python
def linear_score(value, min_normal, max_normal, min_possible, max_possible):
    if min_normal <= value <= max_normal:
        return 100  # Optimal range
    elif value < min_normal:
        return max(0, (value - min_possible) / (min_normal - min_possible) * 100)
    else:
        return max(0, (max_possible - value) / (max_possible - max_normal) * 100)
```

### 2. Threshold Scoring  
For binary/categorical markers:
```python
def threshold_score(value, threshold, higher_is_better=True):
    if higher_is_better:
        return 100 if value >= threshold else 20
    else:
        return 100 if value <= threshold else 20
```

### 3. Multi-Range Scoring
For complex biomarkers with multiple optimal zones:
```python
def multi_range_score(value, ranges):
    for range_def in ranges:
        if range_def['min'] <= value <= range_def['max']:
            return range_def['score']
    return 0  # Outside all defined ranges
```

## 🎨 Pillar Allocation System

### Evidence-Based Weighting
Each biomarker + biometric contributes to health pillars using **weight-based allocation** (not percentages):

| Biomarker | Nutrition | Movement | Sleep | Cognitive | Stress | Connection | Core Care |
|-----------|-----------|----------|-------|-----------|--------|------------|-----------|
| **Glucose** | 4 | 7 | 0 | 5 | 4 | 0 | 0 |
| **HDL Cholesterol** | 5 | 4 | 0 | 0 | 0 | 0 | 6 |
| **Bodyfat** | 7 | 6 | 4 | 4 | 5 | 0 | 0 |

### Multi-Stage Allocation Process
```python
def process_biomarker_scoring(raw_value, reference_ranges, pillar_weights, pillar_configs):
    # Stage 1: Raw score (0-1 scale)
    raw_score = calculate_raw_score(raw_value, reference_ranges)
    
    # Stage 2: Pillar weight allocation 
    raw_weighted_scores = {}
    for pillar, weight in pillar_weights.items():
        if weight > 0:
            raw_weighted_scores[pillar] = raw_score * weight
    
    # Stage 3: Pillar normalization
    normalized_scores = {}
    for pillar, raw_weighted in raw_weighted_scores.items():
        pillar_max = pillar_configs[pillar]['max_possible']  # e.g., 130 for Movement
        marker_weight = pillar_configs[pillar]['marker_percentage']  # e.g., 0.54 for Movement
        
        # Final normalization: (100/pillar_max) × marker_weight × raw_weighted
        normalized_scores[pillar] = (100 / pillar_max) * marker_weight * raw_weighted
        
    return {
        'raw_score': raw_score,
        'raw_weighted': raw_weighted_scores,
        'normalized': normalized_scores
    }
```

**Key Process**: 
1. **Raw score**: 0-1 scale from reference ranges
2. **Weight allocation**: Raw score × pillar weight  
3. **Pillar normalization**: Accounts for pillar max scores and marker/survey weight distribution

## 📋 Reference Range Management

### Standard Reference Ranges
```json
{
  "glucose_fasting": {
    "unit": "mg/dL",
    "optimal": {"min": 65, "max": 99},
    "acceptable": {"min": 100, "max": 125},
    "concerning": {"min": 126, "max": 200}
  }
}
```

### Gender-Specific Ranges
```json
{
  "hemoglobin": {
    "male": {"min": 13.8, "max": 17.2, "unit": "g/dL"},
    "female": {"min": 12.1, "max": 15.1, "unit": "g/dL"}
  }
}
```

### Age-Adjusted Ranges
```json
{
  "blood_pressure_systolic": {
    "age_18_39": {"optimal": 120, "high": 140},
    "age_40_59": {"optimal": 125, "high": 145},
    "age_60_plus": {"optimal": 130, "high": 150}
  }
}
```

## 🛠️ Implementation Details

### Data Input Format
```python
patient_biomarkers = {
    "patient_id": "12345",
    "demographics": {
        "age": 35,
        "gender": "female", 
        "weight": 65,
        "height": 165
    },
    "lab_results": {
        "glucose_fasting": 92,
        "hdl_cholesterol": 58,
        "ldl_cholesterol": 115,
        "triglycerides": 85,
        # ... 89 total biomarkers
    }
}
```

### Score Output Structure
```python
biomarker_scores = {
    "patient_id": "12345",
    "individual_biomarkers": {
        "glucose_fasting": {
            "raw_value": 92,
            "raw_score": 0.85,  # 0-1 scale from reference ranges
            "raw_weighted_scores": {
                "Nutrition": 6.8,      # 0.85 * weight(8)
                "Movement": 2.55,      # 0.85 * weight(3)
                "Sleep": 1.7,          # 0.85 * weight(2)
                "Core_Care": 1.7       # 0.85 * weight(2)
            },
            "normalized_scores": {
                "Nutrition": 1.95,     # (100/258) * 0.72 * 6.8
                "Movement": 1.06,      # (100/130) * 0.54 * 2.55
                "Sleep": 0.69,         # (100/98) * 0.63 * 1.7
                "Core_Care": 0.62      # (100/137) * 0.495 * 1.7
            },
            "max_possible_scores": {
                "Nutrition": 2.28,     # (100/258) * 0.72 * 8
                "Movement": 1.25,      # (100/130) * 0.54 * 3
                "Sleep": 0.81,         # (100/98) * 0.63 * 2
                "Core_Care": 0.72      # (100/137) * 0.495 * 2
            }
        }
    }
}
```

## ⚙️ Configuration Options

### Missing Data Handling
```python
MISSING_DATA_STRATEGIES = {
    "skip": "Exclude from scoring entirely",
    "default_score": "Use configurable default (typically 50)",
    "population_average": "Use age/gender matched population average",
    "interpolate": "Use related biomarkers for estimation"
}
```

### Score Scaling Options
```python
SCALING_METHODS = {
    "linear": "Standard linear scaling 0-100",
    "logarithmic": "Log scale for skewed distributions", 
    "percentile": "Population percentile ranking",
    "z_score": "Standard deviations from population mean"
}
```

## 🔍 Quality Assurance

### Validation Rules
- All scores must be 0-100 range
- Pillar allocations must sum to biomarker score
- Reference ranges must have clinical backing
- Gender/age adjustments must be evidence-based

### Audit Trail
```python
audit_trail = {
    "biomarker": "glucose_fasting",
    "raw_value": 92,
    "reference_range": {"min": 65, "max": 99},
    "scoring_method": "linear",
    "raw_score": 0.85,  # 0-1 scale
    "pillar_weights": {"Nutrition": 8, "Movement": 3, "Sleep": 2, "Core_Care": 2},
    "raw_weighted": {"Nutrition": 6.8, "Movement": 2.55, "Sleep": 1.7, "Core_Care": 1.7},
    "pillar_configs": {
        "Nutrition": {"max": 258, "marker_weight": 0.72},
        "Movement": {"max": 130, "marker_weight": 0.54}
    },
    "final_normalized": {"Nutrition": 1.95, "Movement": 1.06, "Sleep": 0.69, "Core_Care": 0.62}
}
```

## 📊 Statistical Analysis

### Population Benchmarking
- Age-adjusted percentiles for each biomarker
- Gender-specific distribution analysis
- Correlation analysis between biomarkers
- Trend analysis for score validation

### Score Distribution Validation
- Normal distribution checks for scaled scores
- Outlier detection and handling
- Cross-biomarker consistency validation
- Pillar score balance verification

## 🔧 Integration Points

### Database Schema
```sql
CREATE TABLE biomarker_scores (
    patient_id VARCHAR(50),
    biomarker_name VARCHAR(100), 
    raw_value DECIMAL(10,3),
    normalized_score DECIMAL(5,2),
    pillar_allocations JSON,
    created_at TIMESTAMP
);
```

### API Endpoints
```python
@app.route('/score-biomarkers', methods=['POST'])
def score_biomarkers(patient_data):
    scores = biomarker_scoring_engine.process(patient_data)
    return {"scores": scores, "audit_trail": audit_trail}
```

---

**The biomarker scoring system provides clinically accurate, evidence-based health assessments that integrate seamlessly with survey and education data for comprehensive patient evaluation.**
