# API Reference - Core Functions and Classes

Complete reference for WellPath system functions, classes, and methods.

## 🏗️ Core Classes

### RecommendationConfigGenerator
**File**: `src/recommendation_config_generator.py`

Main class for analyzing health recommendations and generating algorithm configurations.

#### Methods

##### `__init__(self, csv_directory='src/ref_csv_files_airtable')`
Initialize the generator with reference CSV files.

**Parameters**:
- `csv_directory` (str): Path to directory containing reference CSV files

**Raises**:
- `FileNotFoundError`: If required CSV files are missing

##### `analyze_recommendation(self, recommendation_text: str) -> RecommendationAnalysis`
Analyze recommendation text to determine algorithm type and parameters.

**Parameters**:
- `recommendation_text` (str): The health recommendation to analyze

**Returns**:
- `RecommendationAnalysis`: Object containing algorithm type, confidence, and reasoning

**Example**:
```python
generator = RecommendationConfigGenerator()
analysis = generator.analyze_recommendation("Add one daily serving of fiber-rich food")
# Returns: algorithm_type='binary_threshold', confidence=0.95
```

##### `generate_config(self, recommendation_id: str, recommendation_text: str) -> dict`
Generate complete algorithm configuration from recommendation.

**Parameters**:
- `recommendation_id` (str): Unique identifier (e.g., "REC0001.1")
- `recommendation_text` (str): The health recommendation text

**Returns**:
- `dict`: Complete algorithm configuration with metadata

##### `process_recommendations_batch(self, recommendations: List[dict]) -> List[dict]`
Process multiple recommendations in batch with deduplication.

**Parameters**:
- `recommendations` (List[dict]): List of recommendation dictionaries with 'id' and 'text' keys

**Returns**:
- `List[dict]`: Generated configurations with audit information

---

### AlgorithmAnalysis
**File**: `src/recommendation_config_generator.py`

Data class for algorithm analysis results.

#### Attributes
- `algorithm_type` (str): Determined algorithm type
- `confidence` (float): Confidence score (0.0-1.0)
- `reasoning` (str): Explanation of algorithm selection
- `keywords_found` (List[str]): Keywords that influenced decision
- `threshold_value` (Optional[float]): Extracted threshold value
- `metric_suggestions` (List[str]): Suggested metrics for recommendation

---

## 🧮 Scoring Functions

### Biomarker Scoring
**File**: `src/biomarker_scoring.py`

#### `calculate_biomarker_score(value: float, reference_range: dict, method: str = 'linear') -> float`
Calculate normalized score for a biomarker value.

**Parameters**:
- `value` (float): Raw biomarker value
- `reference_range` (dict): Reference range with 'min', 'max', 'optimal' keys
- `method` (str): Scoring method ('linear', 'threshold', 'multi_range')

**Returns**:
- `float`: Normalized score (0-100)

**Example**:
```python
score = calculate_biomarker_score(
    value=92,
    reference_range={'min': 65, 'max': 99, 'optimal': 85},
    method='linear'
)
# Returns: 95.2
```

#### `allocate_to_pillars(biomarker_score: float, pillar_weights: dict) -> dict`
Allocate biomarker score across health pillars.

**Parameters**:
- `biomarker_score` (float): Normalized biomarker score
- `pillar_weights` (dict): Pillar allocation percentages

**Returns**:
- `dict`: Score allocation by pillar

### Survey Scoring
**File**: `src/survey_scoring.py`

#### `calculate_question_score(response: Any, question_config: dict) -> float`
Calculate score for individual survey question.

**Parameters**:
- `response` (Any): Raw survey response
- `question_config` (dict): Question configuration with scoring rules

**Returns**:
- `float`: Question score (0-100)

#### `calculate_complex_logic_score(patient_data: dict, logic_config: dict) -> float`
Calculate score for complex multi-question logic.

**Parameters**:
- `patient_data` (dict): Complete patient survey data
- `logic_config` (dict): Complex logic configuration

**Returns**:
- `float`: Calculated score incorporating multiple inputs

**Example**:
```python
# Protein intake calculation using BMR and activity level
score = calculate_complex_logic_score(
    patient_data={'weight': 70, 'age': 35, 'activity_level': 'moderate'},
    logic_config={'type': 'protein_bmr', 'target_ratio': 0.8}
)
```

