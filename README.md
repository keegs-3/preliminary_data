# WellPath Scoring System

Comprehensive health assessment pipeline that processes biomarkers, survey responses, and education engagement to generate personalized wellness scores and patient breakdowns.

## Repository Structure

```
preliminary_data/
├── README.md                   # This file
├── setup.py                    # Package installation script
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore patterns
│
├── src/                       # Source code
│   ├── algorithms/            # Algorithm implementations
│   ├── generated_configs/     # Generated algorithm configurations
│   ├── ref_csv_files_airtable/# Reference data (CSV files)
│   ├── schemas/               # Data schemas and validation
│   └── recommendation_config_generator.py
│
├── scripts/                   # Executable scripts
│   ├── wellpath_score_runner_survey_v2.py  # Survey scoring (recommended)
│   ├── WellPath_score_runner_combined.py   # Combined scoring
│   ├── Patient_score_breakdown_generator.py # Patient reports
│   └── generate_*.py          # Data generation utilities
│
├── config/                    # Configuration management
│   └── paths.py              # Centralized path management
│
├── docs/                      # Documentation
├── tests/                     # Test suite
├── archive/                   # Old/unused files
│
└── [Output Directories]       # Generated outputs (preserved structure)
    ├── WellPath_Score_Markers/
    ├── WellPath_Score_Survey/
    ├── WellPath_Score_Combined/
    └── WellPath_Score_Breakdown/
```

## Overview

The WellPath system evaluates patient health across 7 core pillars:
- **Healthful Nutrition** (Markers: 72%, Survey: 18%, Education: 10%)
- **Movement + Exercise** (Markers: 54%, Survey: 36%, Education: 10%)  
- **Restorative Sleep** (Markers: 63%, Survey: 27%, Education: 10%)
- **Cognitive Health** (Markers: 36%, Survey: 54%, Education: 10%)
- **Stress Management** (Markers: 27%, Survey: 63%, Education: 10%)
- **Connection + Purpose** (Markers: 18%, Survey: 72%, Education: 10%)
- **Core Care** (Markers: 49.5%, Survey: 40.5%, Education: 10%)

## Processing Pipeline

### 1. Marker Analysis
- **Input**: Raw laboratory values and biometric data
- **Processor**: Marker scoring runners (various implementations)
- **Output**: `WellPath_Score_Markers/` - Normalized marker scores with pillar contributions
- **Key Features**: Lab value interpretation, reference ranges, multi-pillar impact analysis

### 2. Survey Processing  
- **Input**: Patient survey responses across all health domains
- **Processor**: `scripts/wellpath_score_runner_survey_v2.py` (recommended clean implementation)
- **Output**: `WellPath_Score_Survey/` - Survey scores with complex logic calculations
- **Complex Logic Includes**:
  - Exercise frequency + duration rollups (Cardio, Strength, HIIT, Flexibility)
  - Stress level + frequency + coping methods interactions
  - Sleep issues + frequency mapping with multi-pillar impact
  - Personalized protein/calorie targets based on BMR
  - Substance use scoring with quit time bonuses
  - Cognitive activity and sleep protocol counting

### 3. Combined Processing
- **Processor**: `scripts/WellPath_score_runner_combined.py`
- **Function**: Integrates marker, survey, and education data with pillar-specific weightings
- **Output**: `WellPath_Score_Combined/comprehensive_patient_scores_detailed.csv`
- **Key Features**: 
  - Applies pillar allocation weights
  - Calculates final composite scores 
  - Generates improvement potential analysis
  - Maintains audit trail from all components

### 4. Patient Breakdown Generation
- **Processor**: `scripts/Patient_score_breakdown_generator.py`
- **Function**: Creates comprehensive individual patient reports for UI consumption
- **Output**: `WellPath_Score_Breakdown/` directory with individual patient files
- **Report Structure**:
  ```
  ├── Overall Wellness Score & Demographics
  ├── Detailed Pillar Breakdown (component analysis)
  ├── Raw Laboratory Values
  ├── Detailed Biomarker Contributions (Response → Raw → Weight → Weighted → Pillar)
  ├── Detailed Survey Contributions (Response → Raw → Weight → Weighted → Pillar) 
  ├── Complex Survey Calculations (rollup categories)
  └── Education Engagement Analysis
  ```

### 5. Algorithm Configuration System
- **Processor**: `recommendation_config_generator.py`
- **Function**: Converts natural language health recommendations into production-ready scoring algorithms
- **Input**: Health recommendations in plain English
- **Output**: `src/generated_configs/` - Complete algorithm configurations with metadata
- **Integration**: Links with `metric_types_v3` and `units_v3` databases for automatic metric/unit resolution

## Algorithm Configuration Types

The system supports 14 distinct algorithm types across 5 categories:

### Binary Threshold Algorithms
- **Daily Binary** (`SC-BIN-DAILY-*`) - Pass/fail daily goals (e.g., "Add one daily serving of fiber")
- **Frequency Binary** (`SC-BIN-FREQ-*`) - Pass/fail over time windows

