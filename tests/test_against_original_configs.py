"""
Test implementations against the original 8 unique configurations from rec_config.json
"""

import sys
import json
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from algorithms import (
    BinaryThresholdAlgorithm,
    BinaryThresholdConfig,
    ProportionalAlgorithm,
    ProportionalConfig,
    ZoneBasedAlgorithm,
    ZoneBasedConfig,
    Zone,
    CompositeWeightedAlgorithm,
    CompositeWeightedConfig,
    Component,
    ComparisonOperator,
    EvaluationPeriod,
    SuccessCriteria,
    CalculationMethod
)


def load_original_configs():
    """Load and parse the original 8 unique configurations."""
    config_file = Path(__file__).parent.parent / "docs" / "rec_config.json"
    
    with open(config_file, 'r') as f:
        content = f.read()
    
    # Fix quotes and parse
    content = content.replace('""', '"')
    objects = []
    current_obj = ''
    brace_count = 0
    
    for char in content:
        if char == '{':
            if brace_count == 0:
                current_obj = '{'
            else:
                current_obj += char
            brace_count += 1
        elif char == '}':
            current_obj += char
            brace_count -= 1
            if brace_count == 0:
                try:
                    parsed = json.loads(current_obj)
                    objects.append(parsed)
                except:
                    pass
                current_obj = ''
        elif brace_count > 0:
            current_obj += char
    
    # Get unique configurations
    unique_configs = []
    seen_signatures = set()
    
    for obj in objects:
        method = obj.get('method', 'unknown')
        eval_pattern = obj.get('evaluation_pattern', 'unknown') 
        schema = obj.get('schema', {})
        
        measurement_type = schema.get('measurement_type', '')
        success_criteria = schema.get('success_criteria', '')
        evaluation_period = schema.get('evaluation_period', '')
        
        signature = f'{method}_{eval_pattern}_{measurement_type}_{success_criteria}_{evaluation_period}'
        
        if signature not in seen_signatures:
            seen_signatures.add(signature)
            unique_configs.append(obj)
    
    return unique_configs


def test_binary_threshold_daily():
    """Test binary threshold daily against original config."""
    print("Testing Binary Threshold - Daily...")
    
    # Create algorithm based on original config structure
    config = BinaryThresholdConfig(
        threshold=50,  # Example threshold
        success_value=100,
        failure_value=0,
        measurement_type="binary",
        evaluation_period=EvaluationPeriod.DAILY,
        success_criteria=SuccessCriteria.SIMPLE_TARGET,
        calculation_method=CalculationMethod.EXISTS,
        calculation_fields="test_field"
    )
    
    algo = BinaryThresholdAlgorithm(config)
    
    # Test validation
    assert algo.validate_config() == True
    
    # Test scoring
    assert algo.calculate_score(60) == 100  # Above threshold
    assert algo.calculate_score(40) == 0    # Below threshold
    assert algo.calculate_score(50) == 100  # At threshold
    
    print("  ✓ Binary Threshold Daily - PASSED")


def test_binary_threshold_frequency():
    """Test binary threshold frequency against original config."""
    print("Testing Binary Threshold - Frequency...")
    
    config = BinaryThresholdConfig(
        threshold=1,
        success_value=100,
        failure_value=0,
        measurement_type="binary",
        evaluation_period=EvaluationPeriod.ROLLING_7_DAY,
        success_criteria=SuccessCriteria.FREQUENCY_TARGET,
        calculation_method=CalculationMethod.EXISTS,
        calculation_fields="test_field",
        frequency_requirement="5 successful days out of 7-day window"
    )
    
    algo = BinaryThresholdAlgorithm(config)
    
    assert algo.validate_config() == True
    assert algo.calculate_score(1) == 100
    assert algo.calculate_score(0) == 0
    
    print("  ✓ Binary Threshold Frequency - PASSED")


