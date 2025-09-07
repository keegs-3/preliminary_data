# WellPath Health Analytics System - Complete User Guide

## Overview

The WellPath system is a comprehensive health analytics platform that generates personalized health recommendations and impact scores based on biomarker data and survey responses. The system processes patient data through multiple scoring algorithms to provide actionable health insights across seven evidence-based health pillars.

## System Architecture

### Core Components

1. **Data Generation**
   - `generate_biomarker_dataset.py` - Synthetic patient biomarker data
   - `generate_survey_dataset.py` - Lifestyle survey data generation  

2. **Scoring Engines**
   - `WellPath_score_runner_survey.py` - Survey scoring with custom logic
   - `WellPath_score_runner_markers.py` - Biomarker scoring with reference ranges
   - `WellPath_score_runner_combined.py` - Integrated scoring system

3. **Analysis & Impact**
   - `wellpath_impact_scorer_improved.py` - Statistical impact scoring with 4 scaling methods
   - `Patient_score_breakdown_generator.py` - Individual patient audit trails

4. **Data Management**
   - `Recommendations_JSON_Updater.py` - Airtable to JSON converter for recommendation data

### Health Pillars Framework

The system operates on 7 evidence-based health pillars with weighted contributions:

| Pillar | Weight | Marker % | Survey % | Education % |
|--------|--------|----------|----------|-------------|
| **Healthful Nutrition** | 25% | 72% | 18% | 10% |
| **Movement + Exercise** | 20% | 54% | 36% | 10% |
| **Restorative Sleep** | 15% | 63% | 27% | 10% |
| **Stress Management** | 15% | 27% | 63% | 10% |
| **Cognitive Health** | 10% | 36% | 54% | 10% |
| **Connection + Purpose** | 10% | 18% | 72% | 10% |
| **Core Care** | 15% | 49.5% | 40.5% | 10% |

---

## Quick Start Guide

### Prerequisites

```bash
pip install pandas numpy uuid random datetime openpyxl
```

### Complete Workflow (Start to Finish)

#### Option 1: Synthetic Data (For Testing/Development)

**Step 1: Generate Biomarker Data**
```bash
python generate_biomarker_dataset.py
```
**Outputs:** `data/dummy_lab_results_full.csv` - 89 columns of biomarker data

**Step 2: Generate Survey Data**
```bash
python generate_survey_dataset.py
```
**Outputs:** `data/synthetic_patient_survey.csv` - 320 columns of lifestyle survey responses

#### Option 2: Real Patient Data (For Production)

Prepare your data files according to these exact specifications:

**Biomarker Data Format** - Must contain **exactly 89 columns**:

Required Patient Demographics (19 columns):
```
patient_id, collection_date, age, sex, athlete, cycle_phase, menopausal_status,
height_in, weight_lb, bmi, sleep_score, percent_body_fat, smm_to_ffm, 
hip_to_waist, genetic_risk_score, diet_quality, stress_level, health_profile, fitness_level
```

Required Biomarker Columns (70 columns):
```
vo2_max, grip_strength, visceral_fat, hrv, hdl, ldl, triglycerides, total_cholesterol,
lp(a), apob, omega3_index, rdw, resting_heart_rate, magnesium_rbc, vitamin_d,
serum_ferritin, total_iron_binding_capacity, transferrin_saturation, hscrp, wbc,
lymphocytes, neutrophils, eosinophils, lymphocyte_percent, neut_lymph_ratio,
fasting_glucose, fasting_insulin, homa_ir, hba1c, alt, uric_acid, alkaline_phosphatase,
testosterone, albumin, serum_protein, hemoglobin, hematocrit, egfr, cystatin_c, bun,
vitamin_b12, folate_serum, folate_rbc, creatinine, homocysteine, cortisol_morning,
tsh, calcium_serum, calcium_ionized, dhea_s, estradiol, progesterone, ast, ggt,
sodium, potassium, ck, iron, mch, mchc, mcv, rbc, platelet, ferritin,
free_testosterone, shbg, rem_sleep, deep_sleep, blood_pressure_systolic, blood_pressure_diastolic
```

**Survey Data Format** - Must contain **exactly 320 columns** with specific question IDs (1.01, 1.02, 2.11, etc.)

### Data Processing Pipeline

#### Step 3: Run Survey Scoring
```bash
python WellPath_score_runner_survey.py
```
**Requires:** Biomarker + Survey CSV files  
**Outputs to `/WellPath_Score_Survey/`:**
- `per_question_scores_full_weighted.csv` - Individual question scores with custom logic
- `question_gap_analysis.csv` - Missing data analysis
- `synthetic_patient_pillar_scores_survey_with_max_pct.csv` - Pillar-level survey scores

