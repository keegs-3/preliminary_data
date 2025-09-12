# WellPath Complete Health Platform

End-to-end health assessment and adherence tracking system - from synthetic patient generation through personalized scoring, recommendation algorithms, and intelligent triggering for nudges and challenges.

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

## Complete System Overview

The WellPath platform provides comprehensive health assessment and adherence tracking across multiple interconnected systems:

### 1. **Patient Generation System** 
Synthetic patient data with standardized IDs, profile conditions, and logically driven biomarkers, metrics, and survey responses for testing and development.

### 2. **Health Assessment Pipeline**
Evaluates patient health across 7 core pillars using weighted scoring:
- **Healthful Nutrition** (Markers: 72%, Survey: 18%, Education: 10%)
- **Movement + Exercise** (Markers: 54%, Survey: 36%, Education: 10%)  
- **Restorative Sleep** (Markers: 63%, Survey: 27%, Education: 10%)
- **Cognitive Health** (Markers: 36%, Survey: 54%, Education: 10%)
- **Stress Management** (Markers: 27%, Survey: 63%, Education: 10%)
- **Connection + Purpose** (Markers: 18%, Survey: 72%, Education: 10%)
- **Core Care** (Markers: 49.5%, Survey: 40.5%, Education: 10%)

### 3. **Adherence Scoring Architecture**
Revolutionary system converting 182+ health recommendations into 8 core algorithmic patterns with configuration-driven scoring.

### 4. **Intelligent Triggering System** *(Future Integration)*
Logic-driven nudges, check-ins, and challenges based on adherence patterns and health outcomes (currently in Airtable, planned for repository integration).

## Complete Processing Pipeline

### Phase 1: Patient Generation & Data Creation

#### 1.1 Patient Profile Generation
- **Function**: Creates synthetic patients with standardized IDs and consistent health profiles
- **Logic**: Profile conditions drive coherent biomarker/metric/survey response patterns
- **Output**: Standardized patient datasets for testing and development

#### 1.2 Survey Generation  
- **Function**: Generates survey responses aligned with patient profiles
- **Logic**: Survey answers reflect underlying health conditions consistently
- **Integration**: Responses correlate with biomarker values and health outcomes

### Phase 2: Health Assessment Scoring

#### 2.1 Marker/Metric Analysis
- **Input**: Raw laboratory values and biometric data (generated or real)
- **Processor**: Marker scoring runners (various implementations)
- **Output**: `WellPath_Score_Markers/` - Normalized marker scores with pillar contributions
- **Key Features**: Lab value interpretation, reference ranges, multi-pillar impact analysis

#### 2.2 Survey Processing  
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

#### 2.3 Combined Processing
- **Processor**: `scripts/WellPath_score_runner_combined.py`
- **Function**: Integrates marker, survey, and education data with pillar-specific weightings
- **Output**: `WellPath_Score_Combined/comprehensive_patient_scores_detailed.csv`
- **Key Features**: 
  - Applies pillar allocation weights (Markers/Survey/Education per pillar)
  - Calculates final composite scores 
  - Generates improvement potential analysis
  - Maintains audit trail from all components

#### 2.4 Patient Breakdown Generation
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

#### 2.5 Impact Scoring
- **Function**: Analyzes improvement potential and prioritizes intervention areas
- **Output**: Personalized recommendations based on score analysis and improvement opportunities

### Phase 3: Adherence Architecture & Recommendation System

#### 3.1 Data Foundation Setup
- **New Tracked Metrics**: Flexible metric taxonomy (`src/ref_csv_files_airtable/metric_types_v3.csv`)
- **Calculated Metrics**: Derived metric engine (`src/ref_csv_files_airtable/calculated_metrics.csv`)
- **Unit Standardization**: Consistent measurement system (`src/ref_csv_files_airtable/units_v3.csv`)
- **Screening Compliance**: Medical requirements tracking framework

#### 3.2 Algorithm Configuration Generation
- **Processor**: `recommendation_config_generator.py`
- **Function**: Converts natural language health recommendations into production-ready scoring algorithms
- **Input**: Health recommendations in plain English (182+ recommendations)
- **Output**: `src/generated_configs/` - Complete algorithm configurations with metadata
- **Intelligence**: NLP-driven algorithm selection from 8 core types

#### 3.3 Adherence Scoring Engine
- **Architecture**: 8 core algorithmic patterns handle infinite recommendation complexity
- **Algorithms**: Binary Threshold, Minimum Frequency, Weekly Elimination, Proportional, Zone-Based, Composite Weighted, Categorical Filter, Constrained Weekly Allowance
- **Implementation**: Configuration-driven scoring with unified 0-100 scale
- **Testing**: 73 complex configurations validated with 100% success rate

