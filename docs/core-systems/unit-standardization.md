# Unit Standardization System

The WellPath unit standardization system enables flexible user input while maintaining algorithmic consistency through automatic conversion to standardized base units.

## 🎯 Overview

The unit standardization engine:
- **Accepts flexible input**: Users enter data in familiar units (cups, pounds, feet/inches)
- **Converts to base units**: Algorithms work with standardized units (mL, kg, cm)
- **Handles complex conversions**: Temperature (°F↔°C), compound measurements (feet+inches↔cm)
- **Maintains audit trails**: Full conversion history for debugging and validation
- **Supports user preferences**: Remember and apply user's preferred units

## 📊 System Architecture

### Layer Separation
```
User Input Layer    →  Conversion Layer  →  Algorithm Layer    →  Display Layer
"8 cups"           →  1893 mL           →  Score calculation  →  "8 cups (excellent!)"
"5'10\""           →  177.8 cm          →  BMI calculation   →  "5'10\" (177.8 cm)"
"98.6°F"          →  37°C              →  Fever detection   →  "98.6°F (normal)"
```

### Core Components

#### 1. Unit Conversion Service
**Location**: `src/core_systems/unit_conversion_service.py`

Handles all unit conversions with support for:
- **Linear conversions**: `cups × 236.588 = mL`
- **Temperature conversions**: `(°F - 32) × 5/9 = °C`
- **Compound conversions**: `5'10" = 177.8 cm`
- **Scale mappings**: `1-10 scale → 1-5 scale`

```python
converter = UnitConversionService()

# Standard conversion
result = converter.convert_to_base(8, 'cup')
# Returns: {'converted_value': 1893.0, 'base_unit': 'milliliter'}

# Complex conversion
height = converter.convert_to_base("5'10\"", 'feet_inches')  
# Returns: {'converted_value': 177.8, 'base_unit': 'centimeter'}

# Temperature conversion
temp = converter.convert_to_base(98.6, 'fahrenheit')
# Returns: {'converted_value': 37.0, 'base_unit': 'celsius'}
```

#### 2. Enhanced Recommendation Engine
**Location**: `src/core_systems/recommendation_engine_with_units.py`

Processes user input with automatic conversion:

```python
engine = RecommendationEngineWithUnits()

# User enters "8 cups of water"
result = engine.process_user_input(
    user_id="user123",
    metric_id="dietary_water",
    value=8,
    input_unit="cup"
)

# Algorithm processes 1893 mL
# User sees results in preferred units
```

#### 3. Database Integration
**Location**: `src/database/schema_unit_conversion.sql`

Stores both original input and converted values:

```sql
-- Metric entries with conversion support
CREATE TABLE metric_entries (
    user_id VARCHAR(50),
    metric_id VARCHAR(50),
    value DECIMAL(15,6),           -- Base unit value (algorithms use this)
    original_value DECIMAL(15,6),  -- User's original input
    original_unit VARCHAR(50),     -- Unit user entered
    base_unit VARCHAR(50),         -- Base unit for algorithms
    conversion_method VARCHAR(50)  -- Conversion type used
);

-- User preferences
CREATE TABLE user_unit_preferences (
    user_id VARCHAR(50),
    unit_type VARCHAR(50),    -- 'volume', 'mass', 'length'
    preferred_unit VARCHAR(50) -- 'cup', 'pound', 'feet_inches'
);
```

## 🔧 Configuration Updates

### New Recommendation Config Structure

Enhanced configs include unit display information:

```json
{
  "config_id": "SC-PROP-FREQ-WATER_INTAKE_8_CUPS_5_DAYS",
  "schema": {
    "tracked_metrics": ["dietary_water"],
    "daily_threshold": 1893,        // Always in base units (mL)
    "base_unit": "milliliter",      // Base unit for algorithms
    "display_units": {              // User-friendly options
      "primary": "cup",
      "alternatives": ["fluid_ounce", "liter", "glass"],
      "user_friendly_threshold": "8 cups",
      "technical_threshold": "1893 mL"
    },
    "unit_conversion": {
      "supports_conversion": true,
      "conversion_type": "linear",
      "input_validation": "positive_numeric"
    }
  }
}
```

