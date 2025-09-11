# Survey Scoring System - Complete Guide

The WellPath survey scoring system uses sophisticated calculation methods beyond simple response mapping, supporting both straightforward scoring and complex biomarker-dependent personalized calculations.

## 🎯 Core Design Principles

### 1. Question ID-Based Architecture
All custom logic is mapped to specific question IDs (e.g., "2.11", "3.04", "6.07"), making it backend-agnostic and easily integrated with existing database structures.

### 2. Modular Scoring Functions
Complex logic is encapsulated in standalone functions that accept standardized inputs, enabling easy porting to any programming language or calling as microservices.

### 3. Multi-Pillar Impact Logic
Single questions can appropriately impact multiple health pillars with different weights, reflecting real-world health interconnections.

## 📊 Scoring Architecture

### Basic Structure
- **Simple Questions**: Have direct `response_scores` mapping (e.g., "Poor" = 0.2, "Excellent" = 1.0)
- **Complex Questions**: Use custom `score_fn` functions that take patient data and return calculated scores
- **Multi-component Questions**: Combine multiple survey responses into single scores

### Score Processing Pipeline
```
Raw Response → Custom Logic → Raw Score → Scale (÷10 if >1) → Pillar Weights → Final Score
```

## 🧮 Complex Scoring Functions

### 1. Protein Intake Scoring (Question 2.11)
**Purpose**: Personalized protein recommendations based on BMR and activity level

**Logic**:
- Calculates BMR using Mifflin-St Jeor equation
- Applies activity multiplier (1.2-1.9x based on exercise frequency)
- Sets protein target: 1.0-1.5g per kg body weight
- Scores based on achievement vs personalized target

**Multi-pillar Impact**: Nutrition (6), Movement (6)

### 2. Exercise Rollup Calculations (Questions 3.04-3.11)
**Purpose**: Comprehensive exercise assessment across 4 activity types

**Components**:
- **Cardio**: Frequency (3.04) × Duration (3.08)
- **Strength**: Frequency (3.05) × Duration (3.09)  
- **HIIT**: Frequency (3.06) × Duration (3.10)
- **Flexibility**: Frequency (3.07) × Duration (3.11)

**Scoring Logic**:
```python
def exercise_rollup_score(cardio_freq, cardio_duration, ...):
    cardio_minutes = cardio_freq * cardio_duration
    strength_minutes = strength_freq * strength_duration
    # ... calculate total weekly minutes
    return min(total_minutes / 150, 10)  # WHO recommendation baseline
```

### 3. Sleep Issues Multi-Impact (Questions 4.12-4.19)
**Purpose**: Maps sleep problems to appropriate health pillars with frequency weighting

**Logic**:
- Issue selection (4.12) → Frequency mapping (4.13-4.19)
- Different issues impact different pillars:
  - Sleep quality → Sleep pillar (primary)
  - Stress-related → Stress Management pillar
  - Cognitive issues → Cognitive Health pillar

### 4. Stress + Coping Assessment (Questions 6.01, 6.02, 6.07)
**Purpose**: Integrated stress level, frequency, and coping mechanism scoring

**Components**:
- Stress level (6.01): 1-10 scale
- Stress frequency (6.02): How often experienced
- Coping methods (6.07): Quality and effectiveness of strategies

**Integration Logic**:
```python
def stress_coping_score(stress_level, frequency, coping_methods):
    stress_impact = stress_level * frequency_weight
    coping_effectiveness = calculate_coping_score(coping_methods)
    return max(0, 10 - stress_impact + coping_effectiveness)
```

### 5. Substance Use with Quit Time Bonuses
**Purpose**: Accounts for current use, former use, and time since quitting

**Logic**:
- Current users: Scored based on frequency and amount
- Former users: Bonus points based on quit duration
- Never users: Full points
- Special handling for different substances (alcohol, tobacco, etc.)

## 🔄 Multi-Pillar Impact System

### Pillar Weight Distribution Examples
```python
"2.11": {  # Protein intake
    "pillar_weights": {"Nutrition": 6, "Movement": 6},
    "score_fn": protein_intake_score
},
"6.01": {  # Stress management
    "pillar_weights": {"Stress": 8, "Cognitive": 2, "Sleep": 2},
    "score_fn": stress_level_score
}
```

### Weight Normalization
- Weights are normalized within each pillar
- Questions can impact 1-4 pillars simultaneously
- Total pillar weights sum to the question's maximum contribution

## 🛠️ Implementation Architecture

### Function Signature Standard
```python
def scoring_function(patient_data: dict, question_responses: dict) -> float:
    """
    Standard signature for all custom scoring functions
    
    Args:
        patient_data: Demographics, biomarkers, calculated values
        question_responses: Survey responses keyed by question ID
        
    Returns:
        float: Raw score (will be scaled and weighted downstream)
    """
```

### Backend Integration Points
1. **Question ID mapping** directly to scoring functions
2. **Standardized input format** for patient data
3. **Modular functions** callable as microservices
4. **Multi-language support** through consistent I/O specifications

## 📈 Score Aggregation

### Within-Pillar Aggregation
```python
pillar_score = sum(
    question_weighted_score * question_pillar_weight
    for question in pillar_questions
) / sum(all_pillar_weights)
```

### Final Patient Score
```python
final_score = sum(
    pillar_score * pillar_system_weight
    for pillar in all_pillars
)
```

## 🎛️ Configuration Management

### Pillar System Weights
- **High biomarker pillars**: Nutrition (72% markers), Movement (54% markers)
- **High survey pillars**: Connection (72% survey), Stress (63% survey)
- **Balanced pillars**: Core Care (49.5% markers, 40.5% survey)

### Custom Logic Flags
Each question includes metadata:
- `has_custom_logic`: Boolean flag for complex calculations
- `exclude_from_breakdown`: Hide individual question scores when part of rollups
- `calculation_notes`: Human-readable explanation of logic

## 🔍 Debugging and Audit Trail

### Score Derivation Tracking
```
Question Response → Raw Score → Scaling Factor → Pillar Weights → Final Contribution
"Excellent" → 1.0 → ×1 → Nutrition(0.8) → 0.8 points
```

### Complex Logic Documentation
Each custom function includes:
- Clinical rationale for the calculation method
- Parameter sources (WHO guidelines, research papers)
- Edge case handling
- Expected score ranges and distributions

## 📊 Quality Assurance

### Validation Rules
- All scores must be 0-10 range before pillar weighting
- Multi-pillar weights must sum to question's maximum impact
- Custom functions must handle missing data gracefully
- Score distributions should align with population health norms

### Testing Framework
- Unit tests for each custom scoring function
- Integration tests for pillar weight calculations
- Regression tests against known patient scenarios
- Performance benchmarks for large patient datasets

---

**This system provides clinically meaningful health assessments that account for individual circumstances, medical history, and behavior change over time while maintaining technical flexibility for diverse backend implementations.**