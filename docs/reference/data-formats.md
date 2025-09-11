# Data Formats - Input/Output Specifications

Complete specification of data formats, schemas, and file structures used throughout the WellPath system.

## 📊 Input Data Formats

### 1. Biomarker Data Format
**File**: `dummy_lab_results_full.csv`
**Required Columns**: 89 biomarkers + patient demographics

#### Core Demographics
```csv
patient_id,age,gender,weight,height,bmi
12345,35,female,65,165,23.9
```

#### Required Biomarkers (Sample)
```csv
glucose_fasting,hdl_cholesterol,ldl_cholesterol,triglycerides,total_cholesterol,
hemoglobin_a1c,crp_high_sensitivity,vitamin_d_25_hydroxy,vitamin_b12,folate,
systolic_bp,diastolic_bp,resting_heart_rate,body_fat_percentage,muscle_mass
95,62,118,85,180,5.4,1.2,32,450,12.5,118,76,68,22.1,28.3
```

#### Complete Biomarker List (89 markers)
```python
REQUIRED_BIOMARKERS = [
    # Metabolic Panel
    'glucose_fasting', 'hemoglobin_a1c', 'insulin_fasting',
    
    # Lipid Panel  
    'total_cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides',
    'apolipoprotein_a1', 'apolipoprotein_b', 'lipoprotein_a',
    
    # Inflammatory Markers
    'crp_high_sensitivity', 'esr', 'interleukin_6', 'tnf_alpha',
    
    # Cardiovascular
    'systolic_bp', 'diastolic_bp', 'resting_heart_rate', 'pulse_pressure',
    
    # Body Composition
    'bmi', 'body_fat_percentage', 'muscle_mass', 'visceral_fat',
    
    # Vitamins & Minerals
    'vitamin_d_25_hydroxy', 'vitamin_b12', 'folate', 'iron', 'ferritin',
    
    # Hormones
    'thyroid_stimulating_hormone', 'free_t4', 'free_t3', 'cortisol',
    
    # Kidney Function
    'creatinine', 'blood_urea_nitrogen', 'estimated_gfr',
    
    # Liver Function
    'alt', 'ast', 'alkaline_phosphatase', 'total_bilirubin',
    
    # Complete Blood Count
    'hemoglobin', 'hematocrit', 'white_blood_cell_count', 'platelet_count',
    
    # ... (additional 50+ specialized markers)
]
```

#### Data Quality Requirements
```python
BIOMARKER_VALIDATION = {
    'glucose_fasting': {'min': 60, 'max': 400, 'unit': 'mg/dL'},
    'hdl_cholesterol': {'min': 20, 'max': 100, 'unit': 'mg/dL'},
    'systolic_bp': {'min': 80, 'max': 200, 'unit': 'mmHg'},
    'age': {'min': 18, 'max': 100, 'unit': 'years'},
    'weight': {'min': 40, 'max': 200, 'unit': 'kg'}
}
```

---

### 2. Survey Data Format
**File**: `synthetic_patient_survey.csv`
**Required Columns**: 320+ survey questions across all health domains

#### Core Patient Info
```csv
patient_id,age,gender,height,weight,completion_date
12345,35,female,165,65,2024-01-15
```

#### Survey Question Format
Questions are numbered by section (e.g., 2.11, 3.04, 6.07):

```csv
# Section 2: Nutrition (2.01 - 2.50)
2.01,2.02,2.03,...,2.11,...,2.50
"Good","Daily","3 servings",...,"2.1",...,"Rarely"

# Section 3: Movement (3.01 - 3.20)  
3.01,3.02,3.03,3.04,3.05,3.06,3.07,3.08,3.09,3.10,3.11
"Excellent","30 min","Daily","3","2","1","2","45","30","20","15"

# Section 4: Sleep (4.01 - 4.20)
4.01,4.02,...,4.12,4.13,4.14,...,4.19
"Good","8 hours",...,"Sleep Quality","Weekly","Never",...,"Rarely"

# Section 6: Stress (6.01 - 6.10)
6.01,6.02,6.07
"6","Weekly","Deep breathing, meditation"
```

