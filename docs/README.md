# WellPath Health Analytics & Scoring System

A comprehensive Python-based health analytics platform that generates synthetic patient data, scores wellness metrics across multiple health pillars, and provides personalized health recommendations with impact scoring.

## 🎯 Overview

The WellPath system is designed to:
- **Generate realistic synthetic health data** for testing and development
- **Score patient wellness** across 7 evidence-based health pillars  
- **Calculate personalized recommendation impact scores** using statistical methods
- **Provide comprehensive analytics** for health optimization

## 🗏️ System Architecture

### Core Components

1. **`generate_biomarker_dataset.py`** - Synthetic patient data generation
2. **`generate_survey_dataset.py`** - Lifestyle survey data generation  
3. **`WellPath_score_runner_survey.py`** - Survey scoring engine
4. **`WellPath_score_runner_markers.py`** - Biomarker scoring engine
5. **`WellPath_score_runner_combined.py`** - Integrated scoring system
6. **`wellpath_impact_scorer_improved.py`** - Statistical impact scoring
7. **`Recommendations_JSON_Updater.py`** - Airtable to JSON converter for recommendation data

### 🥼 Health Pillars Framework

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

## 🚀 Quick Start

### Prerequisites

```bash
pip install pandas numpy uuid random datetime openpyxl
```

### Complete Workflow (Start to Finish)

Follow these steps in order to generate all data and run the complete analysis:

#### Step 1: Generate Biomarker Data

```bash
python generate_biomarker_dataset.py
```

**Outputs:**
- `data/dummy_lab_results_full.csv` - Synthetic patient biomarker data

#### Step 2: Generate Survey Data

```bash
python generate_survey_dataset.py
```

**Outputs:**
- `data/synthetic_patient_survey.csv` - Lifestyle survey responses

#### Step 3: Run Survey Scoring

```bash
python WellPath_score_runner_survey.py
```

**Requires:** Both CSV files from Steps 1 & 2  
**Outputs to `/WellPath_Score_Survey/`:**
- `per_question_scores_full_weighted.csv`
- `question_gap_analysis.csv`
- `synthetic_patient_pillar_scores_survey_with_max_pct.csv`

#### Step 4: Run Biomarker Scoring

```bash
python WellPath_score_runner_markers.py
```

**Requires:** `data/dummy_lab_results_full.csv`  
**Outputs to `/WellPath_Score_Markers/`:**
- `marker_gap_analysis_absolute.csv`
- `marker_gap_analysis_relative.csv`
- `marker_pillar_summary.csv`
- `scored_markers_with_max.csv`

#### Step 5: Combine All Scoring Data

```bash
python WellPath_score_runner_combined.py
```

**Requires:**
- `WellPath_Score_Markers/scored_markers_with_max.csv`
- `WellPath_Score_Survey/per_question_scores_full_weighted.csv`
- `data/dummy_lab_results_full.csv`
- `data/synthetic_patient_survey.csv`

**Outputs to `/WellPath_Score_Combined/`:**
- `markers_for_impact_scoring.csv`
- `all_survey_questions_summary.csv`
- `marker_contribution_analysis.csv`
- `detailed_scoring_summary.csv`
- `comprehensive_patient_scores_detailed.csv`

#### Step 6: Update Recommendations Data (Optional - When Airtable Changes)

This step enables you to update the recommendation marker distribution from your Airtable data:

**Prerequisites:**
1. Export your Airtable data to `WellPath Tiered Markers.xlsx`
2. Ensure the Excel file contains columns: `ID`, `Title`, `Raw_impact`, `Primary Markers`, `Secondary Markers`, `Tertiary Markers`, `Primary Metrics`, `Secondary Metrics`, `Tertiary Metrics`

**Run the JSON updater:**
```bash
python Recommendations_JSON_Updater.py
```

