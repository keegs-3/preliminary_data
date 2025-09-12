#!/usr/bin/env python3
"""
Comprehensive Algorithm Verification Test Generator

Automatically generates realistic test data for ALL REC configs in the system
and outputs detailed scoring breakdowns for manual verification.

Features:
- Auto-discovers all REC*.json files in generated_configs/
- Creates realistic 7-day test scenarios for each algorithm type
- Generates mixed success/partial/failure scenarios
- Updates automatically when new RECs are added
- Outputs comprehensive verification file
"""

import sys
import os
import glob
import json
import random
from datetime import datetime
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

# Add src to path for algorithm imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from algorithms.proportional_frequency_hybrid import create_proportional_frequency_hybrid
from algorithms.proportional import ProportionalAlgorithm, ProportionalConfig
from algorithms.binary_threshold import BinaryThresholdAlgorithm, BinaryThresholdConfig
from algorithms.minimum_frequency import calculate_minimum_frequency_score
from algorithms.weekly_elimination import calculate_weekly_elimination_score

@dataclass
class ConfigTestData:
    rec_id: str
    config_file: str
    algorithm_type: str
    config_schema: Dict[str, Any]
    test_values: List[float]
    expected_daily_scores: List[float]
    expected_weekly_score: float
    scenario_description: str
    significance: str