### Proportional Algorithms  
- **Daily Proportional** (`SC-PROP-DAILY-*`) - Percentage achievement daily (e.g., "Take 10,000 steps daily")
- **Frequency Proportional** (`SC-PROP-FREQ-*`) - Percentage achievement over time

### Zone-Based Algorithms
- **3-Tier Daily** (`SC-Z3T-DAILY-*`) - Simple zone scoring (Below/On/Above target)
- **5-Tier Daily** (`SC-Z5T-DAILY-*`) - Detailed zone scoring (Critical/Poor/Fair/Good/Excessive)
- **3-Tier Frequency** (`SC-Z3T-FREQ-*`) - Simple zone frequency scoring
- **5-Tier Frequency** (`SC-Z5T-FREQ-*`) - Detailed zone frequency scoring

### Composite Algorithms
- **Daily Composite** (`SC-COMP-DAILY-*`) - Multi-factor daily scoring
- **Frequency Composite** (`SC-COMP-FREQ-*`) - Multi-factor frequency scoring  
- **Advanced Composite** (`SC-COMP-ADV-*`) - Complex specialized scoring
- **Sleep Advanced** (`SC-COMPOSITE-SLEEP-ADVANCED`) - Sleep duration + schedule consistency with rolling average tolerance

### Specialized Algorithms
- **Weekly Allowance** (`SC-ALLOW-WEEKLY-*`) - Constrained weekly budgets (e.g., "No more than 2 drinks per week")
- **Categorical Filter** (`SC-CAT-*`) - Category-specific rules (e.g., "High-impact exercises 3x/week, low-impact 2x/week")

## Metrics Architecture

### Tracked Metrics vs Calculated Metrics

The WellPath system distinguishes between two types of metrics in algorithm configurations:

#### Tracked Metrics (`tracked_metrics`)
- **Source**: `src/ref_csv_files_airtable/metric_types_v3.csv`
- **Description**: Base metrics from direct measurements or user inputs
- **Examples**: `dietary_fiber`, `sleep_time`, `wake_time`, `body_weight`
- **Usage**: Immediate lookup from data sources, no computation required

#### Calculated Metrics (`calculated_metrics`)  
- **Source**: `src/ref_csv_files_airtable/calculated_metrics.csv`
- **Description**: Derived metrics computed from base metrics using defined formulas
- **Examples**: 
  - `sleep_duration` = `wake_time - sleep_time`
  - `eating_window_duration` = `last_meal_time - first_meal_time`
  - `protein_per_kg` = `dietary_protein_grams / body_weight_kg`
  - `bmi_calculated` = `body_weight_kg / (height_meters^2)`

#### Configuration Structure
Every algorithm configuration contains both arrays:
```json
{
  "tracked_metrics": ["dietary_fiber"],        // Base metrics (if any)
  "calculated_metrics": [],                    // Derived metrics (if any)
  // ... other config properties
}
```

#### Mixed Configurations
Some configurations use both types:
```json
{
  "tracked_metrics": ["body_weight", "height"],
  "calculated_metrics": ["bmi_calculated"],
  // BMI calculation requires both base measurements
}
```

This separation enables:
- **Clear data dependencies**: System knows what to look up vs what to compute
- **Performance optimization**: Avoid unnecessary calculations
- **Error handling**: Different validation rules for base vs derived metrics
- **MVP readiness**: Clean architecture for production deployment

## Key Features

### Algorithm Selection Intelligence
The recommendation generator uses sophisticated NLP keyword matching to automatically select optimal algorithms:

- **Binary Patterns**: "avoid", "eliminate", "add one", "one daily", "single serving" → Binary threshold
- **Proportional Patterns**: "increase", "target", "goal", specific numbers → Proportional scoring
- **Zone Patterns**: "optimal", "range", "between", "excellent/good/fair/poor" → Zone-based scoring
- **Composite Patterns**: "overall", "combined", "multiple", "comprehensive" → Composite scoring
- **Sleep + Schedule Patterns**: "sleep" + "schedule"/"variation"/"consistency" → Advanced sleep composite

### Advanced Sleep Composite Algorithm

The **SC-COMPOSITE-SLEEP-ADVANCED** algorithm handles complex sleep recommendations that combine duration and schedule consistency requirements. It uses a sophisticated 55/45 weighting system:

#### Component Breakdown:
- **Sleep Duration Zone (55%)**: 7-9 hours optimal range with 5-tier scoring
  - Critical (0-5h): 20 points
  - Poor (5-6h): 40 points  
  - Fair (6-7h): 60 points
  - **Optimal (7-9h): 100 points**
  - Excessive (9-12h): 80 points

- **Sleep Time Consistency (22.5%)**: Rolling average tolerance method
  - Daily check: `abs(sleep_time - current_rolling_avg) < 60 minutes`
  - Weekly scoring: `(compliant_nights / 7) * 100`
  - Examples: 7/7 nights = 100%, 6/7 nights = 85.7%, 5/7 nights = 71.4%