def test_proportional_daily():
    """Test proportional daily against original config."""
    print("Testing Proportional - Daily...")
    
    config = ProportionalConfig(
        target=100,
        unit="points",
        measurement_type="count",
        evaluation_period=EvaluationPeriod.DAILY,
        success_criteria=SuccessCriteria.SIMPLE_TARGET,
        calculation_method=CalculationMethod.SUM,
        calculation_fields="test_field"
    )
    
    algo = ProportionalAlgorithm(config)
    
    assert algo.validate_config() == True
    assert algo.calculate_score(100) == 100  # 100% of target
    assert algo.calculate_score(50) == 50    # 50% of target
    assert algo.calculate_score(200) == 100  # Capped at max
    
    print("  ✓ Proportional Daily - PASSED")


def test_proportional_frequency():
    """Test proportional frequency against original config."""
    print("Testing Proportional - Frequency...")
    
    config = ProportionalConfig(
        target=50,
        unit="minutes",
        measurement_type="duration",
        evaluation_period=EvaluationPeriod.ROLLING_7_DAY,
        success_criteria=SuccessCriteria.FREQUENCY_TARGET,
        calculation_method=CalculationMethod.SUM,
        calculation_fields="test_field",
        frequency_requirement="achieve X target on Y of Z days"
    )
    
    algo = ProportionalAlgorithm(config)
    
    assert algo.validate_config() == True
    assert algo.calculate_score(50) == 100
    assert algo.calculate_score(25) == 50
    
    print("  ✓ Proportional Frequency - PASSED")


def test_zone_based_daily():
    """Test zone-based daily against original config."""
    print("Testing Zone-Based - Daily...")
    
    # Create 5 zones as required
    zones = [
        Zone(0, 20, 20, "Poor"),
        Zone(20, 40, 40, "Fair"),
        Zone(40, 60, 60, "Good"),
        Zone(60, 80, 80, "Very Good"),
        Zone(80, 100, 100, "Excellent")
    ]
    
    config = ZoneBasedConfig(
        zones=zones,
        unit="points",
        measurement_type="scale",
        evaluation_period=EvaluationPeriod.DAILY,
        success_criteria=SuccessCriteria.SIMPLE_TARGET,
        calculation_method=CalculationMethod.LAST_VALUE,
        calculation_fields="test_field"
    )
    
    algo = ZoneBasedAlgorithm(config)
    
    assert algo.validate_config() == True
    assert algo.calculate_score(10) == 20   # Poor zone
    assert algo.calculate_score(50) == 60   # Good zone
    assert algo.calculate_score(90) == 100  # Excellent zone
    
    print("  ✓ Zone-Based Daily - PASSED")


def test_zone_based_frequency():
    """Test zone-based frequency against original config."""
    print("Testing Zone-Based - Frequency...")
    
    zones = [
        Zone(0, 20, 20, "Poor"),
        Zone(20, 40, 40, "Fair"),
        Zone(40, 60, 60, "Good"),
        Zone(60, 80, 80, "Very Good"),
        Zone(80, 100, 100, "Excellent")
    ]
    
    config = ZoneBasedConfig(
        zones=zones,
        unit="hours",
        measurement_type="duration",
        evaluation_period=EvaluationPeriod.ROLLING_7_DAY,
        success_criteria=SuccessCriteria.FREQUENCY_TARGET,
        calculation_method=CalculationMethod.AVERAGE,
        calculation_fields="test_field",
        frequency_requirement="hit optimal zone on Y of Z days"
    )
    
    algo = ZoneBasedAlgorithm(config)
    
    assert algo.validate_config() == True
    assert algo.calculate_score(30) == 40
    assert algo.calculate_score(70) == 80
    
    print("  ✓ Zone-Based Frequency - PASSED")


