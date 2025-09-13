# Units Comprehensive HealthKit Corrections

**Complete correction table for all 56 units requiring HealthKit syntax fixes**

| Unit Identifier | Current HealthKit Unit | Corrected HealthKit Unit | Current Conversion | Corrected Conversion | Issue Description |
|-----------------|------------------------|--------------------------|-------------------|---------------------|-------------------|
| **milligram** | `HKUnit.gramUnit(with: .milli)` | `HKUnit.gramUnitWithMetricPrefix(.milli)` | 0.001 | 0.001 | Use official API method name |
| **milligrams_per_deciliter** | `HKUnit.milligramUnit(with: .none).unitDivided(by: HKUnit.literUnit(with: .deci))` | `HKUnit.gramUnitWithMetricPrefix(.milli).unitDividedByUnit(HKUnit.literUnitWithMetricPrefix(.deci))` | - | - | Invalid `.none` prefix and wrong method names |
| **nanograms_per_milliliter** | `HKUnit.gramUnit(with: .nano).unitDivided(by: HKUnit.literUnit(with: .milli))` | `HKUnit.gramUnitWithMetricPrefix(.nano).unitDividedByUnit(HKUnit.literUnitWithMetricPrefix(.milli))` | - | - | Use official API method names |
| **micrograms_per_deciliter** | `HKUnit.gramUnit(with: .micro).unitDivided(by: HKUnit.literUnit(with: .deci))` | `HKUnit.gramUnitWithMetricPrefix(.micro).unitDividedByUnit(HKUnit.literUnitWithMetricPrefix(.deci))` | - | - | Use official API method names |
| **milligrams_per_liter** | `HKUnit.milligramUnit().unitDivided(by: HKUnit.liter())` | `HKUnit.gramUnitWithMetricPrefix(.milli).unitDividedByUnit(HKUnit.literUnit())` | - | - | Non-existent `milligramUnit()` method |
| **micro_international_units_per_milliliter** | `HKUnit.internationalUnit().unitMultiplied(by: HKUnit.milli).unitDivided(by: HKUnit.literUnit(with: .milli))` | `HKUnit.internationalUnit().unitMultipliedByUnit(HKUnit.gramUnitWithMetricPrefix(.micro)).unitDividedByUnit(HKUnit.literUnitWithMetricPrefix(.milli))` | - | - | Wrong multiplication unit and method names |
| **nanograms_per_deciliter** | `HKUnit.gramUnit(with: .nano).unitDivided(by: HKUnit.literUnit(with: .deci))` | `HKUnit.gramUnitWithMetricPrefix(.nano).unitDividedByUnit(HKUnit.literUnitWithMetricPrefix(.deci))` | - | - | Use official API method names |
| **picograms_per_milliliter** | `HKUnit.gramUnit(with: .pico).unitDivided(by: HKUnit.literUnit(with: .milli))` | `HKUnit.gramUnitWithMetricPrefix(.pico).unitDividedByUnit(HKUnit.literUnitWithMetricPrefix(.milli))` | - | - | Use official API method names |
| **microgram** | `HKUnit.gramUnit(with: .micro)` | `HKUnit.gramUnitWithMetricPrefix(.micro)` | 0.000001 | 0.000001 | Use official API method name |
| **millimoles_per_liter** | `HKUnit.moleUnit(with: .milli).unitDivided(by: HKUnit.liter())` | `HKUnit.moleUnitWithMetricPrefix(.milli).unitDividedByUnit(HKUnit.literUnit())` | - | - | Use official API method names |
| **micromoles_per_liter** | `HKUnit.moleUnit(with: .micro).unitDivided(by: HKUnit.liter())` | `HKUnit.moleUnitWithMetricPrefix(.micro).unitDividedByUnit(HKUnit.literUnit())` | - | - | Use official API method names |
| **micrograms_per_day** | `HKUnit.gramUnit(with: .micro).unitDivided(by: HKUnit.day())` | `HKUnit.gramUnitWithMetricPrefix(.micro).unitDividedByUnit(HKUnit.day())` | - | - | Use official API method names |
| **milli_international_units_per_liter** | `HKUnit.internationalUnit().unitMultiplied(by: HKUnit.milli).unitDivided(by: HKUnit.liter())` | `HKUnit.internationalUnit().unitMultipliedByUnit(HKUnit.gramUnitWithMetricPrefix(.milli)).unitDividedByUnit(HKUnit.literUnit())` | - | - | Wrong multiplication unit and method names |
| **picograms_per_cell** | `HKUnit.gramUnit(with: .pico).unitDivided(by: HKUnit.count())` | `HKUnit.gramUnitWithMetricPrefix(.pico).unitDividedByUnit(HKUnit.count())` | - | - | Use official API method names |
| **mole** | `HKUnit.moleUnit(withMolarMass: 1.0)` | `HKUnit.moleUnitWithMolarMass(HKUnitMolarMassBloodGlucose)` | - | - | Use proper molar mass constant |
| **nanogram** | `HKUnit.gramUnit(with: .nano)` | `HKUnit.gramUnitWithMetricPrefix(.nano)` | 0 | 0.000000001 | Missing proper conversion factor |
| **picogram** | `HKUnit.gramUnit(with: .pico)` | `HKUnit.gramUnitWithMetricPrefix(.pico)` | 0 | 0.000000000001 | Missing proper conversion factor |
| **milliliter** | `HKUnit.literUnit(with: .milli)` | `HKUnit.literUnitWithMetricPrefix(.milli)` | - | - | Use official API method name |
| **kilometer** | `HKUnit.meterUnit(with: .kilo)` | `HKUnit.meterUnitWithMetricPrefix(.kilo)` | 1000 | 1000 | Use official API method name |
| **centimeter** | `HKUnit.meterUnit(with: .centi)` | `HKUnit.meterUnitWithMetricPrefix(.centi)` | 0.01 | 0.01 | Use official API method name |
| **femtoliter** | `HKUnit.literUnit(with: .femto)` | `HKUnit.literUnitWithMetricPrefix(.femto)` | 0 | 0.000000000000001 | Missing proper conversion factor |
| **milliliters_per_kilogram_per_minute** | `HKUnit.literUnit(with: .milli).unitDivided(by: HKUnit.kilogram()).unitDivided(by: HKUnit.minute())` | `HKUnit.literUnitWithMetricPrefix(.milli).unitDividedByUnit(HKUnit.kilogram()).unitDividedByUnit(HKUnit.minute())` | - | - | Use official API method name |
| **milliliters_per_minute_per_1_73_m2** | `HKUnit.literUnit(with: .milli).unitDivided(by: HKUnit.minute())` | `HKUnit.literUnitWithMetricPrefix(.milli).unitDividedByUnit(HKUnit.minute())` | - | - | Use official API method name |
| **deciliter** | `HKUnit.literUnit(with: .deci)` | `HKUnit.literUnitWithMetricPrefix(.deci)` | 0.1 | 0.1 | Use official API method name |
| **microliter** | `HKUnit.literUnit(with: .micro)` | `HKUnit.literUnitWithMetricPrefix(.micro)` | 0.000001 | 0.000001 | Use official API method name |
| **per_microliter** | `HKUnit.count().unitDivided(by: HKUnit.literUnit(with: .micro))` | `HKUnit.count().unitDividedByUnit(HKUnit.literUnitWithMetricPrefix(.micro))` | - | - | Use official API method names |
| **million_per_microliter** | `HKUnit.count().unitDivided(by: HKUnit.literUnit(with: .micro))` | `HKUnit.count().unitDividedByUnit(HKUnit.literUnitWithMetricPrefix(.micro))` | - | - | Use official API method names |
| **millimeter** | `HKUnit.meterUnit(with: .milli)` | `HKUnit.meterUnitWithMetricPrefix(.milli)` | 0.001 | 0.001 | Use official API method name |
| **microsecond** | `HKUnit.secondUnit(with: .micro)` | `HKUnit.secondUnitWithMetricPrefix(.micro)` | 0.000017 | 0.000001 | Wrong conversion factor and method name |
| **millisecond** | `HKUnit.secondUnit(with: .milli)` | `HKUnit.secondUnitWithMetricPrefix(.milli)` | 0.016667 | 0.001 | Wrong conversion factor and method name |
| **kilojoule** | `HKUnit.jouleUnit(with: .kilo)` | `HKUnit.jouleUnitWithMetricPrefix(.kilo)` | 1000 | 1000 | Use official API method name |
| **kilowatt** | `HKUnit.wattUnit(with: .kilo)` | `HKUnit.wattUnitWithMetricPrefix(.kilo)` | 1000 | 1000 | Use official API method name |
| **microsiemens** | `HKUnit.siemenUnit(with: .micro)` | `HKUnit.siemenUnitWithMetricPrefix(.micro)` | - | - | Use official API method name |
| **millivolt** | `HKUnit.voltUnit(with: .milli)` | `HKUnit.voltUnitWithMetricPrefix(.milli)` | 0.001 | 0.001 | Use official API method name |
| **kilohertz** | `HKUnit.hertzUnit(with: .kilo)` | `HKUnit.hertzUnitWithMetricPrefix(.kilo)` | 1000 | 1000 | Use official API method name |
| **kilometers_per_hour** | `HKUnit.meterUnit(with: .kilo).unitDivided(by: HKUnit.hour())` | `HKUnit.meterUnitWithMetricPrefix(.kilo).unitDividedByUnit(HKUnit.hour())` | - | - | Use official API method names |
| **apple_effort_score** | `HKUnit.appleEffortScore()` | `HKUnit.appleEffortScoreUnit()` | - | - | Non-existent method name |
| **timestamp** | `HKUnit.minute()` | `HKUnit.second()` | - | - | Time format should use seconds for precision |
| **time_start** | `HKUnit.minute()` | `HKUnit.second()` | - | - | Time format should use seconds for precision |
| **time_end** | `HKUnit.minute()` | `HKUnit.second()` | - | - | Time format should use seconds for precision |
| **date_month_day** | `HKUnit.minute()` | `HKUnit.day()` | - | - | Date format should use days |
| **date_year_month_day** | `HKUnit.minute()` | `HKUnit.day()` | - | - | Date format should use days |
| **hours_minutes** | `HKUnit.hour().unitMultiplied(by: .minute())` | `HKUnit.minute()` | - | - | Invalid syntax, should use single unit |
| **years** | `HKUnit.day().unitMultiplied(by: 365.25)` | `HKUnit.day().unitMultipliedByUnit(HKUnit(from: "year"))` | - | - | Use proper multiplication syntax |
| **months** | `HKUnit.day().unitMultiplied(by: 30.44)` | `HKUnit.day().unitMultipliedByUnit(HKUnit(from: "month"))` | - | - | Use proper multiplication syntax |
| **years_months** | `HKUnit.day()` | `HKUnit.day()` | - | - | Valid but should be consistent |
| **years_months_days** | `HKUnit.day()` | `HKUnit.day()` | - | - | Valid but should be consistent |
| **months_days** | `HKUnit.day()` | `HKUnit.day()` | - | - | Valid but should be consistent |
| **grams_per_deciliter** | `HKUnit.gram().unitDivided(by: HKUnit.literUnit(with: .deci))` | `HKUnit.gramUnit().unitDividedByUnit(HKUnit.literUnitWithMetricPrefix(.deci))` | - | - | Use official API method names |
| **kilograms_per_square_meter** | `HKUnit.kilogram().unitDivided(by: HKUnit.meter().unitRaised(toPower: 2))` | `HKUnit.kilogramUnit().unitDividedByUnit(HKUnit.meterUnit().unitRaisedToPower(2))` | - | - | Use official API method names |
| **grams_per_serving** | `HKUnit.gram().unitDivided(by: HKUnit.count())` | `HKUnit.gramUnit().unitDividedByUnit(HKUnit.count())` | - | - | Use official API method name |
| **nanomoles_per_liter** | `HKUnit.moleUnit(with: .nano).unitDivided(by: HKUnit.liter())` | `HKUnit.moleUnitWithMetricPrefix(.nano).unitDividedByUnit(HKUnit.literUnit())` | - | - | Use official API method names |
| **units_per_liter** | `HKUnit.internationalUnit().unitDivided(by: HKUnit.liter())` | `HKUnit.internationalUnit().unitDividedByUnit(HKUnit.literUnit())` | - | - | Use official API method name |
| **per_deciliter** | `HKUnit.count().unitDivided(by: HKUnit.literUnit(with: .deci))` | `HKUnit.count().unitDividedByUnit(HKUnit.literUnitWithMetricPrefix(.deci))` | - | - | Use official API method names |
| **per_milliliter** | `HKUnit.count().unitDivided(by: HKUnit.literUnit(with: .milli))` | `HKUnit.count().unitDividedByUnit(HKUnit.literUnitWithMetricPrefix(.milli))` | - | - | Use official API method names |
| **per_liter** | `HKUnit.count().unitDivided(by: HKUnit.liter())` | `HKUnit.count().unitDividedByUnit(HKUnit.literUnit())` | - | - | Use official API method name |
| **millimeters_per_hour** | `HKUnit.meterUnit(with: .milli).unitDivided(by: HKUnit.hour())` | `HKUnit.meterUnitWithMetricPrefix(.milli).unitDividedByUnit(HKUnit.hour())` | - | - | Use official API method names |
| **millimeters_per_second** | `HKUnit.meterUnit(with: .milli).unitDivided(by: HKUnit.second())` | `HKUnit.meterUnitWithMetricPrefix(.milli).unitDividedByUnit(HKUnit.second())` | - | - | Use official API method names |

