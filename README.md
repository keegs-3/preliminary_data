# WellPath Scoring System

Comprehensive health assessment pipeline that processes biomarkers, survey responses, and education engagement to generate personalized wellness scores and patient breakdowns.

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
- **Processor**: `wellpath_score_runner_survey_v2.py` (recommended clean implementation)
- **Output**: `WellPath_Score_Survey/` - Survey scores with complex logic calculations
- **Complex Logic Includes**:
  - Exercise frequency + duration rollups (Cardio, Strength, HIIT, Flexibility)
  - Stress level + frequency + coping methods interactions
  - Sleep issues + frequency mapping with multi-pillar impact
  - Personalized protein/calorie targets based on BMR
  - Substance use scoring with quit time bonuses
  - Cognitive activity and sleep protocol counting

### 3. Combined Processing
- **Processor**: `WellPath_score_runner_combined.py`
- **Function**: Integrates marker, survey, and education data with pillar-specific weightings
- **Output**: `WellPath_Score_Combined/comprehensive_patient_scores_detailed.csv`
- **Key Features**: 
  - Applies pillar allocation weights
  - Calculates final composite scores 
  - Generates improvement potential analysis
  - Maintains audit trail from all components

### 4. Patient Breakdown Generation
- **Processor**: `Patient_score_breakdown_generator.py`
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

## Key Features

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
```

## Usage

1. **Run Survey Processing**: `python wellpath_score_runner_survey_v2.py`
2. **Run Combined Processing**: `python WellPath_score_runner_combined.py`
3. **Generate Patient Breakdowns**: `python Patient_score_breakdown_generator.py`

## Output Files

- **Markers**: Individual biomarker analysis and pillar contributions
- **Survey**: Clean survey scoring with complex logic rollups
- **Combined**: Integrated scoring with pillar weightings and final scores
- **Breakdowns**: Individual patient reports with complete audit trails

The system provides comprehensive transparency from raw inputs through final scores, enabling detailed patient counseling and improvement recommendations.