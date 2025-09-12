"""
Unit Conversion Service
======================

Handles conversion between user input units and standardized base units for WellPath.
Supports complex conversions like Fahrenheit->Celsius and feet+inches->centimeters.

Key Features:
- Linear conversions (cups -> mL, pounds -> kg)
- Temperature conversions with proper formulas
- Compound conversions (feet+inches -> cm)
- Scale mappings (1-10 scale -> 1-5 scale)
- Bidirectional conversion for display
"""

import pandas as pd
import re
from typing import Dict, Any, Optional, Union, Tuple
from decimal import Decimal, ROUND_HALF_UP


class UnitConversionService:
    def __init__(self, csv_path: str = "src/ref_csv_files_airtable/unit_standardization.csv"):
        """Initialize conversion service with unit standards"""
        self.units_df = pd.read_csv(csv_path)
        self.units_dict = self._build_units_lookup()
        self.base_units = self._get_base_units()
        
    def _build_units_lookup(self) -> Dict[str, Dict]:
        """Build lookup dictionary from CSV data"""
        units = {}
        for _, row in self.units_df.iterrows():
            unit_id = row['Unit Identifier']
            units[unit_id] = {
                'display_name': row['Display Name'],
                'symbol': row['Symbol'],
                'unit_type': row['Unit Type'],
                'conversion_factor': row['Conversion Factor'] if pd.notna(row['Conversion Factor']) else None,
                'is_base_unit': str(row['Is Base Unit']).lower() == 'checked',
                'healthkit_equivalent': row['HealthKit Equivalent'],
                'base_unit': row['Base Unit'],
                'special_conversion': row['Special Conversion'] if pd.notna(row['Special Conversion']) else None
            }
        return units
        
    def _get_base_units(self) -> Dict[str, str]:
        """Get mapping of unit types to their base units"""
        base_units = {}
        for unit_id, unit_info in self.units_dict.items():
            if unit_info['is_base_unit']:
                base_units[unit_info['unit_type']] = unit_id
        return base_units
        
    def convert_to_base(self, value: Union[float, str], from_unit: str) -> Dict[str, Any]:
        """
        Convert user input to base unit for storage/algorithms
        
        Args:
            value: The value to convert (number or special format like "5'10\"")
            from_unit: Source unit identifier
            
        Returns:
            Dict with conversion details and base unit value
        """
        if from_unit not in self.units_dict:
            raise ValueError(f"Unknown unit: {from_unit}")
            
        unit_info = self.units_dict[from_unit]
        special_conversion = unit_info['special_conversion']
        
        # Handle special conversions
        if special_conversion == 'temperature':
            base_value = self._convert_temperature_to_base(value, from_unit)
        elif special_conversion == 'compound_height':
            base_value = self._convert_compound_height_to_base(value, from_unit)
        elif unit_info['conversion_factor'] and from_unit != unit_info['base_unit']:
            # Standard linear conversion
            base_value = float(value) * unit_info['conversion_factor']
        else:
            # Already in base unit or no conversion needed
            base_value = float(value)
            
        # Get base unit for this unit type
        base_unit = self._get_base_unit_for_type(unit_info['unit_type'])
        
        return {
            'original_value': value,
            'original_unit': from_unit,
            'converted_value': round(base_value, 6),
            'base_unit': base_unit,
            'conversion_method': special_conversion or 'linear'
        }
        
    def convert_from_base(self, base_value: float, base_unit: str, target_unit: str) -> Dict[str, Any]:
        """
        Convert from base unit to target unit for display
        
        Args:
            base_value: Value in base unit
            base_unit: Base unit identifier  
            target_unit: Target unit for display
            
        Returns:
            Dict with display value and formatting info
        """
        if target_unit not in self.units_dict:
            raise ValueError(f"Unknown target unit: {target_unit}")
            
        target_info = self.units_dict[target_unit]
        special_conversion = target_info['special_conversion']
        
        # Handle special conversions
        if special_conversion == 'temperature':
            display_value = self._convert_temperature_from_base(base_value, base_unit, target_unit)
        elif special_conversion == 'compound_height':
            display_value = self._convert_compound_height_from_base(base_value, target_unit)
            return {
                'value': display_value,  # Will be formatted string like "5'10\""
                'unit': target_unit,
                'symbol': target_info['symbol'],
                'formatted_display': display_value
            }
        elif target_info['conversion_factor'] and target_unit != base_unit:
            # Standard linear conversion
            display_value = base_value / target_info['conversion_factor']
        else:
            # Already in target unit
            display_value = base_value
            
        return {
            'value': round(display_value, 2),
            'unit': target_unit,
            'symbol': target_info['symbol'],
            'formatted_display': f"{round(display_value, 2)} {target_info['symbol']}"
        }
        
    def _convert_temperature_to_base(self, value: float, from_unit: str) -> float:
        """Convert temperature to base unit (Celsius)"""
        if from_unit == 'fahrenheit':
            # F to C: (F - 32) × 5/9
            return (float(value) - 32) * 5/9
        elif from_unit == 'celsius':
            return float(value)
        else:
            raise ValueError(f"Unsupported temperature unit: {from_unit}")
            
    def _convert_temperature_from_base(self, celsius_value: float, base_unit: str, target_unit: str) -> float:
        """Convert temperature from base (Celsius) to target unit"""
        if target_unit == 'fahrenheit':
            # C to F: (C × 9/5) + 32
            return (celsius_value * 9/5) + 32
        elif target_unit == 'celsius':
            return celsius_value
        else:
            raise ValueError(f"Unsupported temperature unit: {target_unit}")
            
    def _convert_compound_height_to_base(self, value: str, from_unit: str) -> float:
        """
        Convert compound height (e.g., "5'10\"") to centimeters
        
        Supports formats:
        - "5'10\"" (5 feet 10 inches)
        - "5'10" (5 feet 10 inches, no quote)
        - "70" (70 inches total)
        - "5.83" (5.83 feet decimal)
        """
        if from_unit != 'feet_inches':
            raise ValueError(f"Compound height conversion only supports feet_inches, got: {from_unit}")
            
        value_str = str(value).strip()
        
        # Pattern: 5'10" or 5'10
        feet_inches_pattern = r"(\d+)'(\d+)\"?"
        match = re.match(feet_inches_pattern, value_str)
        
        if match:
            feet = int(match.group(1))
            inches = int(match.group(2))
            total_inches = (feet * 12) + inches
        else:
            try:
                # Try as decimal feet (5.83) or total inches (70)
                numeric_value = float(value_str)
                if numeric_value > 15:  # Assume inches if > 15 (no one is 15+ feet tall)
                    total_inches = numeric_value
                else:  # Assume decimal feet
                    total_inches = numeric_value * 12
            except ValueError:
                raise ValueError(f"Unable to parse height format: {value_str}")
                
        # Convert inches to centimeters (1 inch = 2.54 cm)
        return total_inches * 2.54
        
    def _convert_compound_height_from_base(self, cm_value: float, target_unit: str) -> str:
        """Convert centimeters to compound height format"""
        if target_unit != 'feet_inches':
            raise ValueError(f"Compound height display only supports feet_inches, got: {target_unit}")
            
        # Convert cm to inches
        total_inches = cm_value / 2.54
        
        # Convert to feet and inches
        feet = int(total_inches // 12)
        inches = int(total_inches % 12)
        
        return f"{feet}'{inches}\""
        
    def _get_base_unit_for_type(self, unit_type: str) -> str:
        """Get the base unit identifier for a given unit type"""
        for unit_id, unit_info in self.units_dict.items():
            if unit_info['unit_type'] == unit_type and unit_info['is_base_unit']:
                return unit_id
        raise ValueError(f"No base unit found for type: {unit_type}")
        
    def get_supported_units_for_type(self, unit_type: str) -> Dict[str, Dict]:
        """Get all supported units for a given type (for UI dropdowns)"""
        units = {}
        for unit_id, unit_info in self.units_dict.items():
            if unit_info['unit_type'] == unit_type:
                units[unit_id] = {
                    'display_name': unit_info['display_name'],
                    'symbol': unit_info['symbol'],
                    'is_base': unit_info['is_base_unit']
                }
        return units
        
    def validate_unit_compatibility(self, unit1: str, unit2: str) -> bool:
        """Check if two units are of the same type and can be converted"""
        if unit1 not in self.units_dict or unit2 not in self.units_dict:
            return False
        return self.units_dict[unit1]['unit_type'] == self.units_dict[unit2]['unit_type']


# Example usage and testing
if __name__ == "__main__":
    converter = UnitConversionService()
    
    # Test volume conversion
    water_conversion = converter.convert_to_base(8, 'cup')
    print(f"8 cups -> {water_conversion}")
    
    display_back = converter.convert_from_base(
        water_conversion['converted_value'], 
        water_conversion['base_unit'], 
        'cup'
    )
    print(f"Back to cups: {display_back}")
    
    # Test temperature conversion
    temp_conversion = converter.convert_to_base(98.6, 'fahrenheit')
    print(f"98.6°F -> {temp_conversion}")
    
    # Test compound height conversion
    height_conversion = converter.convert_to_base("5'10\"", 'feet_inches')
    print(f"5'10\" -> {height_conversion}")
    
    height_display = converter.convert_from_base(
        height_conversion['converted_value'],
        height_conversion['base_unit'],
        'feet_inches'
    )
    print(f"Back to feet/inches: {height_display}")