# Airtable Corrections Required

## 🚨 **Critical HealthKit Mapping Errors to Fix**

The following corrections need to be made in Airtable before regenerating CSV files. These errors will cause app crashes if not fixed.

## 1. **REMOVE Invalid HealthKit Identifiers**

### ❌ **These HealthKit identifiers DO NOT EXIST:**

| Record ID | Metric | Current (INVALID) | Action |
|-----------|--------|------------------|--------|
| `rec0rSFQ8gP9rPSup` | `vegetable_serving` | `HKQuantityTypeIdentifier.dietaryVegetables` | **DELETE** - Replace with empty string |
| `recMi1W2H0fBc2kdF` | `fruit_serving` | `HKQuantityTypeIdentifier.dietaryFruit` | **DELETE** - Replace with empty string |
| `rec92qNjhMWzybyB9` | `added_sugar_consumed` | `HKQuantityTypeIdentifier.dietaryAddedSugar` | **REPLACE** with `HKQuantityTypeIdentifierDietarySugar` |
| `recWctXUxSNalVoS2` | `strength_session` | `HKQuantityTypeIdentifier.exerciseTime` | **REPLACE** with `HKQuantityTypeIdentifierAppleExerciseTime` |
| `rec1fxwQJNVEfEJnR` | `meditation_session` | `HKQuantityTypeIdentifier.mindfulSession` | **REPLACE** with `HKCategoryTypeIdentifierMindfulSession` |

## 2. **Fix HealthKit Identifier Format**

### ❌ **Wrong Format (using dots instead of proper constants):**

| Current Format | Correct Format |
|----------------|----------------|
| `HKQuantityTypeIdentifier.stepCount` | `HKQuantityTypeIdentifierStepCount` |
| `HKQuantityTypeIdentifier.bodyMass` | `HKQuantityTypeIdentifierBodyMass` |
| `HKQuantityTypeIdentifier.dietaryWater` | `HKQuantityTypeIdentifierDietaryWater` |

**ACTION**: Search and replace all `HKQuantityTypeIdentifier.` with `HKQuantityTypeIdentifier` (remove the dot)

## 3. **Add Missing Data Type Classification**

### **New Column Needed: `healthkit_data_type`**

Add a new column to specify the HealthKit data type category:

| Metric ID | Current `data_entry_type` | New `healthkit_data_type` | HealthKit Identifier |
|-----------|--------------------------|--------------------------|---------------------|
| `birth_date` | `time_only` | `characteristic` | `HKCharacteristicTypeIdentifierDateOfBirth` |
| `gender` | `category_select` | `characteristic` | `HKCharacteristicTypeIdentifierBiologicalSex` |
| `supplement_taken` | `time_only` | `category` | `` (WellPath-only) |
| `meditation_session` | `time_only` | `category` | `HKCategoryTypeIdentifierMindfulSession` |
| `strength_session` | `time_only` | `workout` | `HKWorkoutActivityTypeFunctionalStrengthTraining` |
| `step_taken` | `quantity` | `quantity` | `HKQuantityTypeIdentifierStepCount` |

## 4. **Specific Record Corrections**

### **Priority 1: Critical Errors (App will crash)**

**Record: `rec0rSFQ8gP9rPSup` (vegetable_serving)**
```
CURRENT: healthkit_equivalent = "HKQuantityTypeIdentifier.dietaryVegetables"
CORRECT: healthkit_equivalent = ""
REASON: This identifier doesn't exist in HealthKit
```

**Record: `recMi1W2H0fBc2kdF` (fruit_serving)**
```
CURRENT: healthkit_equivalent = "HKQuantityTypeIdentifier.dietaryFruit"  
CORRECT: healthkit_equivalent = ""
REASON: This identifier doesn't exist in HealthKit
```

**Record: `rec92qNjhMWzybyB9` (added_sugar_consumed)**
```
CURRENT: healthkit_equivalent = "HKQuantityTypeIdentifier.dietaryAddedSugar"
CORRECT: healthkit_equivalent = "HKQuantityTypeIdentifierDietarySugar"
REASON: HealthKit has "Sugar" not "AddedSugar"
```

### **Priority 2: Format Corrections**

**Record: `reciBtcIb0Nj7Y56B` (step_taken)**
```
CURRENT: healthkit_equivalent = "HKQuantityTypeIdentifier.stepCount"
CORRECT: healthkit_equivalent = "HKQuantityTypeIdentifierStepCount"
REASON: Remove dot notation, use constant name
```

**Record: `recunORvw3BNmaN4P` (weight)**
```
CURRENT: healthkit_equivalent = "HKQuantityTypeIdentifier.bodyMass"
CORRECT: healthkit_equivalent = "HKQuantityTypeIdentifierBodyMass"
REASON: Remove dot notation, use constant name
```

### **Priority 3: Data Type Reclassification**

