# Raw Metrics Catalog

## Overview

Raw metrics are the foundation of the WellPath system - direct measurements from devices, user input, or manual logging. These 87 metrics capture real-world health and wellness data that feeds into calculated metrics and scoring algorithms.

## Quick Reference

### By Category

| Category | Count | Examples |
|----------|-------|----------|
| **Nutrition** | 31 | water_consumed, vegetable_serving, protein_serving, calories |
| **Exercise & Movement** | 15 | strength_session, step_taken, walking_session |
| **Sleep & Recovery** | 8 | sleep_time, wake_time, sleep_routine_adherence |
| **Mental Wellness** | 12 | meditation_session, stress_level_rating, mood_rating |
| **Health Screening** | 12 | physical_exam_date, dental_screening_date, skin_check_date |
| **Body Composition & Performance** | 9 | weight, body_fat_measured, vo2_max_measured, hrv_measured |
| **Lifestyle** | 16 | screen_time_session, sunlight_exposure, social_interaction |
| **Demographics** | 2 | birth_date, gender |

## Detailed Metrics Reference

### Nutrition & Hydration (19 metrics)

#### Core Nutritional Tracking

**`water_consumed`** - Water Consumed  
- **Type**: quantity | **Unit**: milliliter | **Range**: 50-1000 mL
- **HealthKit**: HKQuantityTypeIdentifierDietaryWater
- **Description**: Amount of water consumed in each instance
- **Generates**: `daily_water_consumption`

**`vegetable_serving`** - Vegetable Serving  
- **Type**: quantity | **Unit**: serving | **Range**: 0.5-3.0 servings
- **Description**: Each serving of vegetables consumed
- **Generates**: `daily_vegetable_servings`

**`protein_serving`** - Protein Serving  
- **Type**: quantity | **Unit**: serving | **Range**: 0.5-2.0 servings  
- **HealthKit**: HKQuantityTypeIdentifierDietaryProtein
- **Description**: Each serving of protein consumed
- **Generates**: `daily_protein_servings`

**`fiber_serving`** - Fiber Serving  
- **Type**: quantity | **Unit**: serving | **Range**: 0.5-3.0 servings
- **HealthKit**: HKQuantityTypeIdentifierDietaryFiber  
- **Description**: Each serving of fiber consumed
- **Generates**: `daily_fiber_serving`

**`fruit_serving`** - Fruit Serving  
- **Type**: quantity | **Unit**: serving | **Range**: 0.5-2.0 servings
- **Description**: Each serving of fruit consumed  
- **Generates**: `daily_fruit_serving`

#### Detailed Nutritional Components

**`calories`** - Calories  
- **Type**: quantity | **Unit**: kcal | **Range**: 50-2000 kcal
- **HealthKit**: HKQuantityTypeIdentifierActiveEnergyBurned
- **Description**: Calories consumed or burned
- **Generates**: `daily_calorie_intake`

**`protein_grams`** - Protein Grams  
- **Type**: quantity | **Unit**: gram | **Range**: 1-100 g
- **HealthKit**: HKQuantityTypeIdentifierDietaryProtein
- **Description**: Grams of protein consumed
- **Generates**: `daily_protein_grams`, `protein_per_kg`

**`fiber_grams`** - Fiber Grams  
- **Type**: quantity | **Unit**: gram | **Range**: 1-50 g
- **HealthKit**: HKQuantityTypeIdentifierDietaryFiber
- **Description**: Grams of fiber consumed  
- **Generates**: `daily_fiber_grams`

**`added_sugar_consumed`** - Added Sugar Consumed  
- **Type**: quantity | **Unit**: gram | **Range**: 0-50 g
- **HealthKit**: HKQuantityTypeIdentifierDietarySugar
- **Description**: Grams of added sugar consumed in each instance
- **Generates**: `daily_added_sugar_consumed`

**`saturated_fat_consumed`** - Saturated Fat Consumed  
- **Type**: quantity | **Unit**: gram | **Range**: 0-50 g
- **HealthKit**: HKQuantityTypeIdentifierDietaryFatSaturated
- **Description**: Grams of saturated fat consumed
- **Generates**: `daily_saturated_fat`, `saturated_fat_percentage`

**`caffeine_consumed`** - Caffeine Consumed  
- **Type**: quantity | **Unit**: milligram | **Range**: 10-400 mg
- **HealthKit**: HKQuantityTypeIdentifierDietaryCaffeine
- **Description**: Milligrams of caffeine consumed in each instance
- **Generates**: `daily_caffeine_consumed`, `last_caffeine_consumption_time`

#### Additional Metrics

**`sunlight_exposure`** - Sunlight Exposure  
- **Type**: time_only | **Unit**: hours_minutes | **Range**: 0-720 min
- **HealthKit**: HKQuantityTypeIdentifierTimeInDaylight
- **Description**: Time spent in natural daylight
- **Generates**: `daily_sunlight_exposure`

**`brushing_session`** - Brushing Session  
- **Type**: time_only | **Unit**: session | **Range**: 1-10 min
- **HealthKit**: HKCategoryTypeIdentifierToothbrushingEvent
- **Description**: Tooth brushing session
- **Generates**: `daily_brushing_sessions`

