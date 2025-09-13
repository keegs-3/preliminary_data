# Calculated Metrics Reference

## Overview

Calculated metrics are derived values computed from raw metrics using standardized formulas. WellPath defines 134 calculated metrics organized into 8 calculation types, providing aggregated insights, patterns, and derived health indicators.

## Calculation Type Hierarchy

```
Calculated Metrics (134 total)
├── Sum Calculations (45 metrics)
│   ├── Daily Aggregations (32)
│   ├── Weekly Summaries (8)
│   └── Duration Totals (5)
├── Count Calculations (22 metrics)
│   ├── Session Counts (15)
│   ├── Event Counts (5)
│   └── Source Diversity (2)
├── Average Calculations (8 metrics)
│   ├── Weekly Averages (6)
│   └── Adherence Percentages (2)
├── Difference Calculations (18 metrics)
│   ├── Session Durations (15)
│   └── Time Intervals (3)
├── Date Difference Calculations (8 metrics)
│   └── Screening Intervals
├── Standard Deviation Calculations (2 metrics)
│   └── Consistency Metrics
├── Custom Calculations (15 metrics)
│   ├── Compliance Statuses (8)
│   ├── Body Composition (3)
│   ├── Nutritional Ratios (2)
│   └── Complex Derivations (2)
└── Min/Max Calculations (16 metrics)
    ├── Meal Timing (2)
    ├── Substance Timing (3)
    └── Activity Patterns (11)
```

## Calculation Types

### 1. Sum Calculations (45 metrics)
**Formula Pattern**: `SUM(source_metric) WHERE date = target_date`

Aggregate raw metrics into daily, weekly, or period totals.

#### Daily Nutritional Aggregations (12 metrics)

| Metric ID | Formula | Source | Unit |
|-----------|---------|--------|------|
| `daily_vegetable_servings` | SUM(vegetable_serving) WHERE date = target_date | vegetable_serving | serving |
| `daily_protein_servings` | SUM(protein_serving) WHERE date = target_date | protein_serving | serving |
| `daily_water_consumption` | SUM(water_consumed) WHERE date = target_date | water_consumed | milliliter |
| `daily_fiber_serving` | SUM(fiber_serving) WHERE date = target_date | fiber_serving | serving |
| `daily_fruit_serving` | SUM(fruit_serving) WHERE date = target_date | fruit_serving | serving |
| `daily_added_sugar_consumed` | SUM(added_sugar_consumed) WHERE date = target_date | added_sugar_consumed | gram |
| `daily_protein_grams` | SUM(protein_grams) WHERE date = target_date | protein_grams | gram |
| `daily_fiber_grams` | SUM(fiber_grams) WHERE date = target_date | fiber_grams | gram |
| `daily_caffeine_consumed` | SUM(caffeine_consumed) WHERE date = target_date | caffeine_consumed | milligram |
| `daily_processed_meat_serving` | SUM(processed_meat_serving) WHERE date = target_date | processed_meat_serving | serving |
| `daily_whole_grain_servings` | SUM(whole_grain_serving) WHERE date = target_date | whole_grain_serving | serving |
| `daily_legume_servings` | SUM(legume_serving) WHERE date = target_date | legume_serving | serving |

#### Daily Activity Aggregations (8 metrics)

| Metric ID | Formula | Source | Unit |
|-----------|---------|--------|------|
| `daily_steps` | SUM(step_taken) WHERE date = target_date | step_taken | step |
| `daily_active_time` | SUM(active_time) WHERE date = target_date | active_time | minutes |
| `daily_sunlight_exposure` | SUM(sunlight_exposure) WHERE date = target_date | sunlight_exposure | minutes |
| `daily_calories` | SUM(calories) WHERE date = target_date | calories | kilocalorie |

#### Duration Totals from Sessions (12 metrics)

| Metric ID | Formula | Source | Unit |
|-----------|---------|--------|------|
| `daily_strength_training_duration` | SUM(strength_session_duration) WHERE date = target_date | strength_session_duration | minutes |
| `daily_meditation_duration` | SUM(meditation_session_duration) WHERE date = target_date | meditation_session_duration | minutes |
| `daily_hiit_duration` | SUM(hiit_session_duration) WHERE date = target_date | hiit_session_duration | minutes |
| `daily_mobility_duration` | SUM(mobility_session_duration) WHERE date = target_date | mobility_session_duration | minutes |
| `daily_outdoor_time_duration` | SUM(outdoor_time_session_duration) WHERE date = target_date | outdoor_time_session_duration | minutes |
| `daily_screen_time_duration` | SUM(screen_time_session_duration) WHERE date = target_date | screen_time_session_duration | minutes |
| `daily_brain_training_duration` | SUM(brain_training_session_duration) WHERE date = target_date | brain_training_session_duration | minutes |
| `daily_walking_duration` | SUM(walking_session_duration) WHERE date = target_date | walking_session_duration | minutes |
| `daily_zone2_cardio_duration` | SUM(zone2_cardio_session_duration) WHERE date = target_date | zone2_cardio_session_duration | minutes |
| `daily_stress_management_duration` | SUM(stress_management_session_duration) WHERE date = target_date | stress_management_session_duration | minutes |
| `daily_breathwork_mindfulness_duration` | SUM(breathwork_mindfulness_session_duration) WHERE date = target_date | breathwork_mindfulness_session_duration | minutes |
| `daily_post_meal_activity_duration` | SUM(post_meal_activity_duration) WHERE date = target_date | post_meal_activity_duration | minutes |