#### Step 4: Run Biomarker Scoring
```bash
python WellPath_score_runner_markers.py
```
**Requires:** Biomarker CSV file  
**Outputs to `/WellPath_Score_Markers/`:**
- `scored_markers_with_max.csv` - Individual biomarker scores with reference ranges
- `marker_gap_analysis_absolute.csv` - Improvement potential analysis
- `marker_gap_analysis_relative.csv` - Relative performance analysis
- `marker_pillar_summary.csv` - Pillar-level biomarker scores

#### Step 5: Combine All Scoring Data
```bash
python WellPath_score_runner_combined.py
```
**Requires:** All outputs from Steps 3 & 4 plus original data files  
**Outputs to `/WellPath_Score_Combined/`:**
- `comprehensive_patient_scores_detailed.csv` - Complete patient profiles
- `markers_for_impact_scoring.csv` - Formatted for impact analysis
- `all_survey_questions_summary.csv` - Survey analysis summary
- `marker_contribution_analysis.csv` - Biomarker impact breakdown
- `detailed_scoring_summary.csv` - Complete scoring audit trail

#### Step 5.5: Generate Individual Patient Breakdowns
```bash
python Patient_score_breakdown_generator.py
```
**Requires:** `WellPath_Score_Combined/comprehensive_patient_scores_detailed.csv`  
**Outputs to `/WellPath_Score_Breakdown/`:**
- Individual patient breakdown files with complete audit trails
- Complex survey calculation analysis
- UI-ready patient reports with scoring transparency

**Report Features:**
- **Survey Structure Alignment**: Survey questions follow same audit trail as biomarkers (Response → Raw Score → Weight → Weighted Score → Pillar Contribution)
- **Complex Calculations**: Proper rollups for exercise types, stress+coping interactions, sleep issues with frequency mapping
- **No Redundancy**: Individual component questions (3.04-3.11, 6.01-6.02, 6.07, 4.13-4.19) excluded from detailed breakdown since they're part of complex logic
- **Complete Transparency**: Raw scores, weights, weighted scores, and normalized pillar contributions for all components

#### Step 6: Update Recommendations Data (Optional - When Airtable Changes)

**Prerequisites:**
1. Export your Airtable data to `WellPath Tiered Markers.xlsx`
2. Ensure the Excel file contains columns: `ID`, `Title`, `Raw_impact`, `Primary Markers`, `Secondary Markers`, `Tertiary Markers`, `Primary Metrics`, `Secondary Metrics`, `Tertiary Metrics`

```bash
python Recommendations_JSON_Updater.py
```

**What this does:**
- Creates `Recommendations_List_Old/` backup folder
- Moves existing `recommendations_list.json` to backup with timestamp
- Converts Excel data to proper JSON format with standardized marker names
- Replaces `recommendations_list.json` with updated data

**Excel File Format Requirements:**

| Column Name | Description | Example |
|-------------|-------------|---------|
| `ID` | Unique recommendation identifier | "REC0001.1" |
| `Title` | Recommendation title | "Increase Fiber Intake" |
| `Raw_impact` | Evidence-based impact score | 75 |
| `Primary Markers` | Comma-separated primary markers | "LDL,ApoB,hsCRP" |
| `Secondary Markers` | Comma-separated secondary markers | "HbA1c,Fasting Glucose" |
| `Tertiary Markers` | Comma-separated tertiary markers | "" |

**Automatic Marker Name Standardization:**
```python
# Excel format → JSON format
"Total Cholesterol" → "total_cholesterol"
"Blood Pressure - Systolic" → "blood_pressure_systolic" 
"Vitamin D" → "vitamin_d"
"% Bodyfat" → "bodyfat"
"VO2 Max" → "vo2_max"
```

#### Step 7: Run Impact Scoring
```bash
python wellpath_impact_scorer_improved.py
```

Automatically runs all 4 scaling methods (linear, percentile, log_normal, z_score) and generates results for each.

**Requires:** All outputs from Step 5 + updated `recommendations_list.json`  
**Outputs to `/Recommendation_Impact_Scores/`:**
- `detailed_impact_scores_{method}.csv` - All ~9,100 personalized impact scores
- `summary_impact_scores_{method}.csv` - Key metrics summary  
- `statistical_patient_summary_{method}.csv` - Top 5 recommendations per patient

