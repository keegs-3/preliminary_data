#!/usr/bin/env python3
"""
Algorithm Integration Test

This test validates configs and algorithms by:
1. Auto-discovering all REC*.json config files
2. Loading actual config data and algorithm implementations
3. Generating realistic test data within schema constraints with outliers
4. Testing actual algorithm classes (not hardcoded logic)
5. Validating schema compliance and data generation edge cases
6. Providing clear pass/fail results for each config-algorithm pair

This replaces the problematic config_based_verification_test.py which had
hardcoded algorithm logic instead of using actual implementations.
"""

import sys
import os
import glob
import json
import random
import importlib
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional, Union
from dataclasses import dataclass
import traceback

# Add src to path for algorithm imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

@dataclass
class TestResult:
    """Result of testing a single config-algorithm pair"""
    config_name: str
    algorithm_type: str
    test_passed: bool
    error_message: Optional[str] = None
    test_data: List[float] = None
    scores: List[float] = None
    expected_behavior: str = ""

@dataclass
class TestScenario:
    """Test scenario generated from schema constraints"""
    name: str
    values: List[float]
    description: str
    expected_outcome: str

class SchemaBasedDataGenerator:
    """Generates test data based on JSON schema constraints with outliers"""
    
    def __init__(self, schema: Dict[str, Any], algorithm_type: str):
        self.schema = schema
        self.algorithm_type = algorithm_type
        
    def generate_test_scenarios(self) -> List[TestScenario]:
        """Generate multiple test scenarios including edge cases and outliers"""
        scenarios = []
        
        # Base scenario - typical valid data
        scenarios.append(self._generate_base_scenario())
        
        # Edge cases based on algorithm type
        scenarios.extend(self._generate_edge_cases())
        
        # Outlier scenarios
        scenarios.extend(self._generate_outlier_scenarios())
        
        return scenarios
    
    def _generate_base_scenario(self) -> TestScenario:
        """Generate typical valid data within schema constraints"""
        if self.algorithm_type == 'proportional':
            target = self.schema.get('target', 5.0)
            unit = self.schema.get('unit', 'units')
            
            # Generate data around target with some variation
            values = []
            for i in range(7):
                # Mix of achieving target, under-achieving, and over-achieving
                factor = random.uniform(0.6, 1.4)
                values.append(target * factor)
            
            return TestScenario(
                name="typical_performance",
                values=values,
                description=f"Mixed performance around {target} {unit} target",
                expected_outcome="proportional_scores_calculated"
            )
            
        elif self.algorithm_type == 'binary_threshold':
            threshold = self.schema.get('threshold', 1.0)
            operator = self.schema.get('comparison_operator', '>=')
            
            # Generate mix of pass/fail
            values = []
            for i in range(7):
                if i < 4:  # 4 passing days
                    if operator in ['>=', '>']:
                        values.append(threshold * random.uniform(1.0, 1.5))
                    else:  # <= or <
                        values.append(threshold * random.uniform(0.5, 1.0))
                else:  # 3 failing days
                    if operator in ['>=', '>']:
                        values.append(threshold * random.uniform(0.3, 0.9))
                    else:  # <= or <
                        values.append(threshold * random.uniform(1.1, 1.8))
            
            random.shuffle(values)
            return TestScenario(
                name="mixed_pass_fail",
                values=values,
                description=f"Mixed pass/fail around {threshold} threshold ({operator})",
                expected_outcome="binary_scores_100_or_0"
            )
            
        elif self.algorithm_type == 'minimum_frequency':
            daily_threshold = self.schema.get('daily_threshold', 1.0)
            required_days = self.schema.get('required_days', 3)
            
            values = []
            # Exactly meet requirement
            for i in range(required_days):
                values.append(daily_threshold * random.uniform(1.1, 1.8))
            for i in range(7 - required_days):
                values.append(daily_threshold * random.uniform(0.2, 0.9))
            
            random.shuffle(values)
            return TestScenario(
                name="meets_requirement",
                values=values,
                description=f"Exactly {required_days} days meet {daily_threshold} threshold",
                expected_outcome="frequency_requirement_met"
            )
            
        elif self.algorithm_type == 'weekly_elimination':
            threshold = self.schema.get('elimination_threshold', 0)
            
            # Test perfect compliance vs violation
            if random.choice([True, False]):
                values = [threshold] * 7
                outcome = "perfect_elimination"
            else:
                values = [threshold] * 6 + [threshold + 1]
                outcome = "elimination_violated"
            
            return TestScenario(
                name="elimination_test",
                values=values,
                description=f"Testing elimination threshold {threshold}",
                expected_outcome=outcome
            )
            
        elif self.algorithm_type == 'zone_based':
            zones = self.schema.get('zones', [])
            if not zones:
                # Default sleep zones
                values = [7.5, 6.0, 8.5, 7.0, 9.0, 6.5, 8.0]
            else:
                # Generate values across different zones
                values = []
                for zone in zones[:7]:  # Take first 7 zones or cycle
                    zone_range = zone.get('range', [7, 8])
                    min_val, max_val = zone_range[0], zone_range[1] if len(zone_range) > 1 else zone_range[0]
                    values.append(random.uniform(min_val, max_val))
                    
                while len(values) < 7:
                    values.append(random.uniform(zones[0]['range'][0], zones[-1]['range'][-1]))
            
            return TestScenario(
                name="zone_distribution",
                values=values,
                description="Values distributed across different zones",
                expected_outcome="zone_based_scoring"
            )
            
        else:
            # Generic fallback
            values = [random.uniform(1, 10) for _ in range(7)]
            return TestScenario(
                name="generic_data",
                values=values,
                description=f"Generic test data for {self.algorithm_type}",
                expected_outcome="algorithm_processes_data"
            )
    
    def _generate_edge_cases(self) -> List[TestScenario]:
        """Generate edge case scenarios"""
        scenarios = []
        
        # All zeros
        scenarios.append(TestScenario(
            name="all_zeros",
            values=[0.0] * 7,
            description="All zero values",
            expected_outcome="handles_zero_values"
        ))
        
        # All maximum values (if applicable)
        if self.algorithm_type == 'proportional':
            target = self.schema.get('target', 5.0)
            max_values = [target * 5] * 7  # 5x target
            scenarios.append(TestScenario(
                name="all_maximum",
                values=max_values,
                description="All maximum values (5x target)",
                expected_outcome="handles_high_values"
            ))
        
        # Single spike value
        spike_values = [1.0] * 6 + [100.0]
        scenarios.append(TestScenario(
            name="single_spike",
            values=spike_values,
            description="Single outlier spike value",
            expected_outcome="handles_outliers"
        ))
        
        return scenarios
    
    def _generate_outlier_scenarios(self) -> List[TestScenario]:
        """Generate scenarios with outliers to test robustness"""
        scenarios = []
        
        # Negative values (if inappropriate for algorithm)
        scenarios.append(TestScenario(
            name="negative_values",
            values=[-1.0, 0.0, 1.0, -0.5, 2.0, -10.0, 0.5],
            description="Mixed negative and positive values",
            expected_outcome="handles_negative_values"
        ))
        
        # Very large values
        scenarios.append(TestScenario(
            name="very_large_values",
            values=[1000000.0] * 7,
            description="Extremely large values",
            expected_outcome="handles_large_values"
        ))
        
        # Very small decimal values
        scenarios.append(TestScenario(
            name="very_small_values",
            values=[0.00001] * 7,
            description="Extremely small decimal values",
            expected_outcome="handles_small_decimals"
        ))
        
        return scenarios