### Phase 4: Challenges & Extensions *(Future Integration)*

#### 4.1 Challenge System Architecture
- **Foundation**: Same 8 algorithmic patterns as recommendations
- **Differentiation**: Time-bound goals with streak bonuses and enhanced gamification
- **Scaling**: Identical tracking mechanisms, different timescales (30-day challenges vs. indefinite recommendations)
- **Integration**: Seamless extension of existing adherence architecture

#### 4.2 Intelligent Triggering System *(Planned)*
- **Logic Engine**: Rule-based triggers for nudges and check-ins
- **Data Source**: Currently in Airtable, planned for repository integration
- **Triggers**: Adherence pattern analysis, score thresholds, behavioral indicators
- **Actions**: Automated nudges, personalized challenges, health check-ins

## Core Algorithm Architecture

The WellPath adherence system uses **8 core algorithmic patterns** to handle infinite recommendation complexity:

### 1. **Binary Threshold** (`SC-BINARY-DAILY`)
- **Pattern**: Simple pass/fail scoring (100 or 0)
- **Use Case**: "Take vitamins daily", "Add one serving of fiber"

### 2. **Minimum Frequency** (`SC-MINIMUM-FREQUENCY`) 
- **Pattern**: Must achieve threshold on ≥X days per week
- **Use Case**: "Exercise 30+ minutes on at least 3 days per week"

### 3. **Weekly Elimination** (`SC-WEEKLY-ELIMINATION`)
- **Pattern**: Zero tolerance - any violation fails entire week
- **Use Case**: "No smoking every day", "Finish caffeine by 2pm daily"

### 4. **Proportional** (`SC-PROPORTIONAL-DAILY/FREQUENCY`)
- **Pattern**: Gradual scoring based on target achievement percentage
- **Use Case**: "Work toward 10,000 steps daily"

### 5. **Zone-Based** (`SC-ZONE-BASED-DAILY/FREQUENCY`)
- **Pattern**: Multi-tier scoring with optimal ranges
- **Use Case**: "Sleep 7-9 hours optimally"

### 6. **Composite Weighted** (`SC-COMPOSITE-DAILY/FREQUENCY`)
- **Pattern**: Weighted combination of multiple components
- **Use Case**: "Overall fitness" (exercise + steps + active minutes)

### 7. **Categorical Filter** (`SC-CATEGORICAL-FILTER`)
- **Pattern**: Different rules for different categories
- **Use Case**: "High-impact exercises 3x/week, low-impact 2x/week"

### 8. **Constrained Weekly Allowance** (`SC-CONSTRAINED-WEEKLY-ALLOWANCE`)
- **Pattern**: Weekly budget limits with penalties
- **Use Case**: "≤2 takeout meals per week"

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
  - `bmi_calculated` = `body_weight_kg / (height_meters^2)`
  - `eating_window_duration` = `last_meal_time - first_meal_time`
  - `protein_per_kg` = `total_daily_protein_g / body_weight_kg`
  - `first_meal_delay` = `first_meal_time - wake_time`
  - `saturated_fat_percentage` = `(saturated_fat_grams * 9) / total_daily_calories * 100`

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

### Complete Data Flow Architecture

