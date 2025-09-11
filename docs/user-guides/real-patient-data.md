# WellPath Health Analytics System Documentation

## 📋 Overview

The WellPath system is a comprehensive health analytics platform that generates personalized health recommendations and impact scores based on biomarker data and survey responses. The system processes patient data through multiple scoring algorithms to provide actionable health insights across seven key health pillars.

## 🚀 Quick Start

### Option 1: Synthetic Data (For Testing/Development)

Generate synthetic patient data to test the system:

```bash
# Step 1: Generate synthetic biomarker data (50 patients, 89 columns)
python generate_biomarker_dataset.py

# Step 2: Generate synthetic survey data (50 patients, 320 columns)
python generate_survey_dataset.py
```

### Option 2: Real Patient Data (For Production)

#### Step 1: Format Your Data Files

Prepare your biomarker and survey CSV files according to the specifications below.

#### Step 2: Validate Data Format

Ensure your files match the exact column requirements:

## 📊 Data Format Requirements

### Biomarker Data Format

Your biomarker CSV file must contain **exactly 89 columns** with these exact column names:

#### Required Patient Demographics (6 columns):
```
patient_id, collection_date, age, sex, athlete, cycle_phase, menopausal_status,
height_in, weight_lb, bmi, sleep_score, percent_body_fat, smm_to_ffm, 
hip_to_waist, genetic_risk_score, diet_quality, stress_level, health_profile, fitness_level
```

#### Required Biomarker Columns (70 columns):
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

**Example row:**
```csv
patient_id,collection_date,age,sex,athlete,cycle_phase,menopausal_status,height_in,weight_lb,bmi,sleep_score,percent_body_fat,smm_to_ffm,hip_to_waist,genetic_risk_score,diet_quality,stress_level,health_profile,fitness_level,vo2_max,grip_strength,visceral_fat,hrv,hdl,ldl,triglycerides,total_cholesterol,lp(a),apob,omega3_index,rdw,resting_heart_rate,magnesium_rbc,vitamin_d,serum_ferritin,total_iron_binding_capacity,transferrin_saturation,hscrp,wbc,lymphocytes,neutrophils,eosinophils,lymphocyte_percent,neut_lymph_ratio,fasting_glucose,fasting_insulin,homa_ir,hba1c,alt,uric_acid,alkaline_phosphatase,testosterone,albumin,serum_protein,hemoglobin,hematocrit,egfr,cystatin_c,bun,vitamin_b12,folate_serum,folate_rbc,creatinine,homocysteine,cortisol_morning,tsh,calcium_serum,calcium_ionized,dhea_s,estradiol,progesterone,ast,ggt,sodium,potassium,ck,iron,mch,mchc,mcv,rbc,platelet,ferritin,free_testosterone,shbg,rem_sleep,deep_sleep,blood_pressure_systolic,blood_pressure_diastolic
patient_1,2024-01-15,34,male,no,NA,NA,70.2,175.8,25.1,7.2,18.5,0.82,0.89,moderate,moderate,moderate,average,moderate,42.1,98.5,8.2,45.2,52.1,128.5,142.2,180.7,12.5,0.89,4.2,13.8,65.2,2.1,32.8,89.5,298.5,22.1,1.8,6.2,1.8,3.9,0.5,29.1,2.2,89.2,8.5,2.1,5.2,18.5,4.8,89.5,520.2,4.2,7.1,14.8,42.1,95.2,1.08,15.8,425.2,18.9,8.2,0.89,12.5,8.9,2.1,9.8,1.25,215.8,28.9,2.1,22.5,22.1,142.5,139.8,142.1,82.5,175.2,89.2,18.9,35.2,82.1,78.9,118.5,82.1
```

### Survey Data Format

