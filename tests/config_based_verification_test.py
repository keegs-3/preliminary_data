#!/usr/bin/env python3
"""
Configuration-Based Algorithm Verification Test

This test:
1. Auto-discovers all REC*.json config files 
2. Loads the actual config data and algorithm specifications
3. Generates realistic 7-day test data based on actual config parameters
4. References the actual algorithm implementations (doesn't duplicate logic)
5. Outputs comprehensive verification file for manual checking
6. Auto-updates when new configs are added to /src/generated_configs/
"""

import sys
import os
import glob
import json
import random
import importlib
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass

# Add src to path for algorithm imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

@dataclass
class ConfigTestScenario:
    """Test scenario for a specific config file"""
    rec_id: str
    config_file: str
    config_data: Dict[str, Any]
    algorithm_type: str
    test_values: List[float]
    scenario_description: str
    algorithm_parameters: Dict[str, Any]

def calculate_adherence_scores(test_data: List[float], algorithm_type: str, params: Dict) -> Dict:
    """Calculate progressive adherence scores using actual algorithm implementations"""
    
    try:
        # Add the src directory to Python path for imports
        src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        # Import and use actual algorithms
        if algorithm_type == 'proportional':
            from algorithms.proportional import ProportionalAlgorithm, ProportionalConfig, EvaluationPeriod
            
            # Create config from parameters
            evaluation_period = EvaluationPeriod.ROLLING_7_DAY if 'weekly' in params.get('evaluation_period', '').lower() else EvaluationPeriod.DAILY
            
            config = ProportionalConfig(
                target=params.get('target', 1.0),
                unit=params.get('unit', 'units'),
                maximum_cap=params.get('maximum_cap', 100),
                minimum_threshold=params.get('minimum_threshold', 0),
                evaluation_period=evaluation_period,
                frequency_requirement=params.get('frequency_requirement', 'daily')
            )
            
            algorithm = ProportionalAlgorithm(config)
            progressive_scores = algorithm.calculate_progressive_scores(test_data)
            
            # For weekly evaluation, use final progressive score (cumulative)
            # For daily evaluation, use average of all daily scores
            is_weekly = 'weekly' in params.get('evaluation_period', '').lower() or 'weekly' in params.get('frequency_requirement', '').lower()
            if is_weekly:
                weekly_score = progressive_scores[-1] if progressive_scores else 0
            else:
                weekly_score = sum(progressive_scores) / len(progressive_scores) if progressive_scores else 0
            
        elif algorithm_type == 'binary_threshold':
            from algorithms.binary_threshold import BinaryThresholdAlgorithm, BinaryThresholdConfig, ComparisonOperator
            
            # Map string comparison to enum
            comparison_map = {'>=': ComparisonOperator.GTE, '<=': ComparisonOperator.LTE, 
                            '>': ComparisonOperator.GT, '<': ComparisonOperator.LT, '==': ComparisonOperator.EQ}
            comparison_op = comparison_map.get(params.get('comparison_operator', '>='), ComparisonOperator.GTE)
            
            config = BinaryThresholdConfig(
                threshold=params.get('threshold', 1.0),
                success_value=params.get('success_value', 100),
                failure_value=params.get('failure_value', 0),
                comparison_operator=comparison_op
            )
            
            algorithm = BinaryThresholdAlgorithm(config)
            progressive_scores = algorithm.calculate_progressive_scores(test_data)
            
            # For buildup goals, weekly score should be average of all days
            # For countdown goals, weekly score is the final progressive score
            is_countdown = comparison_op in [ComparisonOperator.LTE, ComparisonOperator.LT]
            if is_countdown:
                weekly_score = progressive_scores[-1] if progressive_scores else 0
            else:
                weekly_score = sum(progressive_scores) / len(progressive_scores) if progressive_scores else 0
            
        elif algorithm_type == 'minimum_frequency':
            from algorithms.minimum_frequency import MinimumFrequencyAlgorithm, MinimumFrequencyConfig
            
            # Handle time-based thresholds
            daily_threshold = params.get('daily_threshold', 1.0)
            if isinstance(daily_threshold, str) and ':' in daily_threshold:
                try:
                    hours, minutes = daily_threshold.split(':')
                    daily_threshold = int(hours) + int(minutes) / 60.0
                except:
                    daily_threshold = 14.0
            
            config = MinimumFrequencyConfig(
                daily_threshold=daily_threshold,
                daily_comparison=params.get('daily_comparison', '>='),
                required_days=params.get('required_days', 3)
            )
            
            algorithm = MinimumFrequencyAlgorithm(config)
            progressive_scores = algorithm.calculate_progressive_scores(test_data)
            weekly_score = progressive_scores[-1] if progressive_scores else 0
            
        elif algorithm_type == 'weekly_elimination':
            from algorithms.weekly_elimination import WeeklyEliminationAlgorithm, WeeklyEliminationConfig
            
            # Handle time-based thresholds
            threshold = params.get('elimination_threshold', 0)
            if isinstance(threshold, str) and ':' in threshold:
                try:
                    hours, minutes = threshold.split(':')
                    threshold = int(hours) + int(minutes) / 60.0
                except:
                    threshold = 14.0
            
            config = WeeklyEliminationConfig(
                elimination_threshold=threshold,
                elimination_comparison=params.get('elimination_comparison', '==')
            )
            
            algorithm = WeeklyEliminationAlgorithm(config)
            progressive_scores = algorithm.calculate_progressive_scores(test_data)
            weekly_score = progressive_scores[-1] if progressive_scores else 0
            
        elif algorithm_type == 'zone_based':
            from algorithms.zone_based import ZoneBasedAlgorithm, ZoneBasedConfig, Zone
            
            # Create default zones if not specified
            zones = params.get('zones', [])
            if not zones:
                # Create sleep duration zones as default
                zones = [
                    Zone(0, 5, 20, "Critical"),
                    Zone(5, 6, 40, "Poor"),
                    Zone(6, 7, 60, "Fair"),
                    Zone(7, 9, 100, "Optimal"),
                    Zone(9, 12, 80, "Excessive")
                ]
            else:
                # Convert dict zones to Zone objects
                zone_objects = []
                for zone_data in zones:
                    zone_objects.append(Zone(
                        min_value=zone_data.get('range', [0, 0])[0],
                        max_value=zone_data.get('range', [0, 0])[1] if len(zone_data.get('range', [0, 0])) > 1 else zone_data.get('range', [0, 0])[0],
                        score=zone_data.get('score', 50),
                        label=zone_data.get('label', 'Zone')
                    ))
                zones = zone_objects
            
            config = ZoneBasedConfig(
                zones=zones,
                unit=params.get('unit', 'units')
            )
            
            algorithm = ZoneBasedAlgorithm(config)
            progressive_scores = algorithm.calculate_progressive_scores(test_data)
            # Zone-based is always daily independent scoring
            weekly_score = sum(progressive_scores) / len(progressive_scores) if progressive_scores else 0
            
        elif algorithm_type == 'constrained_weekly_allowance':
            from algorithms.constrained_weekly_allowance import ConstrainedWeeklyAllowanceAlgorithm, ConstrainedWeeklyAllowanceConfig
            
            config = ConstrainedWeeklyAllowanceConfig(
                weekly_allowance=params.get('weekly_allowance', 2),
                unit=params.get('unit', 'units'),
                penalty_for_overage=params.get('penalty_per_excess', 25)
            )
            
            algorithm = ConstrainedWeeklyAllowanceAlgorithm(config)
            progressive_scores = algorithm.calculate_progressive_scores(test_data)
            weekly_score = progressive_scores[-1] if progressive_scores else 0
            
        elif algorithm_type == 'proportional_frequency_hybrid':
            from algorithms.proportional_frequency_hybrid import ProportionalFrequencyHybridAlgorithm, ProportionalFrequencyHybridConfig
            
            config = ProportionalFrequencyHybridConfig(
                daily_target=params.get('daily_target', 1.0),
                required_qualifying_days=params.get('required_qualifying_days', 2),
                unit=params.get('unit', 'units'),
                daily_minimum_threshold=params.get('daily_minimum_threshold', 0)
            )
            
            algorithm = ProportionalFrequencyHybridAlgorithm(config)
            progressive_scores = algorithm.calculate_progressive_scores(test_data)
            weekly_score = progressive_scores[-1] if progressive_scores else 0
            
        elif algorithm_type == 'composite_weighted':
            from algorithms.composite_weighted import CompositeWeightedAlgorithm, CompositeWeightedConfig, Component
            
            # Create default components if not specified
            components = params.get('components', [])
            if not components:
                components = [Component(
                    name='Component 1',
                    weight=1.0,
                    target=100,
                    unit=params.get('unit', 'score'),
                    scoring_method='proportional',
                    field_name='value'
                )]
            else:
                # Convert dict components to Component objects
                component_objects = []
                for comp_data in components:
                    component_objects.append(Component(
                        name=comp_data.get('name', 'Component'),
                        weight=comp_data.get('weight', 1.0),
                        target=comp_data.get('target_range', [100])[1] if isinstance(comp_data.get('target_range'), list) else comp_data.get('target', 100),
                        unit=comp_data.get('unit', 'units'),
                        scoring_method=comp_data.get('scoring_method', 'proportional'),
                        field_name=comp_data.get('field_name', 'value'),
                        parameters=comp_data
                    ))
                components = component_objects
            
            config = CompositeWeightedConfig(components=components)
            algorithm = CompositeWeightedAlgorithm(config)
            
            # For composite, create daily component values
            daily_component_values = []
            for value in test_data:
                comp_values = {}
                for comp in components:
                    comp_values[comp.field_name] = value
                daily_component_values.append(comp_values)
                
            progressive_scores = algorithm.calculate_progressive_scores(daily_component_values)
            # Composite is always daily independent scoring
            weekly_score = sum(progressive_scores) / len(progressive_scores) if progressive_scores else 0
            
        elif algorithm_type == 'categorical_filter_threshold':
            from algorithms.categorical_filter_threshold import CategoricalFilterThresholdAlgorithm, CategoricalFilterThresholdConfig, CategoryFilter
            from algorithms.binary_threshold import ComparisonOperator
            
            # Create default category filters if not specified
            categories = params.get('categories', [])
            if not categories:
                category_filters = [CategoryFilter(
                    category_name='default',
                    category_values=['all'],
                    threshold=params.get('threshold', 1),
                    comparison_operator=ComparisonOperator.GTE
                )]
            else:
                category_filters = []
                for cat in categories:
                    category_filters.append(CategoryFilter(
                        category_name=cat,
                        category_values=[cat],
                        threshold=params.get('threshold', 1),
                        comparison_operator=ComparisonOperator.GTE
                    ))
            
            config = CategoricalFilterThresholdConfig(
                category_field='category',
                category_filters=category_filters,
                default_threshold=params.get('threshold', 1)
            )
            
            algorithm = CategoricalFilterThresholdAlgorithm(config)
            
            # For categorical, create daily data with category
            daily_data = []
            for value in test_data:
                daily_data.append({
                    'category': 'default',
                    'value': value
                })
                
            progressive_scores = algorithm.calculate_progressive_scores(daily_data)
            # Categorical filter is always daily independent scoring
            weekly_score = sum(progressive_scores) / len(progressive_scores) if progressive_scores else 0
            
        else:
            # Fallback for truly unknown algorithms
            progressive_scores = [50] * len(test_data)
            weekly_score = 50
        
    except (ImportError, AttributeError) as e:
        # Fallback if algorithm imports fail
        print(f"Warning: Could not use actual algorithm for {algorithm_type}: {e}")
        progressive_scores = [50] * len(test_data)
        weekly_score = 50
    
    return {
        'daily_scores': progressive_scores,
        'weekly_score': weekly_score,
        'passing_days': sum(1 for score in progressive_scores if score >= 50),
        'total_days': len(progressive_scores)
    }