### 2. Count Calculations (22 metrics)
**Formula Pattern**: `COUNT(source_metric) WHERE date = target_date`

Count occurrences of events, sessions, or behaviors.

#### Session Counts (15 metrics)

| Metric ID | Description | Source | Unit |
|-----------|-------------|--------|------|
| `daily_meals` | Total number of meals consumed per day | meal_logged | meal |
| `daily_snacks` | Total number of snack episodes per day | snack_logged | snack |
| `daily_strength_training_sessions` | Number of strength training sessions per day | strength_session | session |
| `daily_meditation_sessions` | Number of meditation sessions per day | meditation_session | session |
| `daily_hiit_sessions` | Number of HIIT sessions per day | hiit_session | session |
| `daily_mobility_sessions` | Number of mobility sessions per day | mobility_session | session |
| `daily_outdoor_time_sessions` | Number of outdoor time sessions per day | outdoor_time_session | session |
| `daily_screen_time_sessions` | Number of screen time sessions per day | screen_time_session | session |
| `daily_brain_training_sessions` | Number of brain training sessions per day | brain_training_session | session |
| `daily_stress_management_sessions` | Number of stress management sessions per day | stress_management_session | session |
| `daily_gratitude_sessions` | Number of gratitude practice sessions per day | gratitude_practice_session | session |
| `daily_walking_sessions` | Number of walking sessions per day | walking_session | session |
| `daily_brushing_sessions` | Number of teeth brushing sessions per day | brushing_session | session |
| `daily_flossing_sessions` | Number of dental flossing sessions per day | flossing_session | session |
| `zone2_cardio_sessions` | Number of Zone 2 cardio sessions per day | zone2_cardio_session | session |

#### Event & Behavior Counts (7 metrics)

| Metric ID | Description | Source | Unit |
|-----------|-------------|--------|------|
| `daily_exercise_snacks` | Number of exercise snacks per day | exercise_snack | snack |
| `daily_mindful_eating_episodes` | Number of mindful eating episodes per day | mindful_eating_episode | episode |
| `daily_takeout_meal` | Number of takeout meals per day | takeout_meal | meal |
| `daily_plant_based_meal` | Number of plant-based meals per day | plant_based_meal | meal |
| `daily_whole_food_meals` | Number of whole food meals per day | whole_food_meal | meal |
| `daily_large_meals` | Number of large meals per day | large_meal | meal |
| `daily_alcoholic_drinks` | Number of alcoholic beverages per day | alcoholic_drink | drink |

### 3. Average Calculations (8 metrics)
**Formula Pattern**: `AVG(source_metric) WHERE date >= week_start AND date <= week_end`

Calculate weekly averages for subjective ratings and adherence metrics.

#### Weekly Rating Averages (6 metrics)

| Metric ID | Description | Source | Scale |
|-----------|-------------|--------|-------|
| `avg_weekly_stress_level_rating` | Average stress level over 7 days | stress_level_rating | 1-5 |
| `avg_weekly_mood_rating` | Average mood rating over 7 days | mood_rating | 1-5 |
| `avg_weekly_sleep_environment_score` | Average sleep environment quality over 7 days | sleep_environment_score | 1-5 |
| `avg_weekly_focus_rating` | Average cognitive focus over 7 days | focus_rating | 1-5 |
| `avg_weekly_memory_clarity_rating` | Average memory clarity over 7 days | memory_clarity_rating | 1-5 |
| `avg_weekly_sleep_routine_adherence` | Average sleep routine adherence over 7 days | sleep_routine_adherence | percent |

#### Adherence Percentages (2 metrics)

| Metric ID | Formula | Description |
|-----------|---------|-------------|
| `weekly_supplement_adherence` | (COUNT(supplement_taken) / 7) * 100 | Weekly supplement adherence percentage |
| `weekly_medication_adherence` | (COUNT(medication_taken) / 7) * 100 | Weekly medication adherence percentage |