class TestDataGenerator:
    """Generates realistic test data based on algorithm types and thresholds"""
    
    def __init__(self):
        self.algorithm_handlers = {
            'proportional': self._generate_proportional_data,
            'proportional_frequency_hybrid': self._generate_hybrid_data,
            'binary_threshold': self._generate_binary_data,
            'minimum_frequency': self._generate_frequency_data,
            'weekly_elimination': self._generate_elimination_data,
            'zone_based': self._generate_zone_data,
            'composite_weighted': self._generate_composite_data,
            'categorical_filter_threshold': self._generate_categorical_data,
            'constrained_weekly_allowance': self._generate_allowance_data
        }
    
    def _extract_target_from_config(self, config_data: Dict) -> Tuple[float, str, str]:
        """Extract target value, unit, and algorithm type from config"""
        schema = config_data.get('configuration_json', {}).get('schema', {})
        method = config_data.get('configuration_json', {}).get('method', '')
        
        # Try to extract target value
        target_raw = schema.get('target', schema.get('daily_target', schema.get('threshold', schema.get('daily_threshold', 1.0))))
        unit = schema.get('unit', 'units')
        
        # Handle time-based thresholds (e.g., "14:00")
        if isinstance(target_raw, str) and ':' in target_raw:
            # Convert time string to hour float for calculation purposes
            try:
                hour, minute = target_raw.split(':')
                target = float(hour) + float(minute) / 60.0
                unit = 'time'
            except:
                target = 14.0  # Default to 2 PM
        else:
            try:
                target = float(target_raw)
            except:
                target = 1.0  # Safe default
        
        return target, unit, method
    
    def _generate_proportional_data(self, target: float, unit: str, config_data: Dict) -> Tuple[List[float], str]:
        """Generate test data for proportional algorithms"""
        # Create mixed scenario: some below, some at, some above target
        values = [
            target * 0.6,   # 60% - partial credit
            target * 1.2,   # 120% - over target (capped at 100%)
            target * 0.8,   # 80% - good progress  
            target * 1.0,   # 100% - perfect
            target * 0.4,   # 40% - needs improvement
            target * 0.9,   # 90% - almost there
            target * 1.1    # 110% - exceeds target
        ]
        
        description = f"Mixed performance around {target} {unit} target"
        return values, description
    
    def _generate_hybrid_data(self, target: float, unit: str, config_data: Dict) -> Tuple[List[float], str]:
        """Generate test data for proportional frequency hybrid"""
        schema = config_data.get('configuration_json', {}).get('schema', {})
        required_days = schema.get('required_qualifying_days', 2)
        
        if required_days <= 2:
            # Low frequency requirement - test consistent partial performance
            values = [target * 0.67] * 7  # All days at 67% - should get partial credit
            description = f"Consistent {target * 0.67:.0f} {unit} daily (67% of target) - tests partial credit fix"
        else:
            # Higher frequency requirement - mixed performance
            values = [
                target * 0.8,   # 80%
                0,              # Rest day
                target * 1.0,   # 100%
                target * 0.87,  # 87%
                target * 0.8,   # 80%
                target * 0.53,  # 53%
                target * 1.0    # 100%
            ]
            description = f"Mixed performance with rest day, {required_days} best days counted"
        
        return values, description
    
    def _generate_binary_data(self, target: float, unit: str, config_data: Dict) -> Tuple[List[float], str]:
        """Generate test data for binary threshold algorithms"""
        schema = config_data.get('configuration_json', {}).get('schema', {})
        comparison = schema.get('comparison_operator', '>=')
        
        if comparison in ['<=', '<']:
            # Limit-based binary (e.g., caffeine limit)
            values = [
                target * 0.75,  # Under limit - PASS
                target * 1.25,  # Over limit - FAIL  
                target * 1.0,   # At limit - PASS
                target * 0.9,   # Under limit - PASS
                target * 1.5,   # Over limit - FAIL
                target * 0.95,  # Under limit - PASS
                target * 0.85   # Under limit - PASS
            ]
            description = f"Limit compliance: ≤{target} {unit} (5/7 successful days)"
        else:
            # Target-based binary (e.g., medication adherence)
            values = [1, 1, 0, 1, 1, 1, 1] if target == 1 else [target, target, 0, target, target, target, target]
            description = f"Daily requirement compliance (6/7 successful days)"
        
        return values, description
    
    def _generate_frequency_data(self, target: float, unit: str, config_data: Dict) -> Tuple[List[float], str]:
        """Generate test data for minimum frequency algorithms"""
        schema = config_data.get('configuration_json', {}).get('schema', {})
        daily_threshold_raw = schema.get('daily_threshold', target)
        required_days = schema.get('required_days', 3)
        comparison = schema.get('daily_comparison', '>=')
        
        # Handle time-based thresholds
        if isinstance(daily_threshold_raw, str) and ':' in daily_threshold_raw:
            # Time-based threshold (e.g., "14:00" for caffeine cutoff)
            daily_threshold = target  # Already converted to float
            if comparison == '<=':
                # Caffeine cutoff scenario - some days before, some after 2pm
                values = []
                for _ in range(required_days):  # Qualifying days (before cutoff)
                    values.append(target - random.uniform(0.5, 2.0))  # 12pm-1:30pm
                for _ in range(7 - required_days):  # Non-qualifying days (after cutoff) 
                    values.append(target + random.uniform(0.5, 4.0))  # 2:30pm-6pm
                random.shuffle(values)
                description = f"Caffeine cutoff: {required_days} days before {daily_threshold_raw}, rest after"
            else:
                values = [target] * 7  # Generic time-based data
                description = f"Time-based threshold pattern"
        else:
            # Numeric threshold
            daily_threshold = float(daily_threshold_raw) if daily_threshold_raw else target
            
            # Create scenario that exactly meets requirement
            qualifying_days = required_days
            non_qualifying_days = 7 - qualifying_days
            
            values = []
            # Add qualifying days
            for _ in range(qualifying_days):
                values.append(daily_threshold * random.uniform(1.0, 1.5))  # Above threshold
            
            # Add non-qualifying days  
            for _ in range(non_qualifying_days):
                values.append(daily_threshold * random.uniform(0.3, 0.9))  # Below threshold
            
            random.shuffle(values)  # Mix up the order
            description = f"Exactly {qualifying_days} days ≥{daily_threshold} {unit} (meets {required_days}/{7} requirement)"
        
        return values, description
    
    def _generate_elimination_data(self, target: float, unit: str, config_data: Dict) -> Tuple[List[float], str]:
        """Generate test data for weekly elimination algorithms"""
        # Test both perfect week and violation scenarios
        if random.choice([True, False]):
            # Perfect elimination week
            values = [0] * 7  # All days meet elimination requirement
            description = f"Perfect elimination week - 0 {unit} all days"
        else:
            # Week with violation
            values = [0, 0, target * 0.5, 0, 0, 0, 0]  # One violation on day 3
            description = f"Elimination violation on day 3 - fails entire week"
        
        return values, description
    
    def _generate_zone_data(self, target: float, unit: str, config_data: Dict) -> Tuple[List[float], str]:
        """Generate test data for zone-based algorithms"""
        # Assuming sleep duration zones: 7-9 hours optimal
        if unit in ['hour', 'hours']:
            values = [
                8.0,    # Optimal zone
                6.5,    # Below optimal  
                7.5,    # Optimal zone
                6.0,    # Poor zone
                8.5,    # Optimal zone
                9.0,    # Optimal zone
                6.0     # Poor zone  
            ]
            description = f"Sleep duration zones: 4 optimal, 2 below optimal, 1 poor"
        else:
            # Generic zone testing around target
            values = [
                target * 0.9,   # Good zone
                target * 1.1,   # Good zone
                target * 0.7,   # Fair zone
                target * 1.0,   # Optimal zone
                target * 1.2,   # Good zone
                target * 0.6,   # Poor zone
                target * 1.0    # Optimal zone
            ]
            description = f"Mixed zone performance around {target} {unit}"
        
        return values, description
    
    def _generate_composite_data(self, target: float, unit: str, config_data: Dict) -> Tuple[List[float], str]:
        """Generate test data for composite weighted algorithms"""
        # Composite algorithms are complex - generate moderate performance
        values = [
            target * 0.75,  # 75%
            target * 0.85,  # 85%
            target * 0.65,  # 65%
            target * 0.90,  # 90%
            target * 0.70,  # 70%
            target * 0.80,  # 80%
            target * 0.88   # 88%
        ]
        description = f"Composite scoring with varied component performance"
        return values, description
    
    def _generate_categorical_data(self, target: float, unit: str, config_data: Dict) -> Tuple[List[float], str]:
        """Generate test data for categorical filter algorithms"""
        values = [2, 1, 3, 2, 1, 2, 3]  # Servings of target categories
        description = f"Categorical food servings with filtering"
        return values, description
    
    def _generate_allowance_data(self, target: float, unit: str, config_data: Dict) -> Tuple[List[float], str]:
        """Generate test data for constrained weekly allowance"""
        # Test scenario that slightly exceeds allowance
        daily_portions = [0, 1, 0, 1, 1, 0, 0]  # 3 total, if allowance is 2
        values = daily_portions
        description = f"Weekly allowance test: 3 total vs {target} allowed"
        return values, description
    
    def generate_test_data(self, config_data: Dict, config_file: str) -> ConfigTestData:
        """Generate comprehensive test data for a given config"""
        
        # Extract basic info
        rec_id = config_data.get('metadata', {}).get('recommendation_id', 'UNKNOWN')
        algorithm_type = config_data.get('scoring_method', 'unknown')
        target, unit, method = self._extract_target_from_config(config_data)
        
        # Generate test values using appropriate handler
        handler = self.algorithm_handlers.get(algorithm_type, self._generate_proportional_data)
        test_values, scenario_desc = handler(target, unit, config_data)
        
        # Calculate expected scores (simplified for now - actual calculation happens in test runner)
        expected_daily_scores = [0.0] * 7  # Placeholder
        expected_weekly_score = 0.0  # Placeholder
        
        return ConfigTestData(
            rec_id=rec_id,
            config_file=config_file,
            algorithm_type=algorithm_type,
            config_schema=config_data.get('configuration_json', {}).get('schema', {}),
            test_values=test_values,
            expected_daily_scores=expected_daily_scores,
            expected_weekly_score=expected_weekly_score,
            scenario_description=scenario_desc,
            significance=f"Tests {algorithm_type} algorithm behavior with realistic data"
        )