**What this does:**
- Creates a `Recommendations_List_Old/` backup folder
- Moves existing `recommendations_list.json` to backup with timestamp
- Converts your Excel data to the proper JSON format
- Replaces `recommendations_list.json` with updated data
- Maps Excel marker names to standardized JSON format (e.g., "Total Cholesterol" → "total_cholesterol")

**Outputs:**
- **Backup**: `Recommendations_List_Old/recommendations_list_backup_YYYYMMDD_HHMMSS.json`
- **Updated**: `recommendations_list.json` (ready for impact scoring)

**Console output example:**
```
=============================================================
Python JSON Creator Script - Excel to JSON Converter
=============================================================
✓ Created backup folder: Recommendations_List_Old
✓ Moved original file to: Recommendations_List_Old/recommendations_list_backup_20250902_143022.json
✓ Successfully replaced: recommendations_list.json
  Total recommendations: 182
  Creation date: 2025-09-02
🎉 Success! Your recommendations_list.json file has been updated.
```

#### Step 7: Run Impact Scoring

```bash
python wellpath_impact_scorer_improved.py
```

This automatically runs all 4 scaling methods (linear, percentile, log_normal, z_score) and generates results for each. **Now uses the updated recommendations data from Step 6.**

**Requires:** All outputs from Step 5 + updated `recommendations_list.json`  
**Outputs to `/Recommendation_Impact_Scores/`:**
- `detailed_impact_scores_linear.csv`
- `detailed_impact_scores_percentile.csv` 
- `detailed_impact_scores_log_normal.csv`
- `detailed_impact_scores_z_score.csv`
- `summary_impact_scores_{method}.csv` (for each method)
- `statistical_patient_summary_{method}.csv` (for each method)

### Quick Test with Existing Data

If you already have all the required files generated, you can skip directly to Step 7:

```bash
python wellpath_impact_scorer_improved.py
```

**Expected Results:**
- Automatically runs all 4 scaling methods
- Processes ~50 patients and ~182 recommendations per method
- Generates ~9,100 personalized impact scores per method
- Shows score distribution for each method: ~16% high impact, 38% medium, 46% low

### Updating Recommendation Data Only

If you only need to update the recommendations data without regenerating patient data:

1. **Export Airtable data** to `WellPath Tiered Markers.xlsx`
2. **Run JSON updater**: `python Recommendations_JSON_Updater.py`
3. **Run impact scoring**: `python wellpath_impact_scorer_improved.py`

## 📊 Data Generation

### Biomarker Dataset Generation

The `generate_biomarker_dataset.py` creates realistic synthetic patients with:

- **Demographics**: Age, sex, athlete status, BMI, body fat percentage
- **Cardiovascular**: Cholesterol panels, blood pressure, heart rate variability
- **Metabolic**: Glucose, insulin, HbA1c, lipid profiles
- **Inflammatory**: CRP, IL-6, TNF-α markers
- **Hormonal**: Sex hormones, thyroid, cortisol
- **Fitness**: VO2 max, grip strength, body composition
- **Sleep**: REM, deep sleep metrics

```python
# Key biomarker categories generated:
record.update(generate_cardiovascular_markers(sex, profile))
record.update(generate_sleep_markers(profile, athlete))  
record.update(generate_inflammation_markers(profile))
record.update(generate_metabolism_markers(sex, fitness_level, profile))
record.update(generate_hormone_markers(sex, age, phase, profile, menopausal_status))
record.update(generate_fitness_markers(sex, profile))
```

### Survey Dataset Generation

The `generate_survey_dataset.py` creates lifestyle questionnaire responses across:

- **Nutrition habits** and dietary patterns
- **Exercise frequency** and activity levels  
- **Sleep quality** and duration patterns
- **Stress management** techniques and levels
- **Cognitive engagement** and mental wellness
- **Social connections** and life purpose
- **Healthcare utilization** and preventive care

## 📢 Scoring Methodology

### Biomarker Scoring

The system uses custom evidence-based reference ranges with defined score mappings for each biomarker:

