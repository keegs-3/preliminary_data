# Units System Reference

## Overview

WellPath implements a comprehensive standardized units system with 151 unit types organized into 12 categories. The system ensures consistent measurement across all health metrics and provides seamless integration with Apple HealthKit units.

## Unit Categories

```
WellPath Units System (156 units)
├── Mass Units (34 units)
│   ├── Basic Mass (kg, g, mg, µg)
│   ├── Body Composition (kg/m², g/kg)
│   └── Laboratory Values (mg/dL, ng/mL, µg/dL)
├── Volume Units (22 units)
│   ├── Liquid Measures (mL, L, cups, fl oz)
│   ├── Spatial Measures (m³, cm³)
│   └── Flow Rates (mL/kg/min, L/min)
├── Count Units (21 units)
│   ├── Basic Counting (count, steps, sessions)
│   ├── Frequency Measures (per µL, million/µL)
│   └── Health-Specific (sources, meals, drinks)
├── Time Units (15 units)
│   ├── Duration (seconds to years)
│   ├── Composite Time (H+M, Y-M-D)
│   └── Timestamps (HH:MM, MM/DD/YYYY)
├── Energy Units (8 units)
│   ├── Nutrition (kcal, kJ)
│   └── Physics (watts, joules)
├── Scale Units (12 units)
│   ├── Ratings (1-3, 1-5, 1-10)
│   ├── Categorical (boolean, gender)
│   └── Clinical (effort score, intensity)
├── Pressure Units (6 units)
│   └── Blood Pressure & Environmental
├── Speed Units (3 units)
│   └── Movement & Activity
├── Percent Units (2 units)
│   └── Ratios & Proportions
├── Measurement Units (3 units)
│   └── Environmental Sensors
├── Electrical Units (4 units)
│   └── Bioelectrical Measurements
├── Frequency Units (2 units)
│   └── Acoustic & Signal Processing
└── Temperature Units (3 units)
    └── Environmental & Body Temperature
```

## Core Unit Categories

### 1. Mass Units (29 units)

#### Basic Mass Measurements

| Unit ID | Display | Symbol | Base Unit | Conversion | HealthKit Equivalent |
|---------|---------|--------|-----------|-------------|---------------------|
| `gram` | Grams | g | - | 1.0 | HKUnit.gram() |
| `kilogram` | Kilograms | kg | gram | 1000 | HKUnit.kilogram() |
| `milligram` | Milligrams | mg | gram | 0.001 | HKUnit.gramUnitWithMetricPrefix(.milli) |
| `microgram` | Micrograms | µg | gram | 0.000001 | HKUnit.gramUnitWithMetricPrefix(.micro) |
| `pound` | Pounds | lbs | kilogram | 0.453592 | HKUnit.pound() |
| `stone` | Stone | st | kilogram | 6.35029 | HKUnit.stone() |

**Usage**: Body weight, food portions, supplement dosages, nutritional content

#### Laboratory & Clinical Mass (18 units)

| Unit ID | Display | Symbol | Description | Clinical Use | HealthKit Equivalent |
|---------|---------|--------|-------------|--------------|---------------------|
| `milligrams_per_deciliter` | mg/dL | mg/dL | Concentration measure | Blood glucose, cholesterol | HKUnit.gramUnitWithMetricPrefix(.milli).unitDividedByUnit(HKUnit.literUnitWithMetricPrefix(.deci)) |
| `nanograms_per_milliliter` | ng/mL | ng/mL | Hormone levels | Vitamin D, testosterone | HKUnit.gramUnitWithMetricPrefix(.nano).unitDividedByUnit(HKUnit.literUnitWithMetricPrefix(.milli)) |
| `micrograms_per_deciliter` | µg/dL | µg/dL | Trace elements | Iron, cortisol | HKUnit.gramUnitWithMetricPrefix(.micro).unitDividedByUnit(HKUnit.literUnitWithMetricPrefix(.deci)) |
| `picograms_per_milliliter` | pg/mL | pg/mL | Ultra-sensitive | Vitamin B12, estradiol | HKUnit.gramUnitWithMetricPrefix(.pico).unitDividedByUnit(HKUnit.literUnitWithMetricPrefix(.milli)) |
| `nanograms_per_deciliter` | ng/dL | ng/dL | Hormone measurement | Free testosterone | HKUnit.gramUnitWithMetricPrefix(.nano).unitDividedByUnit(HKUnit.literUnitWithMetricPrefix(.deci)) |
| `grams_per_deciliter` | g/dL | g/dL | Protein levels | Albumin, hemoglobin | HKUnit.gram().unitDividedByUnit(HKUnit.literUnitWithMetricPrefix(.deci)) |
| `milligrams_per_liter` | mg/L | mg/L | Inflammatory markers | C-reactive protein | HKUnit.gramUnitWithMetricPrefix(.milli).unitDividedByUnit(HKUnit.literUnit()) |
| `nanogram` | Nanograms | ng | gram | 0.000000001 | HKUnit.gramUnitWithMetricPrefix(.nano) |
| `picogram` | Picograms | pg | gram | 0.000000000001 | HKUnit.gramUnitWithMetricPrefix(.pico) |
| `micro_international_units_per_milliliter` | µIU/mL | µIU/mL | Hormone units | TSH, insulin | HKUnit.internationalUnit().unitMultipliedByUnit(HKUnit.gramUnitWithMetricPrefix(.micro)).unitDividedByUnit(HKUnit.literUnitWithMetricPrefix(.milli)) |
| `milli_international_units_per_liter` | mIU/L | mIU/L | Hormone units | LH, FSH | HKUnit.internationalUnit().unitMultipliedByUnit(HKUnit.gramUnitWithMetricPrefix(.milli)).unitDividedByUnit(HKUnit.literUnit()) |
| `mole` | Moles | mol | Molecular units | Blood glucose | HKUnit.moleUnitWithMolarMass(HKUnitMolarMassBloodGlucose) |

