"""
Enhanced Recommendation Engine with Unit Conversion Support
==========================================================

This module extends the existing recommendation engine to handle flexible unit input
and automatic conversion to standardized base units for algorithm processing.

Key Features:
- Automatic unit conversion using UnitConversionService
- Backwards compatible with existing recommendation configs
- Supports complex conversions (temperature, compound height)
- Maintains audit trail of conversions
- User preference management for display units
"""

import json
import pandas as pd
from typing import Dict, Any, List, Optional, Union, Tuple
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
import logging

from .unit_conversion_service import UnitConversionService


class RecommendationEngineWithUnits:
    """Enhanced recommendation engine with unit conversion capabilities"""
    
    def __init__(self, config_dir: str = "src/generated_configs/"):
        """
        Initialize the recommendation engine with unit conversion
        
        Args:
            config_dir: Directory containing recommendation config JSON files
        """
        self.config_dir = config_dir
        self.unit_converter = UnitConversionService()
        self.configs = self._load_recommendation_configs()
        self.logger = logging.getLogger(__name__)
        
    def _load_recommendation_configs(self) -> Dict[str, Dict]:
        """Load and parse recommendation configuration files"""
        configs = {}
        import os
        import glob
        
        for config_file in glob.glob(os.path.join(self.config_dir, "*.json")):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    rec_id = config['metadata']['recommendation_id']
                    configs[rec_id] = config
            except Exception as e:
                self.logger.error(f"Failed to load config {config_file}: {e}")
                
        return configs
        
    def process_user_input(
        self, 
        user_id: str, 
        metric_id: str, 
        value: Union[float, str], 
        input_unit: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process user input with automatic unit conversion
        
        Args:
            user_id: User identifier
            metric_id: Metric being tracked (e.g., 'dietary_water')
            value: User's input value (can be numeric or special format like "5'10\"")
            input_unit: Unit of the input value
            session_id: Session identifier for audit trail
            
        Returns:
            Dict containing processed data and conversion details
        """
        try:
            # Convert to base unit for algorithm processing
            conversion_result = self.unit_converter.convert_to_base(value, input_unit)
            
            # Find matching recommendation configs for this metric
            matching_configs = self._find_configs_for_metric(metric_id)
            
            # Process scores for each matching configuration
            scores = {}
            for config_id, config in matching_configs.items():
                score_result = self._calculate_score_with_conversion(
                    config, 
                    conversion_result['converted_value'],
                    conversion_result['base_unit']
                )
                scores[config_id] = score_result
                
            # Prepare result
            result = {
                'user_id': user_id,
                'metric_id': metric_id,
                'conversion': conversion_result,
                'scores': scores,
                'processed_at': datetime.now().isoformat(),
                'session_id': session_id
            }
            
            # Log conversion for audit
            self._log_conversion_audit(result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing user input: {e}")
            raise
            
    def _find_configs_for_metric(self, metric_id: str) -> Dict[str, Dict]:
        """Find all recommendation configs that track the given metric"""
        matching_configs = {}
        
        for config_id, config in self.configs.items():
            try:
                tracked_metrics = config['configuration_json']['schema']['tracked_metrics']
                if metric_id in tracked_metrics:
                    matching_configs[config_id] = config
            except KeyError:
                continue
                
        return matching_configs
        
    def _calculate_score_with_conversion(
        self, 
        config: Dict, 
        base_value: float, 
        base_unit: str
    ) -> Dict[str, Any]:
        """
        Calculate recommendation score using base unit values
        
        Args:
            config: Recommendation configuration
            base_value: Value in base unit
            base_unit: Base unit identifier
            
        Returns:
            Dict with score calculation results
        """
        schema = config['configuration_json']['schema']
        method = config['configuration_json']['method']
        
        # Validate that config expects this base unit
        expected_base_unit = schema.get('base_unit', schema.get('unit'))  # backwards compatibility
        if expected_base_unit != base_unit:
            raise ValueError(f"Unit mismatch: config expects {expected_base_unit}, got {base_unit}")
            
        # Apply the appropriate scoring algorithm
        if method == 'proportional':
            if schema.get('evaluation_pattern') == 'weekly_frequency':
                score = self._calculate_proportional_frequency_score(schema, base_value)
            elif schema.get('evaluation_pattern') == 'daily_achievement':
                score = self._calculate_proportional_daily_score(schema, base_value)
            else:
                score = self._calculate_basic_proportional_score(schema, base_value)
        elif method == 'binary_threshold':
            score = self._calculate_binary_threshold_score(schema, base_value)
        elif method == 'binary' and schema.get('evaluation_pattern') == 'weekly_frequency':
            score = self._calculate_binary_frequency_score(schema, base_value)
        elif method == 'minimum_frequency':
            score = self._calculate_minimum_frequency_score(schema, base_value)
        elif method == 'weekly_elimination':
            score = self._calculate_weekly_elimination_score(schema, base_value)
        else:
            raise ValueError(f"Unsupported scoring method: {method}")
            
        return {
            'score': score,
            'base_value': base_value,
            'base_unit': base_unit,
            'method': method,
            'config_id': config['config_id']
        }
        
    def _calculate_proportional_frequency_score(self, schema: Dict, value: float) -> float:
        """Calculate score for proportional frequency patterns"""
        threshold = schema['daily_threshold']
        required_days = schema['required_days']
        
        # For individual day assessment, assume this represents one day meeting threshold
        if value >= threshold:
            days_meeting = 1
        else:
            days_meeting = 0
            
        # Proportional scoring: (days_meeting / required_days) * 100
        score = min(100, (days_meeting / required_days) * 100)
        return round(score, 2)
        
    def _calculate_proportional_daily_score(self, schema: Dict, value: float) -> float:
        """Calculate score for proportional daily achievement"""
        target = schema['daily_target']
        
        # Proportional to target: (actual / target) * 100, capped at 100
        score = min(100, (value / target) * 100)
        return round(score, 2)
        
    def _calculate_binary_threshold_score(self, schema: Dict, value: float) -> float:
        """Calculate score for binary threshold patterns"""
        threshold = schema['threshold']
        success_value = schema.get('success_value', 100)
        failure_value = schema.get('failure_value', 0)
        
        if value >= threshold:
            return float(success_value)
        else:
            return float(failure_value)
            
    def _calculate_binary_frequency_score(self, schema: Dict, value: float) -> float:
        """Calculate score for binary frequency patterns"""
        threshold = schema['daily_threshold']
        
        # For binary frequency, if daily threshold is met, assume success for that pattern
        if value >= threshold:
            return 100.0
        else:
            return 20.0  # Standard "failure" score for binary patterns
            
    def _calculate_basic_proportional_score(self, schema: Dict, value: float) -> float:
        """Calculate basic proportional score"""
        # This would need more specific implementation based on the schema
        # For now, assume a simple percentage calculation
        max_value = schema.get('maximum_cap', 100)
        score = min(max_value, (value / max_value) * 100)
        return round(score, 2)
        
    def _calculate_minimum_frequency_score(self, schema: Dict, value: float) -> float:
        """
        Calculate SC-MINIMUM-FREQUENCY score
        
        For single day input, determine if this day meets threshold.
        Full weekly calculation would require 7 daily values.
        This is a simplified version for individual day assessment.
        """
        threshold = schema['daily_threshold']
        comparison = schema['daily_comparison']
        required_days = schema['required_days']
        
        # Check if this day meets the threshold
        day_meets_threshold = False
        if comparison == "<=":
            day_meets_threshold = value <= threshold
        elif comparison == ">=":
            day_meets_threshold = value >= threshold
        elif comparison == "==":
            day_meets_threshold = value == threshold
            
        # For single day input, we can only assess if this day would contribute
        # In real implementation, we'd need all 7 days to calculate final score
        # For now, return 100 if day meets threshold, 0 if not
        # This is a placeholder - full implementation needs weekly data
        
        if day_meets_threshold:
            # This day contributes to the weekly goal
            # Real calculation: successful_days >= required_days ? 100 : 0
            return 100.0  # Placeholder - indicates this day meets criteria
        else:
            return 0.0    # This day does not meet criteria
            
    def _calculate_weekly_elimination_score(self, schema: Dict, value: float) -> float:
        """
        Calculate SC-WEEKLY-ELIMINATION score
        
        For weekly elimination, any violation during the week = 0 for entire week.
        This method handles single day input - full weekly calculation needs all 7 days.
        """
        if schema.get('calculation_method') == 'weekly_sum_limit':
            # Weekly limit variant (e.g., ≤1 takeout meal per week)
            weekly_limit = schema['weekly_limit']
            # For single day, we can't calculate weekly sum yet
            # This is a placeholder - real implementation needs weekly aggregation
            return 100.0 if value <= weekly_limit else 0.0
            
        elif schema.get('calculation_method') == 'monthly_sum_limit':
            # Monthly limit variant
            monthly_limit = schema['monthly_limit']
            # Placeholder for monthly aggregation
            return 100.0 if value <= monthly_limit else 0.0
            
        else:
            # Daily elimination variant (most common)
            elimination_threshold = schema['elimination_threshold']
            comparison = schema['elimination_comparison']
            
            # Check if this day meets elimination criteria
            if comparison == "==":
                day_meets_elimination = (value == elimination_threshold)
            elif comparison == "<=":
                day_meets_elimination = (value <= elimination_threshold)
            elif comparison == ">=":
                day_meets_elimination = (value >= elimination_threshold)
            else:
                day_meets_elimination = False
                
            # For weekly elimination, ALL days must meet criteria
            # Single day violation = entire week fails
            # For single day input, return 100 if meets criteria, 0 if violates
            # Real implementation needs all 7 days: any day fails = week fails
            
            return 100.0 if day_meets_elimination else 0.0
        
    def get_user_display_format(
        self, 
        user_id: str, 
        base_value: float, 
        base_unit: str, 
        metric_id: str
    ) -> Dict[str, Any]:
        """
        Convert base unit value to user's preferred display format
        
        Args:
            user_id: User identifier
            base_value: Value in base unit
            base_unit: Base unit identifier
            metric_id: Metric identifier (to determine unit type)
            
        Returns:
            Dict with display formatting information
        """
        try:
            # Get user's preferred unit for this metric type
            unit_type = self._get_unit_type_for_metric(metric_id)
            preferred_unit = self._get_user_preferred_unit(user_id, unit_type)
            
            # Convert to preferred display unit
            display_result = self.unit_converter.convert_from_base(
                base_value, base_unit, preferred_unit
            )
            
            return {
                'display_value': display_result['value'],
                'display_unit': display_result['unit'],
                'display_symbol': display_result['symbol'],
                'formatted_display': display_result['formatted_display'],
                'base_value': base_value,
                'base_unit': base_unit
            }
            
        except Exception as e:
            self.logger.error(f"Error formatting display: {e}")
            # Fall back to base unit display
            return {
                'display_value': base_value,
                'display_unit': base_unit,
                'display_symbol': base_unit,
                'formatted_display': f"{base_value} {base_unit}",
                'base_value': base_value,
                'base_unit': base_unit
            }
            
    def _get_unit_type_for_metric(self, metric_id: str) -> str:
        """Determine unit type for a metric (volume, mass, etc.)"""
        # This would typically query the metric_types_v3 table or CSV
        # For now, using common patterns
        metric_unit_mapping = {
            'dietary_water': 'volume',
            'body_weight': 'mass',
            'height': 'length',
            'daily_whole_food_meals': 'count'
        }
        
        return metric_unit_mapping.get(metric_id, 'count')
        
    def _get_user_preferred_unit(self, user_id: str, unit_type: str) -> str:
        """Get user's preferred unit for a unit type"""
        # This would typically query the user_unit_preferences table
        # For now, using defaults
        default_preferences = {
            'volume': 'cup',
            'mass': 'pound',
            'length': 'feet_inches',
            'temperature': 'fahrenheit',
            'count': 'count'
        }
        
        return default_preferences.get(unit_type, 'count')
        
    def _log_conversion_audit(self, result: Dict[str, Any]) -> None:
        """Log conversion operation for audit trail"""
        audit_entry = {
            'user_id': result['user_id'],
            'metric_id': result['metric_id'],
            'original_value': result['conversion']['original_value'],
            'original_unit': result['conversion']['original_unit'],
            'converted_value': result['conversion']['converted_value'],
            'base_unit': result['conversion']['base_unit'],
            'conversion_method': result['conversion']['conversion_method'],
            'session_id': result['session_id'],
            'timestamp': result['processed_at']
        }
        
        # This would typically insert into conversion_audit_log table
        self.logger.info(f"Conversion audit: {audit_entry}")
        
    def get_supported_units_for_metric(self, metric_id: str) -> Dict[str, Any]:
        """Get list of supported input units for a metric"""
        unit_type = self._get_unit_type_for_metric(metric_id)
        supported_units = self.unit_converter.get_supported_units_for_type(unit_type)
        
        return {
            'metric_id': metric_id,
            'unit_type': unit_type,
            'supported_units': supported_units
        }
        
    def validate_user_input(
        self, 
        value: Union[float, str], 
        input_unit: str, 
        metric_id: str
    ) -> Dict[str, Any]:
        """
        Validate user input before processing
        
        Args:
            value: Input value
            input_unit: Input unit
            metric_id: Target metric
            
        Returns:
            Validation result with success status and messages
        """
        validation_result = {
            'is_valid': True,
            'messages': [],
            'warnings': []
        }
        
        try:
            # Check if unit is supported
            unit_type = self._get_unit_type_for_metric(metric_id)
            supported_units = self.unit_converter.get_supported_units_for_type(unit_type)
            
            if input_unit not in supported_units:
                validation_result['is_valid'] = False
                validation_result['messages'].append(f"Unsupported unit '{input_unit}' for {unit_type}")
                return validation_result
                
            # Attempt conversion to validate format
            try:
                conversion = self.unit_converter.convert_to_base(value, input_unit)
                
                # Check for reasonable ranges
                base_value = conversion['converted_value']
                if base_value < 0:
                    validation_result['is_valid'] = False
                    validation_result['messages'].append("Value cannot be negative")
                elif base_value > 1000000:  # Arbitrary large number check
                    validation_result['warnings'].append("Value seems unusually large")
                    
            except ValueError as e:
                validation_result['is_valid'] = False
                validation_result['messages'].append(f"Invalid value format: {str(e)}")
                
        except Exception as e:
            validation_result['is_valid'] = False
            validation_result['messages'].append(f"Validation error: {str(e)}")
            
        return validation_result


# Example usage
if __name__ == "__main__":
    # Initialize the enhanced engine
    engine = RecommendationEngineWithUnits()
    
    # Process user input: "I drank 8 cups of water"
    result = engine.process_user_input(
        user_id="user123",
        metric_id="dietary_water", 
        value=8,
        input_unit="cup",
        session_id="session_456"
    )
    
    print("Processing Result:")
    print(json.dumps(result, indent=2, default=str))
    
    # Get display format for user
    display = engine.get_user_display_format(
        user_id="user123",
        base_value=result['conversion']['converted_value'],
        base_unit=result['conversion']['base_unit'],
        metric_id="dietary_water"
    )
    
    print("\nUser Display Format:")
    print(json.dumps(display, indent=2))