**`alcoholic_drink`** - Alcoholic Drink  
- **Type**: quantity | **Unit**: drink | **Range**: Single drink
- **Description**: Alcoholic beverage consumed
- **Generates**: `daily_alcoholic_drinks`

**`cigarette`** - Cigarette  
- **Type**: quantity | **Unit**: cigarette | **Range**: Single cigarette
- **Description**: Cigarette smoked
- **Generates**: `daily_cigarettes`

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
- **Description**: Walking exercise session
- **Generates**: `daily_walking_sessions`, `walking_session_duration`

**`mobility_session`** - Mobility Session  
- **Type**: time_only | **Unit**: session | **Range**: 5-60 min
- **Description**: Individual mobility or flexibility session
- **Generates**: `daily_mobility_sessions`, `mobility_session_duration`

#### Activity Tracking

**`step_taken`** - Step Taken  
- **Type**: quantity | **Unit**: step | **Range**: Single step
- **HealthKit**: HKQuantityTypeIdentifierStepCount
- **Description**: Individual step recorded by device
- **Generates**: `daily_steps`

**`active_time`** - Active Time  
- **Type**: time_only | **Unit**: hours_minutes | **Range**: 0-720 min
- **HealthKit**: HKQuantityTypeIdentifierAppleExerciseTime
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
- **HealthKit**: HKCategoryTypeIdentifierSleepAnalysis
- **Description**: Total sleep duration in minutes
- **Generates**: `sleep_duration`, `sleep_time_consistency`

**`wake_time`** - Wake Time  
- **Type**: time_only | **Unit**: timestamp | **Range**: Wake time  
- **HealthKit**: HKCategoryTypeIdentifierSleepAnalysis
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
- **HealthKit**: HKCategoryTypeIdentifierMindfulSession
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
- **HealthKit**: HKQuantityTypeIdentifierBodyMass
- **Description**: Body weight measurement taken
- **Generates**: `bmi_calculated`, `protein_per_kg`

**`height_measured`** - Height Measured  
- **Type**: measurement | **Unit**: centimeter | **Range**: 100-250 cm
- **HealthKit**: HKQuantityTypeIdentifierHeight
- **Description**: Height measurement taken
- **Generates**: `bmi_calculated`

**`body_fat_measured`** - Body Fat Measurement  
- **Type**: measurement | **Unit**: percent | **Range**: 5-50%
- **HealthKit**: HKQuantityTypeIdentifierBodyFatPercentage
- **Description**: Body fat percentage measurement

**`lean_body_mass_measured`** - Lean Body Mass  
- **Type**: measurement | **Unit**: kilogram | **Range**: 20-100 kg
- **HealthKit**: HKQuantityTypeIdentifierLeanBodyMass
- **Description**: Lean body mass measurement

**`visceral_fat_measured`** - Visceral Fat  
- **Type**: measurement | **Unit**: percent | **Range**: 1-30%
- **Description**: Visceral fat percentage measurement

#### Performance Metrics

**`vo2_max_measured`** - VO2 Max Measurement  
- **Type**: measurement | **Unit**: mL/kg/min | **Range**: 15-80
- **HealthKit**: HKQuantityTypeIdentifierVO2Max
- **Description**: VO2 Max measurement taken

**`hrv_measured`** - HRV Measurement  
- **Type**: measurement | **Unit**: millisecond | **Range**: 10-200 ms
- **HealthKit**: HKQuantityTypeIdentifierHeartRateVariabilitySDNN
- **Description**: Heart rate variability measurement

**`resting_heart_rate`** - Resting Heart Rate  
- **Type**: measurement | **Unit**: bpm | **Range**: 40-120 bpm
- **HealthKit**: HKQuantityTypeIdentifierRestingHeartRate
- **Description**: Resting heart rate measurement

**`grip_strength`** - Grip Strength  
- **Type**: measurement | **Unit**: kilogram | **Range**: 10-100 kg
- **Description**: Grip strength measurement

#### Additional Nutrition Sources & Quality

**`caffeine_source`** - Caffeine Source  
- **Type**: category_select | **Values**: coffee/tea/energy_drink/other
- **Description**: Source of caffeine consumption
- **Generates**: `daily_caffeine_sources`

**`ultraprocessed_food`** - Ultraprocessed Food  
- **Type**: time_only | **Unit**: serving | **Range**: Single serving
- **Description**: Ultraprocessed food consumed
- **Generates**: `daily_ultraprocessed_foods`

**`fiber_source`** - Fiber Source  
- **Type**: category_select | **Values**: vegetables/fruits/grains/legumes/other
- **Description**: Source of fiber consumption
- **Generates**: `daily_fiber_sources`

**`healthy_fat_swap`** - Healthy Fat Swap  
- **Type**: time_only | **Unit**: swap | **Range**: Single swap
- **Description**: Healthy fat substitution made
- **Generates**: `daily_healthy_fat_swaps`

