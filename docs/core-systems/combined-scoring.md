# Combined Scoring System

The WellPath combined scoring system integrates biomarker, survey, and education data using pillar-specific weightings to generate final patient wellness scores.

## 🎯 Overview

The combined scoring engine:
- **Integrates three data sources** with evidence-based weighting
- **Applies pillar-specific weights** for balanced health assessment  
- **Generates comprehensive scores** across 7 health pillars
- **Provides audit trails** showing score derivation from all components
- **Calculates improvement potential** for targeted interventions

## 📊 Integration Architecture

### Pillar Weighting System
Each health pillar uses different weights for the three data sources:

| Pillar | Markers % | Survey % | Education % | Clinical Rationale |
|--------|-----------|----------|-------------|-------------------|
| **Healthful Nutrition** | 72% | 18% | 10% | Biomarkers strongly reflect nutritional status |
| **Movement + Exercise** | 54% | 36% | 10% | Balanced objective/subjective assessment |
| **Restorative Sleep** | 63% | 27% | 10% | Sleep biomarkers highly predictive |
| **Cognitive Health** | 36% | 54% | 10% | Self-reported cognitive function critical |
| **Stress Management** | 27% | 63% | 10% | Stress primarily subjective experience |
| **Connection + Purpose** | 18% | 72% | 10% | Social connection best assessed via survey |
| **Core Care** | 49.5% | 40.5% | 10% | Balanced preventive care assessment |

### Score Integration Formula
```python
def calculate_pillar_score(pillar_name, marker_score, survey_score, education_score):
    weights = PILLAR_WEIGHTS[pillar_name]
    
    combined_score = (
        marker_score * weights['markers'] + 
        survey_score * weights['survey'] + 
        education_score * weights['education']
    ) / 100
    
    return min(max(combined_score, 0), 100)  # Clamp to 0-100
```

## 🔄 Processing Pipeline

### 1. Data Preparation
```python
# Load component scores
marker_scores = load_marker_scores()      # From WellPath_Score_Markers/
survey_scores = load_survey_scores()      # From WellPath_Score_Survey/ 
education_scores = load_education_scores()  # From education processing

# Validate data completeness
validate_patient_data_completeness(marker_scores, survey_scores, education_scores)
```

### 2. Score Alignment  
```python
# Ensure all scores are on 0-100 scale
marker_scores_normalized = normalize_scores(marker_scores, method='percentile')
survey_scores_normalized = normalize_scores(survey_scores, method='direct')
education_scores_normalized = normalize_scores(education_scores, method='completion')
```

### 3. Pillar Integration
```python
for patient_id in all_patients:
    for pillar in HEALTH_PILLARS:
        # Get component scores for this pillar
        marker_pillar_score = get_pillar_score(marker_scores, patient_id, pillar)
        survey_pillar_score = get_pillar_score(survey_scores, patient_id, pillar) 
        education_pillar_score = get_pillar_score(education_scores, patient_id, pillar)
        
        # Calculate weighted combination
        combined_pillar_score = calculate_pillar_score(
            pillar, marker_pillar_score, survey_pillar_score, education_pillar_score
        )
        
        # Store with audit trail
        store_combined_score(patient_id, pillar, combined_pillar_score, audit_trail)
```

### 4. Overall Score Calculation
```python
def calculate_overall_wellness_score(pillar_scores):
    # Equal weighting across pillars for overall score
    return sum(pillar_scores.values()) / len(pillar_scores)
```

## 📋 Output Structure

### Comprehensive Patient Scores
```python
combined_scores = {
    "patient_id": "12345",
    "overall_wellness_score": 78.5,
    "pillar_scores": {
        "Nutrition": 82.3,
        "Movement": 75.1, 
        "Sleep": 79.8,
        "Cognitive": 77.2,
        "Stress": 74.6,
        "Connection": 80.0,
        "Core_Care": 81.4
    },
    "component_breakdown": {
        "Nutrition": {
            "markers_contribution": 68.9,    # 82.3 * 0.72 = 59.3 points
            "survey_contribution": 8.9,      # 82.3 * 0.18 = 14.8 points  
            "education_contribution": 4.5,   # 82.3 * 0.10 = 8.2 points
            "total": 82.3
        }
    },
    "data_completeness": {
        "markers_coverage": 0.92,    # 92% of expected biomarkers available
        "survey_coverage": 0.98,     # 98% of survey questions completed
        "education_coverage": 0.85   # 85% of education modules engaged
    }
}
```

### Audit Trail Structure
```python
audit_trail = {
    "patient_id": "12345",
    "pillar": "Nutrition", 
    "final_score": 82.3,
    "components": {
        "markers": {
            "raw_score": 85.2,
            "weight": 0.72,
            "contribution": 61.3,
            "source_biomarkers": ["glucose", "hdl_cholesterol", "triglycerides"]
        },
        "survey": {
            "raw_score": 78.6,
            "weight": 0.18,
            "contribution": 14.1,
            "source_questions": ["2.01", "2.02", "2.11"]
        },
        "education": {
            "raw_score": 72.0,
            "weight": 0.10, 
            "contribution": 7.2,
            "source_modules": ["nutrition_basics", "meal_planning"]
        }
    },
    "calculation_timestamp": "2024-01-15T10:30:00Z"
}
```

## 🔍 Quality Assurance