### Combined Scoring
**File**: `src/combined_scoring.py`

#### `calculate_pillar_score(pillar_name: str, marker_score: float, survey_score: float, education_score: float) -> float`
Calculate final pillar score from component scores.

**Parameters**:
- `pillar_name` (str): Name of health pillar
- `marker_score` (float): Biomarker component score
- `survey_score` (float): Survey component score  
- `education_score` (float): Education component score

**Returns**:
- `float`: Final weighted pillar score

#### `calculate_overall_wellness_score(pillar_scores: dict) -> float`
Calculate overall wellness score from pillar scores.

**Parameters**:
- `pillar_scores` (dict): Scores for all health pillars

**Returns**:
- `float`: Overall wellness score (equally weighted average)

---

## 🔧 Utility Functions

### Data Processing
**File**: `src/utils/data_processing.py`

#### `validate_patient_data(patient_data: dict) -> ValidationResult`
Validate patient data completeness and format.

**Parameters**:
- `patient_data` (dict): Patient data dictionary

**Returns**:
- `ValidationResult`: Validation status and error details

#### `normalize_scores(scores: List[float], method: str = 'percentile') -> List[float]`
Normalize scores to 0-100 scale.

**Parameters**:
- `scores` (List[float]): Raw scores to normalize
- `method` (str): Normalization method ('percentile', 'min_max', 'z_score')

**Returns**:
- `List[float]`: Normalized scores

### Configuration Management
**File**: `src/utils/config_manager.py`

#### `load_pillar_weights() -> dict`
Load pillar weighting configuration.

**Returns**:
- `dict`: Pillar weights for all health pillars

#### `validate_config(config: dict) -> bool`
Validate algorithm configuration structure.

**Parameters**:
- `config` (dict): Algorithm configuration to validate

**Returns**:
- `bool`: True if configuration is valid

---

## 📊 Algorithm Implementations

### Binary Threshold
**File**: `src/algorithms/binary_threshold.py`

#### `BinaryThresholdAlgorithm.calculate(actual_value: float, config: dict) -> float`
Execute binary threshold scoring algorithm.

**Parameters**:
- `actual_value` (float): Actual measured/reported value
- `config` (dict): Algorithm configuration with threshold parameters

**Returns**:
- `float`: Score (success_value or failure_value)

**Logic**:
```python
if actual_value >= threshold:
    return success_value  # Typically 100
else:
    return failure_value  # Typically 0
```

### Proportional Scoring
**File**: `src/algorithms/proportional.py`

#### `ProportionalAlgorithm.calculate(actual_value: float, config: dict) -> float`
Execute proportional scoring algorithm.

**Parameters**:
- `actual_value` (float): Actual achieved value
- `config` (dict): Algorithm configuration with target and caps

**Returns**:
- `float`: Proportional score (0-100, capped at maximum_cap)

**Logic**:
```python
percentage_achieved = (actual_value / target_value) * 100
return min(percentage_achieved, maximum_cap)
```

### Composite Weighted
**File**: `src/algorithms/composite_weighted.py`

#### `CompositeWeightedAlgorithm.calculate(patient_data: dict, config: dict) -> float`
Execute composite algorithm with weighted components.

**Parameters**:
- `patient_data` (dict): All patient data for component calculations
- `config` (dict): Composite algorithm configuration

**Returns**:
- `float`: Weighted combination of component scores

**Example Configuration**:
```json
{
  "components": [
    {"metric": "sleep_duration", "weight": 55, "target": 8},
    {"metric": "sleep_consistency", "weight": 22.5, "algorithm": "rolling_average"},
    {"metric": "wake_consistency", "weight": 22.5, "algorithm": "rolling_average"}
  ]
}
```

---

## 📈 Data Export Functions

### Patient Breakdown Generator
**File**: `src/patient_breakdown_generator.py`

#### `generate_patient_breakdown(patient_id: str) -> str`
Generate comprehensive text breakdown for individual patient.

**Parameters**:
- `patient_id` (str): Unique patient identifier

**Returns**:
- `str`: Formatted text breakdown with scores and recommendations

#### `generate_cohort_summary(patient_ids: List[str]) -> dict`
Generate summary statistics for patient cohort.

**Parameters**:
- `patient_ids` (List[str]): List of patient identifiers

**Returns**:
- `dict`: Cohort statistics and distributions