#### Composite Mass Units (4 units)

| Unit ID | Display | Symbol | Formula | Purpose |
|---------|---------|--------|---------|---------|
| `grams_per_kg` | g/kg | g/kg | grams ÷ kilograms | Protein per body weight |
| `kilograms_per_square_meter` | kg/m² | kg/m² | kg ÷ m² | Body Mass Index |
| `grams_per_serving` | g/serving | g/serving | grams ÷ serving | Nutritional density |

### 2. Volume Units (22 units)

#### Liquid Measurements

| Unit ID | Display | Symbol | Base Unit | Conversion | HealthKit Equivalent |
|---------|---------|--------|-----------|-------------|---------------------|
| `milliliter` | Milliliters | mL | - | 1.0 | HKUnit.literUnitWithMetricPrefix(.milli) |
| `liter` | Liters | L | milliliter | 1000 | HKUnit.liter() |
| `fluid_ounce` | Fluid Ounces | fl oz | milliliter | 29.5735 | HKUnit.fluidOunceUS() |
| `cup` | Cups | cups | milliliter | 236.588 | HKUnit.cupUS() |
| `teaspoon` | Teaspoons | tsp | milliliter | 4.92892 | HKUnit.teaspoon() |
| `tablespoon` | Tablespoons | tbsp | milliliter | 14.7868 | HKUnit.tablespoon() |

**Usage**: Hydration tracking, liquid nutrition, medication volumes

#### Spatial & Flow Measurements

| Unit ID | Display | Symbol | Description | Usage |
|---------|---------|--------|-------------|-------|
| `meter` | Meters | m | Distance measure | Height, walking distance |
| `centimeter` | Centimeters | cm | Small distances | Height measurement |
| `inch` | Inches | in | Imperial distance | Height (US users) |
| `foot` | Feet | ft | Imperial distance | Height display |
| `milliliters_per_kilogram_per_minute` | mL/kg/min | mL/kg/min | Oxygen uptake | VO2 Max measurement |
| `femtoliter` | Femtoliters | fL | milliliter | 0.000000000000001 | HKUnit.literUnitWithMetricPrefix(.femto) |

### 3. Count Units (21 units)

#### Basic Counting

| Unit ID | Display | Symbol | HealthKit Equivalent | Usage |
|---------|---------|--------|---------------------|-------|
| `count` | Count | count | HKUnit.count() | General counting, adherence |
| `step` | Steps | steps | HKUnit.count() | Daily step tracking |
| `session` | Sessions | session | HKUnit.count() | Exercise sessions, practices |
| `meal` | Meals | meals | HKUnit.count() | Daily meal tracking |
| `serving` | Servings | serving | HKUnit.count() | Nutritional portions |

#### Health-Specific Counts

| Unit ID | Display | Symbol | Description | Examples |
|---------|---------|--------|-------------|----------|
| `sources` | Sources | sources | Dietary diversity | Vegetable types, grain varieties |
| `drink` | Drinks | drinks | Beverage counting | Alcoholic beverages |
| `cigarette` | Cigarettes | cigarettes | Smoking tracking | Daily cigarette count |
| `episode` | Episodes | episodes | Behavior instances | Mindful eating episodes |
| `event` | Events | event | Social interactions | Meaningful conversations |

#### Physiological Counts

| Unit ID | Display | Symbol | Description | Clinical Relevance |
|---------|---------|--------|-------------|-------------------|
| `beats_per_minute` | BPM | bpm | Heart rate | Resting HR, exercise HR |
| `breaths_per_minute` | Breaths/min | breaths/min | Respiratory rate | Breathing exercises |
| `billion_per_liter` | Billion/L | ×10⁹/L | Blood cells | Complete blood count |
| `per_microliter` | per µL | /µL | Cell counts | White blood cells |
| `million_per_microliter` | Million/µL | million/µL | RBC count | Red blood cell analysis |