### 4. Difference Calculations (18 metrics)
**Formula Pattern**: `end_time - start_time` or `target_time - reference_time`

Calculate durations between timestamps or time intervals.

#### Session Durations (15 metrics)

| Metric ID | Formula | Description | Unit |
|-----------|---------|-------------|------|
| `strength_session_duration` | strength_session.end_time - strength_session.start_time | Individual strength session duration | minutes |
| `meditation_session_duration` | meditation_session.end_time - meditation_session.start_time | Individual meditation session duration | minutes |
| `hiit_session_duration` | hiit_session.end_time - hiit_session.start_time | Individual HIIT session duration | minutes |
| `mobility_session_duration` | mobility_session.end_time - mobility_session.start_time | Individual mobility session duration | minutes |
| `outdoor_time_session_duration` | outdoor_session.end_time - outdoor_session.start_time | Individual outdoor session duration | minutes |
| `screen_time_session_duration` | screen_time_session.end_time - screen_time_session.start_time | Individual screen session duration | minutes |
| `brain_training_session_duration` | brain_training_session.end_time - brain_training_session.start_time | Individual brain training duration | minutes |
| `stress_management_session_duration` | stress_management_session.end_time - stress_management_session.start_time | Individual stress management duration | minutes |
| `breathwork_mindfulness_session_duration` | breathwork_session.end_time - breathwork_session.start_time | Individual breathwork duration | minutes |
| `walking_session_duration` | walking_session.end_time - walking_session.start_time | Individual walking session duration | minutes |
| `zone2_cardio_session_duration` | zone2_cardio_session.end_time - zone2_cardio_session.start_time | Individual Zone 2 cardio duration | minutes |

#### Time Intervals & Buffers (7 metrics)

| Metric ID | Formula | Description | Unit |
|-----------|---------|-------------|------|
| `sleep_duration` | abs(wake_time - sleep_time) | Total sleep time excluding wake periods | hours_minutes |
| `eating_window_duration` | last_meal_time - first_meal_time | Duration of daily eating window | hours |
| `first_meal_delay` | first_meal_time - wake_time | Time between wake and first meal | hours |
| `last_meal_buffer` | sleep_time - last_meal_time | Time between last meal and sleep | hours |
| `last_alcoholic_drink_buffer` | sleep_time - last_alcoholic_drink_time | Time between last drink and sleep | hours |
| `screen_time_buffer` | sleep_time - last_screen_time | Time between last screen use and sleep | hours |
| `last_caffeine_consumption_buffer` | sleep_time - last_caffeine_consumption_time | Time between last caffeine and sleep | hours |

### 5. Date Difference Calculations (8 metrics)
**Formula Pattern**: `DATEDIF(past_date, TODAY(), time_unit)`

Calculate time intervals since health screenings for compliance tracking.

| Metric ID | Formula | Description | Unit |
|-----------|---------|-------------|------|
| `years_since_physical` | DATEDIF(physical_exam_date, TODAY(), 'YEARS') | Time since last physical exam | years |
| `months_since_dental_exam` | DATEDIF(dental_exam_date, TODAY(), 'MONTHS') | Time since last dental exam | months |
| `months_since_vision_check` | DATEDIF(vision_check_date, TODAY(), 'MONTHS') | Time since last eye exam | months |
| `months_since_skin_check` | DATEDIF(skin_check_date, TODAY(), 'MONTHS') | Time since last skin check | months |
| `years_since_colonoscopy` | DATEDIF(colonoscopy_date, TODAY(), 'YEARS') | Time since last colonoscopy | years |
| `months_since_mammogram` | DATEDIF(mammogram_date, TODAY(), 'MONTHS') | Time since last mammogram | months |
| `years_since_cervical_screening` | DATEDIF(cervical_screening_date, TODAY(), 'YEARS') | Time since last cervical screening | years |
| `years_since_psa_test` | DATEDIF(psa_test_date, TODAY(), 'YEARS') | Time since last PSA test | years |

### 6. Standard Deviation Calculations (2 metrics)
**Formula Pattern**: `STDEV(values) WHERE date >= analysis_start AND date <= analysis_end`

Measure consistency and variability in time-based metrics.

| Metric ID | Formula | Description | Unit |
|-----------|---------|-------------|------|
| `sleep_time_consistency` | STDEV(sleep_time) WHERE date >= analysis_start AND date <= analysis_end | Sleep schedule consistency (lower = better) | minutes |
| `wake_time_consistency` | STDEV(wake_time) WHERE date >= analysis_start AND date <= analysis_end | Wake schedule consistency (lower = better) | minutes |

### 7. Custom Calculations (15 metrics)

#### Compliance Status Calculations (8 metrics)
**Formula Pattern**: `calculate_compliance(time_since, interval_requirement, user_factors)`