Your survey CSV file must contain **exactly 320 columns** with specific question IDs. See [Survey Data Format](#survey-data-format) section below for complete specifications.

## 🔄 Processing Pipeline

### Step 1: Update File Paths (For Real Data)

Update the file paths in your scoring scripts:

```bash
# Update file paths in the scoring scripts
python WellPath_score_runner_markers.py
python WellPath_score_runner_survey.py  
python WellPath_score_runner_combined.py

# Or specify custom files
python wellpath_impact_scorer_improved.py \
  --recommendations-file "your_recommendations.json" \
  --markers-file "your_markers.csv" \
  --comprehensive-file "your_comprehensive.csv"
```

### Step 2: Run Survey Scoring

```bash
python WellPath_score_runner_survey.py
```

**Requires:** Biomarker + Survey CSV files  
**Outputs to `/WellPath_Score_Survey/`:**
- `per_question_scores_full_weighted.csv`
- `question_gap_analysis.csv`
- `synthetic_patient_pillar_scores_survey_with_max_pct.csv`

### Step 3: Run Biomarker Scoring

```bash
python WellPath_score_runner_markers.py
```

**Requires:** Biomarker CSV file  
**Outputs to `/WellPath_Score_Markers/`:**
- `marker_gap_analysis_absolute.csv`
- `marker_gap_analysis_relative.csv`
- `marker_pillar_summary.csv`
- `scored_markers_with_max.csv`

### Step 4: Combine All Scoring Data

```bash
python WellPath_score_runner_combined.py
```

**Requires:**
- `WellPath_Score_Markers/scored_markers_with_max.csv`
- `WellPath_Score_Survey/per_question_scores_full_weighted.csv`
- Your biomarker CSV file
- Your survey CSV file

**Outputs to `/WellPath_Score_Combined/`:**
- `markers_for_impact_scoring.csv`
- `all_survey_questions_summary.csv`
- `marker_contribution_analysis.csv`
- `detailed_scoring_summary.csv`
- `comprehensive_patient_scores_detailed.csv`

### Step 5: Run Impact Scoring

```bash
python wellpath_impact_scorer_improved.py
```

This automatically runs all 4 scaling methods (linear, percentile, log_normal, z_score) and generates results for each.

**Requires:** All outputs from Step 4  
**Outputs to `/Recommendation_Impact_Scores/`:**
- `detailed_impact_scores_linear.csv`
- `detailed_impact_scores_percentile.csv` 
- `detailed_impact_scores_log_normal.csv`
- `detailed_impact_scores_z_score.csv`
- `summary_impact_scores_{method}.csv` (for each method)
- `statistical_patient_summary_{method}.csv` (for each method)

## 🎯 Expected Results

### Impact Scoring Results

```bash
============================================================
🧪 Running LINEAR scaling method
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

### Example Personalized Recommendation

**Patient:** patient_3  
**Recommendation:** "Increase Fiber Intake"  
- **Key Markers**: 9 markers across 7 pillars with varying improvement potentials
- **Total Raw Points**: 3.354 (sum of all marker-pillar impact calculations)
- **Final Score**: 8.23 (after percentile statistical scaling)
- **Tier**: High (score ≥7)
- **Affected Markers**: 9 markers across 7 pillars with varying improvement potentials

### Recommendation Categories

- **Primary Markers** (weight: 1.0) - Direct biomarker evidence
- **Secondary Markers** (weight: 0.7) - Supporting evidence  
- **Tertiary Markers** (weight: 0.4) - Indirect associations

## 📁 File Structure & Outputs

### Input Data Files (Generated by Steps 1-2)
```
data/
├── dummy_lab_results_full.csv           # Generated biomarker data (Step 1)
└── synthetic_patient_survey.csv         # Generated survey responses (Step 2)
```

### Intermediate Output Files

#### WellPath_Score_Survey/ (Step 2)
```
├── per_question_scores_full_weighted.csv
├── question_gap_analysis.csv
└── synthetic_patient_pillar_scores_survey_with_max_pct.csv
```

#### WellPath_Score_Markers/ (Step 3)
```
├── marker_gap_analysis_absolute.csv
├── marker_gap_analysis_relative.csv
├── marker_pillar_summary.csv
└── scored_markers_with_max.csv
```

#### WellPath_Score_Combined/ (Step 4)
```
├── markers_for_impact_scoring.csv
├── all_survey_questions_summary.csv
├── marker_contribution_analysis.csv
├── detailed_scoring_summary.csv
└── comprehensive_patient_scores_detailed.csv
```

### Final Impact Scoring Results (Step 5)

#### Recommendation_Impact_Scores/
```
├── detailed_impact_scores_linear.csv        # All 9,100+ scores using linear scaling
├── detailed_impact_scores_percentile.csv    # All 9,100+ scores using percentile scaling  
├── detailed_impact_scores_log_normal.csv    # All 9,100+ scores using log-normal scaling
├── detailed_impact_scores_z_score.csv       # All 9,100+ scores using z-score scaling
├── summary_impact_scores_linear.csv         # Key metrics summary (linear)
├── summary_impact_scores_percentile.csv     # Key metrics summary (percentile)
├── summary_impact_scores_log_normal.csv     # Key metrics summary (log-normal)
├── summary_impact_scores_z_score.csv        # Key metrics summary (z-score)
├── statistical_patient_summary_linear.csv   # Patient-level statistics (linear)
├── statistical_patient_summary_percentile.csv  # Patient-level statistics (percentile)
├── statistical_patient_summary_log_normal.csv  # Patient-level statistics (log-normal)
└── statistical_patient_summary_z_score.csv     # Patient-level statistics (z-score)
```

## 🛠 Troubleshooting

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

**Memory Issues with Large Datasets:**
```python
# Process in smaller batches
patient_subset = ['patient_1', 'patient_2', ...]  
python wellpath_impact_scorer_improved.py --base-dir . --patient-subset patient_1 patient_2
```

**Inconsistent Patient IDs:**
- Ensure the same patient IDs are used across biomarker and survey files
- Use consistent formatting (e.g., "patient_1", "patient_2", not mixed formats)
- For reproducible synthetic data, use `np.random.seed(42)`

**Column Name Mismatches:**
```python
# Common issues with real data
# ❌ Wrong: "Patient ID", "Patient_ID", "patientid" 
# ✅ Correct: "patient_id"

# ❌ Wrong: "Q1.01", "question_1_01", "1-01"
# ✅ Correct: "1.01"

# Verify column names match exactly using:
print(df.columns.tolist())
```

### Real Data Integration Troubleshooting

**Survey Question Format Issues:**
```python
# Question IDs must be exact strings
# ✅ Correct format: "1.01", "2.11", "10.33"
# ❌ Wrong format: 1.01, "1.1", "01.01"

# Fix column names if needed:
df.columns = [str(col).strip() for col in df.columns]
```

**Biomarker Value Types:**
```python
# Ensure numeric columns are proper floats
numeric_cols = ['age', 'weight_lb', 'hdl', 'ldl', 'triglycerides', ...]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
```

**Missing Data Patterns:**
```python
# Check for missing data patterns
print(df.isnull().sum())

# For critical columns, ensure no missing values:
critical_cols = ['patient_id', 'age', 'sex', 'weight_lb']
missing_critical = df[critical_cols].isnull().any(axis=1)
print(f"Rows with missing critical data: {missing_critical.sum()}")
```

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

**File Structure Verification:**
```bash
# Expected directory structure after running all scripts
WellPath/
├── data/
│   ├── dummy_lab_results_full.csv (or your real biomarker data)
│   └── synthetic_patient_survey.csv (or your real survey data)
├── WellPath_Score_Markers/
│   ├── scored_markers_with_max.csv
│   └── [other marker scoring files]
├── WellPath_Score_Survey/
│   ├── per_question_scores_full_weighted.csv  
│   └── [other survey scoring files]
├── WellPath_Score_Combined/
│   ├── comprehensive_patient_scores_detailed.csv
│   └── [other combined files]
└── WellPath_Impact_Scoring/
    ├── detailed_impact_scores_percentile.csv
    └── [other impact scoring results]
```

## 📊 Analytics & Insights

### Key Metrics Generated

- **Individual Marker Scores**: Raw values, normalized scores, improvement potential
- **Pillar Scores**: Combined weighted scores across all health dimensions
- **Improvement Potential**: Quantified opportunity for health optimization
- **Recommendation Impact**: Personalized priority ranking for interventions
- **Population Analytics**: Cohort-level insights and trends

### Example Analysis

```python
# Analyze top improvement opportunities
high_impact_recs = impact_df[impact_df['final_score'] >= 6]
print(f"High-impact recommendations: {len(high_impact_recs)}")

# Identify population health trends  
pillar_averages = comprehensive_df.groupby('age')[pillar_columns].mean()
```

## 🔬 Research Applications

This system is designed for:

- **Health intervention research** - A/B testing wellness programs
- **Biomarker validation studies** - Testing new health metrics
- **Personalized medicine development** - Algorithm training data
- **Population health analytics** - Identifying health trends
- **Digital health platform testing** - Realistic test datasets

## 📚 API Reference

### Core Functions

```python
# Data generation
generate_patients(n=50, outfile="patients.csv")
generate_survey_data(n=50, outfile="surveys.csv")

# Scoring
create_comprehensive_patient_file() → (comprehensive_df, markers_df)
run_statistical_impact_scoring(base_dir, method) → (impact_df, summary_df)

# Analysis
create_marker_contribution_analysis(df, output_dir)
create_all_survey_summary(df, output_dir)
```

## 🔧 Configuration

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

## 🧪 Advanced Features

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

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Add tests for new functionality
4. Commit changes: `git commit -am 'Add new feature'`
5. Push to branch: `git push origin feature/new-feature`
6. Submit Pull Request

### Development Guidelines

- Follow existing code structure and naming conventions
- Add docstrings for all new functions
- Include example usage in function docstrings  
- Test with various patient populations and edge cases

## 🚀 Next Steps

1. **Setup**: Run data generation scripts to create initial datasets
2. **Configure**: Update file paths and pillar weights for your use case  
3. **Run**: Execute scoring pipelines to generate comprehensive analytics
4. **Analyze**: Use generated CSV files to derive health insights
5. **Extend**: Add custom biomarkers, surveys, or scoring methods as needed

The WellPath system provides a complete foundation for health analytics, from data generation through personalized recommendations, with extensive customization options for research and clinical applications.
