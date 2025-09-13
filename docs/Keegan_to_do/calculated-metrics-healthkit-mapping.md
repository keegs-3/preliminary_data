# Calculated Metrics HealthKit Mapping - Complete Action List

## ADD Two New Columns to Your Calculated Metrics Airtable

**Add these columns:**
1. `healthkit_equivalent` 
2. `healthkit_data_type`

## ✅ **METRICS WITH HEALTHKIT EQUIVALENTS** (12 total)

### **Direct Nutrition Matches (6 metrics)**

| Record ID | Metric | Add `healthkit_equivalent` | Add `healthkit_data_type` |
|-----------|--------|---------------------------|--------------------------|
| `recHu8HXEQmRbKRf3` | daily_steps | HKQuantityTypeIdentifierStepCount | quantity |
| `recUCwywKgmppMKhV` | daily_water_consumption | HKQuantityTypeIdentifierDietaryWater | quantity |
| `rec8cT84Wh19MzvqU` | daily_caffeine_consumed | HKQuantityTypeIdentifierDietaryCaffeine | quantity |
| `recG5r0B2rnihsElx` | daily_added_sugar_consumed | HKQuantityTypeIdentifierDietarySugar | quantity |
| `recymReSeyd1ZawKw` | daily_fiber_grams | HKQuantityTypeIdentifierDietaryFiber | quantity |
| `recknNj3bejPa9gNc` | daily_protein_grams | HKQuantityTypeIdentifierDietaryProtein | quantity |

### **Body Composition (2 metrics)**

| Record ID | Metric | Add `healthkit_equivalent` | Add `healthkit_data_type` |
|-----------|--------|---------------------------|--------------------------|
| `rec7K3BZOSteS0STt` | daily_saturated_fat | HKQuantityTypeIdentifierDietaryFatSaturated | quantity |
| `recfu2uyTnGXRDE4u` | bmi_calculated | HKQuantityTypeIdentifierBodyMassIndex | quantity |

### **Exercise Duration (4 metrics)**

| Record ID | Metric | Add `healthkit_equivalent` | Add `healthkit_data_type` |
|-----------|--------|---------------------------|--------------------------|
| `rec5IeICLAinb5el7` | daily_strength_training_duration | HKQuantityTypeIdentifierAppleExerciseTime | quantity |
| `recTH7DLHsLEv8CHC` | daily_hiit_duration | HKQuantityTypeIdentifierAppleExerciseTime | quantity |
| `recOhfe6gLgdiVgBE` | daily_walking_duration | HKQuantityTypeIdentifierAppleExerciseTime | quantity |
| `recMKXJdq99o40g1C` | daily_active_time | HKQuantityTypeIdentifierAppleExerciseTime | quantity |

### **Substance Use (1 metric)**

| Record ID | Metric | Add `healthkit_equivalent` | Add `healthkit_data_type` |
|-----------|--------|---------------------------|--------------------------|
| `recnFPsFwhY5iwRM5` | daily_alcoholic_drinks | HKQuantityTypeIdentifierNumberOfAlcoholicBeverages | quantity |

### **Energy (1 metric)**

| Record ID | Metric | Add `healthkit_equivalent` | Add `healthkit_data_type` |
|-----------|--------|---------------------------|--------------------------|
| `recZO2jCVHI2wG1kV` | daily_calories | HKQuantityTypeIdentifierDietaryEnergyConsumed | quantity |

### **Environmental (1 metric)**

| Record ID | Metric | Add `healthkit_equivalent` | Add `healthkit_data_type` |
|-----------|--------|---------------------------|--------------------------|
| `recrfCrEg0e31v400` | daily_sunlight_exposure | HKQuantityTypeIdentifierTimeInDaylight | quantity |

## ❌ **ALL OTHER CALCULATED METRICS** (122+ metrics)

**For ALL remaining metrics, set:**

| All Other Record IDs | Add `healthkit_equivalent` | Add `healthkit_data_type` |
|---------------------|---------------------------|--------------------------|
| Every other record | (leave blank) | wellpath |

### **Examples of WellPath-Only Metrics:**

| Record ID | Metric | `healthkit_equivalent` | `healthkit_data_type` |
|-----------|--------|----------------------|----------------------|
| `recGpA90JnwA5Lwwi` | daily_meals | (blank) | wellpath |
| `reczD2kuUQSd7Ke6F` | daily_vegetable_servings | (blank) | wellpath |
| `rec4SIuNTsoKcIYwj` | weekly_fruit_source_summary | (blank) | wellpath |
| `recIT4ThuaKu4YE2j` | weekly_supplement_adherence | (blank) | wellpath |
| `reczY7QPX3FOKp74m` | months_since_dental_exam | (blank) | wellpath |
| `rec9UyPB9IH6JVY1S` | sleep_time_consistency | (blank) | wellpath |
| `recOgMyuq9svPrOWv` | saturated_fat_percentage | (blank) | wellpath |
| `recV15gLGNvPjCjXz` | daily_post_meal_activity_sessions | (blank) | wellpath |

## 🎯 **COMPLETE SUMMARY**

### **HealthKit Compatible Calculated Metrics (13 total):**
- **6 Nutrition metrics** - steps, water, caffeine, sugar, fiber, protein
- **2 Body composition** - saturated fat, BMI  
- **4 Exercise duration** - strength, HIIT, walking, active time
- **1 Substance tracking** - alcohol (daily total)
- **1 Energy tracking** - calories
- **1 Environmental** - sunlight exposure

### **WellPath Innovation Calculated Metrics (120+ total):**
- **Food diversity tracking** (vegetable sources, fruit varieties, etc.)
- **Meal pattern analysis** (timing, quality, mindful eating)
- **Adherence monitoring** (supplements, medications, routines)  
- **Health screening intervals** (dental, vision, colonoscopy timing)
- **Behavioral insights** (consistency, social interaction, stress)
- **Advanced derivations** (eating windows, post-meal activity)

## ✅ **COMPLETION CHECKLIST**

- [ ] Add `healthkit_equivalent` column to calculated metrics Airtable
- [ ] Add `healthkit_data_type` column to calculated metrics Airtable  
- [ ] Set 13 records with HealthKit identifiers and `quantity` type  
- [ ] Set 121+ records with blank HealthKit and `wellpath` type
- [ ] Export updated calculated_metrics.csv
- [ ] Verify 13 HealthKit mappings work correctly
- [ ] Confirm 121+ WellPath innovations are properly categorized

## 🚀 **VALUE PROPOSITION**

**Your calculated metrics provide:**
- **10% HealthKit compatible** (13/134 metrics) - seamless integration for basics
- **90% WellPath innovations** (121/134 metrics) - advanced insights beyond any other platform
- **Comprehensive behavior tracking** - patterns Apple Health can't capture
- **Preventive care monitoring** - proactive health management
- **Food quality analysis** - beyond just nutrients to actual food sources

**This positions WellPath as the most comprehensive health tracking platform available!**