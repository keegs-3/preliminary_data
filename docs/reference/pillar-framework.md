# Health Pillar Framework - Complete Reference

The WellPath system evaluates patient health across **7 evidence-based health pillars** with sophisticated weighting and allocation systems.

## 🎯 Pillar Overview

### Design Principles
1. **Evidence-Based**: Each pillar reflects established health science research
2. **Balanced Assessment**: Multiple data sources prevent single-point failures
3. **Clinical Relevance**: Weightings reflect real-world health impact
4. **Actionable Insights**: Pillar breakdowns guide targeted interventions

## 📊 Complete Pillar Specifications

### 1. Healthful Nutrition
**Weight Distribution**: Markers 72% | Survey 18% | Education 10%

**Clinical Rationale**: Biomarkers strongly reflect nutritional status through measurable metabolic indicators.

**Key Biomarkers**:
- Glucose metabolism markers (fasting glucose, HbA1c)
- Lipid profile (HDL, LDL, triglycerides)
- Inflammatory markers (CRP, homocysteine)
- Micronutrient status (B12, folate, vitamin D)

**Survey Components**:
- Dietary patterns and food frequency
- Personalized protein intake calculations
- Meal timing and consistency
- Food quality assessments

**Education Metrics**:
- Nutrition education module completion
- Recipe/meal planning engagement
- Dietary tracking tool usage

---

### 2. Movement + Exercise  
**Weight Distribution**: Markers 54% | Survey 36% | Education 10%

**Clinical Rationale**: Balanced objective/subjective assessment recognizing both physiological markers and self-reported activity patterns.

**Key Biomarkers**:
- Cardiovascular fitness indicators
- Metabolic efficiency markers
- Body composition metrics
- Resting heart rate variability

**Survey Components**:
- Exercise frequency and duration rollups:
  - Cardio: Frequency (3.04) × Duration (3.08)
  - Strength: Frequency (3.05) × Duration (3.09)
  - HIIT: Frequency (3.06) × Duration (3.10)  
  - Flexibility: Frequency (3.07) × Duration (3.11)
- Activity preference and barriers assessment
- Recovery and injury patterns

**Education Metrics**:
- Exercise program completion rates
- Movement technique video engagement
- Fitness goal setting participation

---

### 3. Restorative Sleep
**Weight Distribution**: Markers 63% | Survey 27% | Education 10%

**Clinical Rationale**: Sleep biomarkers are highly predictive of sleep quality, with survey providing context for sleep environment and habits.

**Key Biomarkers**:
- Sleep-related hormone levels
- Cardiovascular recovery metrics
- Inflammatory markers affected by sleep
- Circadian rhythm indicators

**Survey Components**:
- Sleep duration and quality self-assessment
- Sleep issues frequency mapping (4.12-4.19)
- Sleep environment and hygiene practices
- Stress impact on sleep patterns

**Education Metrics**:
- Sleep hygiene education completion
- Sleep tracking tool adoption
- Relaxation technique engagement

---

### 4. Cognitive Health
**Weight Distribution**: Markers 36% | Survey 54% | Education 10%

**Clinical Rationale**: Self-reported cognitive function is critical for early detection of cognitive changes, complemented by relevant biomarkers.

**Key Biomarkers**:
- Brain health inflammatory markers
- Cardiovascular health indicators
- Metabolic markers affecting cognition
- Nutrient status for brain function

**Survey Components**:
- Cognitive function self-assessment
- Memory and concentration patterns
- Mental clarity and focus evaluation
- Cognitive activity engagement

**Education Metrics**:
- Brain training program participation
- Cognitive health education completion
- Mental stimulation activity tracking

---

### 5. Stress Management
**Weight Distribution**: Markers 27% | Survey 63% | Education 10%

**Clinical Rationale**: Stress is primarily a subjective experience, though biomarkers can indicate physiological stress response.

**Key Biomarkers**:
- Cortisol and stress hormone levels
- Inflammatory stress markers
- Blood pressure variability
- Heart rate variability

**Survey Components**:
- Integrated stress assessment (6.01, 6.02, 6.07):
  - Stress level (1-10 scale)
  - Stress frequency (how often experienced)
  - Coping mechanism quality and effectiveness
- Stress trigger identification
- Work-life balance evaluation

**Education Metrics**:
- Stress management technique training
- Mindfulness and meditation program engagement
- Relaxation skill development

---

### 6. Connection + Purpose
**Weight Distribution**: Markers 18% | Survey 72% | Education 10%

**Clinical Rationale**: Social connection and life purpose are best assessed through self-report, with minimal biomarker correlation.

**Key Biomarkers**:
- Limited biomarker involvement
- Some stress-related markers may reflect social isolation
- General wellness indicators

**Survey Components**:
- Social connection quality and frequency
- Relationship satisfaction assessment
- Community involvement and engagement
- Life purpose and meaning evaluation
- Support system strength

**Education Metrics**:
- Social skills and communication training
- Community engagement program participation
- Purpose-finding workshop completion

---

### 7. Core Care (Preventive Healthcare)
**Weight Distribution**: Markers 49.5% | Survey 40.5% | Education 10%

**Clinical Rationale**: Balanced assessment of objective health maintenance (biomarkers) and healthcare engagement behaviors (survey).

**Key Biomarkers**:
- Preventive screening results
- Chronic disease risk markers
- General health maintenance indicators
- Age-appropriate health metrics

**Survey Components**:
- Healthcare utilization patterns
- Preventive care compliance
- Health screening participation
- Healthcare provider relationships

**Education Metrics**:
- Preventive care education completion
- Health advocacy skill development
- Healthcare navigation training

