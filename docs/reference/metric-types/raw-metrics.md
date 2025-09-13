# Raw Metrics Catalog

## Overview

Raw metrics are the foundation of the WellPath system - direct measurements from devices, user input, or manual logging. These 88 metrics capture real-world health and wellness data that feeds into calculated metrics and scoring algorithms.

## Quick Reference

### By Category

| Category | Count | Examples |
|----------|-------|----------|
| **Nutrition** | 19 | water_consumed, vegetable_serving, protein_serving |
| **Exercise & Movement** | 15 | strength_session, step_taken, walking_session |
| **Sleep & Recovery** | 8 | sleep_time, wake_time, sleep_routine_adherence |
| **Mental Wellness** | 12 | meditation_session, stress_level_rating, mood_rating |
| **Health Screening** | 8 | physical_exam_date, dental_screening_date |
| **Body Composition** | 5 | weight, body_fat_measured, height_measured |
| **Lifestyle** | 10 | screen_time_session, sunlight_exposure, social_interaction |
| **Performance** | 4 | vo2_max_measured, hrv_measured, grip_strength |
| **Personal Care** | 5 | brushing_session, skincare_routine, sunscreen_application |
| **Demographics** | 2 | birth_date, gender |

## Detailed Metrics Reference

### Nutrition & Hydration (19 metrics)

#### Core Nutritional Tracking

**`water_consumed`** - Water Consumed  
- **Type**: quantity | **Unit**: milliliter | **Range**: 50-1000 mL
- **HealthKit**: HKQuantityTypeIdentifier.dietaryWater
- **Description**: Amount of water consumed in each instance
- **Generates**: `daily_water_consumption`

**`vegetable_serving`** - Vegetable Serving  
- **Type**: quantity | **Unit**: serving | **Range**: 0.5-3.0 servings
- **HealthKit**: HKQuantityTypeIdentifier.dietaryVegetables
- **Description**: Each serving of vegetables consumed
- **Generates**: `daily_vegetable_servings`

**`protein_serving`** - Protein Serving  
- **Type**: quantity | **Unit**: serving | **Range**: 0.5-2.0 servings  
- **HealthKit**: HKQuantityTypeIdentifier.dietaryProtein
- **Description**: Each serving of protein consumed
- **Generates**: `daily_protein_servings`

**`fiber_serving`** - Fiber Serving  
- **Type**: quantity | **Unit**: serving | **Range**: 0.5-3.0 servings
- **HealthKit**: HKQuantityTypeIdentifier.dietaryFiber  
- **Description**: Each serving of fiber consumed
- **Generates**: `daily_fiber_serving`

**`fruit_serving`** - Fruit Serving  
- **Type**: quantity | **Unit**: serving | **Range**: 0.5-2.0 servings
- **HealthKit**: HKQuantityTypeIdentifier.dietaryFruit
- **Description**: Each serving of fruit consumed  
- **Generates**: `daily_fruit_serving`

#### Detailed Nutritional Components

**`protein_grams`** - Protein Grams  
- **Type**: quantity | **Unit**: gram | **Range**: 1-100 g
- **HealthKit**: HKQuantityTypeIdentifier.dietaryProtein
- **Description**: Grams of protein consumed
- **Generates**: `daily_protein_grams`, `protein_per_kg`

**`fiber_grams`** - Fiber Grams  
- **Type**: quantity | **Unit**: gram | **Range**: 1-50 g
- **HealthKit**: HKQuantityTypeIdentifier.dietaryFiber
- **Description**: Grams of fiber consumed  
- **Generates**: `daily_fiber_grams`

**`added_sugar_consumed`** - Added Sugar Consumed  
- **Type**: quantity | **Unit**: gram | **Range**: 0-50 g
- **HealthKit**: HKQuantityTypeIdentifier.dietaryAddedSugar
- **Description**: Grams of added sugar consumed in each instance
- **Generates**: `daily_added_sugar_consumed`

**`saturated_fat_consumed`** - Saturated Fat Consumed  
- **Type**: quantity | **Unit**: gram | **Range**: 0-50 g
- **Description**: Grams of saturated fat consumed
- **Generates**: `daily_saturated_fat`, `saturated_fat_percentage`