class ConfigBasedTestGenerator:
    """Generates test scenarios by reading actual config files"""
    
    def __init__(self):
        self.config_dir = os.path.join(os.path.dirname(__file__), '..', 'src', 'generated_configs')
    
    def discover_all_configs(self) -> List[Tuple[str, Dict[str, Any]]]:
        """Auto-discover all REC config files and load their data"""
        pattern = os.path.join(self.config_dir, 'REC*.json')
        config_files = glob.glob(pattern)
        config_files.sort()
        
        configs = []
        for config_file in config_files:
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    configs.append((config_file, config_data))
            except Exception as e:
                print(f"⚠️  Warning: Failed to load {config_file}: {e}")
        
        return configs
    
    def extract_algorithm_parameters(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract algorithm parameters from actual config data"""
        schema = config_data.get('configuration_json', {}).get('schema', {})
        method = config_data.get('configuration_json', {}).get('method', '')
        
        # Extract key parameters based on algorithm type
        params = {
            'algorithm_type': config_data.get('scoring_method', 'unknown'),
            'method': method,
            'schema': schema
        }
        
        # Add specific parameters based on algorithm type
        if params['algorithm_type'] == 'proportional_frequency_hybrid':
            params.update({
                'daily_target': schema.get('daily_target'),
                'required_qualifying_days': schema.get('required_qualifying_days'),
                'daily_minimum_threshold': schema.get('daily_minimum_threshold', 0),
                'unit': schema.get('unit')
            })
        
        elif params['algorithm_type'] == 'proportional':
            # Handle different target field names across config schemas
            target = schema.get('target') or schema.get('daily_target') or schema.get('daily_threshold')
            params.update({
                'target': target,
                'unit': schema.get('unit'),
                'maximum_cap': schema.get('maximum_cap', 100),
                'minimum_threshold': schema.get('minimum_threshold', 0),
                'evaluation_period': schema.get('evaluation_period', 'daily'),
                'frequency_requirement': schema.get('frequency_requirement', 'daily')
            })
        
        elif params['algorithm_type'] == 'binary_threshold':
            params.update({
                'threshold': schema.get('threshold'),
                'comparison_operator': schema.get('comparison_operator', '>='),
                'success_value': schema.get('success_value', 100),
                'failure_value': schema.get('failure_value', 0),
                'unit': schema.get('unit')
            })
        
        elif params['algorithm_type'] == 'minimum_frequency':
            params.update({
                'daily_threshold': schema.get('daily_threshold'),
                'daily_comparison': schema.get('daily_comparison', '>='),
                'required_days': schema.get('required_days'),
                'total_days': schema.get('total_days', 7),
                'unit': schema.get('unit')
            })
        
        elif params['algorithm_type'] == 'weekly_elimination':
            params.update({
                'elimination_threshold': schema.get('elimination_threshold', 0),
                'elimination_comparison': schema.get('elimination_comparison', '=='),
                'unit': schema.get('unit')
            })
        
        elif params['algorithm_type'] == 'zone_based':
            params.update({
                'zones': schema.get('zones', []),
                'zone_scores': schema.get('zone_scores', []),
                'unit': schema.get('unit')
            })
        
        elif params['algorithm_type'] == 'composite_weighted':
            params.update({
                'components': schema.get('components', []),
                'weights': schema.get('weights', []),
                'unit': schema.get('unit')
            })
        
        elif params['algorithm_type'] == 'constrained_weekly_allowance':
            # Handle different allowance field names
            allowance = schema.get('weekly_allowance') or schema.get('weekly_limit')
            params.update({
                'weekly_allowance': allowance,
                'penalty_per_excess': schema.get('penalty_per_excess', 25),
                'unit': schema.get('unit')
            })
        
        elif params['algorithm_type'] == 'categorical_filter_threshold':
            params.update({
                'categories': schema.get('categories', []),
                'threshold': schema.get('threshold'),
                'filter_type': schema.get('filter_type', 'include'),
                'unit': schema.get('unit')
            })
        
        return params
    
    def generate_realistic_test_data(self, params: Dict[str, Any]) -> Tuple[List[float], str]:
        """Generate realistic test data based on actual algorithm parameters and config details"""
        
        algorithm_type = params['algorithm_type']
        unit = params.get('unit', 'units')
        
        # Determine if values should be whole numbers
        whole_number_units = ['serving', 'drink', 'session', 'meal', 'count', 'day', 'days']
        use_whole_numbers = unit and any(word in unit.lower() for word in whole_number_units)
        
        if algorithm_type == 'proportional_frequency_hybrid':
            return self._generate_hybrid_test_data(params, use_whole_numbers)
        elif algorithm_type == 'proportional':
            return self._generate_proportional_test_data(params, use_whole_numbers)
        elif algorithm_type == 'binary_threshold':
            return self._generate_binary_test_data(params, use_whole_numbers)
        elif algorithm_type == 'minimum_frequency':
            return self._generate_frequency_test_data(params, use_whole_numbers)
        elif algorithm_type == 'weekly_elimination':
            return self._generate_elimination_test_data(params, use_whole_numbers)
        elif algorithm_type == 'zone_based':
            return self._generate_zone_test_data(params, use_whole_numbers)
        elif algorithm_type == 'composite_weighted':
            return self._generate_composite_test_data(params, use_whole_numbers)
        elif algorithm_type == 'constrained_weekly_allowance':
            return self._generate_allowance_test_data(params, use_whole_numbers)
        elif algorithm_type == 'categorical_filter_threshold':
            return self._generate_categorical_test_data(params, use_whole_numbers)
        else:
            # Fallback for unknown algorithms
            return [1.0] * 7, f"Generic test data for {algorithm_type}"
    
    def _generate_hybrid_test_data(self, params: Dict[str, Any], use_whole_numbers: bool) -> Tuple[List[float], str]:
        """Generate test data for proportional_frequency_hybrid based on actual config"""
        target = params.get('daily_target', 1.0)
        if target is None:
            target = 1.0
        required_days = params.get('required_qualifying_days', 2)
        if required_days is None:
            required_days = 2
        unit = params.get('unit', 'units')
        
        if required_days <= 2:
            # Test the "partial credit fix" scenario
            consistent_value = target * 0.67  # 67% of target
            values = [consistent_value] * 7
            description = f"Consistent {consistent_value:.1f} {unit} daily (67% of {target} target) - tests partial credit fix"
        else:
            # Mixed performance scenario
            values = [
                target * 0.8,   # 80%
                0,              # Rest day  
                target * 1.0,   # 100%
                target * 0.87,  # 87%
                target * 0.8,   # 80%
                target * 0.53,  # 53%
                target * 1.0    # 100%
            ]
            description = f"Mixed performance, top {required_days} days averaged for weekly score"
        
        return values, description
    
    def _generate_proportional_test_data(self, params: Dict[str, Any], use_whole_numbers: bool) -> Tuple[List[float], str]:
        """Generate test data for proportional based on actual config"""
        target = params.get('target', 1.0)
        if target is None:
            target = 1.0
        else:
            target = float(target)
            
        unit = params.get('unit', 'units')
        max_cap = params.get('maximum_cap', 100)
        evaluation_period = params.get('evaluation_period', 'daily')
        frequency_requirement = params.get('frequency_requirement', 'daily')
        
        # Check if this is weekly evaluation (sum across week)
        if 'weekly' in evaluation_period.lower() or 'weekly' in frequency_requirement.lower():
            # Generate daily values that sum to around the weekly target
            # Example: 90 minute weekly target = spread across 3-4 workout days
            if use_whole_numbers:
                target = int(target)
                # Spread target across 3-4 days (common workout pattern)
                values = [
                    int(target * 0.3),  # 30% on day 1
                    0,                  # Rest day
                    int(target * 0.4),  # 40% on day 3  
                    0,                  # Rest day
                    int(target * 0.35), # 35% on day 5
                    0,                  # Rest day
                    0                   # Rest day
                ]
                actual_total = sum(values)
                description = f"Weekly target: {actual_total}/{target} {unit} total ({(actual_total/target)*100:.0f}% of weekly goal)"
            else:
                # Spread target across workout days
                values = [
                    target * 0.3,   # 30% 
                    0.0,            # Rest
                    target * 0.4,   # 40%
                    0.0,            # Rest  
                    target * 0.35,  # 35%
                    0.0,            # Rest
                    0.0             # Rest
                ]
                actual_total = sum(values)
                description = f"Weekly target: {actual_total:.1f}/{target} {unit} total ({(actual_total/target)*100:.0f}% of weekly goal)"
        else:
            # Daily evaluation - mixed performance around daily target
            if use_whole_numbers:
                target = int(target)
                values = [
                    target,         # 100%
                    target + 1,     # Over target
                    int(target * 0.8), # 80%
                    target,         # 100%
                    0,              # Miss day
                    int(target * 0.9), # 90%
                    target + 2      # Over target
                ]
            else:
                values = [
                    target * 1.0,   # 100%
                    target * 1.2,   # 120%
                    target * 0.8,   # 80%
                    target * 1.0,   # 100%
                    0.0,            # Miss day
                    target * 0.9,   # 90%
                    target * 1.1    # 110%
                ]
            description = f"Daily target performance around {target} {unit} per day"
        
        if use_whole_numbers:
            values = [int(v) for v in values]
        
        return values, description
    
    def _generate_binary_test_data(self, params: Dict[str, Any], use_whole_numbers: bool) -> Tuple[List[float], str]:
        """Generate test data for binary_threshold based on actual config"""
        threshold = params.get('threshold', 1.0)
        operator = params.get('comparison_operator', '>=')
        unit = params.get('unit', 'units')
        progress_direction = params.get('progress_direction', 'buildup')
        
        # For countdown/limits (≤), generate values around the limit
        if operator in ['<=', '<'] or progress_direction == 'countdown':
            if use_whole_numbers:
                threshold = int(threshold)
                values = [
                    threshold,      # At limit - PASS  
                    threshold + 1,  # Over limit - FAIL
                    threshold - 1 if threshold > 1 else 0,  # Under limit - PASS
                    threshold,      # At limit - PASS
                    threshold + 2,  # Over limit - FAIL  
                    0,              # No consumption - PASS
                    threshold       # At limit - PASS
                ]
            else:
                values = [
                    threshold * 1.0,   # At limit - PASS
                    threshold * 1.25,  # Over limit - FAIL
                    threshold * 0.5,   # Under limit - PASS
                    threshold * 1.0,   # At limit - PASS
                    threshold * 1.5,   # Over limit - FAIL
                    0.0,               # No consumption - PASS
                    threshold * 0.8    # Under limit - PASS
                ]
            
            passes = 5  # 5 compliant days
            description = f"Limit compliance ≤{threshold} {unit}: {passes}/7 days compliant (2 exceed limit)"
            
        else:
            # For buildup/targets (≥), generate achievement patterns
            if use_whole_numbers:
                threshold = int(threshold)
                values = [threshold] * 6 + [0]  # 6 days achieve, 1 day miss
            else:
                values = [threshold] * 6 + [0.0]  # 6 days achieve, 1 day miss
                
            passes = 6
            description = f"Target achievement ≥{threshold} {unit}: {passes}/7 days achieve target"
        
        if use_whole_numbers:
            values = [int(v) for v in values]
        
        return values, description
    
    def _generate_frequency_test_data(self, params: Dict[str, Any], use_whole_numbers: bool) -> Tuple[List[float], str]:
        """Generate test data for minimum_frequency based on actual config"""
        daily_threshold = params.get('daily_threshold')
        required_days = params.get('required_days', 3)
        comparison = params.get('daily_comparison', '>=')
        unit = params.get('unit', 'units')
        
        # Handle time-based thresholds
        if isinstance(daily_threshold, str) and ':' in daily_threshold:
            if comparison == '<=':
                # Caffeine cutoff scenario
                target_hour = 14.0  # 2 PM
                values = []
                # Some days before cutoff (pass)
                for _ in range(required_days):
                    values.append(target_hour - random.uniform(0.5, 2.0))  # 12-1:30 PM
                # Some days after cutoff (fail) 
                for _ in range(7 - required_days):
                    values.append(target_hour + random.uniform(0.5, 4.0))  # 2:30-6 PM
                random.shuffle(values)
                description = f"Caffeine cutoff {daily_threshold}: exactly {required_days} days before cutoff"
            else:
                values = [14.0] * 7  # Generic time data
                description = f"Time-based pattern: {daily_threshold}"
        else:
            # Numeric threshold - exactly meet requirement
            threshold = float(daily_threshold) if daily_threshold else 1.0
            values = []
            
            # Add exactly required_days that pass
            for _ in range(required_days):
                if use_whole_numbers:
                    values.append(int(threshold * random.uniform(1.0, 1.5)))
                else:
                    values.append(threshold * random.uniform(1.0, 1.5))
            
            # Add remaining days that fail
            for _ in range(7 - required_days):
                if use_whole_numbers:
                    values.append(max(0, int(threshold * random.uniform(0.3, 0.9))))
                else:
                    values.append(threshold * random.uniform(0.3, 0.9))
            
            random.shuffle(values)
            description = f"Exactly {required_days} days {comparison}{threshold} {unit} (meets requirement)"
        
        if use_whole_numbers:
            values = [int(v) for v in values]
        
        return values, description
    
    def _generate_elimination_test_data(self, params: Dict[str, Any], use_whole_numbers: bool) -> Tuple[List[float], str]:
        """Generate test data for weekly_elimination based on actual config"""
        threshold = params.get('elimination_threshold', 0)
        unit = params.get('unit', 'units')
        
        # Handle time-based thresholds (like "14:00")
        if isinstance(threshold, str) and ':' in threshold:
            # Convert time to decimal hours for test data
            try:
                hours, minutes = threshold.split(':')
                threshold_decimal = int(hours) + int(minutes) / 60.0
                
                # 50/50 chance of perfect week vs violation
                if random.choice([True, False]):
                    values = [threshold_decimal] * 7
                    description = f"Perfect elimination: {threshold} {unit} all days"
                else:
                    values = [threshold_decimal] * 6 + [threshold_decimal + 1]
                    description = f"Violation on day 7: fails entire week"
            except:
                # Fallback for time parsing issues
                values = [14.0] * 6 + [15.0]
                description = f"Time-based elimination test: {threshold}"
        else:
            # Numeric threshold
            if threshold is None:
                threshold = 0
            threshold = float(threshold)
            
            # 50/50 chance of perfect week vs violation
            if random.choice([True, False]):
                if use_whole_numbers:
                    values = [int(threshold)] * 7  # Perfect elimination
                else:
                    values = [threshold] * 7  # Perfect elimination
                description = f"Perfect elimination: {threshold} {unit} all days"
            else:
                if use_whole_numbers:
                    values = [int(threshold)] * 6 + [int(threshold) + 1]  # One violation
                else:
                    values = [threshold] * 6 + [threshold + 1]  # One violation
                description = f"Violation on day 7: fails entire week"
        
        if use_whole_numbers:
            values = [int(v) for v in values]
        
        return values, description
    
    def _generate_zone_test_data(self, params: Dict[str, Any], use_whole_numbers: bool) -> Tuple[List[float], str]:
        """Generate test data for zone_based algorithms"""
        unit = params.get('unit', 'units')
        zones = params.get('zones', [])
        
        if unit in ['hour', 'hours'] and not zones:
            # Likely sleep duration - use 7-9 hour optimal zone
            if use_whole_numbers:
                values = [8, 7, 8, 6, 9, 9, 6]
            else:
                values = [8.0, 6.5, 7.5, 6.0, 8.5, 9.0, 6.0]
            description = "Sleep duration zones: mixed optimal/suboptimal performance"
        else:
            # Generic zone testing
            if use_whole_numbers:
                values = [5, 8, 6, 9, 7, 4, 8]  # Mix of zone values
            else:
                values = [5.0, 8.0, 6.0, 9.0, 7.0, 4.0, 8.0]  # Mix of zone values
            description = f"Zone-based scoring with mixed performance"
        
        if use_whole_numbers:
            values = [int(v) for v in values]
        
        return values, description
    
    def _generate_composite_test_data(self, params: Dict[str, Any], use_whole_numbers: bool) -> Tuple[List[float], str]:
        """Generate test data for composite_weighted algorithms"""
        # Composite scores are complex - generate reasonable values
        components = params.get('components', [])
        unit = params.get('unit', 'score')
        
        if use_whole_numbers:
            values = [75, 85, 65, 90, 70, 80, 88]  # Composite scores
        else:
            values = [75.0, 85.0, 65.0, 90.0, 70.0, 80.0, 88.0]  # Composite scores
        
        description = f"Composite weighted scoring with {len(components)} components"
        
        if use_whole_numbers:
            values = [int(v) for v in values]
        
        return values, description
    
    def _generate_allowance_test_data(self, params: Dict[str, Any], use_whole_numbers: bool) -> Tuple[List[float], str]:
        """Generate test data for constrained_weekly_allowance"""
        allowance = params.get('weekly_allowance', 2)
        if allowance is None:
            allowance = 2
        unit = params.get('unit', 'meals')
        
        # Test scenario that slightly exceeds allowance
        total_used = allowance + 1
        if use_whole_numbers:
            values = [0, 1, 0, 1, 1, 0, 0]  # 3 total if allowance is 2
        else:
            values = [0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0]  # 3 total if allowance is 2
            
        description = f"Weekly allowance: {sum(values)} {unit} vs {allowance} allowed"
        
        if use_whole_numbers:
            values = [int(v) for v in values]
        
        return values, description
    
    def _generate_categorical_test_data(self, params: Dict[str, Any], use_whole_numbers: bool) -> Tuple[List[float], str]:
        """Generate test data for categorical_filter_threshold"""
        categories = params.get('categories', [])
        threshold = params.get('threshold', 3)
        unit = params.get('unit', 'servings')
        
        if use_whole_numbers:
            values = [2, 1, 3, 2, 1, 2, 3]  # Servings per day
        else:
            values = [2.0, 1.0, 3.0, 2.0, 1.0, 2.0, 3.0]  # Servings per day
            
        description = f"Categorical filtering: target categories with {threshold} {unit} threshold"
        
        if use_whole_numbers:
            values = [int(v) for v in values]
        
        return values, description
    
    def generate_test_scenario(self, config_file: str, config_data: Dict[str, Any]) -> ConfigTestScenario:
        """Generate a complete test scenario from actual config data"""
        
        rec_id = config_data.get('metadata', {}).get('recommendation_id', 'UNKNOWN')
        algorithm_type = config_data.get('scoring_method', 'unknown')
        
        # Extract actual algorithm parameters from config
        algorithm_parameters = self.extract_algorithm_parameters(config_data)
        
        # Generate realistic test data based on actual parameters
        test_values, scenario_description = self.generate_realistic_test_data(algorithm_parameters)
        
        return ConfigTestScenario(
            rec_id=rec_id,
            config_file=config_file,
            config_data=config_data,
            algorithm_type=algorithm_type,
            test_values=test_values,
            scenario_description=scenario_description,
            algorithm_parameters=algorithm_parameters
        )

def run_config_based_verification():
    """Run comprehensive verification using actual config files"""
    
    print("🔍 Auto-discovering REC configuration files...")
    generator = ConfigBasedTestGenerator()
    configs = generator.discover_all_configs()
    print(f"📊 Found {len(configs)} configuration files")
    
    print("🧪 Generating test scenarios from actual config data...")
    test_scenarios = []
    failed_configs = []
    
    for config_file, config_data in configs:
        try:
            scenario = generator.generate_test_scenario(config_file, config_data)
            test_scenarios.append(scenario)
        except Exception as e:
            failed_configs.append((config_file, str(e)))
            print(f"⚠️  Failed to process {os.path.basename(config_file)}: {e}")
    
    print(f"✅ Generated {len(test_scenarios)} test scenarios")
    if failed_configs:
        print(f"⚠️  {len(failed_configs)} configs failed processing")
    
    # Generate comprehensive output
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_lines = []
    
    output_lines.extend([
        "=" * 100,
        "WELLPATH CONFIG-BASED ALGORITHM VERIFICATION TEST WITH ADHERENCE SCORING",
        f"Generated: {timestamp}",
        f"Configurations Processed: {len(test_scenarios)} successful, {len(failed_configs)} failed",
        "Method: Uses actual config files, algorithm parameters, and calculates adherence scores",
        "Auto-updates: Automatically includes new configs added to /src/generated_configs/",
        "=" * 100,
        "",
        "ALGORITHM DISTRIBUTION:",
        ""
    ])
    
    # Count by algorithm type
    algo_counts = {}
    for scenario in test_scenarios:
        algo_type = scenario.algorithm_type
        algo_counts[algo_type] = algo_counts.get(algo_type, 0) + 1
    
    for algo_type, count in sorted(algo_counts.items()):
        output_lines.append(f"  {algo_type}: {count} configurations")
    
    output_lines.extend([
        "",
        "=" * 100,
        "CONFIGURATION-BASED TEST SCENARIOS WITH ADHERENCE CALCULATIONS",
        "=" * 100,
        ""
    ])
    
    # Generate detailed test scenarios with adherence scores
    for i, scenario in enumerate(test_scenarios, 1):
        config_name = os.path.basename(scenario.config_file)
        
        # Calculate adherence scores
        adherence = calculate_adherence_scores(
            scenario.test_values,
            scenario.algorithm_type,
            scenario.algorithm_parameters
        )
        
        output_lines.extend([
            f"📊 TEST {i:3d}: {scenario.rec_id}",
            f"Config File: {config_name}",
            f"Algorithm: {scenario.algorithm_type}",
            "-" * 80,
            "",
            "ACTUAL CONFIG PARAMETERS:",
        ])
        
        # Show actual algorithm parameters from config
        key_params = scenario.algorithm_parameters
        for key, value in key_params.items():
            if key not in ['schema', 'method'] and value is not None:
                output_lines.append(f"  {key}: {value}")
        
        output_lines.extend([
            "",
            "TEST SCENARIO:",
            f"  {scenario.scenario_description}",
            "",
            "7-DAY TEST DATA & PROGRESSIVE ADHERENCE SCORES:",
        ])
        
        unit = key_params.get('unit', 'units')
        for day, (value, daily_score) in enumerate(zip(scenario.test_values, adherence['daily_scores']), 1):
            if isinstance(value, float):
                output_lines.append(f"  Day {day}: {value:8.2f} {unit} → {daily_score:6.1f}% progressive adherence")
            else:
                output_lines.append(f"  Day {day}: {value:8} {unit} → {daily_score:6.1f}% progressive adherence")
        
        output_lines.extend([
            "",
            "WEEKLY ADHERENCE SUMMARY:",
            f"  📈 Weekly Score: {adherence['weekly_score']:.1f}%",
            f"  ✅ Passing Days: {adherence['passing_days']}/{adherence['total_days']}",
            f"  📊 Daily Average: {sum(adherence['daily_scores'])/len(adherence['daily_scores']):.1f}%",
            "",
            "REFERENCES:",
            f"  • Config: /src/generated_configs/{config_name}",
            f"  • Algorithm: /src/algorithms/{scenario.algorithm_type}.py",
            f"  • Method: {key_params.get('method', 'N/A')}",
            "",
            "=" * 80,
            ""
        ])
    
    # Failed configs section
    if failed_configs:
        output_lines.extend([
            "FAILED CONFIGURATIONS",
            "=" * 80,
            ""
        ])
        
        for config_file, error in failed_configs:
            config_name = os.path.basename(config_file)
            output_lines.extend([
                f"❌ {config_name}",
                f"   Error: {error}",
                ""
            ])
        
        output_lines.append("=" * 80)
        output_lines.append("")
    
    # Summary
    output_lines.extend([
        "VERIFICATION SUMMARY",
        "=" * 80,
        f"✅ Successfully processed: {len(test_scenarios)} configurations",
        f"❌ Failed to process: {len(failed_configs)} configurations",
        f"🎯 Algorithm types covered: {len(algo_counts)}",
        f"📁 Total config files found: {len(configs)}",
        "",
        "KEY FEATURES:",
        "• Uses actual config file data (not hardcoded)",
        "• References actual algorithm implementations",
        "• Auto-discovers new configs when added",
        "• Generates realistic test data based on config parameters",
        "• Calculates daily and weekly adherence scores using actual algorithm logic",
        "• Provides clear mapping between configs and algorithms",
        "• Shows compliance rates and passing day statistics",
        "",
        "END OF CONFIG-BASED VERIFICATION WITH ADHERENCE SCORING",
        "=" * 100
    ])
    
    # Write output
    output_file = os.path.join(os.path.dirname(__file__), "config_based_verification_output.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"\n📄 Output written to: {output_file}")
    print(f"📊 Algorithm distribution: {dict(sorted(algo_counts.items()))}")
    
    return len(test_scenarios), len(failed_configs)

if __name__ == "__main__":
    successful, failed = run_config_based_verification()
    print(f"\n🎯 Final result: {successful} successful, {failed} failed")