- **Wake Time Consistency (22.5%)**: Rolling average tolerance method
  - Same methodology as sleep time consistency
  - Tracks wake_time variance against rolling average

#### Rolling Average Calculation:
- **Night 1**: sleep_time = baseline
- **Night 2**: average = (night1 + night2) / 2
- **Night 3**: average = (night1 + night2 + night3) / 3
- **Continue through 7 days**, then rolling 7-day window

This approach balances sleep quality (duration) with consistency (schedule) while allowing for realistic life flexibility.

### Automatic Metric & Unit Linking
- **Metric Detection**: Searches `metric_types_v3` database for best matching health metrics
- **Unit Resolution**: Links proper units from `units_v3` database with validation
- **Schema Integration**: Uses metric validation schemas for appropriate targets and ranges

### Survey Structure Alignment
- Survey questions follow same audit trail as biomarkers: **Response → Raw Score → Weight → Weighted Score → Pillar Contribution**
- Individual questions (e.g., 3.04, 6.01) excluded from detailed breakdown when part of complex logic
- Complex calculations properly grouped (exercise types, stress+coping, sleep issues)

### Complex Survey Logic
- **Exercise Rollups**: Combines frequency (3.04-3.07) + duration (3.08-3.11) into activity categories
- **Stress Assessment**: Integrates stress level (6.01) + frequency (6.02) + coping methods (6.07) 
- **Sleep Issues**: Maps issues (4.12) to frequencies (4.13-4.19) with multi-pillar impact weights
- **Personalized Targets**: BMR-based protein/calorie recommendations using patient demographics
- **Substance Scoring**: Current/former use with duration penalties and quit time bonuses

### Data Flow
```
Raw Lab Data → Marker Runners → Normalized Marker Scores
Survey Responses → Survey Runner v2 → Complex Logic Calculations  
Education Data → Education Processing → Engagement Scores
        ↓
Combined Runner → Pillar Weightings → Comprehensive Patient Scores
        ↓
Breakdown Generator → Individual Patient Reports (UI Ready)

Recommendations → Config Generator → Algorithm Configurations → Scoring System Integration
```

## Getting Started

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd preliminary_data

# Install the package in development mode
pip install -e .

# Or install dependencies directly
pip install -r requirements.txt
```

### Quick Start
```bash
# Run the core WellPath processing pipeline
cd scripts
python wellpath_score_runner_survey_v2.py      # 1. Survey processing
python WellPath_score_runner_combined.py       # 2. Combined scoring  
python Patient_score_breakdown_generator.py    # 3. Patient reports
```

## Usage

### Core WellPath Processing
1. **Run Survey Processing**: `python scripts/wellpath_score_runner_survey_v2.py`
2. **Run Combined Processing**: `python scripts/WellPath_score_runner_combined.py`
3. **Generate Patient Breakdowns**: `python scripts/Patient_score_breakdown_generator.py`

### Recommendation Algorithm Generation
4. **Generate Algorithm Configs**: 
   ```python
   from recommendation_config_generator import process_recommendation
   
   # Single recommendation
   config, filepath = process_recommendation("Add one daily serving of fiber-rich food")
   
   # Batch processing
   recommendations = ["Add one daily serving of fiber", "Take 10,000 steps daily"]
   for rec in recommendations:
       config, path = process_recommendation(rec)
   ```

### Algorithm Integration
5. **Use Generated Algorithms**:
   ```python
   # Load config and create algorithm instance
   from algorithms import create_algorithm_from_config
   
   with open('generated_configs/SC-BIN-DAILY-DIETARY_.json') as f:
       config = json.load(f)
   
   algo = create_algorithm_from_config(config)
   score = algo.calculate_score(user_data)
   ```

## Output Files

### Core WellPath Outputs
- **Markers**: Individual biomarker analysis and pillar contributions
- **Survey**: Clean survey scoring with complex logic rollups
- **Combined**: Integrated scoring with pillar weightings and final scores
- **Breakdowns**: Individual patient reports with complete audit trails

### Algorithm Configuration Outputs
- **Generated Configs**: `src/generated_configs/` - Individual algorithm configuration files
- **Master Config List**: `all_generated_configs.json` - Single source for all generated algorithms
- **Algorithm Implementations**: `src/algorithms/` - Type-safe Python algorithm classes
- **Documentation**: `docs/Recommendation_Algorithm_Generator_README.md` - Complete system documentation

## System Architecture

The WellPath system now provides end-to-end health assessment capabilities:

1. **Assessment Pipeline**: Processes biomarkers, surveys, and education data
2. **Algorithm Generation**: Converts recommendations into executable scoring algorithms  
3. **Patient Scoring**: Applies algorithms to generate personalized health scores
4. **Reporting**: Creates comprehensive patient breakdowns with improvement recommendations

The system provides comprehensive transparency from raw inputs through final scores, enabling detailed patient counseling and improvement recommendations. The algorithm configuration system ensures new health recommendations can be rapidly deployed with proper algorithmic backing.