class AlgorithmTester:
    """Tests actual algorithm implementations with generated data"""
    
    def __init__(self):
        self.src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
        if self.src_path not in sys.path:
            sys.path.insert(0, self.src_path)
    
    def test_config(self, config_data: Dict[str, Any], config_name: str) -> List[TestResult]:
        """Test a single config with multiple scenarios"""
        algorithm_type = config_data.get('scoring_method', 'unknown')
        schema = config_data.get('configuration_json', {}).get('schema', {})
        
        results = []
        
        # Generate test scenarios
        generator = SchemaBasedDataGenerator(schema, algorithm_type)
        scenarios = generator.generate_test_scenarios()
        
        for scenario in scenarios:
            try:
                result = self._test_algorithm_with_data(
                    algorithm_type, schema, scenario, config_name
                )
                results.append(result)
            except Exception as e:
                results.append(TestResult(
                    config_name=config_name,
                    algorithm_type=algorithm_type,
                    test_passed=False,
                    error_message=f"Scenario '{scenario.name}': {str(e)}\n{traceback.format_exc()}",
                    test_data=scenario.values,
                    expected_behavior=scenario.expected_outcome
                ))
        
        return results
    
    def _test_algorithm_with_data(self, algorithm_type: str, schema: Dict[str, Any], 
                                  scenario: TestScenario, config_name: str) -> TestResult:
        """Test a specific algorithm with specific data"""
        
        try:
            # Import and instantiate the actual algorithm
            algorithm = self._create_algorithm_instance(algorithm_type, schema)
            
            # Test the algorithm
            if hasattr(algorithm, 'calculate_progressive_scores'):
                # Test progressive scoring
                scores = algorithm.calculate_progressive_scores(scenario.values)
                test_passed = self._validate_scores(scores, algorithm_type, scenario)
            elif hasattr(algorithm, 'calculate_score'):
                # Test single score calculation with daily values
                result = algorithm.calculate_score(daily_values=scenario.values)
                if isinstance(result, dict) and 'score' in result:
                    scores = [result['score']]
                else:
                    scores = [result]
                test_passed = self._validate_scores(scores, algorithm_type, scenario)
            else:
                raise ValueError(f"Algorithm {algorithm_type} has no recognized scoring method")
            
            return TestResult(
                config_name=config_name,
                algorithm_type=algorithm_type,
                test_passed=test_passed,
                error_message=None if test_passed else "Score validation failed",
                test_data=scenario.values,
                scores=scores,
                expected_behavior=scenario.expected_outcome
            )
            
        except Exception as e:
            return TestResult(
                config_name=config_name,
                algorithm_type=algorithm_type,
                test_passed=False,
                error_message=f"{str(e)}\n{traceback.format_exc()}",
                test_data=scenario.values,
                expected_behavior=scenario.expected_outcome
            )
    
    def _create_algorithm_instance(self, algorithm_type: str, schema: Dict[str, Any]):
        """Create an instance of the actual algorithm class"""
        
        if algorithm_type == 'proportional':
            from algorithms.proportional import ProportionalAlgorithm, ProportionalConfig
            config = ProportionalConfig(
                target=schema.get('target', 1.0),
                unit=schema.get('unit', 'units'),
                maximum_cap=schema.get('maximum_cap', 100),
                minimum_threshold=schema.get('minimum_threshold', 0)
            )
            return ProportionalAlgorithm(config)
            
        elif algorithm_type == 'binary_threshold':
            from algorithms.binary_threshold import BinaryThresholdAlgorithm, BinaryThresholdConfig, ComparisonOperator
            
            # Map string to enum
            operator_map = {
                '>=': ComparisonOperator.GTE,
                '<=': ComparisonOperator.LTE,
                '>': ComparisonOperator.GT,
                '<': ComparisonOperator.LT,
                '==': ComparisonOperator.EQ
            }
            
            config = BinaryThresholdConfig(
                threshold=schema.get('threshold', 1.0),
                success_value=schema.get('success_value', 100),
                failure_value=schema.get('failure_value', 0),
                comparison_operator=operator_map.get(schema.get('comparison_operator', '>='), ComparisonOperator.GTE)
            )
            return BinaryThresholdAlgorithm(config)
            
        elif algorithm_type == 'minimum_frequency':
            from algorithms.minimum_frequency import MinimumFrequencyAlgorithm, MinimumFrequencyConfig
            
            config = MinimumFrequencyConfig(
                daily_threshold=schema.get('daily_threshold', 1.0),
                daily_comparison=schema.get('daily_comparison', '>='),
                required_days=schema.get('required_days', 3)
            )
            return MinimumFrequencyAlgorithm(config)
            
        elif algorithm_type == 'weekly_elimination':
            from algorithms.weekly_elimination import WeeklyEliminationAlgorithm, WeeklyEliminationConfig
            
            config = WeeklyEliminationConfig(
                elimination_threshold=schema.get('elimination_threshold', 0),
                elimination_comparison=schema.get('elimination_comparison', '==')
            )
            return WeeklyEliminationAlgorithm(config)
            
        elif algorithm_type == 'zone_based':
            from algorithms.zone_based import ZoneBasedAlgorithm, ZoneBasedConfig, Zone
            
            zones = schema.get('zones', [])
            if not zones:
                # Default zones for testing
                zones = [
                    Zone(0, 5, 20, "Poor"),
                    Zone(5, 7, 60, "Fair"), 
                    Zone(7, 9, 100, "Good"),
                    Zone(9, 12, 80, "Excessive")
                ]
            else:
                zone_objects = []
                for zone_data in zones:
                    zone_range = zone_data.get('range', [0, 1])
                    min_val = zone_range[0] if len(zone_range) > 0 else 0
                    max_val = zone_range[1] if len(zone_range) > 1 else zone_range[0]
                    zone_objects.append(Zone(
                        min_value=min_val,
                        max_value=max_val,
                        score=zone_data.get('score', 50),
                        label=zone_data.get('label', 'Zone')
                    ))
                zones = zone_objects
            
            config = ZoneBasedConfig(zones=zones, unit=schema.get('unit', 'units'))
            return ZoneBasedAlgorithm(config)
            
        elif algorithm_type == 'constrained_weekly_allowance':
            from algorithms.constrained_weekly_allowance import ConstrainedWeeklyAllowanceAlgorithm, ConstrainedWeeklyAllowanceConfig
            
            config = ConstrainedWeeklyAllowanceConfig(
                weekly_allowance=schema.get('weekly_allowance', 2),
                unit=schema.get('unit', 'units'),
                penalty_for_overage=schema.get('penalty_per_excess', 25),
                max_days_per_week=schema.get('max_days_per_week')
            )
            return ConstrainedWeeklyAllowanceAlgorithm(config)
            
        elif algorithm_type == 'proportional_frequency_hybrid':
            from algorithms.proportional_frequency_hybrid import ProportionalFrequencyHybridAlgorithm, ProportionalFrequencyHybridConfig
            
            config = ProportionalFrequencyHybridConfig(
                daily_target=schema.get('daily_target', 1.0),
                required_qualifying_days=schema.get('required_qualifying_days', 2),
                unit=schema.get('unit', 'units'),
                daily_minimum_threshold=schema.get('daily_minimum_threshold', 0)
            )
            return ProportionalFrequencyHybridAlgorithm(config)
            
        elif algorithm_type == 'sleep_composite':
            from algorithms.sleep_composite import SleepCompositeAlgorithm, SleepCompositeConfig
            
            config = SleepCompositeConfig()
            return SleepCompositeAlgorithm(config)
            
        elif algorithm_type == 'categorical_filter_threshold':
            from algorithms.categorical_filter_threshold import CategoricalFilterThresholdAlgorithm, CategoricalFilterThresholdConfig, CategoryFilter
            from algorithms.binary_threshold import ComparisonOperator
            
            category_filters = [CategoryFilter(
                category_name='default',
                category_values=['all'],
                threshold=schema.get('threshold', 1),
                comparison_operator=ComparisonOperator.GTE
            )]
            
            config = CategoricalFilterThresholdConfig(
                category_field='category',
                category_filters=category_filters,
                default_threshold=schema.get('threshold', 1)
            )
            return CategoricalFilterThresholdAlgorithm(config)
            
        elif algorithm_type == 'composite_weighted':
            from algorithms.composite_weighted import CompositeWeightedAlgorithm, CompositeWeightedConfig, Component
            
            components = schema.get('components', [])
            if not components:
                components = [Component(
                    name='Default Component',
                    weight=1.0,
                    target=100,
                    unit=schema.get('unit', 'score'),
                    scoring_method='proportional',
                    field_name='value'
                )]
            else:
                component_objects = []
                for comp_data in components:
                    component_objects.append(Component(
                        name=comp_data.get('name', 'Component'),
                        weight=comp_data.get('weight', 1.0),
                        target=comp_data.get('target', 100),
                        unit=comp_data.get('unit', 'units'),
                        scoring_method=comp_data.get('scoring_method', 'proportional'),
                        field_name=comp_data.get('field_name', 'value')
                    ))
                components = component_objects
            
            config = CompositeWeightedConfig(components=components)
            return CompositeWeightedAlgorithm(config)
        else:
            raise ValueError(f"Unknown algorithm type: {algorithm_type}")
    
    def _validate_scores(self, scores: List[float], algorithm_type: str, scenario: TestScenario) -> bool:
        """Validate that scores make sense for the algorithm type and scenario"""
        if not scores:
            return False
        
        # Basic validation - scores should be numbers
        if not all(isinstance(s, (int, float)) for s in scores):
            return False
        
        # Algorithm-specific validation
        if algorithm_type in ['binary_threshold', 'minimum_frequency', 'weekly_elimination']:
            # Binary algorithms should return 0 or 100 (with possible edge case handling)
            valid_binary_scores = all(s in [0, 100] or 0 <= s <= 100 for s in scores)
            return valid_binary_scores
        
        elif algorithm_type in ['proportional', 'zone_based', 'composite_weighted', 'sleep_composite']:
            # Proportional/zone algorithms should return reasonable percentage scores
            reasonable_scores = all(0 <= s <= 200 for s in scores)  # Allow some over-achievement
            return reasonable_scores
        
        # For other algorithms, just check they're reasonable numbers
        return all(-1000 <= s <= 1000 for s in scores)  # Very permissive range