**`healthy_fat_usage`** - Healthy Fat Usage  
- **Type**: time_only | **Unit**: usage | **Range**: Single usage
- **Description**: Healthy fat used in cooking/eating
- **Generates**: `daily_healthy_fat_usage`

**`vegetable_source`** - Vegetable Source  
- **Type**: category_select | **Values**: fresh/frozen/canned/other
- **Description**: Source type of vegetables consumed
- **Generates**: `daily_vegetable_sources`

**`added_sugar_serving`** - Added Sugar Serving  
- **Type**: quantity | **Unit**: serving | **Range**: 0.5-5.0 servings
- **Description**: Added sugar serving consumed
- **Generates**: `daily_added_sugar_servings`

**`whole_grain_source`** - Whole Grain Source  
- **Type**: category_select | **Values**: bread/pasta/rice/cereal/other
- **Description**: Source type of whole grains consumed
- **Generates**: `daily_whole_grain_sources`

**`legume_source`** - Legume Source  
- **Type**: category_select | **Values**: beans/lentils/chickpeas/other
- **Description**: Source type of legumes consumed
- **Generates**: `daily_legume_sources`

**`fruit_source_type`** - Fruit Source Type  
- **Type**: category_select | **Values**: fresh/frozen/dried/canned/other
- **Description**: Source type of fruit consumed
- **Generates**: `daily_fruit_source_types`

**`mindful_eating_episode`** - Mindful Eating Episode  
- **Type**: time_only | **Unit**: episode | **Range**: Single episode
- **Description**: Mindful eating practice episode
- **Generates**: `daily_mindful_eating_episodes`

### Lifestyle (10 metrics)

#### Social & Environmental

**`social_interaction`** - Social Interaction  
- **Type**: time_only | **Unit**: session | **Range**: 5-480 min
- **Description**: Social interaction session
- **Generates**: `daily_social_interactions`

**`outdoor_time_session`** - Outdoor Time Session  
- **Type**: time_only | **Unit**: session | **Range**: 5-480 min
- **Description**: Time spent outdoors
- **Generates**: `daily_outdoor_time`

**`screen_time_session`** - Screen Time Session  
- **Type**: time_only | **Unit**: session | **Range**: 1-720 min
- **Description**: Screen time session
- **Generates**: `daily_screen_time`

#### Supplements & Medications

**`supplement_taken`** - Supplement Taken  
- **Type**: time_only | **Unit**: dose | **Range**: Single dose
- **Description**: Supplement dose taken
- **Generates**: `daily_supplements`

**`medication_taken`** - Medication Taken  
- **Type**: time_only | **Unit**: dose | **Range**: Single dose
- **Description**: Medication dose taken
- **Generates**: `daily_medications`

**`peptide_taken`** - Peptide Taken  
- **Type**: time_only | **Unit**: dose | **Range**: Single dose
- **Description**: Peptide dose taken
- **Generates**: `daily_peptides`

#### Personal Care

**`flossing_session`** - Flossing Session  
- **Type**: time_only | **Unit**: session | **Range**: 1-5 min
- **Description**: Dental flossing session
- **Generates**: `daily_flossing_sessions`

**`skincare_routine`** - Skincare Routine  
- **Type**: time_only | **Unit**: session | **Range**: 2-30 min
- **Description**: Skincare routine session
- **Generates**: `daily_skincare_sessions`

**`sunscreen_application`** - Sunscreen Application  
- **Type**: time_only | **Unit**: application | **Range**: Single application
- **Description**: Sunscreen application
- **Generates**: `daily_sunscreen_applications`

### Health Screening & Demographics (14 metrics)

#### Health Screening Dates

**`skin_check_date`** - Last Skin Check Date  
- **Type**: time_only | **Unit**: timestamp | **Max Age**: 20 years
- **Description**: Date of most recent dermatology screening
- **Generates**: `years_since_skin_check`

**`vision_check_date`** - Last Vision Check Date  
- **Type**: time_only | **Unit**: timestamp | **Max Age**: 20 years
- **Description**: Date of most recent vision examination
- **Generates**: `years_since_vision_check`

**`hpv_pap_date`** - Last HPV/Pap Date  
- **Type**: time_only | **Unit**: timestamp | **Max Age**: 20 years
- **Description**: Date of most recent HPV/Pap screening
- **Generates**: `years_since_hpv_pap`

**`psa_date`** - Last PSA Date  
- **Type**: time_only | **Unit**: timestamp | **Max Age**: 20 years
- **Description**: Date of most recent PSA screening
- **Generates**: `years_since_psa`

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
- **HealthKit**: HKCharacteristicTypeIdentifierDateOfBirth
- **Description**: User's date of birth for age calculation
- **Generates**: `user_age`

**`gender`** - Gender  
- **Type**: category_select | **Values**: male/female/other/prefer_not_to_say
- **HealthKit**: HKCharacteristicTypeIdentifierBiologicalSex
- **Description**: User's biological gender for health recommendations
- **Generates**: Gender-specific compliance statuses

---

**Next**: [Calculated Metrics](calculated-metrics.md) | [Units Reference](../units/) | [Back to Overview](README.md)