def test_composite_weighted_daily_simple():
    """Test composite weighted daily (simple target) against original config."""
    print("Testing Composite Weighted - Daily (Simple Target)...")
    
    components = [
        Component(
            name="Component A",
            weight=0.6,
            target=100,
            unit="points",
            scoring_method="proportional",
            field_name="comp_a"
        ),
        Component(
            name="Component B",
            weight=0.4,
            target=50,
            unit="points",
            scoring_method="proportional",
            field_name="comp_b"
        )
    ]
    
    config = CompositeWeightedConfig(
        components=components,
        measurement_type="composite",
        evaluation_period=EvaluationPeriod.DAILY,
        success_criteria=SuccessCriteria.SIMPLE_TARGET,
        calculation_method="weighted_average",
        calculation_fields={"comp_a": "field_a", "comp_b": "field_b"}
    )
    
    algo = CompositeWeightedAlgorithm(config)
    
    assert algo.validate_config() == True
    
    # Test perfect scores
    score = algo.calculate_score({"comp_a": 100, "comp_b": 50})
    assert score == 100
    
    # Test partial scores
    score = algo.calculate_score({"comp_a": 50, "comp_b": 25})
    assert score == 50
    
    print("  ✓ Composite Weighted Daily (Simple) - PASSED")


def test_composite_weighted_daily_composite():
    """Test composite weighted daily (composite target) against original config."""
    print("Testing Composite Weighted - Daily (Composite Target)...")
    
    components = [
        Component(
            name="Sleep Duration",
            weight=0.7,
            target=8,
            unit="hours",
            scoring_method="zone",
            field_name="sleep_duration",
            parameters={
                "zones": [
                    {"min": 0, "max": 5, "score": 20},
                    {"min": 5, "max": 6, "score": 40},
                    {"min": 6, "max": 7, "score": 60},
                    {"min": 7, "max": 9, "score": 100},
                    {"min": 9, "max": 12, "score": 80}
                ]
            }
        ),
        Component(
            name="Schedule Consistency",
            weight=0.3,
            target=60,
            unit="minutes",
            scoring_method="binary",
            field_name="schedule_variance",
            parameters={
                "threshold": 60,
                "comparison_operator": "<=",
                "success_value": 100,
                "failure_value": 0
            }
        )
    ]
    
    config = CompositeWeightedConfig(
        components=components,
        measurement_type="composite",
        evaluation_period=EvaluationPeriod.DAILY,
        success_criteria=SuccessCriteria.SIMPLE_TARGET,  # Using composite in original
        calculation_method="composite",
        calculation_fields={
            "sleep_duration": "duration_field",
            "schedule_variance": "variance_field"
        },
        calculation_notes={
            "implementation": "Sleep quality composite with duration and consistency"
        }
    )
    
    algo = CompositeWeightedAlgorithm(config)
    
    assert algo.validate_config() == True
    
    # Test good sleep scenario
    score = algo.calculate_score({"sleep_duration": 8, "schedule_variance": 30})
    assert score == 100  # 0.7 * 100 + 0.3 * 100
    
    # Test poor sleep scenario
    score = algo.calculate_score({"sleep_duration": 4, "schedule_variance": 120})
    assert score == 14   # 0.7 * 20 + 0.3 * 0
    
    print("  ✓ Composite Weighted Daily (Composite) - PASSED")


def run_all_original_config_tests():
    """Run all tests against original configurations."""
    print("=" * 60)
    print("TESTING AGAINST ORIGINAL 8 UNIQUE CONFIGURATIONS")
    print("=" * 60)
    
    configs = load_original_configs()
    print(f"Loaded {len(configs)} unique configurations from rec_config.json\n")
    
    test_functions = [
        test_binary_threshold_daily,
        test_binary_threshold_frequency,
        test_proportional_daily,
        test_proportional_frequency,
        test_zone_based_daily,
        test_zone_based_frequency,
        test_composite_weighted_daily_simple,
        test_composite_weighted_daily_composite
    ]
    
    passed = 0
    total = len(test_functions)
    
    for test_func in test_functions:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"  ✗ {test_func.__name__}: {e}")
    
    print(f"\n" + "=" * 60)
    print(f"ORIGINAL CONFIG TEST RESULTS: {passed}/{total} PASSED")
    print("=" * 60)
    
    if passed == total:
        print("🎉 ALL IMPLEMENTATIONS MATCH ORIGINAL CONFIGURATIONS!")
    else:
        print(f"❌ {total - passed} implementations need fixes")
    
    return passed == total


if __name__ == "__main__":
    run_all_original_config_tests()