---

## Data Generation Details

### Biomarker Dataset Generation

Creates realistic synthetic patients with:

- **Demographics**: Age, sex, athlete status, BMI, body fat percentage
- **Cardiovascular**: Cholesterol panels, blood pressure, heart rate variability
- **Metabolic**: Glucose, insulin, HbA1c, lipid profiles
- **Inflammatory**: CRP, IL-6, TNF-α markers
- **Hormonal**: Sex hormones, thyroid, cortisol
- **Fitness**: VO2 max, grip strength, body composition
- **Sleep**: REM, deep sleep metrics

### Survey Dataset Generation

Creates lifestyle questionnaire responses across:

- **Nutrition habits** and dietary patterns
- **Exercise frequency** and activity levels  
- **Sleep quality** and duration patterns
- **Stress management** techniques and levels
- **Cognitive engagement** and mental wellness
- **Social connections** and life purpose
- **Healthcare utilization** and preventive care

---

## Scoring Methodology

### Biomarker Scoring

Uses custom evidence-based reference ranges with defined score mappings:

```python
def score_biomarker(value, ranges_config):
    """
    Score biomarkers on 0-1 scale based on custom-defined ranges
    """
    for range_config in ranges_config:
        if range_config['min'] <= value <= range_config['max']:
            return range_config['score']  # Returns 0.0-1.0
    return 0.0
```

**Example Configuration:**
```python
"ldl": {
    "ranges": [
        {"min": 0, "max": 100, "score": 1.0},      # Optimal
        {"min": 100, "max": 130, "score": 0.8},    # Good  
        {"min": 130, "max": 160, "score": 0.6},    # Borderline
        {"min": 160, "max": 190, "score": 0.3},    # High
        {"min": 190, "max": 999, "score": 0.0}     # Very High
    ]
}
```

### Survey Scoring

Survey responses use both simple mapping and sophisticated custom logic:

**Simple Response Mapping:**
```python
response_scores = {
    "Daily": 1.0,
    "Several times a week": 0.8, 
    "Weekly": 0.6,
    "Occasionally": 0.4,
    "Rarely or Never": 0.2
}
```

**Complex Custom Logic Examples:**
- **Protein Intake**: Personalized targets based on age, weight (Q2.11)
- **Movement Scoring**: Frequency + duration for cardio, strength, flexibility, HIIT (Q3.04-3.11)
- **Sleep Issues**: Multi-pillar impact with frequency weighting (Q4.12-4.19)
- **Stress Management**: Context-aware coping strategy scoring (Q6.01-6.07)
- **Substance Use**: Time-since-quit bonuses and usage trend analysis (Q8.01-8.38)

### Combined Pillar Scoring Algorithm

```python
def calculate_pillar_score(patient_data, pillar_config):
    """
    1. Score each marker/survey item (0.0-1.0)
    2. Multiply by item weight for the pillar
    3. Sum all weighted scores for the pillar
    4. Calculate max possible pillar score
    5. Convert to percentage: (actual_sum / max_sum) * 100
    6. Apply pillar weight in final combination
    """
    
    pillar_weighted_sum = 0
    pillar_max_sum = 0
    
    for item in pillar_items:
        item_score = score_item(patient_data[item])  # 0.0-1.0
        item_weight = pillar_config[item]['weight']
        
        pillar_weighted_sum += (item_score * item_weight)
        pillar_max_sum += (1.0 * item_weight)  # Max possible
    
    pillar_percentage = (pillar_weighted_sum / pillar_max_sum) * 100
    return pillar_percentage
```

---

## Statistical Impact Scoring

### Scaling Methods

1. **Linear Scaling**: Simple min-max normalization (0-10 scale)
2. **Percentile Scaling**: Bottom 10%→0-2, Middle 80%→2-8, Top 10%→8-10
3. **Log-Normal Scaling**: Log transformation for skewed distributions
4. **Z-Score Scaling**: Standard score normalization for normal distributions

### Impact Calculation Process