**`caffeine_consumed`** - Caffeine Consumed  
- **Type**: quantity | **Unit**: milligram | **Range**: 10-400 mg
- **HealthKit**: HKQuantityTypeIdentifier.dietaryCaffeine
- **Description**: Milligrams of caffeine consumed in each instance
- **Generates**: `daily_caffeine_consumed`, `last_caffeine_consumption_time`

#### Food Quality & Sources

**`whole_grain_serving`** - Whole Grain Serving  
- **Type**: quantity | **Unit**: serving | **Range**: 0.5-5 servings
- **Description**: Serving of whole grains consumed
- **Generates**: `daily_whole_grain_servings`

**`legume_serving`** - Legume Serving  
- **Type**: quantity | **Unit**: serving | **Range**: 0.5-3 servings
- **Description**: Serving of legumes consumed
- **Generates**: `daily_legume_servings`

**`processed_meat_serving`** - Processed Meat Serving  
- **Type**: quantity | **Unit**: serving | **Range**: 0.5-2.0 servings
- **Description**: Each serving of processed meat consumed
- **Generates**: `daily_processed_meat_serving`

#### Meal Types & Patterns

**`meal_logged`** - Meal Logged  
- **Type**: time_only | **Unit**: meal | **Range**: Single occurrence
- **Description**: Each time a user logs a meal entry
- **Generates**: `daily_meals`, `first_meal_time`, `last_meal_time`

**`snack_logged`** - Snack Logged  
- **Type**: time_only | **Unit**: snack | **Range**: Single occurrence
- **Description**: Each time a user logs a snack entry
- **Generates**: `daily_snacks`

**`plant_based_meal`** - Plant-Based Meal  
- **Type**: time_only | **Unit**: meal | **Range**: Single meal
- **Description**: Meal that is primarily or entirely plant-based
- **Generates**: `daily_plant_based_meal`

**`whole_food_meal`** - Whole Food Meal  
- **Type**: time_only | **Unit**: meal | **Range**: Single meal
- **Description**: Meal consisting primarily of whole foods
- **Generates**: `daily_whole_food_meals`

**`takeout_meal`** - Takeout Meal  
- **Type**: time_only | **Unit**: meal | **Range**: Single meal
- **Description**: Meal sourced via carryout/delivery
- **Generates**: `daily_takeout_meal`

**`large_meal`** - Large Meal  
- **Type**: time_only | **Unit**: meal | **Range**: Single meal
- **Description**: Large meal consumed
- **Generates**: `daily_large_meals`

### Exercise & Movement (15 metrics)

#### Structured Exercise Sessions

**`strength_session`** - Strength Training Session  
- **Type**: time_only | **Unit**: session | **Range**: 5-180 min
- **HealthKit**: HKQuantityTypeIdentifier.exerciseTime
- **Description**: Individual strength training workout session
- **Generates**: `daily_strength_training_sessions`, `strength_session_duration`

**`zone2_cardio_session`** - Zone 2 Cardio Session  
- **Type**: time_only | **Unit**: session | **Range**: 20-90 min
- **Description**: Zone 2 cardiovascular training session
- **Generates**: `zone2_cardio_sessions`, `zone2_cardio_session_duration`

**`hiit_session`** - HIIT Session  
- **Type**: time_only | **Unit**: session | **Range**: 10-60 min
- **Description**: High-intensity interval training session
- **Generates**: `daily_hiit_sessions`, `hiit_session_duration`

**`walking_session`** - Walking Session  
- **Type**: time_only | **Unit**: session | **Range**: 5-300 min
- **HealthKit**: HKQuantityTypeIdentifier.walkingRunningDistance
- **Description**: Walking exercise session
- **Generates**: `daily_walking_sessions`, `walking_session_duration`

**`mobility_session`** - Mobility Session  
- **Type**: time_only | **Unit**: session | **Range**: 5-60 min
- **Description**: Individual mobility or flexibility session
- **Generates**: `daily_mobility_sessions`, `mobility_session_duration`

#### Activity Tracking

**`step_taken`** - Step Taken  
- **Type**: quantity | **Unit**: step | **Range**: Single step
- **HealthKit**: HKQuantityTypeIdentifier.stepCount
- **Description**: Individual step recorded by device
- **Generates**: `daily_steps`

