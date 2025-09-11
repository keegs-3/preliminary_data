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
Raw Lab Values → Reference Range Check → Score Normalization → Pillar Allocation → Final Scores
     ↓                    ↓                     ↓                    ↓               ↓
   125 mg/dL        Normal Range          Score: 85/100     Nutrition: 6.8    Final: 68.5
                    (65-99 mg/dL)                            Movement: 1.7
```

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
Each biomarker contributes to health pillars based on clinical evidence:

| Biomarker | Nutrition | Movement | Sleep | Cognitive | Stress | Connection | Core Care |
|-----------|-----------|----------|-------|-----------|--------|------------|-----------|
| **Glucose** | 60% | 20% | 5% | 5% | 5% | 0% | 5% |
| **HDL Cholesterol** | 40% | 35% | 5% | 5% | 5% | 0% | 10% |
| **Blood Pressure** | 20% | 25% | 15% | 5% | 20% | 0% | 15% |
| **CRP** | 30% | 20% | 10% | 10% | 20% | 0% | 10% |

### Allocation Calculation
```python
def allocate_to_pillars(biomarker_score, pillar_weights):
    allocated_scores = {}
    for pillar, weight in pillar_weights.items():
        allocated_scores[pillar] = biomarker_score * (weight / 100)
    return allocated_scores
```

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
    "overall_biomarker_score": 78.5,
    "pillar_scores": {
        "Nutrition": 82.3,
        "Movement": 75.1,
        "Sleep": 79.8,
        "Cognitive": 77.2,
        "Stress": 74.6,
        "Connection": 80.0,
        "Core_Care": 81.4
    },
    "individual_biomarkers": {
        "glucose_fasting": {
            "raw_value": 92,
            "score": 95,
            "pillar_allocations": {
                "Nutrition": 57.0,  # 95 * 0.6
                "Movement": 19.0,   # 95 * 0.2
                "Sleep": 4.8        # 95 * 0.05
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
    "calculated_score": 95,
    "pillar_weights": {"Nutrition": 60, "Movement": 20},
    "final_allocations": {"Nutrition": 57.0, "Movement": 19.0}
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