```python
def score_biomarker(value, ranges_config):
    """
    Score biomarkers on 0-1 scale based on custom-defined ranges
    Each range has an associated score value (0.0-1.0)
    """
    for range_config in ranges_config:
        if range_config['min'] <= value <= range_config['max']:
            return range_config['score']  # Returns 0.0-1.0
    return 0.0  # Default if outside all ranges
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

Survey responses are scored using custom-defined value mappings, plus sophisticated custom logic for complex questions:

```python
# Simple response mapping (0.0-1.0 scale)
response_scores = {
    "Daily": 1.0,
    "Several times a week": 0.8, 
    "Weekly": 0.6,
    "Occasionally": 0.4,
    "Rarely or Never": 0.2
}

# Plus custom logic functions for complex scoring
# (See Technical Architecture document for complete details)
```

### Combined Pillar Scoring Algorithm

The pillar scoring process follows this multi-step calculation:

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
    
    # Step 1-3: Calculate weighted sum
    pillar_weighted_sum = 0
    pillar_max_sum = 0
    
    for item in pillar_items:
        item_score = score_item(patient_data[item])  # 0.0-1.0
        item_weight = pillar_config[item]['weight']
        
        pillar_weighted_sum += (item_score * item_weight)
        pillar_max_sum += (1.0 * item_weight)  # Max possible
    
    # Step 4-5: Convert to percentage
    pillar_percentage = (pillar_weighted_sum / pillar_max_sum) * 100
    
    # Step 6: Apply in final combination with other pillars
    return pillar_percentage
```

**Pillar Weight Application:**
```python
final_pillar_score = (
    marker_percentage * pillar_weights["markers"] + 
    survey_percentage * pillar_weights["survey"] +
    education_percentage * pillar_weights["education"]
)
```

**Note**: For detailed custom survey scoring logic (protein calculations, movement scoring, stress management, etc.), see the Technical Architecture documentation.

## 📈 Statistical Impact Scoring

The impact scorer calculates personalized recommendation scores using multiple scaling methods:

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

**Example from Real Data:**
- **Baseline Impact**: 75 (evidence-based score for "Increase Fiber Intake")
- **Total Raw Points**: 3.354 (sum of all marker-pillar impact calculations)
- **Final Score**: 8.23 (after percentile statistical scaling)
- **Tier**: High (score ≥7)
- **Affected Markers**: 9 markers across 7 pillars with varying improvement potentials

### Recommendation Categories

- **Primary Markers** (weight: 1.0) - Direct biomarker evidence
- **Secondary Markers** (weight: 0.7) - Supporting evidence  
- **Tertiary Markers** (weight: 0.4) - Indirect associations

## 🔄 Airtable Integration & Recommendation Updates

The system includes seamless integration with Airtable data for recommendation management:

### Recommendation Data Management Process

1. **Airtable Export**: Export your recommendations data to `WellPath Tiered Markers.xlsx`
2. **JSON Conversion**: Run `Recommendations_JSON_Updater.py` to convert Excel to JSON format
3. **Automatic Backup**: Original `recommendations_list.json` is automatically backed up
4. **Impact Scoring**: Updated recommendations are immediately available for impact scoring

### Excel File Format Requirements

Your `WellPath Tiered Markers.xlsx` file must contain these columns:

| Column Name | Description | Example |
|-------------|-------------|---------|
| `ID` | Unique recommendation identifier | "REC0001.1" |
| `Title` | Recommendation title | "Increase Fiber Intake" |
| `Raw_impact` | Evidence-based impact score | 75 |
| `Primary Markers` | Comma-separated primary markers | "LDL,ApoB,hsCRP" |
| `Secondary Markers` | Comma-separated secondary markers | "HbA1c,Fasting Glucose" |
| `Tertiary Markers` | Comma-separated tertiary markers | "" |
| `Primary Metrics` | Comma-separated primary metrics | "BMI,% Bodyfat" |
| `Secondary Metrics` | Comma-separated secondary metrics | "" |
| `Tertiary Metrics` | Comma-separated tertiary metrics | "" |

