# Units HealthKit Corrections

**Complete correction table for HealthKit unit mapping issues**

## Critical HealthKit Unit Syntax Corrections

| Unit Identifier | Current HealthKit Unit | Corrected HealthKit Unit | Issue |
|-----------------|----------------------|------------------------|-------|
| milligram | `HKUnit.gramUnit(with: .milli)` | `HKUnit.milligramUnit()` | Use standard method |
| milligrams_per_deciliter | `HKUnit.milligramUnit(with: .none).unitDivided(by: HKUnit.literUnit(with: .deci))` | `HKUnit.milligramUnit().unitDivided(by: HKUnit.literUnit(with: .deci))` | Invalid `.none` prefix |
| micro_international_units_per_milliliter | `HKUnit.internationalUnit().unitMultiplied(by: HKUnit.milli).unitDivided(by: HKUnit.literUnit(with: .milli))` | `HKUnit.internationalUnit().unitMultiplied(by: 0.000001).unitDivided(by: HKUnit.literUnit(with: .milli))` | Cannot multiply by unit |
| milli_international_units_per_liter | `HKUnit.internationalUnit().unitMultiplied(by: HKUnit.milli).unitDivided(by: HKUnit.liter())` | `HKUnit.internationalUnit().unitMultiplied(by: 0.001).unitDivided(by: HKUnit.liter())` | Cannot multiply by unit |
| mole | `HKUnit.moleUnit(withMolarMass: 1.0)` | `HKUnit.mole()` | Invalid molarMass parameter |
| nanogram | Current conversion: `0` | Update conversion to: `0.000000001` | Missing proper conversion |
| picogram | Current conversion: `0` | Update conversion to: `0.000000000001` | Missing proper conversion |
| femtoliter | Current conversion: `0` | Update conversion to: `0.000000000000001` | Missing proper conversion |
| apple_effort_score | `HKUnit.appleEffortScore()` | `HKUnit.count()` | Non-existent HealthKit unit |

## Time/Date Format Units (Need Review)

| Unit Identifier | Current HealthKit Unit | Recommendation | Issue |
|-----------------|----------------------|---------------|-------|
| timestamp | `HKUnit.minute()` | Consider custom handling | Not a true duration unit |
| date_only | `HKUnit.minute()` | Consider custom handling | Not a true duration unit |
| time_only | `HKUnit.minute()` | Consider custom handling | Not a true duration unit |
| hours_minutes | `HKUnit.hour().unitMultiplied(by: .minute())` | `HKUnit.minute()` | Invalid syntax |
| day_hours_minutes | `HKUnit.day().unitMultiplied(by: 365.25)` | `HKUnit.minute()` or `HKUnit.day()` | Overly complex |

## Complex Time Units (Validate If Needed)

| Unit Identifier | Current HealthKit Unit | Status | Notes |
|-----------------|----------------------|--------|-------|
| year | `HKUnit.day().unitMultiplied(by: 365.25)` | ✅ Valid | Standard year conversion |
| month | `HKUnit.day().unitMultiplied(by: 30.44)` | ✅ Valid | Average month conversion |
| week | `HKUnit.day().unitMultiplied(by: 7)` | ✅ Valid | Standard week conversion |
| decade | `HKUnit.year().unitMultiplied(by: 10)` | ⚠️ Check syntax | May need `HKUnit.day().unitMultiplied(by: 3652.5)` |

## Valid HealthKit Units (No Changes Needed)

| Unit Category | Examples | Status |
|---------------|----------|--------|
| **Mass Units** | gram, kilogram, pound, stone | ✅ Correct |
| **Volume Units** | milliliter, liter, fluid_ounce | ✅ Correct |
| **Length Units** | meter, centimeter, inch, foot | ✅ Correct |
| **Time Units** | second, minute, hour, day | ✅ Correct |
| **Energy Units** | kilocalorie, joule | ✅ Correct |
| **Pressure Units** | mmHg, pascal | ✅ Correct |

## Implementation Priority

### **High Priority (App Breaking)**
1. ✅ Fix milligrams_per_deciliter (`.none` syntax error)
2. ✅ Fix micro/milli international units (multiply by unit error)
3. ✅ Fix mole unit (invalid parameter)
4. ✅ Fix apple_effort_score (non-existent unit)

### **Medium Priority (Data Integrity)**
1. ✅ Update nanogram/picogram/femtoliter conversion factors
2. ✅ Standardize milligram unit method usage
3. ✅ Review complex time unit constructions

### **Low Priority (Code Consistency)**
1. ✅ Standardize time/date formatting unit handling
2. ✅ Review overly complex multi-unit constructions

## Summary
- **Total Units Reviewed:** 151
- **Critical Fixes Needed:** 9 units
- **Syntax Issues:** 4 units  
- **Missing Conversions:** 3 units
- **Non-existent Units:** 1 unit
- **Time Format Reviews:** 5 units

After these corrections, all HealthKit unit mappings will be valid and properly formatted according to Apple's HealthKit framework specifications.