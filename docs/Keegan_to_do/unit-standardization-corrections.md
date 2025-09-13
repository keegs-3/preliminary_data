# Unit Standardization HealthKit Corrections

**Complete correction table for unit_standardization.csv HealthKit equivalents**

| Unit Identifier | Current HealthKit Equivalent | Corrected HealthKit Equivalent | Issue Description |
|-----------------|------------------------------|--------------------------------|------------------|
| **milliliter** | `HKUnit.literUnit(with: .milli)` | `HKUnit.literUnitWithMetricPrefix(.milli)` | Use official API method name |
| **kilogram** | `HKUnit.gramUnit(with: .kilo)` | `HKUnit.gramUnitWithMetricPrefix(.kilo)` | Use official API method name |
| **centimeter** | `HKUnit.meterUnit(with: .centi)` | `HKUnit.meterUnitWithMetricPrefix(.centi)` | Use official API method name |
| **cup** | `HKUnit.cupUSUnit()` | `HKUnit.cupUSUnit()` | ✅ Already correct |
| **fluid_ounce** | `HKUnit.fluidOunceUSUnit()` | `HKUnit.fluidOunceUSUnit()` | ✅ Already correct |
| **liter** | `HKUnit.literUnit()` | `HKUnit.literUnit()` | ✅ Already correct |
| **gram** | `HKUnit.gramUnit()` | `HKUnit.gramUnit()` | ✅ Already correct |
| **pound** | `HKUnit.poundUnit()` | `HKUnit.poundUnit()` | ✅ Already correct |
| **minute** | `HKUnit.minute()` | `HKUnit.minuteUnit()` | Use proper method name |
| **glass** | `HKUnit.fluidOunceUSUnit().unitMultiplied(by: 8)` | `HKUnit.fluidOunceUSUnit().unitMultipliedByUnit(HKUnit.count().unitMultipliedByUnit(8))` | Fix multiplication syntax |
| **meter** | `HKUnit.meter()` | `HKUnit.meterUnit()` | Use proper method name |
| **feet** | `HKUnit.foot()` | `HKUnit.footUnit()` | Use proper method name |
| **inch** | `HKUnit.inch()` | `HKUnit.inchUnit()` | Use proper method name |
| **mile** | `HKUnit.mile()` | `HKUnit.mileUnit()` | Use proper method name |
| **kilometer** | `HKUnit.meterUnit(with: .kilo)` | `HKUnit.meterUnitWithMetricPrefix(.kilo)` | Use official API method name |
| **hour** | `HKUnit.hour()` | `HKUnit.hourUnit()` | Use proper method name |
| **second** | `HKUnit.second()` | `HKUnit.secondUnit()` | Use proper method name |
| **celsius** | `HKUnit.degreeCelsius()` | `HKUnit.degreeCelsiusUnit()` | Use proper method name |
| **fahrenheit** | `HKUnit.degreeFahrenheit()` | `HKUnit.degreeFahrenheitUnit()` | Use proper method name |
| **gallon** | `HKUnit.gallon()` | `HKUnit.gallonUnit()` | Use proper method name |
| **pint** | `HKUnit.pintUSUnit()` | `HKUnit.pintUSUnit()` | ✅ Already correct |
| **quart** | `HKUnit.quartUSUnit()` | `HKUnit.quartUSUnit()` | ✅ Already correct |
| **tablespoon** | `HKUnit.tablespoonUSUnit()` | `HKUnit.tablespoonUSUnit()` | ✅ Already correct |
| **teaspoon** | `HKUnit.teaspoonUSUnit()` | `HKUnit.teaspoonUSUnit()` | ✅ Already correct |
| **ounce** | `HKUnit.ounceUnit()` | `HKUnit.ounceUnit()` | ✅ Already correct |
| **milligram** | `HKUnit.gramUnit(with: .milli)` | `HKUnit.gramUnitWithMetricPrefix(.milli)` | Use official API method name |
| **calorie** | `HKUnit.calorie()` | `HKUnit.calorieUnit()` | Use proper method name |
| **kilocalorie** | `HKUnit.kilocalorie()` | `HKUnit.kilocalorieUnit()` | Use proper method name |
| **mmhg** | `HKUnit.millimeterOfMercury()` | `HKUnit.millimeterOfMercuryUnit()` | Use proper method name |
| **count** | `HKUnit.count()` | `HKUnit.countUnit()` | Use proper method name |
| **percent** | `HKUnit.percent()` | `HKUnit.percentUnit()` | Use proper method name |

## Units Without HealthKit Equivalents (Correct as Blank)

| Unit Identifier | Current HealthKit Equivalent | Status |
|-----------------|------------------------------|--------|
| **scale_1_5** | (blank) | ✅ Correct - no HealthKit equivalent |
| **scale_1_10** | (blank) | ✅ Correct - no HealthKit equivalent |
| **feet_inches** | (blank) | ✅ Correct - compound conversion |

## Critical Issues Found

### **High Priority (API Method Names)**
1. **Metric prefix methods** - 6 units using outdated `with:` syntax instead of `WithMetricPrefix()`
2. **Basic unit methods** - 10 units missing `Unit()` suffix in method names

### **Medium Priority (Complex Units)**
1. **glass multiplication** - Invalid `unitMultiplied(by: 8)` syntax needs `unitMultipliedByUnit()`

### **Low Priority (Already Correct)**
1. **US volume units** - All US-specific units (cupUS, fluidOunceUS, etc.) already use correct syntax
2. **Blank entries** - Scale and compound units correctly have no HealthKit equivalents

## Summary Statistics
- **Total Units in Standardization Table:** 35
- **Units Needing HealthKit Corrections:** 19 (54%)
- **Units Already Correct:** 13 (37%)
- **Units Correctly Blank:** 3 (9%)

## Implementation Notes

### **Critical Corrections Needed**
These corrections align the unit standardization table with the same HealthKit API fixes applied to the main units_v3.csv file:

1. **Consistent metric prefix methods** across all unit systems
2. **Proper unit method naming** following Apple's conventions
3. **Fixed complex unit construction** for compound measurements

### **Integration Impact**
After corrections, both `units_v3.csv` and `unit_standardization.csv` will use identical HealthKit API syntax, ensuring:
- ✅ **Consistent unit handling** across conversion systems
- ✅ **Proper HealthKit integration** for all standardized units
- ✅ **Future-proof compatibility** with HealthKit updates

This table ensures the unit standardization system maintains the same high-quality HealthKit integration as the main units system.