### Unit Standardization Reference

**Source**: `src/ref_csv_files_airtable/unit_standardization.csv`

Defines all supported units and conversion factors:

| Unit | Display Name | Symbol | Type | Conversion Factor | Base Unit | Special Conversion |
|------|--------------|--------|------|-------------------|-----------|-------------------|
| `milliliter` | Milliliter | mL | volume | 1.0 | ✓ (base) | linear |
| `cup` | Cup | cup | volume | 236.588 | milliliter | linear |
| `glass` | Glass | glass | volume | 236.588 | milliliter | linear |
| `celsius` | Celsius | °C | temperature | 1.0 | ✓ (base) | linear |
| `fahrenheit` | Fahrenheit | °F | temperature | - | celsius | temperature |
| `feet_inches` | Feet+Inches | ft+in | length | - | centimeter | compound_height |

## ⚙️ Conversion Logic

### Linear Conversions
Most unit conversions use simple multiplication:

```python
def convert_linear(value, factor):
    return value * factor

# Examples:
# 8 cups × 236.588 = 1893 mL
# 150 lbs × 0.453592 = 68 kg  
```

### Temperature Conversions
Temperature requires offset and scale adjustments:

```python
def fahrenheit_to_celsius(f_temp):
    return (f_temp - 32) * 5/9

def celsius_to_fahrenheit(c_temp):
    return (c_temp * 9/5) + 32

# Examples:
# 98.6°F → (98.6 - 32) × 5/9 = 37°C
# 37°C → (37 × 9/5) + 32 = 98.6°F
```

### Compound Height Conversions
Height supports multiple input formats:

```python
# Supported formats:
"5'10\""     → 177.8 cm  (5 feet 10 inches)
"5'10"       → 177.8 cm  (no quotes)
"70"         → 177.8 cm  (total inches)
"5.83"       → 177.8 cm  (decimal feet)

def parse_feet_inches(height_str):
    if "'" in height_str:
        # Parse "5'10\"" format
        feet, inches = parse_feet_inches_format(height_str)
        total_inches = (feet * 12) + inches
    else:
        value = float(height_str)
        if value > 15:  # Assume inches
            total_inches = value
        else:          # Assume decimal feet
            total_inches = value * 12
    
    return total_inches * 2.54  # Convert to cm
```

## 🎨 User Experience

### Input Flexibility
Users can enter measurements in their preferred units:

```typescript
// Frontend unit picker
<UnitInput 
  metricType="volume"
  options={["cup", "fluid_ounce", "liter", "glass"]}
  value={8}
  unit="cup"
  onChange={(value, unit) => submitMeasurement(value, unit)}
/>
```

### Display Consistency 
The system remembers and applies user preferences:

```python
# User prefers cups for volume
user_pref = get_user_preference("user123", "volume")  # Returns "cup"

# Convert 1893 mL back to cups for display
display = converter.convert_from_base(1893, "milliliter", "cup")
# Returns: {"value": 8.0, "symbol": "cup", "formatted_display": "8.0 cup"}
```

### Validation and Feedback
Input validation provides immediate feedback:

```python
validation = engine.validate_user_input(8, "cup", "dietary_water")
# Returns:
{
  "is_valid": true,
  "messages": [],
  "warnings": []
}

# Invalid input example
validation = engine.validate_user_input(-5, "cup", "dietary_water") 
# Returns:
{
  "is_valid": false,
  "messages": ["Value cannot be negative"],
  "warnings": []
}
```

## 📋 Implementation Checklist

### Phase 1: Core Infrastructure ✅
- [x] Unit conversion service with complex conversion logic
- [x] Database schema updates for conversion support
- [x] Enhanced recommendation engine integration

### Phase 2: Configuration Updates ✅  
- [x] Update recommendation configs with unit metadata
- [x] Migration scripts for existing data
- [x] Validation and testing framework

### Phase 3: API Integration (Pending)
- [ ] Update API endpoints to handle unit conversions
- [ ] Add user preference management endpoints
- [ ] Integration with existing metric ingestion pipeline