```python
def calculate_impact_score(patient_markers, recommendation):
    """
    WellPath Impact Scoring Process:
    
    1. Start with baseline_impact (evidence-based recommendation score)
    2. For each affected marker, calculate improvement points
    3. Apply pillar improvement potential percentage  
    4. Weight by pillar importance and marker category (primary/secondary/tertiary)
    5. Sum all marker impacts to get total_raw_points
    6. Apply statistical scaling to convert to final_score (0-10)
    7. Assign tier based on final score (High ≥7, Medium 4-7, Low <4)
    """
    
    baseline_impact = recommendation['baseline_impact']  # e.g., 75
    total_raw_points = 0
    
    for marker in recommendation['affected_markers']:
        marker_raw_points = 0
        
        # Calculate impact for each pillar this marker affects
        for pillar in marker['affected_pillars']:
            improvement_points = calculate_marker_improvement(patient_data[marker])
            pillar_potential_pct = get_pillar_improvement_potential(patient, pillar)
            pillar_weight = PILLAR_WEIGHTS[pillar]  # e.g., 0.25 for Nutrition
            category_weight = CATEGORY_WEIGHTS[marker['category']]  # 1.0, 0.7, 0.4
            
            pillar_raw_points = (
                improvement_points *            # Patient-specific improvement potential
                (pillar_potential_pct / 100.0) *  # Pillar improvement % (e.g., 58.38%)
                pillar_weight *                 # WellPath pillar weight (e.g., 0.25)
                category_weight                 # Primary=1.0, Secondary=0.7, Tertiary=0.4
            )
            
            marker_raw_points += pillar_raw_points
        
        total_raw_points += marker_raw_points
    
    # Statistical scaling converts total_raw_points to 0-10 final_score
    final_score = apply_statistical_scaling(total_raw_points, method='percentile')
    
    # Assign tier based on final score
    tier = 'high' if final_score >= 7 else 'medium' if final_score >= 4 else 'low'
    
    return {
        'baseline_impact': baseline_impact,      # e.g., 75
        'total_raw_points': total_raw_points,    # e.g., 3.354
        'final_score': final_score,              # e.g., 8.23
        'tier': tier                             # e.g., 'high'
    }
```

### Expected Results

```bash
============================================================
🧪 Running PERCENTILE scaling method
============================================================
📊 Processing 50 patients with 182 recommendations each...

📈 Statistical Summary:
Total impact scores: 9,100
High impact (score ≥ 7): 1,456 (16.0%)
Medium impact (4 ≤ score < 7): 3,458 (38.0%) 
Low impact (score < 4): 4,186 (46.0%)

Mean score: 4.96
Standard deviation: 2.34
```

---

## File Structure & Outputs

### Input Data Files
```
data/
├── dummy_lab_results_full.csv           # Generated biomarker data
└── synthetic_patient_survey.csv         # Generated survey responses
```

### Recommendation Data Files
```
WellPath Tiered Markers.xlsx             # Airtable export (Excel format)
recommendations_list.json                # Converted JSON format (used by impact scorer)
Recommendations_List_Old/                # Backup folder
├── recommendations_list_backup_20250902_143022.json
├── recommendations_list_backup_20250901_091533.json
└── ...                                  # Historical backups with timestamps
```

### Processing Outputs

#### WellPath_Score_Survey/
```
├── per_question_scores_full_weighted.csv
├── question_gap_analysis.csv
└── synthetic_patient_pillar_scores_survey_with_max_pct.csv
```

#### WellPath_Score_Markers/
```
├── marker_gap_analysis_absolute.csv
├── marker_gap_analysis_relative.csv
├── marker_pillar_summary.csv
└── scored_markers_with_max.csv
```

#### WellPath_Score_Combined/
```
├── markers_for_impact_scoring.csv
├── all_survey_questions_summary.csv
├── marker_contribution_analysis.csv
├── detailed_scoring_summary.csv
└── comprehensive_patient_scores_detailed.csv
```

#### WellPath_Score_Breakdown/
```
├── patient_1_complete_breakdown.csv
├── patient_2_complete_breakdown.csv
└── ...                                  # Individual patient audit trails
```

#### Recommendation_Impact_Scores/
```
├── detailed_impact_scores_linear.csv        # All 9,100+ scores using linear scaling
├── detailed_impact_scores_percentile.csv    # All 9,100+ scores using percentile scaling  
├── detailed_impact_scores_log_normal.csv    # All 9,100+ scores using log-normal scaling
├── detailed_impact_scores_z_score.csv       # All 9,100+ scores using z-score scaling
├── summary_impact_scores_{method}.csv       # Key metrics summary for each method
└── statistical_patient_summary_{method}.csv # Top 5 recommendations per patient for each method
```

---

## Configuration

### Pillar Weights Configuration