def discover_all_rec_configs():
    """Auto-discover all REC config files in the generated_configs directory"""
    config_dir = os.path.join(os.path.dirname(__file__), '..', 'src', 'generated_configs')
    pattern = os.path.join(config_dir, 'REC*.json')
    config_files = glob.glob(pattern)
    config_files.sort()  # Sort for consistent ordering
    
    configs = []
    for config_file in config_files:
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                configs.append((config_file, config_data))
        except Exception as e:
            print(f"Warning: Failed to load {config_file}: {e}")
    
    return configs

def run_comprehensive_verification():
    """Run comprehensive verification for ALL REC configs"""
    
    print("🔍 Discovering all REC configuration files...")
    configs = discover_all_rec_configs()
    print(f"📊 Found {len(configs)} REC configuration files")
    
    generator = TestDataGenerator()
    test_data_sets = []
    
    print("🧪 Generating test data for all configurations...")
    for config_file, config_data in configs:
        try:
            test_data = generator.generate_test_data(config_data, config_file)
            test_data_sets.append(test_data)
        except Exception as e:
            print(f"⚠️  Warning: Failed to generate test data for {config_file}: {e}")
    
    # Generate comprehensive output
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_lines = []
    
    output_lines.extend([
        "=" * 100,
        "WELLPATH COMPREHENSIVE ALGORITHM VERIFICATION TEST",
        f"Generated: {timestamp}",
        f"Total Configurations Tested: {len(test_data_sets)}",
        "Auto-updates when new REC configs are added to /src/generated_configs/",
        "=" * 100,
        "",
        "ALGORITHM DISTRIBUTION:",
        ""
    ])
    
    # Count algorithms by type
    algorithm_counts = {}
    for test_data in test_data_sets:
        algo_type = test_data.algorithm_type
        algorithm_counts[algo_type] = algorithm_counts.get(algo_type, 0) + 1
    
    for algo_type, count in sorted(algorithm_counts.items()):
        output_lines.append(f"  {algo_type}: {count} configurations")
    
    output_lines.extend([
        "",
        "=" * 100,
        "INDIVIDUAL CONFIGURATION TESTS",
        "=" * 100,
        ""
    ])
    
    # Generate test for each configuration
    for i, test_data in enumerate(test_data_sets, 1):
        config_name = os.path.basename(test_data.config_file)
        
        output_lines.append(f"📊 TEST {i:2d}: {test_data.rec_id} - {config_name}")
        output_lines.append(f"Algorithm: {test_data.algorithm_type}")
        output_lines.append(f"File: {config_name}")
        output_lines.append("-" * 80)
        output_lines.append("")
        output_lines.append("SCENARIO:")
        output_lines.append(f"  {test_data.scenario_description}")
        output_lines.append("")
        output_lines.append("TEST DATA (7 days):")
        
        for day, value in enumerate(test_data.test_values, 1):
            unit = test_data.config_schema.get('unit', 'units')
            output_lines.append(f"  Day {day}: {value:8.1f} {unit}")
        
        output_lines.append("")
        output_lines.append("ALGORITHM DETAILS:")
        output_lines.append(f"  Method: {test_data.algorithm_type}")
        
        # Add algorithm-specific details
        if test_data.algorithm_type == 'proportional_frequency_hybrid':
            target = test_data.config_schema.get('daily_target', 1.0)
            required_days = test_data.config_schema.get('required_qualifying_days', 2)
            output_lines.append(f"  Daily Target: {target}")
            output_lines.append(f"  Required Qualifying Days: {required_days}")
            output_lines.append(f"  Weekly Score: Average of top {required_days} daily scores")
        
        elif test_data.algorithm_type == 'proportional':
            target = test_data.config_schema.get('target', 1.0)
            output_lines.append(f"  Target: {target}")
            output_lines.append(f"  Weekly Score: Average of all daily proportional scores")
        
        elif test_data.algorithm_type == 'binary_threshold':
            threshold = test_data.config_schema.get('threshold', 1.0)
            comparison = test_data.config_schema.get('comparison_operator', '>=')
            output_lines.append(f"  Threshold: {comparison} {threshold}")
            output_lines.append(f"  Weekly Score: Average of daily binary results")
        
        elif test_data.algorithm_type == 'minimum_frequency':
            daily_threshold = test_data.config_schema.get('daily_threshold', 1.0)
            required_days = test_data.config_schema.get('required_days', 3)
            output_lines.append(f"  Daily Threshold: ≥ {daily_threshold}")
            output_lines.append(f"  Required Days: {required_days}/7")
            output_lines.append(f"  Weekly Score: 100% if requirement met, 0% otherwise")
        
        output_lines.append("")
        output_lines.append(f"SIGNIFICANCE: {test_data.significance}")
        output_lines.append("")
        output_lines.append("=" * 80)
        output_lines.append("")
    
    # Summary
    output_lines.extend([
        "VERIFICATION SUMMARY",
        "=" * 80,
        f"✅ Generated test scenarios for {len(test_data_sets)} configurations",
        f"📈 Algorithm distribution: {len(algorithm_counts)} different types",
        "🔄 Auto-discovery: Test data updates when new configs added",
        "🧪 Realistic scenarios: Mixed success/partial/failure patterns",
        "",
        "NEXT STEPS:",
        "1. Run actual algorithm calculations on this test data",
        "2. Add expected score calculations for each algorithm type", 
        "3. Implement automated scoring verification",
        "4. Set up CI/CD to run this test when configs change",
        "",
        "END OF COMPREHENSIVE VERIFICATION",
        "=" * 100
    ])
    
    # Write output file
    output_file = os.path.join(os.path.dirname(__file__), "comprehensive_algorithm_verification_output.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    # Also print summary to console
    print(f"\n✅ Generated comprehensive test data for {len(test_data_sets)} configurations")
    print(f"📄 Output written to: {output_file}")
    print(f"\nAlgorithm Distribution:")
    for algo_type, count in sorted(algorithm_counts.items()):
        print(f"  {algo_type}: {count} configs")

if __name__ == "__main__":
    run_comprehensive_verification()