### 4. Time Units (15 units)

#### Basic Time Durations

| Unit ID | Display | Symbol | Base Unit | Conversion | Usage |
|---------|---------|--------|-----------|-------------|-------|
| `second` | Seconds | s | minute | 0.016667 | Precise timing |
| `minutes` | Minutes | min | second | 60 | Session durations |
| `hours` | Hours | hr | minute | 60 | Sleep, fasting windows |
| `day` | Days | days | hour | 24 | Multi-day tracking |
| `months` | Months | months | day | 30.44 | Screening intervals |
| `years` | Years | years | day | 365.25 | Age, long-term intervals |

#### Composite Time Formats

| Unit ID | Display | Symbol | Description | Usage | HealthKit Equivalent |
|---------|---------|--------|-------------|-------|---------------------|
| `hours_minutes` | Time (HH:MM) | H+M | Duration format | Sleep duration, meal timing | HKUnit.minute() |
| `timestamp` | Timestamp | DD:HH:MM | Point in time | Event timing | Custom handling (not duration) |
| `years_months_days` | Years, Months, Days | Y-M-D | Age format | Precise age calculation | Custom handling (not duration) |
| `date_year_month_day` | Date (MM/DD/YYYY) | MM/DD/YYYY | Calendar date | Birth dates, appointments | Custom handling (not duration) |

#### Specialized Time Units

| Unit ID | Display | Description | Usage | HealthKit Equivalent |
|---------|---------|-------------|-------|---------------------|
| `time_start` | Start Time | Session beginning | Exercise start times | Custom handling (timestamp) |
| `time_end` | End Time | Session completion | Exercise end times | Custom handling (timestamp) |
| `microsecond` | Microseconds | High-precision timing | HRV measurements | HKUnit.secondUnitWithMetricPrefix(.micro) |
| `millisecond` | Milliseconds | Cardiac intervals | HRV, reaction times | HKUnit.secondUnitWithMetricPrefix(.milli) |

### 5. Energy Units (8 units)

| Unit ID | Display | Symbol | Base Unit | HealthKit Equivalent | Usage |
|---------|---------|--------|-----------|---------------------|-------|
| `kilocalorie` | Calories | kcal | - | HKUnit.kilocalorie() | Daily energy intake/expenditure |
| `joule` | Joules | J | kilocalorie | 0.000239 | HKUnit.joule() | Scientific energy measurement |
| `kilojoule` | Kilojoules | kJ | joule | 1000 | HKUnit.jouleUnitWithMetricPrefix(.kilo) | International energy unit |
| `watts` | Watts | W | kilocalorie | 0.000293 | HKUnit.watt() | Power output measurement |
| `large_calorie` | Calories (Large) | Cal | kilocalorie | 1 | HKUnit.largeCalorie() | Food energy |
| `small_calorie` | Calories (Small) | cal | kilocalorie | 0.001 | HKUnit.smallCalorie() | Scientific calorie |

### 6. Scale Units (12 units)

#### Subjective Rating Scales

| Unit ID | Display | Range | Description | Usage |
|---------|---------|-------|-------------|-------|
| `scale_1_5` | Scale (1-5) | 1-5 | Five-point scale | Mood, stress, sleep quality |
| `scale_1_3` | Scale (1-3) | 1-3 | Three-point scale | Simple assessments |
| `scale_1_10` | Scale (1-10) | 1-10 | Ten-point scale | Detailed ratings |
| `percent` | Percent | 0-100% | Percentage scale | Body fat, adherence rates |

#### Categorical Scales

| Unit ID | Display | Values | Description | Usage |
|---------|---------|--------|-------------|-------|
| `boolean` | Yes/No | true/false | Binary choice | Compliance, completion |
| `male` | Male | M | Gender designation | Demographics |
| `female` | Female | F | Gender designation | Demographics |
| `categorical` | Categories | varies | Multiple choice | Food sources, activity types |

#### Clinical Scales

| Unit ID | Display | Description | HealthKit Equivalent | Usage |
|---------|---------|-------------|---------------------|-------|
| `apple_effort_score` | Apple Effort Score | Exertion rating | HKUnit.appleEffortScoreUnit() | Workout intensity |
| `intensity_category` | Intensity Level | Activity intensity | - | Exercise classification |

### 7. Specialized Categories

#### Pressure Units (6 units)
- `mmhg` - Blood pressure measurement
- `pascal` - Scientific pressure unit  
- `atmosphere` - Environmental pressure
- `inches_mercury` - Weather measurement
- `centimeter_water` - Medical pressure
- `null` - No data indicator

