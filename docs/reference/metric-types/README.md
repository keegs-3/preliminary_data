# Metric Types Reference

## Overview

WellPath defines 88 raw metric types organized into 6 base classes, similar to Apple HealthKit's data type hierarchy. Each metric type represents a specific health or wellness measurement that can be tracked, validated, and processed through the system.

## Base Class Hierarchy

```
WellPath Metric Types
├── Time-Only Metrics (35 types)
│   ├── Session-Based Metrics
│   ├── Event-Based Metrics  
│   └── Routine Metrics
├── Quantity Metrics (22 types)
│   ├── Nutritional Quantities
│   ├── Activity Quantities
│   └── Substance Quantities
├── Measurement Metrics (8 types)
│   ├── Body Composition
│   ├── Performance Metrics
│   └── Health Screenings
├── Rating Metrics (5 types)
│   ├── Subjective Assessments
│   └── Environmental Ratings
├── Category Select Metrics (5 types)
│   └── Categorical Choices
└── Special Metrics (3 types)
    ├── Temporal Metrics
    └── Demographic Metrics
```

## Base Classes

### 1. Time-Only Metrics (`time_only`)
**35 metric types** - Events or sessions tracked by duration or occurrence

These metrics capture activities, sessions, or behaviors that are primarily time-based. They include start/end timestamps or simple occurrence timestamps.

#### Session-Based Metrics (20 types)
Activities with measurable duration:

| Metric ID | Name | Duration Range | HealthKit Equivalent |
|-----------|------|----------------|---------------------|
| `strength_session` | Strength Training Session | 5-180 min | HKQuantityTypeIdentifier.exerciseTime |
| `meditation_session` | Meditation Session | 1-90 min | HKQuantityTypeIdentifier.mindfulSession |
| `zone2_cardio_session` | Zone 2 Cardio Session | 20-90 min | - |
| `hiit_session` | HIIT Session | 10-60 min | - |
| `mobility_session` | Mobility Session | 5-60 min | - |
| `outdoor_time_session` | Outdoor Time Session | 5-480 min | - |
| `screen_time_session` | Screen Time Session | 1-480 min | HKCategoryTypeIdentifier.screenTime |
| `brain_training_session` | Brain Training Session | 5-60 min | - |
| `stress_management_session` | Stress Management Session | 2-60 min | - |
| `breathwork_mindfulness_session` | Breathwork Session | 2-60 min | - |
| `walking_session` | Walking Session | 5-300 min | HKQuantityTypeIdentifier.walkingRunningDistance |
| `journaling_session` | Journaling Session | 2-60 min | - |
| `gratitude_practice_session` | Gratitude Practice Session | 1-90 min | - |
| `active_time` | Active Time | 0-720 min | HKQuantityTypeIdentifier.activeEnergyBurned |
| `sedentary_time` | Sedentary Time | 0-1440 min | - |

#### Event-Based Metrics (10 types)
Discrete occurrences with timestamps:

| Metric ID | Name | Validation | HealthKit Equivalent |
|-----------|------|------------|---------------------|
| `meal_logged` | Meal Logged | Single occurrence | - |
| `snack_logged` | Snack Logged | Single occurrence | - |
| `exercise_snack` | Exercise Snack | 1 occurrence | - |
| `social_interaction` | Social Interaction | Single event | - |
| `mindful_eating_episode` | Mindful Eating Episode | Single occurrence | - |
| `takeout_meal` | Takeout Meal | Single meal | - |
| `plant_based_meal` | Plant-Based Meal | Single meal | - |
| `whole_food_meal` | Whole Food Meal | Single meal | - |
| `large_meal` | Large Meal | Single meal | - |

#### Routine & Adherence Metrics (5 types)
Binary adherence tracking:

| Metric ID | Name | Values | Description |
|-----------|------|--------|-------------|
| `supplement_taken` | Supplement Taken | taken/skipped | Daily supplement adherence |
| `medication_taken` | Medication Taken | taken/skipped | Daily medication adherence |
| `peptide_taken` | Peptide Taken | taken/skipped | Daily peptide adherence |
| `sleep_routine_adherence` | Sleep Routine Adherence | followed/skipped | Sleep routine compliance |
| `brushing_session` | Brushing Session | completed/skipped | Teeth brushing adherence |
| `flossing_session` | Flossing Session | completed/skipped | Dental flossing adherence |