```
PHASE 1: PATIENT GENERATION
Patient Profiles → Profile Conditions → Synthetic Data Generation
        ↓
Biomarker/Metric Generation + Survey Response Generation (Logically Aligned)

PHASE 2: HEALTH ASSESSMENT
Raw Lab Data → Marker Runners → Normalized Marker Scores
Survey Responses → Survey Runner v2 → Complex Logic Calculations  
Education Data → Education Processing → Engagement Scores
        ↓
Combined Runner → Pillar Weightings → Comprehensive Patient Scores
        ↓
Impact Analysis → Improvement Potential → Prioritized Recommendations
        ↓
Breakdown Generator → Individual Patient Reports (UI Ready)

PHASE 3: ADHERENCE ARCHITECTURE
Health Recommendations → Config Generator → Algorithm Configurations
        ↓
Metrics Setup (Tracked + Calculated) + Unit Standardization + Screening Compliance
        ↓
8 Core Algorithm Types → Configuration-Driven Scoring → Unified 0-100 Adherence Scores

PHASE 4: INTELLIGENT SYSTEM (Future)
Adherence Patterns → Logic Rules → Triggering Engine
        ↓
Nudges + Check-ins + Challenges → Patient Engagement → Improved Outcomes
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

### Phase 1: Patient Data Generation
1. **Generate Patient Profiles**: Create synthetic patients with consistent health conditions
2. **Generate Survey Data**: Create aligned survey responses based on patient profiles
3. **Generate Biomarker Data**: Create lab/metric data that correlates with health conditions

### Phase 2: Core WellPath Health Assessment
1. **Run Survey Processing**: `python scripts/wellpath_score_runner_survey_v2.py`
2. **Run Marker Processing**: Process biomarker/lab data through marker runners
3. **Run Combined Processing**: `python scripts/WellPath_score_runner_combined.py`
4. **Generate Patient Breakdowns**: `python scripts/Patient_score_breakdown_generator.py`
5. **Analyze Impact Scoring**: Generate improvement recommendations

### Phase 3: Adherence System Implementation
6. **Setup Data Architecture**:
   - Configure tracked metrics (`metric_types_v3.csv`)
   - Setup calculated metrics (`calculated_metrics.csv`)
   - Standardize units (`units_v3.csv`)
   - Define screening compliance framework

7. **Generate Algorithm Configurations**: 
   ```python
   from recommendation_config_generator import process_recommendation
   
   # Single recommendation
   config, filepath = process_recommendation("Add one daily serving of fiber-rich food")
   
   # Batch processing (182+ recommendations)
   recommendations = ["Add one daily serving of fiber", "Exercise 3x/week", "Sleep 7-9 hours"]
   for rec in recommendations:
       config, path = process_recommendation(rec)
   ```

8. **Implement Adherence Scoring**:
   ```python
   # Load config and create algorithm instance
   from algorithms import create_algorithm_from_config
   
   with open('generated_configs/SC-BINARY-DAILY-DIETARY_.json') as f:
       config = json.load(f)
   
   algo = create_algorithm_from_config(config)
   score = algo.calculate_score(user_data)  # Returns 0-100 adherence score
   ```

9. **Test All Configurations**:
   ```bash
   python tests/test_all.py  # Validates all algorithm configurations (dynamically finds all REC*.json)
   ```

### Phase 4: Future Extensions
10. **Integrate Challenge System**: Extend algorithms for time-bound challenges
11. **Setup Triggering System**: Implement logic rules for nudges and check-ins (from Airtable)

## Output Files & Results

### Phase 1: Generated Patient Data
- **Patient Profiles**: Synthetic patient datasets with standardized IDs
- **Biomarker Data**: Lab/metric values aligned with health conditions
- **Survey Data**: Response patterns consistent with patient profiles

### Phase 2: Health Assessment Outputs
- **Markers**: `WellPath_Score_Markers/` - Individual biomarker analysis and pillar contributions
- **Survey**: `WellPath_Score_Survey/` - Clean survey scoring with complex logic rollups
- **Combined**: `WellPath_Score_Combined/` - Integrated scoring with pillar weightings and final scores
- **Breakdowns**: `WellPath_Score_Breakdown/` - Individual patient reports with complete audit trails
- **Impact Analysis**: Improvement potential rankings and prioritized intervention areas

### Phase 3: Adherence Architecture Outputs
- **Generated Configs**: `src/generated_configs/` - 73+ algorithm configuration files (100% tested)
- **Master Config List**: `all_generated_configs.json` - Single source for all generated algorithms
- **Algorithm Implementations**: `src/algorithms/` - Type-safe Python algorithm classes for all 8 types
- **Adherence Scores**: Unified 0-100 scoring for any health recommendation
- **Testing Results**: Comprehensive validation of all algorithm configurations

### Phase 4: Future System Outputs *(Planned)*
- **Challenge Configurations**: Time-bound algorithm variations with gamification
- **Trigger Rules**: Logic-based nudge and check-in configurations
- **Engagement Analytics**: Patient interaction and adherence pattern analysis

## Complete System Architecture

The WellPath platform provides comprehensive health assessment and adherence tracking:

### **Current Implementation**
1. **Patient Generation**: Synthetic data creation with logical consistency
2. **Health Assessment Pipeline**: Biomarker + survey + education processing with 7-pillar scoring  
3. **Adherence Architecture**: 182+ recommendations → 8 algorithms → infinite scalability
4. **Impact Analysis**: Personalized improvement recommendations and priority ranking

### **Extensibility Foundation**
- **Challenge System**: Same algorithms, different timescales (30-day vs. indefinite)
- **Triggering System**: Logic rules for behavioral interventions
- **Configuration-Driven**: No custom code required for new recommendations
- **Unified Scoring**: Consistent 0-100 scale across all health behaviors

### **Production Readiness**
- **100% Test Coverage**: All 73 complex algorithm configurations validated
- **Comprehensive Documentation**: Executive overview + implementation guides + algorithm references
- **Modular Architecture**: Independent phases can be deployed separately
- **Scalable Design**: Built to handle infinite recommendation complexity through configuration

**Result**: From patient generation through adherence tracking - a complete, extensible health platform ready for production deployment and infinite recommendation scaling.