#### Complex Logic Questions
```python
COMPLEX_QUESTIONS = {
    "2.11": {  # Protein intake calculation
        "inputs": ["age", "gender", "weight", "height", "3.04", "3.05", "3.06"],
        "calculation": "BMR-based personalized protein target",
        "pillar_weights": {"Nutrition": 6, "Movement": 6}
    },
    "exercise_rollup": {  # Exercise frequency × duration
        "inputs": ["3.04", "3.05", "3.06", "3.07", "3.08", "3.09", "3.10", "3.11"],
        "calculation": "Total weekly minutes across 4 exercise types",
        "pillar_weights": {"Movement": 12}
    },
    "stress_coping": {  # Integrated stress assessment
        "inputs": ["6.01", "6.02", "6.07"],
        "calculation": "Stress level × frequency - coping effectiveness",
        "pillar_weights": {"Stress": 8, "Cognitive": 2, "Sleep": 2}
    }
}
```

#### Survey Validation Schema
```python
SURVEY_VALIDATION = {
    "2.11": {"type": "float", "min": 0.5, "max": 5.0},  # Protein g/kg
    "3.04": {"type": "int", "min": 0, "max": 7},        # Cardio days/week  
    "6.01": {"type": "int", "min": 1, "max": 10},       # Stress level
    "4.01": {"type": "categorical", "values": ["Poor", "Fair", "Good", "Excellent"]}
}
```

---

## 📤 Output Data Formats

### 1. Marker Scoring Output
**Directory**: `WellPath_Score_Markers/`

#### `normalized_marker_scores.csv`
```csv
patient_id,biomarker_name,raw_value,normalized_score,pillar_allocations
12345,glucose_fasting,95,85.2,"{""Nutrition"": 61.3, ""Movement"": 17.0}"
12345,hdl_cholesterol,62,78.5,"{""Nutrition"": 31.4, ""Movement"": 27.5, ""Core_Care"": 7.9}"
```

#### `marker_pillar_summary.csv`
```csv
patient_id,Nutrition,Movement,Sleep,Cognitive,Stress,Connection,Core_Care
12345,78.3,72.1,81.4,75.8,68.9,70.2,77.6
```

### 2. Survey Scoring Output  
**Directory**: `WellPath_Score_Survey/`

#### `per_question_scores_full_weighted.csv`
```csv
patient_id,question_id,raw_response,raw_score,weighted_score,pillar_allocations
12345,2.11,"2.1",8.5,8.5,"{""Nutrition"": 4.25, ""Movement"": 4.25}"
12345,3.04,"3",7.5,7.5,"{""Movement"": 7.5}"
12345,exercise_rollup,"calculated",9.2,9.2,"{""Movement"": 9.2}"
```

#### `synthetic_patient_pillar_scores_survey_with_max_pct.csv`
```csv
patient_id,Nutrition,Movement,Sleep,Cognitive,Stress,Connection,Core_Care,max_possible
12345,82.3,75.1,79.8,77.2,74.6,80.0,81.4,100
```

### 3. Combined Scoring Output
**Directory**: `WellPath_Score_Combined/`

#### `comprehensive_patient_scores_detailed.csv`
```csv
patient_id,overall_wellness_score,Nutrition_final,Movement_final,Sleep_final,
          Cognitive_final,Stress_final,Connection_final,Core_Care_final,
          Nutrition_marker_contrib,Nutrition_survey_contrib,Nutrition_education_contrib
12345,78.5,80.2,73.8,80.1,76.8,72.4,79.1,79.6,57.7,14.8,7.7
```

### 4. Patient Breakdown Output
**Directory**: `WellPath_Score_Breakdown/`

#### Individual Patient Files: `patient_[id]_comprehensive_breakdown.txt`
```
=== PATIENT COMPREHENSIVE BREAKDOWN ===
Patient ID: 12345
Overall Wellness Score: 78.5/100

=== PILLAR BREAKDOWN ===
Nutrition: 80.2/100
├── Markers (72%): 78.3 → 56.4 points
├── Survey (18%): 82.3 → 14.8 points  
└── Education (10%): 77.0 → 7.7 points

=== DETAILED BIOMARKER CONTRIBUTIONS ===
glucose_fasting: 95 mg/dL → Score: 85.2
├── Raw Value: 95 (Reference: 65-99 mg/dL)
├── Normalization: Linear scoring → 85.2/100
├── Pillar Weights: Nutrition(60%), Movement(20%), Sleep(5%)
└── Final Contributions: Nutrition(51.1), Movement(17.0), Sleep(4.3)
```