### 2. Quantity Metrics (`quantity`)
**22 metric types** - Measurable amounts with specific units

#### Nutritional Quantities (14 types)

| Metric ID | Unit | Range | HealthKit Equivalent |
|-----------|------|-------|---------------------|
| `vegetable_serving` | serving | 0.5-3.0 | HKQuantityTypeIdentifier.dietaryVegetables |
| `protein_serving` | serving | 0.5-2.0 | HKQuantityTypeIdentifier.dietaryProtein |
| `water_consumed` | milliliter | 50-1000 | HKQuantityTypeIdentifier.dietaryWater |
| `fiber_serving` | serving | 0.5-3.0 | HKQuantityTypeIdentifier.dietaryFiber |
| `fruit_serving` | serving | 0.5-2.0 | HKQuantityTypeIdentifier.dietaryFruit |
| `added_sugar_consumed` | gram | 0-50 | HKQuantityTypeIdentifier.dietaryAddedSugar |
| `processed_meat_serving` | serving | 0.5-2.0 | - |
| `caffeine_consumed` | milligram | 10-400 | HKQuantityTypeIdentifier.dietaryCaffeine |
| `ultraprocessed_food` | serving | 1 | - |
| `saturated_fat_consumed` | gram | 0-50 | - |
| `fiber_grams` | gram | 1-50 | HKQuantityTypeIdentifier.dietaryFiber |
| `protein_grams` | gram | 1-100 | HKQuantityTypeIdentifier.dietaryProtein |
| `added_sugar_serving` | serving | 0.5-10 | - |
| `whole_grain_serving` | serving | 0.5-5 | - |
| `legume_serving` | serving | 0.5-3 | - |

#### Activity & Lifestyle Quantities (5 types)

| Metric ID | Unit | Range | HealthKit Equivalent |
|-----------|------|-------|---------------------|
| `step_taken` | step | 1 | HKQuantityTypeIdentifier.stepCount |
| `sunlight_exposure` | minutes | 5-300 | - |
| `alcoholic_drink` | drink | 1-10 | - |
| `cigarette` | cigarette | 1-50 | - |
| `calories` | kilocalorie | 1-5000 | HKQuantityTypeIdentifier.activeEnergyBurned |

#### Health Tracking (3 types)

| Metric ID | Unit | Range | Description |
|-----------|------|-------|-------------|
| `healthy_fat_swap` | count | completed/skipped | Healthy fat substitutions |
| `sunscreen_application` | session | applied/skipped | UV protection adherence |
| `skincare_routine` | session | 2-30 min | Daily skincare duration |

### 3. Measurement Metrics (`measurement`)
**8 metric types** - Clinical or performance measurements

#### Body Composition (5 types)

| Metric ID | Unit | Range | HealthKit Equivalent |
|-----------|------|-------|---------------------|
| `weight` | kilogram | 30-300 kg | HKQuantityTypeIdentifier.bodyMass |
| `body_fat_measured` | percent | 5-50% | HKQuantityTypeIdentifier.bodyFatPercentage |
| `lean_body_mass_measured` | kilogram | 20-100 kg | HKQuantityTypeIdentifier.leanBodyMass |
| `visceral_fat_measured` | percent | 1-30% | - |
| `height_measured` | centimeter | 100-250 cm | HKQuantityTypeIdentifier.height |

#### Performance Metrics (3 types)

| Metric ID | Unit | Range | HealthKit Equivalent |
|-----------|------|-------|---------------------|
| `hrv_measured` | millisecond | 10-200 ms | HKQuantityTypeIdentifier.heartRateVariabilitySDNN |
| `vo2_max_measured` | mL/kg/min | 15-80 | HKQuantityTypeIdentifier.vo2Max |
| `resting_heart_rate` | bpm | 40-120 | HKQuantityTypeIdentifier.restingHeartRate |
| `grip_strength` | kilogram | 10-100 kg | - |

### 4. Rating Metrics (`rating`)
**5 metric types** - Subjective 1-5 scale assessments

| Metric ID | Scale | Description |
|-----------|-------|-------------|
| `stress_level_rating` | 1-5 | Perceived stress level |
| `mood_rating` | 1-5 | Daily mood assessment |
| `sleep_environment_score` | 1-5 | Sleep environment quality |
| `focus_rating` | 1-5 | Cognitive focus level |
| `memory_clarity_rating` | 1-5 | Memory and mental clarity |