**`active_time`** - Active Time  
- **Type**: time_only | **Unit**: hours_minutes | **Range**: 0-720 min
- **HealthKit**: HKQuantityTypeIdentifier.activeEnergyBurned
- **Description**: Time spent in active movement
- **Generates**: `daily_active_time`, `activity_sessions`

**`sedentary_time`** - Sedentary Time  
- **Type**: time_only | **Unit**: hours_minutes | **Range**: 0-1440 min
- **Description**: Time spent in sedentary activities

**`exercise_snack`** - Exercise Snack  
- **Type**: time_only | **Unit**: session | **Range**: Single occurrence
- **Description**: Brief bout of physical activity
- **Generates**: `daily_exercise_snacks`, `daily_post_meal_exercise_snacks`

### Sleep & Recovery (8 metrics)

#### Core Sleep Tracking

**`sleep_time`** - Sleep Time  
- **Type**: time_only | **Unit**: timestamp | **Range**: Sleep onset time
- **HealthKit**: HKQuantityTypeIdentifier.sleepAnalysis
- **Description**: Total sleep duration in minutes
- **Generates**: `sleep_duration`, `sleep_time_consistency`

**`wake_time`** - Wake Time  
- **Type**: time_only | **Unit**: timestamp | **Range**: Wake time  
- **Description**: Time of waking up
- **Generates**: `sleep_duration`, `wake_time_consistency`, `first_meal_delay`

#### Sleep Quality & Environment

**`sleep_routine_adherence`** - Sleep Routine Adherence  
- **Type**: time_only | **Unit**: count | **Values**: followed/skipped
- **Description**: Whether sleep routine was followed
- **Generates**: `avg_weekly_sleep_routine_adherence`

**`sleep_environment_score`** - Sleep Environment Score  
- **Type**: rating | **Unit**: scale_1_5 | **Values**: 1-5
- **Description**: Sleep environment quality rating
- **Generates**: `avg_weekly_sleep_environment_score`

**`evening_routine`** - Evening Routine  
- **Type**: time_only | **Unit**: session | **Range**: 5-60 min
- **Description**: Evening routine practice session
- **Generates**: `weekly_evening_routine_adherence`

### Mental Wellness (12 metrics)

#### Mindfulness & Meditation

**`meditation_session`** - Meditation Session  
- **Type**: time_only | **Unit**: session | **Range**: 1-90 min
- **HealthKit**: HKQuantityTypeIdentifier.mindfulSession
- **Description**: Individual meditation or mindfulness session
- **Generates**: `daily_meditation_sessions`, `meditation_session_duration`

**`breathwork_mindfulness_session`** - Breathwork Session  
- **Type**: time_only | **Unit**: session | **Range**: 2-60 min
- **Description**: Breathwork or mindfulness practice session
- **Generates**: `daily_breathwork_mindfulness_sessions`

**`gratitude_practice_session`** - Gratitude Practice Session  
- **Type**: time_only | **Unit**: session | **Range**: 1-90 min
- **Description**: Gratitude practice session
- **Generates**: `daily_gratitude_sessions`

#### Stress & Emotional Wellness

**`stress_management_session`** - Stress Management Session  
- **Type**: time_only | **Unit**: session | **Range**: 2-60 min
- **Description**: Stress management practice session
- **Generates**: `daily_stress_management_sessions`

**`stress_level_rating`** - Stress Level Rating  
- **Type**: rating | **Unit**: scale_1_5 | **Values**: 1-5
- **Description**: Perceived stress level on 1-5 scale
- **Generates**: `avg_weekly_stress_level_rating`

**`mood_rating`** - Mood Rating  
- **Type**: rating | **Unit**: scale_1_5 | **Values**: 1-5
- **Description**: Mood level on 1-5 scale
- **Generates**: `avg_weekly_mood_rating`

#### Cognitive Functions

**`brain_training_session`** - Brain Training Session  
- **Type**: time_only | **Unit**: session | **Range**: 5-60 min
- **Description**: Cognitive training activity session
- **Generates**: `daily_brain_training_sessions`

**`focus_rating`** - Focus Rating  
- **Type**: rating | **Unit**: scale_1_5 | **Values**: 1-5
- **Description**: Cognitive focus rating on 1-5 scale
- **Generates**: `avg_weekly_focus_rating`