```python
pillar_weights = {
    "Healthful Nutrition": {"markers": 0.72, "survey": 0.18, "education": 0.10},
    "Movement + Exercise": {"markers": 0.54, "survey": 0.36, "education": 0.10},
    "Restorative Sleep": {"markers": 0.63, "survey": 0.27, "education": 0.10},
    "Cognitive Health": {"markers": 0.36, "survey": 0.54, "education": 0.10},
    "Stress Management": {"markers": 0.27, "survey": 0.63, "education": 0.10},
    "Connection + Purpose": {"markers": 0.18, "survey": 0.72, "education": 0.10},
    "Core Care": {"markers": 0.495, "survey": 0.405, "education": 0.10}
}
```

### Directory Configuration

```python
# Update paths in WellPath_score_runner_combined.py
base_dir = r"C:\Your\Path\To\WellPath\Data"

# Input files
marker_detailed_file = os.path.join(base_dir, "WellPath_Score_Markers", "scored_markers_with_max.csv")
survey_detailed_file = os.path.join(base_dir, "WellPath_Score_Survey", "per_question_scores_full_weighted.csv")
```

---

## Troubleshooting

### Common Data Format Issues

**Data Format Validation Errors:**
```bash
❌ KeyError: 'patient_id' not found
❌ ValueError: columns don't match expected format
```
**Solution:** 
- Verify your biomarker file has exactly 89 columns with correct names
- Verify your survey file has exactly 320 columns with correct question IDs
- Ensure patient_id columns match exactly between files
- Use the synthetic data generators as templates for proper formatting

**Missing Input Files:**
```bash
# For synthetic data testing
python generate_biomarker_dataset.py
python generate_survey_dataset.py

# For real data, ensure your files match the required format
```

**Excel File Issues:**
```bash
❌ Error: Excel file 'WellPath Tiered Markers.xlsx' not found
```
**Solution:** Export your Airtable data to Excel format with the required columns

**Memory Issues with Large Datasets:**
```python
# Process in smaller batches
patient_subset = ['patient_1', 'patient_2', ...]  
python wellpath_impact_scorer_improved.py --patient-subset patient_1 patient_2
```

**Inconsistent Patient IDs:**
- Ensure the same patient IDs are used across biomarker and survey files
- Use consistent formatting (e.g., "patient_1", "patient_2", not mixed formats)
- For reproducible synthetic data, use `np.random.seed(42)`

### Debug Mode

```python
import warnings
warnings.filterwarnings('default')  # Show all warnings

# Enable verbose output in scoring scripts
DEBUG = True

# Check intermediate file generation
import os
print("Generated files:")
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith('.csv'):
            print(f"  {os.path.join(root, file)}")
```

### Verification Steps

To verify everything is working correctly:

1. **Check File Structure**: Ensure you have the required directory structure
2. **Validate Data Format**: Use synthetic generators as templates
3. **Test with Sample Data**: Start with a small patient subset (5-10 patients)  
4. **Validate Output**: Check that CSV files are generated with expected columns
5. **Review Logs**: Look for error messages in the console output
6. **Cross-reference Patient IDs**: Ensure consistency across all files

---

## Research Applications

This system is designed for:

- **Health intervention research** - A/B testing wellness programs
- **Biomarker validation studies** - Testing new health metrics
- **Personalized medicine development** - Algorithm training data
- **Population health analytics** - Identifying health trends
- **Digital health platform testing** - Realistic test datasets

---

## Advanced Features

### Custom Biomarker Generation

```python
def generate_custom_markers(profile, custom_ranges):
    """
    Add your own biomarkers with custom reference ranges
    """
    markers = {}
    for marker_name, ranges in custom_ranges.items():
        markers[marker_name] = generate_realistic_value(profile, ranges)
    return markers
```

### Custom Survey Questions

```python
def add_custom_survey_questions(base_questions, custom_questions):
    """
    Extend the survey with domain-specific questions
    """
    return {**base_questions, **custom_questions}
```

### Impact Scoring Customization

```python
# Add new scaling method
def apply_custom_scaling(raw_scores):
    """
    Implement your own scaling algorithm
    """
    return scaled_scores
```

---

## Next Steps

1. **Setup**: Run data generation scripts to create initial datasets
2. **Configure**: Update file paths and pillar weights for your use case  
3. **Run**: Execute scoring pipelines to generate comprehensive analytics
4. **Update Recommendations**: Use Airtable integration to keep recommendation data current
5. **Analyze**: Use generated CSV files to derive health insights
6. **Extend**: Add custom biomarkers, surveys, or scoring methods as needed

The WellPath system provides a complete foundation for health analytics, from data generation through personalized recommendations, with extensive customization options for research and clinical applications.