### Automatic Marker Name Standardization

The JSON updater automatically converts Excel marker names to standardized JSON format:

```python
# Excel format → JSON format
"Total Cholesterol" → "total_cholesterol"
"Blood Pressure - Systolic" → "blood_pressure_systolic" 
"Vitamin D" → "vitamin_d"
"% Bodyfat" → "bodyfat"
"VO2 Max" → "vo2_max"
```

### Backup System

Every time you run the JSON updater:
- Creates `Recommendations_List_Old/` folder if it doesn't exist
- Moves existing `recommendations_list.json` to backup folder with timestamp
- Example backup: `recommendations_list_backup_20250902_143022.json`
- Preserves all historical versions for rollback if needed

## 📁 File Structure & Outputs

### Input Data Files (Generated by Steps 1-2)
```
data/
├── dummy_lab_results_full.csv           # Generated biomarker data (Step 1)
└── synthetic_patient_survey.csv         # Generated survey responses (Step 2)
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

### Intermediate Output Files

#### WellPath_Score_Survey/ (Step 3)
```
├── per_question_scores_full_weighted.csv
├── question_gap_analysis.csv
└── synthetic_patient_pillar_scores_survey_with_max_pct.csv
```

#### WellPath_Score_Markers/ (Step 4)
```
├── marker_gap_analysis_absolute.csv
├── marker_gap_analysis_relative.csv
├── marker_pillar_summary.csv
└── scored_markers_with_max.csv
```

#### WellPath_Score_Combined/ (Step 5)
```
├── markers_for_impact_scoring.csv
├── all_survey_questions_summary.csv
├── marker_contribution_analysis.csv
├── detailed_scoring_summary.csv
└── comprehensive_patient_scores_detailed.csv
```

### Final Impact Scoring Results (Step 7)

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
├── statistical_patient_summary_linear.csv   # Top 5 recommendations per patient (linear)
├── statistical_patient_summary_percentile.csv # Top 5 recommendations per patient (percentile)
├── statistical_patient_summary_log_normal.csv # Top 5 recommendations per patient (log-normal)
└── statistical_patient_summary_z_score.csv  # Top 5 recommendations per patient (z-score)
```

### Expected Console Output

When you run the final impact scoring step, you'll see output for each scaling method:

```
🎯 WellPath Statistical Impact Scorer
Running all scaling methods...

============================================================
🧪 Running LINEAR scaling method
============================================================
🚀 Starting Statistical WellPath Impact Scoring
   Scaling method: linear
   Input files:
     Recommendations (full): .\recommendations_list.json
     Recommendations (from OpenAI): .\recommendation_subset_builder.json
     Markers: .\WellPath_Score_Combined\markers_for_impact_scoring.csv
     Comprehensive: .\WellPath_Score_Combined\comprehensive_patient_scores_detailed.csv
   Output directory: .\Recommendation_Impact_Scores
============================================================
📋 Recommendation Selection:
   Total recommendations in JSON: 323
   Unique base IDs found: 182
   Selected recommendations: 182
🎯 Initialized Statistical Impact Scorer
   Recommendations: 182
   Patients: 50
📊 Step 1: Calculating raw impact points...
🔄 Processing 50 patients...
✅ Raw points calculation complete: 9100 recommendation scores
📈 Step 2: Applying linear scaling to convert to 0-10 scores...
📊 Final Score Statistics (after linear scaling):
   Min: 0.00
   Mean: 4.12
   Max: 10.00
   Std: 2.89
✅ Linear scaling completed successfully!

============================================================
🧪 Running PERCENTILE scaling method
============================================================
[Similar output for percentile method...]

🎉 All scaling methods completed!
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

### Custom Marker Mapping

```python
# Add custom marker name mappings in get_csv_to_json_mapping()
def get_csv_to_json_mapping():
    return {
        'Your Custom Marker': 'your_custom_marker',
        'Special Biomarker (Units)': 'special_biomarker',
        # ... existing mappings
    }