### 5. Category Select Metrics (`category_select`)
**5 metric types** - Categorical selections from predefined options

| Metric ID | Options | Source Options |
|-----------|---------|----------------|
| `caffeine_source` | 5 types | coffee, tea, energy_drink, soda, supplement |
| `fruit_source_type` | 8 types | berries, citrus, tropical, grapes, melons, dried_fruits, apples_pears, stone_fruits |
| `fiber_source` | 6 types | vegetables, fruits, whole_grains, legumes, nuts_seeds, supplement |
| `vegetable_source` | 9 types | leafy_greens, cruciferous, colorful_peppers, root_vegetables, alliums, tomatoes, squash_zucchini, mushrooms, starchy_vegetables |
| `whole_grain_source` | 9 types | oats, quinoa, brown_rice, whole_wheat, barley, buckwheat, millet, whole_grain_bread, farro |
| `legume_source` | 10 types | lentils, chickpeas, black_beans, kidney_beans, pinto_beans, navy_beans, split_peas, black_eyed_peas, edamame, green_peas |

### 6. Special Metrics (3 types)

#### Temporal Metrics (2 types)

| Metric ID | Data Type | Description |
|-----------|-----------|-------------|
| `wake_time` | timestamp | Daily wake time |
| `sleep_time` | timestamp | Daily sleep onset time |

#### Health Screening Dates (8 types)

| Metric ID | Purpose | Max Age |
|-----------|---------|---------|
| `dental_screening_date` | Dental exam tracking | 20 years |
| `physical_exam_date` | Annual physical tracking | 20 years |
| `skin_check_date` | Dermatology screening | 20 years |
| `vision_check_date` | Eye exam tracking | 20 years |
| `colonoscopy_date` | Colorectal screening | 20 years |
| `mammogram_date` | Breast cancer screening | 20 years |
| `hpv_pap_date` | Cervical cancer screening | 20 years |
| `psa_date` | Prostate screening | 20 years |

#### Demographic Metrics (2 types)

| Metric ID | Values | Purpose |
|-----------|--------|---------|
| `birth_date` | Date | Age calculation, screening eligibility |
| `gender` | male/female/other/prefer_not_to_say | Gender-specific health recommendations |

## Data Entry Types

Each metric specifies its data entry pattern:

| Entry Type | Description | Time Fields | Examples |
|------------|-------------|-------------|----------|
| `time_only` | Timestamp or duration | timestamp OR time_start,time_end | Sessions, events, routines |
| `quantity` | Amount with timestamp | timestamp | Servings, weights, volumes |
| `measurement` | Clinical measurement | timestamp | Body composition, vitals |
| `rating` | Subjective scale | timestamp | Mood, stress, environment |
| `category_select` | Categorical choice | timestamp | Food sources, activity types |

## Validation Schemas

Every metric type includes validation rules:

### Range Validation
```json
{
  "water_consumed": {
    "range": {"min": 50, "max": 1000},
    "unit": "milliliter",
    "data_entry_type": "quantity"
  }
}
```

### Values Validation  
```json
{
  "supplement_taken": {
    "values": ["taken", "skipped"],
    "data_entry_type": "time_only"
  }
}
```

### Duration Validation
```json
{
  "meditation_session": {
    "range": {"min": 1, "max": 90},
    "unit": "session",
    "time_fields": "time_start,time_end"
  }
}
```

## HealthKit Integration

42 metrics map directly to HealthKit equivalents:

### Direct Mappings
- `step_taken` → `HKQuantityTypeIdentifier.stepCount`
- `water_consumed` → `HKQuantityTypeIdentifier.dietaryWater`
- `weight` → `HKQuantityTypeIdentifier.bodyMass`
- `meditation_session` → `HKQuantityTypeIdentifier.mindfulSession`

### WellPath Extensions
48 metrics extend beyond HealthKit's scope:
- Detailed nutrition source tracking
- Behavioral adherence metrics  
- Environmental factors
- Routine compliance tracking

---

**Next**: [Raw Metrics Catalog](raw-metrics.md) | [Calculated Metrics](calculated-metrics.md) | [Units System](../units/)