### CSV Export Functions
**File**: `src/export/csv_exporter.py`

#### `export_comprehensive_scores(patient_scores: List[dict], output_path: str) -> None`
Export comprehensive patient scores to CSV.

**Parameters**:
- `patient_scores` (List[dict]): List of patient score dictionaries
- `output_path` (str): Path for output CSV file

#### `export_pillar_summary(pillar_data: dict, output_path: str) -> None`
Export pillar summary statistics to CSV.

**Parameters**:
- `pillar_data` (dict): Aggregated pillar score data
- `output_path` (str): Path for output CSV file

---

## 🔍 Validation Functions

### Score Validation
**File**: `src/validation/score_validator.py`

#### `validate_score_range(score: float) -> bool`
Validate score is within acceptable 0-100 range.

**Parameters**:
- `score` (float): Score to validate

**Returns**:
- `bool`: True if score is valid

#### `validate_pillar_allocations(allocations: dict, total_score: float, tolerance: float = 0.1) -> bool`
Validate pillar allocations sum correctly.

**Parameters**:
- `allocations` (dict): Pillar allocation scores
- `total_score` (float): Expected total score
- `tolerance` (float): Acceptable difference tolerance

**Returns**:
- `bool`: True if allocations are valid

### Data Quality Functions
**File**: `src/validation/data_quality.py`

#### `detect_outliers(values: List[float], method: str = 'iqr') -> List[int]`
Detect statistical outliers in data.

**Parameters**:
- `values` (List[float]): Data values to analyze
- `method` (str): Outlier detection method ('iqr', 'z_score', 'modified_z')

**Returns**:
- `List[int]`: Indices of detected outliers

#### `calculate_data_completeness(patient_data: dict, required_fields: List[str]) -> float`
Calculate data completeness percentage.

**Parameters**:
- `patient_data` (dict): Patient data dictionary
- `required_fields` (List[str]): List of required field names

**Returns**:
- `float`: Completeness percentage (0.0-1.0)

---

## 🎯 Constants and Enums

### Health Pillars
```python
HEALTH_PILLARS = [
    "Healthful_Nutrition",
    "Movement_Exercise", 
    "Restorative_Sleep",
    "Cognitive_Health",
    "Stress_Management",
    "Connection_Purpose",
    "Core_Care"
]
```

### Algorithm Types
```python
ALGORITHM_TYPES = [
    "binary_threshold",
    "proportional", 
    "zone_based_3tier",
    "zone_based_5tier",
    "composite_weighted",
    "constrained_weekly_allowance",
    "categorical_filter_threshold",
    "rolling_average_tolerance",
    "meal_based_frequency",
    "weekly_pattern_binary",
    "daily_consistency_check",
    "range_optimization",
    "percentage_based_reduction",
    "time_window_compliance"
]
```

### Pillar Weights
```python
PILLAR_WEIGHTS = {
    "Healthful_Nutrition": {"markers": 72, "survey": 18, "education": 10},
    "Movement_Exercise": {"markers": 54, "survey": 36, "education": 10},
    "Restorative_Sleep": {"markers": 63, "survey": 27, "education": 10},
    "Cognitive_Health": {"markers": 36, "survey": 54, "education": 10},
    "Stress_Management": {"markers": 27, "survey": 63, "education": 10},
    "Connection_Purpose": {"markers": 18, "survey": 72, "education": 10},
    "Core_Care": {"markers": 49.5, "survey": 40.5, "education": 10}
}
```

---

## 🔧 Error Handling

### Custom Exceptions
**File**: `src/exceptions.py`

#### `ConfigurationError`
Raised when algorithm configuration is invalid or incomplete.

#### `DataValidationError` 
Raised when input data fails validation checks.

#### `ScoringError`
Raised when score calculation encounters unexpected conditions.

#### `PillarAllocationError`
Raised when pillar weight allocations don't sum correctly.

### Error Codes
- `E001`: Missing required biomarker data
- `E002`: Invalid score range (outside 0-100)
- `E003`: Pillar allocation mismatch  
- `E004`: Algorithm configuration schema violation
- `E005`: Reference range data missing
- `E006`: Survey response format error
- `E007`: Patient ID not found
- `E008`: Insufficient data for scoring

---

**This API reference provides comprehensive documentation for all public functions and classes in the WellPath scoring system, enabling developers to integrate and extend the system effectively.**