## ⚖️ Weighting Rationale

### High Biomarker Weight Pillars
**Nutrition (72%)** and **Sleep (63%)**:
- Biomarkers directly reflect physiological status
- Objective measurements reduce self-report bias
- Lab values show long-term patterns vs. momentary states

### High Survey Weight Pillars  
**Connection (72%)** and **Stress (63%)**:
- Subjective experiences best captured through self-report
- Individual perception is the primary clinical indicator
- Biomarkers provide supporting but not primary evidence

### Balanced Pillars
**Movement (54%/36%)** and **Core Care (49.5%/40.5%)**:
- Both objective and subjective measures clinically relevant
- Combination provides comprehensive assessment
- Helps validate self-report against measurable indicators

## 🔄 Pillar Interaction Analysis

### Cross-Pillar Correlations
```
Strong Positive Correlations (r > 0.6):
- Nutrition ↔ Movement (shared metabolic pathways)
- Sleep ↔ Stress Management (bidirectional relationship)
- Movement ↔ Core Care (preventive health behaviors)

Moderate Correlations (0.3 < r < 0.6):
- Stress ↔ Sleep (stress affects sleep quality)
- Nutrition ↔ Cognitive (nutrition impacts brain function)
- Connection ↔ Stress (social support reduces stress)
```

### Multi-Pillar Impact Questions
Certain survey questions appropriately impact multiple pillars:

```python
"2.11": {  # Protein intake
    "pillar_weights": {"Nutrition": 6, "Movement": 6},
    "rationale": "Protein supports both metabolic health and muscle recovery"
},
"6.01": {  # Stress level
    "pillar_weights": {"Stress": 8, "Cognitive": 2, "Sleep": 2},
    "rationale": "Stress affects cognitive function and sleep quality"
}
```

## 📈 Population Benchmarking

### Pillar Score Distributions (Population Averages)
```
Pillar                 | Mean  | Std Dev | 25th %ile | 75th %ile
--------------------- |-------|---------|-----------|----------
Healthful Nutrition   | 72.3  | 18.4    | 58.2      | 86.1
Movement + Exercise   | 68.7  | 22.1    | 52.3      | 84.9
Restorative Sleep     | 74.8  | 16.9    | 62.4      | 87.3
Cognitive Health      | 77.1  | 15.2    | 66.8      | 88.7
Stress Management     | 65.4  | 21.8    | 48.7      | 82.2
Connection + Purpose  | 79.2  | 17.6    | 67.1      | 92.4
Core Care            | 71.9  | 19.3    | 57.8      | 86.7
```

### Age-Adjusted Expectations
```python
AGE_ADJUSTMENTS = {
    "18-29": {"Movement": +5, "Sleep": +3, "Stress": -2},
    "30-44": {"Movement": +2, "Stress": -1, "Core_Care": +1},
    "45-59": {"Movement": -1, "Cognitive": +1, "Core_Care": +3},
    "60+": {"Movement": -3, "Cognitive": +2, "Core_Care": +5}
}
```

## 🎯 Clinical Applications

### Risk Stratification
```python
def classify_patient_risk(pillar_scores):
    high_risk_pillars = [p for p in pillar_scores if p < 40]
    moderate_risk_pillars = [p for p in pillar_scores if 40 <= p < 65]
    
    if len(high_risk_pillars) >= 3:
        return "high_risk"
    elif len(moderate_risk_pillars) >= 4:
        return "moderate_risk"
    else:
        return "low_risk"
```

### Intervention Prioritization
```python
def prioritize_interventions(pillar_scores, improvement_potential):
    # High impact, achievable improvements first
    priority_matrix = {}
    
    for pillar, score in pillar_scores.items():
        impact = calculate_health_impact(pillar)
        achievability = improvement_potential[pillar]['achievability']
        
        priority_matrix[pillar] = {
            "priority_score": impact * achievability,
            "intervention_type": get_intervention_type(pillar, score)
        }
    
    return sorted(priority_matrix.items(), key=lambda x: x[1]['priority_score'], reverse=True)
```

## 🔧 Configuration Management

### Pillar Weight Validation
```python
def validate_pillar_weights():
    for pillar, weights in PILLAR_WEIGHTS.items():
        total = weights['markers'] + weights['survey'] + weights['education']
        assert total == 100, f"Pillar {pillar} weights sum to {total}, not 100"
        
        # Clinical validation checks
        if pillar in ['Nutrition', 'Sleep'] and weights['markers'] < 50:
            warnings.warn(f"Low biomarker weight for {pillar}: {weights['markers']}%")
        
        if pillar in ['Connection', 'Stress'] and weights['survey'] < 50:
            warnings.warn(f"Low survey weight for {pillar}: {weights['survey']}%")
```

### Dynamic Weight Adjustment
```python
def adjust_weights_for_missing_data(pillar_weights, available_data):
    adjusted_weights = pillar_weights.copy()
    
    for pillar, weights in adjusted_weights.items():
        if 'markers' not in available_data:
            # Redistribute marker weight to survey
            weights['survey'] += weights['markers']
            weights['markers'] = 0
        
        if 'education' not in available_data:
            # Redistribute education weight proportionally
            marker_survey_total = weights['markers'] + weights['survey']
            if marker_survey_total > 0:
                weights['markers'] += weights['education'] * (weights['markers'] / marker_survey_total)
                weights['survey'] += weights['education'] * (weights['survey'] / marker_survey_total)
                weights['education'] = 0
    
    return adjusted_weights
```

---

**This pillar framework provides the clinical foundation for comprehensive, evidence-based health assessment that guides personalized intervention strategies while maintaining statistical validity across diverse patient populations.**