**`memory_clarity_rating`** - Memory Clarity Rating  
- **Type**: rating | **Unit**: scale_1_5 | **Values**: 1-5
- **Description**: Memory and mental clarity rating on 1-5 scale
- **Generates**: `avg_weekly_memory_clarity_rating`

**`journaling_session`** - Journaling Session  
- **Type**: time_only | **Unit**: session | **Range**: 2-60 min
- **Description**: Journaling or reflection session
- **Generates**: `daily_journaling_sessions`

### Body Composition & Performance (9 metrics)

#### Body Composition

**`weight`** - Weight Measurement  
- **Type**: measurement | **Unit**: kilogram | **Range**: 30-300 kg
- **HealthKit**: HKQuantityTypeIdentifier.bodyMass
- **Description**: Body weight measurement taken
- **Generates**: `bmi_calculated`, `protein_per_kg`

**`height_measured`** - Height Measured  
- **Type**: measurement | **Unit**: centimeter | **Range**: 100-250 cm
- **HealthKit**: HKQuantityTypeIdentifier.height
- **Description**: Height measurement taken
- **Generates**: `bmi_calculated`

**`body_fat_measured`** - Body Fat Measurement  
- **Type**: measurement | **Unit**: percent | **Range**: 5-50%
- **HealthKit**: HKQuantityTypeIdentifier.bodyFatPercentage
- **Description**: Body fat percentage measurement

**`lean_body_mass_measured`** - Lean Body Mass  
- **Type**: measurement | **Unit**: kilogram | **Range**: 20-100 kg
- **HealthKit**: HKQuantityTypeIdentifier.leanBodyMass
- **Description**: Lean body mass measurement

**`visceral_fat_measured`** - Visceral Fat  
- **Type**: measurement | **Unit**: percent | **Range**: 1-30%
- **Description**: Visceral fat percentage measurement

#### Performance Metrics

**`vo2_max_measured`** - VO2 Max Measurement  
- **Type**: measurement | **Unit**: mL/kg/min | **Range**: 15-80
- **HealthKit**: HKQuantityTypeIdentifier.vo2Max
- **Description**: VO2 Max measurement taken

**`hrv_measured`** - HRV Measurement  
- **Type**: measurement | **Unit**: millisecond | **Range**: 10-200 ms
- **HealthKit**: HKQuantityTypeIdentifier.heartRateVariabilitySDNN
- **Description**: Heart rate variability measurement

**`resting_heart_rate`** - Resting Heart Rate  
- **Type**: measurement | **Unit**: bpm | **Range**: 40-120 bpm
- **HealthKit**: HKQuantityTypeIdentifier.restingHeartRate
- **Description**: Resting heart rate measurement

**`grip_strength`** - Grip Strength  
- **Type**: measurement | **Unit**: kilogram | **Range**: 10-100 kg
- **Description**: Grip strength measurement

### Health Screening & Demographics (10 metrics)

#### Health Screening Dates

**`dental_screening_date`** - Last Dental Exam Date  
- **Type**: time_only | **Unit**: timestamp | **Max Age**: 20 years
- **Description**: Date of most recent dental cleaning/exam
- **Generates**: `months_since_dental_exam`

**`physical_exam_date`** - Last Physical Exam Date  
- **Type**: time_only | **Unit**: timestamp | **Max Age**: 20 years
- **Description**: Date of most recent annual physical examination
- **Generates**: `years_since_physical`

**`colonoscopy_date`** - Last Colonoscopy Date  
- **Type**: time_only | **Unit**: timestamp | **Max Age**: 20 years
- **Description**: Date of most recent colonoscopy screening
- **Generates**: `years_since_colonoscopy`

**`mammogram_date`** - Last Mammogram Date  
- **Type**: time_only | **Unit**: timestamp | **Max Age**: 20 years
- **Description**: Date of most recent mammogram screening
- **Generates**: `months_since_mammogram`

#### Demographics

**`birth_date`** - Date of Birth  
- **Type**: time_only | **Unit**: date | **Range**: 0-120 years
- **Description**: User's date of birth for age calculation
- **Generates**: `user_age`

**`gender`** - Gender  
- **Type**: category_select | **Values**: male/female/other/prefer_not_to_say
- **Description**: User's biological gender for health recommendations
- **Generates**: Gender-specific compliance statuses

---

**Next**: [Calculated Metrics](calculated-metrics.md) | [Units Reference](../units/) | [Back to Overview](README.md)