#### Speed Units (3 units)
- `meters_per_second` - Scientific velocity
- `miles_per_hour` - Transportation speed
- `kilometers_per_hour` - International speed

#### Environmental Units (3 each)

**Measurement**:
- `decibel` - Sound level measurement
- `lux` - Light intensity measurement  
- `diopter` - Vision correction measurement

**Electrical**:
- `microsiemens` - Conductivity measurement
- `volt` - Electrical potential
- `siemen` - Electrical conductance

**Temperature**:
- `degrees_fahrenheit` - US temperature scale
- `degrees_celsius` - International temperature
- `kelvin` - Scientific temperature

## HealthKit Integration

### Direct Mappings (98 units)

WellPath maintains full compatibility with Apple HealthKit units using the correct API method syntax:

#### Critical HealthKit Syntax Corrections Applied

The following units have been updated to use proper HealthKit API methods:

| Unit Type | Corrected Method | Previous Issue |
|-----------|------------------|----------------|
| Metric Prefix Units | `gramUnitWithMetricPrefix(.milli)` | Used deprecated `gramUnit(with:)` |
| Compound Units | `unitDividedByUnit()` | Used deprecated `unitDivided(by:)` |
| Apple Effort Score | `appleEffortScoreUnit()` | Used non-existent `appleEffortScore()` |
| International Units | `unitMultipliedByUnit()` | Used invalid `unitMultiplied(by:)` |
| Mole Units | `moleUnitWithMolarMass(HKUnitMolarMassBloodGlucose)` | Used invalid parameter |

All HealthKit unit mappings now follow Apple's official HealthKit framework specifications.

```swift
// Example HealthKit mappings (using correct API methods)
step -> HKUnit.count()
kilogram -> HKUnit.kilogram()  
milliliter -> HKUnit.literUnitWithMetricPrefix(.milli)
kilocalorie -> HKUnit.kilocalorie()
beats_per_minute -> HKUnit.count().unitDividedByUnit(HKUnit.minute())
milligram -> HKUnit.gramUnitWithMetricPrefix(.milli)
apple_effort_score -> HKUnit.appleEffortScoreUnit()
```

### WellPath Extensions (56 units)

Units that extend beyond HealthKit's scope:
- Detailed nutritional units (servings, sources)
- Behavioral tracking units (sessions, episodes)  
- Clinical assessment scales (1-5 ratings)
- Composite time formats (hours_minutes)
- Health screening intervals (months, years)

## Conversion System

### Automatic Conversions

The system automatically handles unit conversions using base units and conversion factors:

```python
# Example conversions
pounds_to_kg = weight_lbs * 0.453592
mg_to_g = dosage_mg * 0.001
hours_to_minutes = duration_hr * 60
```

### Display Units

Each unit specifies whether it's a display unit (`is_display_unit: checked`):

| Context | Preferred Units |
|---------|-----------------|
| **US Users** | pounds, inches, Fahrenheit, fl oz |
| **International** | kilograms, centimeters, Celsius, mL |
| **Clinical** | mg/dL, mmHg, bpm |
| **Fitness** | steps, sessions, minutes, kcal |

## Validation & Quality

### Range Validation
Each unit includes appropriate ranges:
```json
{
  "blood_pressure_systolic": {"range": {"min": 60, "max": 300}, "unit": "mmhg"},
  "body_weight": {"range": {"min": 30, "max": 300}, "unit": "kilogram"},
  "daily_steps": {"range": {"min": 0, "max": 100000}, "unit": "step"}
}
```

### Data Quality Scoring
Units contribute to data quality assessment:
- **Precision**: More precise units (mg vs g) score higher
- **Appropriateness**: Age-appropriate ranges for pediatric vs adult
- **Consistency**: Unit consistency across related metrics

## Implementation Guidelines

### Choosing Units

1. **HealthKit First**: Use HealthKit equivalents when available
2. **User Preference**: Respect locale and user settings  
3. **Clinical Standards**: Follow medical conventions for health metrics
4. **Precision**: Choose appropriate precision for measurement type
5. **Time Format Handling**: Use custom handling for timestamp/date units (not duration units)

### Custom Units

To add custom units:
1. Define in `units_v3.csv` with conversion factors
2. Specify HealthKit equivalent if applicable
3. Set appropriate validation ranges
4. Mark as display unit if user-facing

### Metric-Unit Pairing

Each metric specifies its allowed units:
```csv
# metric_types_v3.csv
water_consumed,quantity,milliliter,"range: 50-1000"
weight,measurement,kilogram,"range: 30000-300000"  
mood_rating,rating,scale_1_5,"values: 1,2,3,4,5"
```

---

**Next**: [Data Sources](../data-sources/) | [Compliance Rules](../compliance/) | [Back to Overview](../metric-types/)