```

## 🛠 Troubleshooting

### Common Issues

**"Required file not found" Error**:
```bash
❌ Required file not found: .\recommendations_list.json
❌ Required file not found: .\WellPath_Score_Combined\markers_for_impact_scoring.csv
```
**Solution**: Run the data generation and scoring scripts first, or use custom file paths:
```bash
# Generate required files
python generate_biomarker_dataset.py
python generate_survey_dataset.py  
python WellPath_score_runner_combined.py

# Or specify custom files
python wellpath_impact_scorer_improved.py \
  --recommendations-file "your_recommendations.json" \
  --markers-file "your_markers.csv" \
  --comprehensive-file "your_comprehensive.csv"
```

**Missing Excel File for JSON Update**:
```bash
❌ Error: Excel file 'WellPath Tiered Markers.xlsx' not found
```
**Solution**: Export your Airtable data to Excel format with the required columns, or use a different filename:
```bash
# Rename your Excel file to match expected name
# Or modify the script to use your filename
```

**Pandas/OpenPyXL Not Installed**:
```bash
❌ Error: pandas library not found. Install with: pip install pandas openpyxl
```
**Solution**: Install required Python packages:
```bash
pip install pandas openpyxl
```

**Invalid Excel Column Names**:
```bash
⚠️ Warning: No mapping found for marker: 'Custom Marker Name'
```
**Solution**: Either update your Excel column names to match expected format, or add custom mappings in `get_csv_to_json_mapping()`

**Missing Input Files**:
```bash
# Ensure data generation runs first
python generate_biomarker_dataset.py
python generate_survey_dataset.py
```

**Memory Issues with Large Datasets**:
```python
# Process in smaller batches
patient_subset = ['patient_1', 'patient_2', ...]  
python wellpath_impact_scorer_improved.py --base-dir . --patient-subset patient_1 patient_2
```

**Command Line Interface Not Working**:
- The new simplified version doesn't require command-line arguments
- Just run `python wellpath_impact_scorer_improved.py` directly
- All 4 scaling methods run automatically

**File Path Issues on Windows**:
```bash
# Use quotes around paths with spaces
python wellpath_impact_scorer_improved.py --base-dir "C:\My Path\With Spaces"
```

**Inconsistent Patient IDs**:
- Ensure the same patient IDs are used across biomarker and survey generation
- Use `np.random.seed(42)` for reproducible results

**Backup Folder Permission Issues**:
```bash
⚠️ Warning: Could not create backup: [Errno 13] Permission denied
```
**Solution**: Run script as administrator or ensure write permissions in the directory

### Debug Mode

```python
import warnings
warnings.filterwarnings('default')  # Show all warnings

# Use help to see all command options
python wellpath_impact_scorer_improved.py --help
```

### Verification Steps

To verify everything is working correctly:

1. **Check File Structure**: Ensure you have the required directory structure
2. **Run with Sample Data**: Test with a small patient subset first
3. **Validate Output**: Check that CSV files are generated with expected data
4. **Review Logs**: Look for error messages in the console output
5. **Test JSON Update**: Verify backup creation and JSON conversion work correctly

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

# Recommendation updates
create_backup_folder_and_move_original() → bool
create_recommendations_json(excel_data) → dict
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
- Update README.md when adding new features or changing workflows

---

## 🚀 Next Steps

1. **Setup**: Run data generation scripts to create initial datasets
2. **Configure**: Update file paths and pillar weights for your use case  
3. **Run**: Execute scoring pipelines to generate comprehensive analytics
4. **Update Recommendations**: Use Airtable integration to keep recommendation data current
5. **Analyze**: Use generated CSV files to derive health insights
6. **Extend**: Add custom biomarkers, surveys, or scoring methods as needed

The WellPath system provides a complete foundation for health analytics, from data generation through personalized recommendations, with extensive customization options for research and clinical applications.
