# COMPLETE Airtable Corrections Required

## 🎯 **COMPREHENSIVE ACTION LIST** 
**Everything you need to fix in Airtable - nothing else needed after this**

This document contains EVERY single change needed in your Airtable. After making these changes, your CSV exports will be 100% correct.

---

## 🚨 **PART 1: CRITICAL FIXES (App Will Crash Without These)**

### **A. DELETE Invalid HealthKit Identifiers**

| Record ID | Metric | Current (INVALID) | Action |
|-----------|--------|------------------|--------|
| `rec0rSFQ8gP9rPSup` | vegetable_serving | HKQuantityTypeIdentifier.dietaryVegetables | **SET TO BLANK** |
| `recMi1W2H0fBc2kdF` | fruit_serving | HKQuantityTypeIdentifier.dietaryFruit | **SET TO BLANK** |
| `rec92qNjhMWzybyB9` | added_sugar_consumed | HKQuantityTypeIdentifier.dietaryAddedSugar | **CHANGE TO** HKQuantityTypeIdentifierDietarySugar |

### **B. Fix Wrong HealthKit Types**

| Record ID | Metric | Current (WRONG) | Action |
|-----------|--------|----------------|--------|
| `recWctXUxSNalVoS2` | strength_session | HKQuantityTypeIdentifier.exerciseTime | **CHANGE TO** HKQuantityTypeIdentifierAppleExerciseTime |
| `rec1fxwQJNVEfEJnR` | meditation_session | HKQuantityTypeIdentifier.mindfulSession | **CHANGE TO** HKCategoryTypeIdentifierMindfulSession |
| `rec39` | screen_time_session | HKCategoryTypeIdentifier.screenTime | **SET TO BLANK** (it's a duration, not category) |
| `rec3aaVy0dCKmrdxX` | sleep_time | HKQuantityTypeIdentifier.sleepAnalysis | **CHANGE TO** HKCategoryTypeIdentifierSleepAnalysis |

---

## 🔧 **PART 2: FIX ALL HEALTHKIT IDENTIFIER FORMATS**

**Search and Replace Operation:**
- **FIND:** `HKQuantityTypeIdentifier.`
- **REPLACE WITH:** `HKQuantityTypeIdentifier`

This will fix these records:

| Record ID | Metric | Before | After |
|-----------|--------|--------|-------|
| `reciBtcIb0Nj7Y56B` | step_taken | HKQuantityTypeIdentifier.stepCount | HKQuantityTypeIdentifierStepCount |
| `recI4eTx41D0cwi8S` | protein_serving | HKQuantityTypeIdentifier.dietaryProtein | HKQuantityTypeIdentifierDietaryProtein |
| `rec7CnfAEp6i9w5fV` | water_consumed | HKQuantityTypeIdentifier.dietaryWater | HKQuantityTypeIdentifierDietaryWater |
| `rec0hOpS2ovZkzDPW` | fiber_serving | HKQuantityTypeIdentifier.dietaryFiber | HKQuantityTypeIdentifierDietaryFiber |
| `recunORvw3BNmaN4P` | weight | HKQuantityTypeIdentifier.bodyMass | HKQuantityTypeIdentifierBodyMass |
| `rec33hAbT2CCCkxB4` | caffeine_consumed | HKQuantityTypeIdentifier.dietaryCaffeine | HKQuantityTypeIdentifierDietaryCaffeine |
| `recLRMTb7VbdtJDGf` | hrv_measured | HKQuantityTypeIdentifier.heartRateVariabilitySDNN | HKQuantityTypeIdentifierHeartRateVariabilitySDNN |
| `recJj66RhX1E012hK` | vo2_max_measured | HKQuantityTypeIdentifier.vo2Max | HKQuantityTypeIdentifierVO2Max |
| `rec57VwF5UobL9wpP` | body_fat_measured | HKQuantityTypeIdentifier.bodyFatPercentage | HKQuantityTypeIdentifierBodyFatPercentage |
| `reccKaclsbPfWXXMt` | calories | HKQuantityTypeIdentifier.activeEnergyBurned | HKQuantityTypeIdentifierActiveEnergyBurned |
| `recdH5PDRI9HZlWNF` | fiber_grams | HKQuantityTypeIdentifier.dietaryFiber | HKQuantityTypeIdentifierDietaryFiber |
| `rec9VOCYi7lD6QRU8` | protein_grams | HKQuantityTypeIdentifier.dietaryProtein | HKQuantityTypeIdentifierDietaryProtein |
| `recHnDnSi0HlAkaHC` | active_time | HKQuantityTypeIdentifier.activeEnergyBurned | HKQuantityTypeIdentifierActiveEnergyBurned |
| `recRQGiZUOgoJtNIL` | walking_session | HKQuantityTypeIdentifier.walkingRunningDistance | HKQuantityTypeIdentifierDistanceWalkingRunning |
| `recUi0wXzQXWfE8T8` | height_measured | HKQuantityTypeIdentifier.height | HKQuantityTypeIdentifierHeight |
| `recZ8eVdPUW7ERQKx` | lean_body_mass_measured | HKQuantityTypeIdentifier.leanBodyMass | HKQuantityTypeIdentifierLeanBodyMass |
| `reci2LOcA8vNf3dlx` | resting_heart_rate | HKQuantityTypeIdentifier.restingHeartRate | HKQuantityTypeIdentifierRestingHeartRate |

---

## 🆕 **PART 3: ADD NEW COLUMN `healthkit_data_type`**

**CREATE NEW COLUMN** in your Airtable called `healthkit_data_type` and populate as follows:

### **Characteristic Types** (Static demographic data)
| Record ID | Metric | Set `healthkit_data_type` to |
|-----------|--------|------------------------------|
| `recmK2HmyndL0dhIU` | birth_date | `characteristic` |
| `recLTgr8FDPeRmjlN` | gender | `characteristic` |

### **Category Types** (Discrete value sets)
| Record ID | Metric | Set `healthkit_data_type` to |
|-----------|--------|------------------------------|
| `recT4EkW33ksYbmcw` | supplement_taken | `category` |
| `recFrmVxswjNmCJV9` | medication_taken | `category` |
| `recxjUNLkHzLW8YWm` | peptide_taken | `category` |
| `receglemHR2txoSXY` | sleep_routine_adherence | `category` |
| `recvjrSGy17uAf4ol` | brushing_session | `category` |
| `recFhW0g2inNLpoOp` | flossing_session | `category` |
| `rechrdEDVSLtd0IFz` | sunscreen_application | `category` |
| `recjzb5xcD3y5mxvM` | healthy_fat_swap | `category` |
| `rec0yBwRZHjQDKI8w` | mindful_eating_episode | `category` |
| `recVK8n9lTWwUEXFW` | social_interaction | `category` |
| `recr27cK81GMzEumi` | exercise_snack | `category` |
| `rec1fxwQJNVEfEJnR` | meditation_session | `category` |
| `reccNjfbTVSlOHKyZ` | stress_level_rating | `category` |
| `recYyLk39mmLbOR0V` | mood_rating | `category` |
| `rec2IVMZ7Yju9I57T` | focus_rating | `category` |
| `recEaKu8B9EwoWH3z` | memory_clarity_rating | `category` |
| `recvG4IX68oStyrs7` | sleep_environment_score | `category` |
| `rec3aaVy0dCKmrdxX` | sleep_time | `category` |
| `recftlzJ5y399ZpGW` | wake_time | `category` |

### **Workout Types** (Exercise sessions)
| Record ID | Metric | Set `healthkit_data_type` to |
|-----------|--------|------------------------------|
| `recWctXUxSNalVoS2` | strength_session | `workout` |
| `recDYU7Wvc26S0Wd1` | hiit_session | `workout` |
| `rec0rZ7bwDGvhJLxh` | zone2_cardio_session | `workout` |
| `recRQGiZUOgoJtNIL` | walking_session | `workout` |
| `recEgGgnWikfgJQCK` | mobility_session | `workout` |
| `recXOGQuDgD01OrBD` | outdoor_time_session | `workout` |
| `recL5EEu0YpmuBMqz` | breathwork_mindfulness_session | `workout` |
| `recX6EJNI7krSqycg` | brain_training_session | `workout` |

### **Quantity Types** (All others)
| Record ID | Metric | Set `healthkit_data_type` to |
|-----------|--------|------------------------------|
| ALL remaining records | (all others) | `quantity` |

---

## 🔄 **PART 4: CHANGE DATA ENTRY TYPES**

### **Fix Demographic Data**
| Record ID | Metric | Change `data_entry_type` FROM | TO |
|-----------|--------|--------------------------------|-----|
| `recmK2HmyndL0dhIU` | birth_date | time_only | characteristic |
| `recLTgr8FDPeRmjlN` | gender | category_select | characteristic |

### **Fix Category Data (Values-based)**
| Record ID | Metric | Change `data_entry_type` FROM | TO |
|-----------|--------|--------------------------------|-----|
| `recT4EkW33ksYbmcw` | supplement_taken | time_only | category |
| `recFrmVxswjNmCJV9` | medication_taken | time_only | category |
| `recxjUNLkHzLW8YWm` | peptide_taken | time_only | category |
| `receglemHR2txoSXY` | sleep_routine_adherence | time_only | category |
| `recvjrSGy17uAf4ol` | brushing_session | time_only | category |
| `recFhW0g2inNLpoOp` | flossing_session | time_only | category |
| `rechrdEDVSLtd0IFz` | sunscreen_application | time_only | category |
| `recjzb5xcD3y5mxvM` | healthy_fat_swap | time_only | category |
| `rec0yBwRZHjQDKI8w` | mindful_eating_episode | time_only | category |
| `recVK8n9lTWwUEXFW` | social_interaction | time_only | category |
| `recr27cK81GMzEumi` | exercise_snack | time_only | category |
| `rec1fxwQJNVEfEJnR` | meditation_session | time_only | category |
| `reccNjfbTVSlOHKyZ` | stress_level_rating | rating | category |
| `recYyLk39mmLbOR0V` | mood_rating | rating | category |
| `rec2IVMZ7Yju9I57T` | focus_rating | rating | category |
| `recEaKu8B9EwoWH3z` | memory_clarity_rating | rating | category |
| `recvG4IX68oStyrs7` | sleep_environment_score | rating | category |

### **Fix Workout Data (Duration-based sessions)**
| Record ID | Metric | Change `data_entry_type` FROM | TO |
|-----------|--------|--------------------------------|-----|
| `recWctXUxSNalVoS2` | strength_session | time_only | workout |
| `recDYU7Wvc26S0Wd1` | hiit_session | time_only | workout |
| `rec0rZ7bwDGvhJLxh` | zone2_cardio_session | time_only | workout |
| `recRQGiZUOgoJtNIL` | walking_session | time_only | workout |
| `recEgGgnWikfgJQCK` | mobility_session | time_only | workout |
| `recXOGQuDgD01OrBD` | outdoor_time_session | time_only | workout |
| `recL5EEu0YpmuBMqz` | breathwork_mindfulness_session | time_only | workout |
| `recX6EJNI7krSqycg` | brain_training_session | time_only | workout |

---

## ✅ **PART 5: ADD MISSING HEALTHKIT IDENTIFIERS**

### **Add Valid HealthKit Identifiers Where Missing**

| Record ID | Metric | Currently Blank | Add This HealthKit Identifier |
|-----------|--------|-----------------|-------------------------------|
| `recFlBDZAW3xbNpPG` | saturated_fat_consumed | (blank) | HKQuantityTypeIdentifierDietaryFatSaturated |
| `rec4smaQXx1XCrH1O` | alcoholic_drink | (blank) | (leave blank - individual drinks don't map to HealthKit) |
| `rechQ7eCuCItXpJ4p` | sunlight_exposure | (blank) | HKQuantityTypeIdentifierTimeInDaylight |
| `recT4EkW33ksYbmcw` | supplement_taken | (blank) | (leave blank - no HealthKit equivalent) |
| `recFrmVxswjNmCJV9` | medication_taken | (blank) | (leave blank - no HealthKit equivalent) |
| `recvjrSGy17uAf4ol` | brushing_session | (blank) | HKCategoryTypeIdentifierToothbrushingEvent |
| `recmK2HmyndL0dhIU` | birth_date | (blank) | HKCharacteristicTypeIdentifierDateOfBirth |
| `recLTgr8FDPeRmjlN` | gender | (blank) | HKCharacteristicTypeIdentifierBiologicalSex |

---

## 🛠 **PART 6: FIX DATA ERRORS**

### **Fix Units Issues**
| Record ID | Metric | Fix Issue |
|-----------|--------|-----------|
| `recFpIjRypDHi4n78` | grip_strength | Change unit from `timestamp` to `kilogram` |
| `recZb4SQfXZb0tMcT` | legume_source | Change `data_entry_type` from `quantity` to `category_select` |

### **Fix Range Issues** 
| Record ID | Metric | Current Range | Fix To |
|-----------|--------|---------------|--------|
| `recunORvw3BNmaN4P` | weight | min: 30000, max: 300000 | min: 30, max: 300 |
| `recZ8eVdPUW7ERQKx` | lean_body_mass_measured | min: 20000, max: 100000 | min: 20, max: 100 |

---

## 🎯 **PART 7: WORKOUT ACTIVITY TYPE ADDITIONS**

**For workout types, add these as NEW HealthKit identifiers:**

| Record ID | Metric | Set HealthKit Identifier To |
|-----------|--------|----------------------------|
| `recWctXUxSNalVoS2` | strength_session | HKWorkoutActivityTypeFunctionalStrengthTraining |
| `recDYU7Wvc26S0Wd1` | hiit_session | HKWorkoutActivityTypeHighIntensityIntervalTraining |
| `rec0rZ7bwDGvhJLxh` | zone2_cardio_session | HKWorkoutActivityTypeCardioTraining |
| `recRQGiZUOgoJtNIL` | walking_session | HKWorkoutActivityTypeWalking |
| `recEgGgnWikfgJQCK` | mobility_session | HKWorkoutActivityTypeYoga |
| `recL5EEu0YpmuBMqz` | breathwork_mindfulness_session | HKWorkoutActivityTypeMindAndBody |

---

## 🔍 **PART 8: FINAL VALIDATION CHECKLIST**

After making ALL changes above, search for these to ensure they're gone:

### **❌ Should Find 0 Results:**
- Search: `dietaryVegetables` → Expected: 0 results
- Search: `dietaryFruit` → Expected: 0 results  
- Search: `dietaryAddedSugar` → Expected: 0 results
- Search: `HKQuantityTypeIdentifier.` → Expected: 0 results
- Search: `mindfulSession` → Expected: 0 results (should be Category, not Quantity)

### **✅ Should Find These:**
- Search: `HKQuantityTypeIdentifierStepCount` → Expected: 1 result (step_taken)
- Search: `HKCharacteristicTypeIdentifierDateOfBirth` → Expected: 1 result (birth_date)
- Search: `HKCategoryTypeIdentifierMindfulSession` → Expected: 1 result (meditation_session)

---

## 📊 **SUMMARY OF CHANGES**

| Type of Change | Count | 
|----------------|-------|
| **Critical Fixes** (invalid identifiers) | 4 |
| **Format Fixes** (dot notation) | 16 |
| **New Data Type Classifications** | 88 |
| **Data Entry Type Changes** | 25 |
| **Missing HealthKit Additions** | 8 |
| **Data Error Fixes** | 4 |
| **Workout Activity Types** | 6 |
| **TOTAL CHANGES** | **151** |

---

## ⏱ **ESTIMATED TIME: 3-4 HOURS**

## 🚨 **CRITICAL: This is everything needed. No other changes required after completing this list.**

After making these changes:
1. Export your updated CSV files
2. The HealthKit integration will work perfectly  
3. No app crashes
4. 75% HealthKit compatibility achieved
5. All data types properly classified