---

## 🔧 Configuration File Formats

### 1. Algorithm Configuration Schema
**File**: `src/generated_configs/REC0001.1-BINARY-THRESHOLD.json`

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
      "measurement_type": "binary",
      "evaluation_period": "daily",
      "success_criteria": "simple_target",
      "calculation_method": "exists",
      "tracked_metrics": ["dietary_fiber"],
      "threshold": 1.0,
      "success_value": 100,
      "failure_value": 0,
      "unit": "serving",
      "frequency_requirement": "daily",
      "description": "Binary threshold scoring for: Add one daily serving..."
    }
  },
  "metadata": {
    "recommendation_text": "Add one daily serving of fiber-rich food",
    "recommendation_id": "REC0001.1",
    "analysis": {
      "algorithm_type": "binary_threshold",
      "confidence": 0.9,
      "reasoning": "Binary/threshold language detected"
    },
    "metric_id": "dietary_fiber",
    "generated_at": "2024-01-15T10:30:00Z"
  }
}
```

### 2. Reference Data Schemas
**Files**: `src/ref_csv_files_airtable/*.csv`

#### `units_v3-Grid view.csv`
```csv
identifier,ui_display,symbol,unit_type,description
serving,Serving,srv,quantity,Standard serving size
step,Step,steps,quantity,Physical activity step count
hour,Hour,hr,time,Time duration in hours
mg_dL,mg/dL,mg/dL,concentration,Milligrams per deciliter
```

#### `metric_types_v3-Grid view.csv`  
```csv
identifier,name,description,units_v3,pillar_weights,validation_schema
dietary_fiber,Dietary Fiber,Daily fiber intake,serving,"{""Nutrition"":100}","{""min"":0,""max"":50}"
daily_steps,Daily Steps,Steps per day,step,"{""Movement"":100}","{""min"":0,""max"":50000}"
sleep_duration,Sleep Duration,Hours of sleep,hour,"{""Sleep"":100}","{""min"":0,""max"":12}"
```

---

## 📋 File Naming Conventions

### Input Files
- **Biomarkers**: `dummy_lab_results_full.csv` (or `lab_results_[date].csv`)
- **Survey**: `synthetic_patient_survey.csv` (or `survey_responses_[date].csv`)
- **Config**: `REC[number].[version]-[ALGORITHM-TYPE].json`

### Output Files
- **Scores**: `[component]_scores_[date].csv`
- **Breakdowns**: `patient_[patient_id]_comprehensive_breakdown.txt`
- **Summaries**: `[analysis_type]_summary_[scaling_method].csv`

### Directory Structure
```
project/
├── data/                           # Input data
│   ├── raw/                       # Raw patient data
│   └── reference/                 # Reference tables
├── WellPath_Score_[Component]/    # Output directories
└── src/generated_configs/         # Algorithm configurations
```

## ✅ Data Validation Checklist

### Pre-Processing Validation
- [ ] Patient IDs are unique and consistent across datasets
- [ ] Required columns present with correct data types
- [ ] Value ranges within acceptable clinical limits
- [ ] No duplicate records for same patient/date
- [ ] Missing data patterns are reasonable (<20% per column)

### Post-Processing Validation  
- [ ] All scores are 0-100 range
- [ ] Pillar allocations sum to component scores
- [ ] Overall scores are weighted averages of pillar scores
- [ ] Audit trails are complete and traceable
- [ ] File formats match specification exactly

### Integration Validation
- [ ] Patient IDs match across all component outputs
- [ ] Score distributions are clinically reasonable
- [ ] No systematic bias in missing data
- [ ] Cross-component correlations are expected
- [ ] Edge cases handled appropriately

---

**Adherence to these data format specifications ensures seamless integration, accurate processing, and reliable results throughout the WellPath scoring pipeline.**