Complex boolean calculations determining health screening compliance based on age, gender, and risk factors.

| Metric ID | Formula Logic | Description |
|-----------|---------------|-------------|
| `physical_compliance_status` | calculate_compliance(years_since_physical, 1) | Annual physical exam compliance |
| `dental_compliance_status` | calculate_compliance(months_since_dental_exam, 6) | Dental exam compliance (6-month intervals) |
| `vision_check_compliance_status` | calculate_compliance(months_since_vision_check, 12) | Vision check compliance (annual) |
| `skin_check_compliance_status` | calculate_compliance(months_since_skin_check, risk_level, skin_check_rules) | Skin check compliance (risk-adjusted) |
| `colonoscopy_compliance_status` | IF(age>=50, calculate_compliance(years_since_colonoscopy, age, risk_level, colonoscopy_rules), not_applicable) | Colonoscopy compliance (age 50+) |
| `mammogram_compliance_status` | IF(gender=female AND age>40, calculate_compliance(months_since_mammogram, age, risk_level, mammogram_rules), not_applicable) | Mammogram compliance (female 40+) |
| `cervical_compliance_status` | IF(gender=female AND age>=21 AND age<=65, calculate_compliance(years_since_cervical_screening, cervical_rules), not_applicable) | Cervical screening compliance (female 21-65) |
| `psa_compliance_status` | IF(gender=male AND age>=45, calculate_compliance(years_since_psa_test, age, risk_level, psa_rules), not_applicable) | PSA test compliance (male 45+) |

#### Body Composition Calculations (3 metrics)

| Metric ID | Formula | Description | Unit |
|-----------|---------|-------------|------|
| `bmi_calculated` | body_weight_kg / (height_meters^2) | Body Mass Index calculation | kg/m² |
| `protein_per_kg` | daily_protein_grams / weight | Protein intake per body weight | g/kg |
| `user_age` | DATEDIF(birth_date, TODAY(), 'YEARS') | Current age calculation | years |

#### Nutritional Ratios (2 metrics)

| Metric ID | Formula | Description | Unit |
|-----------|---------|-------------|------|
| `saturated_fat_percentage` | (daily_saturated_fat * 9) / daily_calories * 100 | Percentage of calories from saturated fat | percent |

### 8. Min/Max Calculations (16 metrics)
**Formula Pattern**: `MIN()` or `MAX()` to find earliest/latest occurrences

#### Meal Timing (2 metrics)

| Metric ID | Formula | Description | Unit |
|-----------|---------|-------------|------|
| `first_meal_time` | MIN(meal_logged) WHERE date = target_date | Time of first meal each day | timestamp |
| `last_meal_time` | MAX(meal_logged) WHERE date = target_date | Time of last meal each day | timestamp |

#### Substance & Activity Timing (3 metrics)

| Metric ID | Formula | Description | Unit |
|-----------|---------|-------------|------|
| `last_alcoholic_drink_time` | MAX(alcoholic_drink_times) WHERE date = target_date | Time of last alcoholic drink | timestamp |
| `last_screen_time` | MAX(screen_time_session.end_time) WHERE date = target_date | Time of last digital device usage | timestamp |
| `last_caffeine_consumption_time` | MAX(caffeine_consumed) WHERE date = target_date | Time of last caffeine intake | timestamp |

## Data Dependencies

### Dependency Chain Examples

**Sleep Analysis Chain**:
```
sleep_time, wake_time → sleep_duration → sleep_duration_zone_score
sleep_time (multiple days) → sleep_time_consistency → consistency_score
```

**Nutritional Analysis Chain**:
```
protein_grams → daily_protein_grams
weight → protein_per_kg (daily_protein_grams ÷ weight)
```

**Health Screening Chain**:
```
physical_exam_date → years_since_physical → physical_compliance_status
birth_date → user_age → age-appropriate_screening_requirements
```

## Implementation Notes

### Calculation Timing
- **Real-time**: Sum, count, and difference calculations update immediately
- **End-of-day**: Min/max meal timing calculations finalize at midnight
- **Weekly**: Average and standard deviation calculations complete on Sunday
- **On-demand**: Compliance status calculations trigger when screening dates update

### Data Quality Handling
- **Missing Data**: Calculations gracefully handle NULL values
- **Validation**: Range checks prevent impossible calculated values
- **Consistency**: Cross-metric validation ensures logical relationships

### Performance Optimization
- **Caching**: Frequently accessed calculations stored in memory
- **Incremental**: Only recalculate affected metrics when source data changes
- **Batch Processing**: Weekly calculations run as scheduled jobs

---

**Next**: [Units System](../units/) | [Algorithm Types](../../algorithms/) | [Back to Overview](README.md)