**Record: `recmK2HmyndL0dhIU` (birth_date)**
```
CURRENT: data_entry_type = "time_only"
CORRECT: data_entry_type = "characteristic"
ADD: healthkit_data_type = "characteristic"
ADD: healthkit_equivalent = "HKCharacteristicTypeIdentifierDateOfBirth"
```

**Record: `recLTgr8FDPeRmjlN` (gender)**
```
CURRENT: data_entry_type = "category_select"  
CORRECT: data_entry_type = "characteristic"
ADD: healthkit_data_type = "characteristic"
ADD: healthkit_equivalent = "HKCharacteristicTypeIdentifierBiologicalSex"
```

## 5. **Systematic Corrections Needed**

### **A. Search and Replace Operations:**

1. **Remove Invalid Identifiers:**
   - Find: `HKQuantityTypeIdentifier.dietaryVegetables`
   - Replace: `` (empty string)

2. **Remove Invalid Identifiers:**
   - Find: `HKQuantityTypeIdentifier.dietaryFruit`
   - Replace: `` (empty string)

3. **Fix Format Issues:**
   - Find: `HKQuantityTypeIdentifier.`
   - Replace: `HKQuantityTypeIdentifier`

4. **Fix Exercise Time:**
   - Find: `HKQuantityTypeIdentifierexerciseTime`
   - Replace: `HKQuantityTypeIdentifierAppleExerciseTime`

### **B. Category Type Corrections:**

Change these from `time_only` to `category` type:

| Metric | Record ID | Change `data_entry_type` | Add `healthkit_data_type` |
|--------|-----------|-------------------------|--------------------------|
| `supplement_taken` | `recT4EkW33ksYbmcw` | `time_only` → `category` | `category` |
| `medication_taken` | `recFrmVxswjNmCJV9` | `time_only` → `category` | `category` |
| `peptide_taken` | `recxjUNLkHzLW8YWm` | `time_only` → `category` | `category` |
| `sleep_routine_adherence` | `receglemHR2txoSXY` | `time_only` → `category` | `category` |
| `brushing_session` | `recvjrSGy17uAf4ol` | `time_only` → `category` | `category` |
| `flossing_session` | `recFhW0g2inNLpoOp` | `time_only` → `category` | `category` |
| `meditation_session` | `rec1fxwQJNVEfEJnR` | `time_only` → `category` | `category` |

### **C. Workout Type Corrections:**

Change these to `workout` type:

| Metric | Record ID | Add `healthkit_data_type` | Add/Update `healthkit_equivalent` |
|--------|-----------|-------------------------|-----------------------------------|
| `strength_session` | `recWctXUxSNalVoS2` | `workout` | `HKWorkoutActivityTypeFunctionalStrengthTraining` |
| `hiit_session` | `recDYU7Wvc26S0Wd1` | `workout` | `HKWorkoutActivityTypeHighIntensityIntervalTraining` |
| `zone2_cardio_session` | `rec0rZ7bwDGvhJLxh` | `workout` | `HKWorkoutActivityTypeCardioTraining` |
| `walking_session` | `recRQGiZUOgoJtNIL` | `workout` | `HKWorkoutActivityTypeWalking` |

## 6. **Validation Steps**

After making changes, validate:

1. **No Invalid Identifiers:**
   ```
   Search for: "dietaryVegetables"
   Expected: 0 results
   ```

2. **No Dot Notation:**
   ```
   Search for: "HKQuantityTypeIdentifier."
   Expected: 0 results
   ```

3. **Valid Format:**
   ```
   Search for: "HKQuantityTypeIdentifierStepCount"
   Expected: Found in step_taken record
   ```

## 7. **Testing After Changes**

1. **Export Updated CSV**
2. **Run Validation Script:**
   ```python
   python validate_healthkit_identifiers.py
   ```
3. **Verify HealthKit Integration:**
   ```swift
   // Should not crash
   let stepType = HKQuantityType.quantityType(forIdentifier: .stepCount)
   ```

## 8. **Timeline**

- **Phase 1 (Critical)**: Fix invalid identifiers that cause crashes (Priority 1)
- **Phase 2 (Important)**: Fix format issues (Priority 2)  
- **Phase 3 (Enhancement)**: Add proper data type classification (Priority 3)

## ✅ **Completion Checklist**

- [ ] Remove `dietaryVegetables` identifier
- [ ] Remove `dietaryFruit` identifier  
- [ ] Fix `dietaryAddedSugar` → `dietarySugar`
- [ ] Remove all dot notation in HealthKit identifiers
- [ ] Add `healthkit_data_type` column
- [ ] Reclassify characteristic types (birth_date, gender)
- [ ] Reclassify category types (adherence metrics)
- [ ] Reclassify workout types (exercise sessions)
- [ ] Export updated CSV files
- [ ] Run validation tests
- [ ] Confirm no app crashes with HealthKit integration

**Estimated Time**: 2-3 hours for systematic corrections

**Risk Level**: HIGH - App will crash with current invalid identifiers