### Phase 4: Frontend Integration (Pending)
- [ ] Unit picker components
- [ ] User preference management UI
- [ ] Display formatting with user's preferred units

### Phase 5: Testing and Rollout (Pending)
- [ ] Comprehensive unit testing
- [ ] Integration testing with real data
- [ ] Performance testing and optimization
- [ ] Gradual rollout with monitoring

## 🔍 Quality Assurance

### Conversion Accuracy Testing
```python
def test_conversion_accuracy():
    converter = UnitConversionService()
    
    # Test roundtrip conversion
    original = 8.0
    converted = converter.convert_to_base(original, 'cup')
    back_converted = converter.convert_from_base(
        converted['converted_value'], 
        converted['base_unit'], 
        'cup'
    )
    
    assert abs(back_converted['value'] - original) < 0.01
```

### Audit Trail Validation
```sql
-- Verify conversion accuracy in database
SELECT 
    original_value,
    original_unit,
    converted_value,
    base_unit,
    CASE 
        WHEN original_unit = 'cup' 
        THEN original_value * 236.588
        ELSE converted_value 
    END as expected_value,
    ABS(converted_value - expected_value) as conversion_error
FROM conversion_audit_log 
WHERE conversion_error > 0.01;
```

### Performance Monitoring
```python
# Monitor conversion performance
@monitor_performance
def convert_to_base(value, unit):
    # Conversion logic
    pass

# Track conversion frequency
conversion_metrics = {
    'total_conversions': counter,
    'conversion_types': histogram,
    'error_rate': gauge
}
```

## 📊 Database Design

### Entity Relationship
```
user_unit_preferences  →  metric_entries  ←  unit_standards
        ↓                      ↓                   ↓
   (user prefs)        (actual measurements)  (conversion rules)
```

### Key Tables

#### unit_standards
Master reference for all supported units:
```sql
CREATE TABLE unit_standards (
    unit_identifier VARCHAR(50) PRIMARY KEY,
    display_name VARCHAR(100),
    symbol VARCHAR(20),
    unit_type VARCHAR(50),           -- volume, mass, length, etc.
    conversion_factor DECIMAL(15,6), -- multiply by this to get base unit
    is_base_unit BOOLEAN,           -- is this the base unit for its type?
    special_conversion VARCHAR(50)   -- temperature, compound_height, etc.
);
```

#### metric_entries (updated)
Stores both user input and converted values:
```sql
ALTER TABLE metric_entries ADD COLUMN (
    original_value DECIMAL(15,6),   -- What user entered
    original_unit VARCHAR(50),      -- Unit user used  
    base_unit VARCHAR(50),          -- Base unit (algorithms use this)
    conversion_method VARCHAR(50)   -- How conversion was done
);
```

#### conversion_audit_log
Complete audit trail for debugging:
```sql
CREATE TABLE conversion_audit_log (
    user_id VARCHAR(50),
    metric_id VARCHAR(50), 
    original_value DECIMAL(15,6),
    original_unit VARCHAR(50),
    converted_value DECIMAL(15,6),
    base_unit VARCHAR(50),
    conversion_method VARCHAR(50),
    conversion_timestamp TIMESTAMP,
    session_id VARCHAR(100)
);
```

## 🚀 Advanced Features

### Batch Conversions
Process multiple measurements efficiently:
```python
def batch_convert(measurements):
    results = []
    for measurement in measurements:
        result = converter.convert_to_base(
            measurement['value'], 
            measurement['unit']
        )
        results.append(result)
    return results
```

### Smart Unit Detection
Automatically suggest appropriate units:
```python
def suggest_unit(value, metric_type):
    if metric_type == 'volume':
        if value < 50:
            return 'fluid_ounce'
        elif value < 20:
            return 'cup'  
        else:
            return 'liter'
    # ... other logic
```

### Conversion Caching
Cache frequent conversions for performance:
```python
@lru_cache(maxsize=10000)
def cached_convert(value, from_unit, to_unit):
    return converter.convert_to_base(value, from_unit)
```

---

**The unit standardization system provides the foundation for a flexible, user-friendly measurement experience while maintaining the precision and consistency required for accurate health algorithm processing.**