### Data Validation Rules
```python
def validate_combined_scores(scores):
    # Score range validation
    for pillar, score in scores['pillar_scores'].items():
        assert 0 <= score <= 100, f"Invalid score for {pillar}: {score}"
    
    # Component contribution validation  
    for pillar, breakdown in scores['component_breakdown'].items():
        total_contribution = (
            breakdown['markers_contribution'] + 
            breakdown['survey_contribution'] + 
            breakdown['education_contribution']
        )
        assert abs(total_contribution - breakdown['total']) < 0.1, f"Component sum mismatch: {pillar}"
    
    # Data completeness validation
    completeness = scores['data_completeness']
    if completeness['markers_coverage'] < 0.7:
        warnings.warn(f"Low marker coverage: {completeness['markers_coverage']}")
```

### Score Distribution Analysis
```python
def analyze_score_distributions(all_patient_scores):
    for pillar in HEALTH_PILLARS:
        pillar_scores = [p['pillar_scores'][pillar] for p in all_patient_scores]
        
        # Statistical analysis
        mean_score = np.mean(pillar_scores)
        std_score = np.std(pillar_scores)
        percentiles = np.percentile(pillar_scores, [25, 50, 75])
        
        # Flag unusual distributions
        if std_score < 5:  # Too narrow distribution
            warnings.warn(f"Low variance in {pillar} scores: {std_score}")
        if mean_score < 40 or mean_score > 85:  # Unusual population mean
            warnings.warn(f"Unusual mean score for {pillar}: {mean_score}")
```

## ⚙️ Configuration Management

### Pillar Weight Configuration
```python
PILLAR_WEIGHTS = {
    "Nutrition": {"markers": 72, "survey": 18, "education": 10},
    "Movement": {"markers": 54, "survey": 36, "education": 10},
    "Sleep": {"markers": 63, "survey": 27, "education": 10},
    "Cognitive": {"markers": 36, "survey": 54, "education": 10},
    "Stress": {"markers": 27, "survey": 63, "education": 10},
    "Connection": {"markers": 18, "survey": 72, "education": 10},
    "Core_Care": {"markers": 49.5, "survey": 40.5, "education": 10}
}

# Validation: Each pillar must sum to 100
for pillar, weights in PILLAR_WEIGHTS.items():
    assert sum(weights.values()) == 100, f"Pillar weights don't sum to 100: {pillar}"
```

### Missing Data Strategies
```python
MISSING_DATA_HANDLING = {
    "markers": {
        "strategy": "population_median",
        "min_coverage": 0.6,  # Require 60% of biomarkers minimum
        "fallback": "exclude_from_calculation"
    },
    "survey": {
        "strategy": "question_specific_default",
        "min_coverage": 0.8,  # Require 80% of survey questions
        "fallback": "reduce_weight_proportionally"  
    },
    "education": {
        "strategy": "zero_score",  # No education = 0 points
        "min_coverage": 0.0,
        "fallback": "continue"
    }
}
```

## 📊 Improvement Potential Analysis

### Gap Analysis
```python
def calculate_improvement_potential(patient_scores):
    improvement_opportunities = {}
    
    for pillar, score in patient_scores['pillar_scores'].items():
        # Calculate potential improvement to reach 85th percentile
        target_score = POPULATION_PERCENTILES[pillar][85]
        potential_gain = max(0, target_score - score)
        
        # Identify which component has most improvement potential
        component_scores = patient_scores['component_breakdown'][pillar]
        bottleneck_component = min(component_scores.items(), key=lambda x: x[1])
        
        improvement_opportunities[pillar] = {
            "current_score": score,
            "target_score": target_score, 
            "potential_gain": potential_gain,
            "bottleneck_component": bottleneck_component[0],
            "priority_level": "high" if potential_gain > 15 else "medium" if potential_gain > 8 else "low"
        }
    
    return improvement_opportunities
```

### Recommendation Targeting
```python
def generate_targeted_recommendations(improvement_analysis):
    recommendations = []
    
    # Prioritize high-impact, achievable improvements
    high_priority_pillars = [
        pillar for pillar, analysis in improvement_analysis.items() 
        if analysis['priority_level'] == 'high'
    ]
    
    for pillar in high_priority_pillars:
        analysis = improvement_analysis[pillar]
        bottleneck = analysis['bottleneck_component']
        
        # Generate component-specific recommendations
        if bottleneck == 'markers':
            recommendations.extend(get_biomarker_improvement_recs(pillar))
        elif bottleneck == 'survey':
            recommendations.extend(get_behavioral_improvement_recs(pillar))
        elif bottleneck == 'education':
            recommendations.extend(get_education_engagement_recs(pillar))
    
    return recommendations
```

## 🔧 Performance Optimization

### Batch Processing
```python
def process_patients_in_batches(patient_list, batch_size=1000):
    for i in range(0, len(patient_list), batch_size):
        batch = patient_list[i:i + batch_size]
        
        # Vectorized operations where possible
        batch_scores = calculate_batch_scores(batch)
        
        # Save batch results
        save_batch_results(batch_scores)
        
        # Progress tracking
        print(f"Processed {min(i + batch_size, len(patient_list))} / {len(patient_list)} patients")
```

### Caching Strategy
```python
@lru_cache(maxsize=10000)
def calculate_pillar_score_cached(pillar_name, marker_score, survey_score, education_score):
    return calculate_pillar_score(pillar_name, marker_score, survey_score, education_score)
```

---

**The combined scoring system provides the final integration layer that transforms individual component assessments into actionable, comprehensive wellness scores with clear improvement pathways.**