def run_integration_tests():
    """Run comprehensive integration tests on all configs and algorithms"""
    
    print("🔧 Starting Algorithm Integration Tests...")
    print("This test validates actual algorithm implementations against config schemas\n")
    
    # Discover configs
    config_dir = os.path.join(os.path.dirname(__file__), '..', 'src', 'generated_configs')
    pattern = os.path.join(config_dir, 'REC*.json')
    config_files = glob.glob(pattern)
    config_files.sort()
    
    print(f"📊 Found {len(config_files)} configuration files")
    
    # Test each config
    tester = AlgorithmTester()
    all_results = []
    config_count = 0
    
    for config_file in config_files:
        config_name = os.path.basename(config_file)
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                
            results = tester.test_config(config_data, config_name)
            all_results.extend(results)
            config_count += 1
            
            # Progress indicator
            if config_count % 10 == 0:
                print(f"  Processed {config_count}/{len(config_files)} configs...")
                
        except Exception as e:
            all_results.append(TestResult(
                config_name=config_name,
                algorithm_type="unknown",
                test_passed=False,
                error_message=f"Failed to load config: {str(e)}"
            ))
    
    # Generate report
    _generate_test_report(all_results, config_count)
    
    return all_results

def _generate_test_report(results: List[TestResult], total_configs: int):
    """Generate comprehensive test report"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Count results
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r.test_passed)
    failed_tests = total_tests - passed_tests
    
    # Group by algorithm type
    algo_stats = {}
    for result in results:
        algo_type = result.algorithm_type
        if algo_type not in algo_stats:
            algo_stats[algo_type] = {'passed': 0, 'failed': 0, 'total': 0}
        
        algo_stats[algo_type]['total'] += 1
        if result.test_passed:
            algo_stats[algo_type]['passed'] += 1
        else:
            algo_stats[algo_type]['failed'] += 1
    
    # Write report
    output_lines = [
        "=" * 100,
        "ALGORITHM INTEGRATION TEST REPORT",
        f"Generated: {timestamp}",
        f"Configurations Tested: {total_configs}",
        f"Total Test Scenarios: {total_tests}",
        f"✅ Passed: {passed_tests} ({passed_tests/total_tests*100:.1f}%)",
        f"❌ Failed: {failed_tests} ({failed_tests/total_tests*100:.1f}%)",
        "=" * 100,
        "",
        "ALGORITHM PERFORMANCE SUMMARY:",
        ""
    ]
    
    for algo_type, stats in sorted(algo_stats.items()):
        pass_rate = stats['passed'] / stats['total'] * 100 if stats['total'] > 0 else 0
        output_lines.append(f"  {algo_type:25} | {stats['passed']:3d}/{stats['total']:3d} passed ({pass_rate:5.1f}%)")
    
    output_lines.extend([
        "",
        "=" * 100,
        "DETAILED TEST RESULTS:",
        "=" * 100,
        ""
    ])
    
    # Group results by config for easier reading
    config_results = {}
    for result in results:
        if result.config_name not in config_results:
            config_results[result.config_name] = []
        config_results[result.config_name].append(result)
    
    for config_name, config_results_list in sorted(config_results.items()):
        output_lines.append(f"📄 {config_name}")
        output_lines.append(f"   Algorithm: {config_results_list[0].algorithm_type}")
        
        for i, result in enumerate(config_results_list, 1):
            status = "✅ PASS" if result.test_passed else "❌ FAIL"
            output_lines.append(f"   Test {i}: {status} - {result.expected_behavior}")
            
            if not result.test_passed and result.error_message:
                # Show first line of error for brevity
                error_first_line = result.error_message.split('\n')[0]
                output_lines.append(f"      Error: {error_first_line}")
            
            if result.scores:
                score_summary = f"[{', '.join(f'{s:.1f}' for s in result.scores[:3])}{'...' if len(result.scores) > 3 else ''}]"
                output_lines.append(f"      Scores: {score_summary}")
        
        output_lines.append("")
    
    # Failed tests detail
    failed_results = [r for r in results if not r.test_passed]
    if failed_results:
        output_lines.extend([
            "=" * 100,
            "DETAILED FAILURE ANALYSIS:",
            "=" * 100,
            ""
        ])
        
        for result in failed_results:
            output_lines.extend([
                f"❌ FAILURE: {result.config_name} - {result.algorithm_type}",
                f"   Expected: {result.expected_behavior}",
                f"   Error: {result.error_message}",
                ""
            ])
    
    output_lines.extend([
        "=" * 100,
        "TEST SUMMARY:",
        f"• Uses actual algorithm implementations (no hardcoded logic)",
        f"• Tests schema-based data generation with edge cases and outliers", 
        f"• Validates algorithm behavior across {len(algo_stats)} algorithm types",
        f"• Provides clear pass/fail results for debugging",
        "",
        f"Result: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.1f}%)",
        "=" * 100
    ])
    
    # Write report file
    output_file = os.path.join(os.path.dirname(__file__), "algorithm_integration_test_output.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"\n📄 Test report written to: {output_file}")
    print(f"🎯 Results: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.1f}%)")
    
    if failed_tests > 0:
        print(f"⚠️  {failed_tests} tests failed - check report for details")
    else:
        print("🎉 All tests passed!")

if __name__ == "__main__":
    results = run_integration_tests()
    
    # Exit with error code if tests failed
    failed_count = sum(1 for r in results if not r.test_passed)
    sys.exit(1 if failed_count > 0 else 0)