## Critical Priorities

### **🚨 High Priority (Application Breaking)**
1. **milligrams_per_deciliter** - Invalid `.none` prefix causes immediate syntax error
2. **apple_effort_score** - Non-existent method name
3. **micro/milli_international_units** - Invalid unit multiplication syntax

### **⚠️ Medium Priority (Data Integrity)**
1. **Missing conversion factors** - nanogram, picogram, femtoliter (3 units)
2. **Wrong conversion factors** - microsecond, millisecond (2 units)
3. **API method inconsistencies** - All metric prefix methods (42 units)

### **📝 Low Priority (Code Consistency)**
1. **Time/date format units** - Consistent base unit usage (6 units)
2. **Complex time units** - Proper multiplication syntax (3 units)

## Count Units - Already Correct ✅

The following **95 count-based units** are already using proper HealthKit syntax and need **NO changes**:

- `serving`, `count`, `step`, `flights_climbed`, `session`, `meal`, `snack`, `cigarette`, `drink`, `episode`, `stroke`, `puff`, `food`, `sources`, `sets`, `packs`, `event`, `times` → All use `HKUnit.count()` ✅
- All scale units (1-3, 1-5, 1-10) → `HKUnit.count()` ✅  
- All categorical units (boolean, null, male, female, etc.) → `HKUnit.count()` ✅
- All compound count units like `beats_per_minute`, `per_microliter` are in the corrections table above

## Summary Statistics
- **Total Units Reviewed:** 151
- **Count Units Already Correct:** 95 (63%) ✅
- **Units Requiring Corrections:** 56 (37%)
- **Critical Syntax Errors:** 42 units
- **Missing/Wrong Conversions:** 5 units
- **Method Name Errors:** 2 units
- **Format/Type Issues:** 7 units

## Implementation Impact
After these corrections:
- ✅ **100% HealthKit API compliance** - All units will use proper Apple framework methods
- ✅ **Consistent syntax** - All metric prefix and division methods standardized  
- ✅ **Accurate conversions** - All missing conversion factors properly set
- ✅ **Future-proof** - Code will be compatible with HealthKit updates

This comprehensive correction ensures robust HealthKit integration across all 151 units in the WellPath system.