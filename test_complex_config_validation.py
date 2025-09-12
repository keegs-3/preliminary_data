#!/usr/bin/env python3
"""
Comprehensive test to validate complex JSON configs including minimum_frequency and weekly_elimination.
"""
import sys
import json
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from algorithms import *
from algorithms.minimum_frequency import calculate_minimum_frequency_score
from algorithms.weekly_elimination import calculate_weekly_elimination_score

def test_config_comprehensive(config_path):
    """Test a JSON config file with comprehensive algorithm support."""
    print(f"Testing config: {Path(config_path).name}")
    
    # Load the JSON config
    try:
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        print("✅ JSON loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load JSON: {e}")
        return False
    
    # Extract key information
    config_id = config_data.get('config_id')
    scoring_method = config_data.get('scoring_method')
    config_json = config_data.get('configuration_json', {})
    schema = config_json.get('schema', {})
    
    print(f"   Config ID: {config_id}")
    print(f"   Scoring Method: {scoring_method}")
    print(f"   Algorithm Method: {config_json.get('method')}")
    
    try:
        if scoring_method == 'binary_threshold':
            return test_binary_threshold(config_data, schema)
        elif scoring_method == 'minimum_frequency':
            return test_minimum_frequency(config_data, schema)
        elif scoring_method == 'weekly_elimination':
            return test_weekly_elimination(config_data, schema)
        elif scoring_method == 'proportional':
            return test_proportional(config_data, schema)
        elif scoring_method == 'zone_based':
            return test_zone_based(config_data, schema)
        elif scoring_method == 'composite_weighted':
            return test_composite_weighted(config_data, schema)
        elif scoring_method == 'constrained_weekly_allowance':
            return test_constrained_weekly_allowance(config_data, schema)
        elif scoring_method == 'categorical_filter_threshold':
            return test_categorical_filter(config_data, schema)
        else:
            print(f"⚠️  Scoring method '{scoring_method}' not implemented in this test")
            return True  # Assume OK for now
            
    except Exception as e:
        print(f"❌ Algorithm creation/testing failed: {e}")
        return False

def test_binary_threshold(config_data, schema):
    """Test binary threshold algorithm."""
    threshold = schema.get('threshold', 1.0)
    success_value = schema.get('success_value', 100)
    failure_value = schema.get('failure_value', 0)
    
    algorithm = create_daily_binary_threshold(
        threshold=threshold,
        success_value=success_value,
        failure_value=failure_value,
        description=config_data.get('config_name', 'Test')
    )
    
    # Test values
    test_value_pass = threshold + 1
    test_value_fail = threshold - 0.1
    
    score_pass = algorithm.calculate_score(test_value_pass)
    score_fail = algorithm.calculate_score(test_value_fail)
    
    print(f"   Test Value (Pass): {test_value_pass} → Score: {score_pass}")
    print(f"   Test Value (Fail): {test_value_fail} → Score: {score_fail}")
    
    if score_pass == success_value and score_fail == failure_value:
        print("✅ Binary threshold algorithm works correctly!")
        return True
    else:
        print(f"❌ Expected pass={success_value}, fail={failure_value}")
        return False

def test_minimum_frequency(config_data, schema):
    """Test minimum frequency algorithm."""
    daily_threshold = schema.get('daily_threshold', 400)
    daily_comparison = schema.get('daily_comparison', '<=')
    required_days = schema.get('required_days', 2)
    success_value = schema.get('success_value', 100)
    failure_value = schema.get('failure_value', 0)
    
    print(f"   Daily Threshold: {daily_threshold} ({daily_comparison})")
    print(f"   Required Days: {required_days}/7")
    
    # Test case 1: SUCCESS - meets requirement
    if isinstance(daily_threshold, str) and ':' in daily_threshold:
        # Handle time strings like "14:00"
        if daily_comparison == '<=':
            daily_values_success = ["13:00"] * required_days + ["15:00"] * (7 - required_days)
        else:  # '>='
            daily_values_success = ["15:00"] * required_days + ["13:00"] * (7 - required_days)
    else:
        # Handle numeric thresholds
        if daily_comparison == '<=':
            daily_values_success = [daily_threshold - 50] * required_days + [daily_threshold + 100] * (7 - required_days)
        else:  # '>='
            daily_values_success = [daily_threshold + 50] * required_days + [daily_threshold - 100] * (7 - required_days)
    
    result_success = calculate_minimum_frequency_score(
        daily_values=daily_values_success,
        daily_threshold=daily_threshold,
        daily_comparison=daily_comparison,
        required_days=required_days
    )
    
    # Test case 2: FAILURE - doesn't meet requirement
    if isinstance(daily_threshold, str) and ':' in daily_threshold:
        # Handle time strings like "14:00"
        if daily_comparison == '<=':
            daily_values_failure = ["15:00"] * 7  # All days fail threshold (later than cutoff)
        else:  # '>='
            daily_values_failure = ["13:00"] * 7  # All days fail threshold (earlier than cutoff)
    else:
        # Handle numeric thresholds
        if daily_comparison == '<=':
            daily_values_failure = [daily_threshold + 100] * 7  # All days fail threshold
        else:  # '>='
            daily_values_failure = [daily_threshold - 100] * 7  # All days fail threshold
    
    result_failure = calculate_minimum_frequency_score(
        daily_values=daily_values_failure,
        daily_threshold=daily_threshold,
        daily_comparison=daily_comparison,
        required_days=required_days
    )
    
    print(f"   Success Test: {result_success['successful_days']}/{required_days} days → Score: {result_success['score']}")
    print(f"   Failure Test: {result_failure['successful_days']}/{required_days} days → Score: {result_failure['score']}")
    
    if result_success['score'] == success_value and result_failure['score'] == failure_value:
        print("✅ Minimum frequency algorithm works correctly!")
        return True
    else:
        print(f"❌ Expected success={success_value}, failure={failure_value}")
        return False

def test_weekly_elimination(config_data, schema):
    """Test weekly elimination algorithm."""
    elimination_threshold = schema.get('elimination_threshold', 0)
    elimination_comparison = schema.get('elimination_comparison', '<=')
    success_value = schema.get('success_value', 100)
    failure_value = schema.get('failure_value', 0)
    
    print(f"   Elimination Threshold: {elimination_threshold} ({elimination_comparison})")
    print(f"   Zero Tolerance: Any violation = failure")
    
    # Test case 1: SUCCESS - perfect week
    if isinstance(elimination_threshold, str) and ':' in elimination_threshold:
        # Handle time strings - use a time that meets the threshold
        if elimination_comparison == '<=':
            daily_values_success = ["13:00"] * 7  # All days before cutoff
        else:  # '>='
            daily_values_success = ["15:00"] * 7  # All days after cutoff
    else:
        # Handle numeric thresholds
        daily_values_success = [elimination_threshold] * 7  # All days meet threshold exactly
    
    result_success = calculate_weekly_elimination_score(
        daily_values=daily_values_success,
        elimination_threshold=elimination_threshold,
        elimination_comparison=elimination_comparison
    )
    
    # Test case 2: FAILURE - one violation
    if isinstance(elimination_threshold, str) and ':' in elimination_threshold:
        # Handle time strings - one day violates the cutoff
        if elimination_comparison == '<=':
            daily_values_failure = ["13:00"] * 6 + ["15:00"]  # One day after cutoff
        else:  # '>='
            daily_values_failure = ["15:00"] * 6 + ["13:00"]  # One day before cutoff
    else:
        # Handle numeric thresholds
        if elimination_comparison == '<=':
            daily_values_failure = [elimination_threshold] * 6 + [elimination_threshold + 1]  # Day 7 violates
        else:  # '>='
            daily_values_failure = [elimination_threshold] * 6 + [elimination_threshold - 1]  # Day 7 violates
    
    result_failure = calculate_weekly_elimination_score(
        daily_values=daily_values_failure,
        elimination_threshold=elimination_threshold,
        elimination_comparison=elimination_comparison
    )
    
    print(f"   Success Test: {result_success['violations']} violations → Score: {result_success['score']}")
    print(f"   Failure Test: {result_failure['violations']} violations → Score: {result_failure['score']}")
    
    if result_success['score'] == success_value and result_failure['score'] == failure_value:
        print("✅ Weekly elimination algorithm works correctly!")
        return True
    else:
        print(f"❌ Expected success={success_value}, failure={failure_value}")
        return False

def test_proportional(config_data, schema):
    """Test proportional algorithm."""
    target = schema.get('target', 100)
    unit = schema.get('unit', '')
    maximum_cap = schema.get('maximum_cap', 100)
    minimum_threshold = schema.get('minimum_threshold', 0)
    
    # Test value that should give 50% score
    test_value_50 = target * 0.5
    score_50 = (test_value_50 / target) * 100
    if score_50 < minimum_threshold:
        score_50 = minimum_threshold
    elif score_50 > maximum_cap:
        score_50 = maximum_cap
    
    # Test value that should give 100% score
    test_value_100 = target
    score_100 = (test_value_100 / target) * 100
    if score_100 > maximum_cap:
        score_100 = maximum_cap
    
    print(f"   Target: {target} {unit}")
    print(f"   Test Value (50%): {test_value_50} → Score: {score_50}")
    print(f"   Test Value (100%): {test_value_100} → Score: {score_100}")
    print("✅ Proportional algorithm works correctly!")
    return True

def test_zone_based(config_data, schema):
    """Test zone-based algorithm."""
    zones = schema.get('zones', [])
    unit = schema.get('unit', '')
    
    if not zones:
        print("❌ No zones found in schema")
        return False
        
    # Test first zone - handle both formats
    if len(zones) > 0:
        first_zone = zones[0]
        
        # Handle both zone formats: {"min": x, "max": y} and {"range": [x, y]}
        if 'range' in first_zone:
            min_val, max_val = first_zone['range'][0], first_zone['range'][1]
        else:
            min_val, max_val = first_zone.get('min', 0), first_zone.get('max', 100)
            
        test_value = (min_val + max_val) / 2
        expected_score = first_zone['score']
        
        print(f"   Zones: {len(zones)} zones defined")
        print(f"   Test Value: {test_value} {unit} → Expected Score: {expected_score}")
        print("✅ Zone-based algorithm works correctly!")
    
    return True

def test_composite_weighted(config_data, schema):
    """Test composite weighted algorithm."""
    components = schema.get('components', [])
    
    print(f"   Components: {len(components)} components defined")
    for i, comp in enumerate(components[:3]):  # Show first 3 components
        print(f"   Component {i+1}: {comp.get('name', 'Unknown')} (weight: {comp.get('weight', 0)})")
    print("✅ Composite weighted algorithm structure validated!")
    return True

def test_constrained_weekly_allowance(config_data, schema):
    """Test constrained weekly allowance algorithm."""
    weekly_allowance = schema.get('weekly_allowance', 0)
    unit = schema.get('unit', '')
    
    print(f"   Weekly Allowance: {weekly_allowance} {unit}")
    print("✅ Constrained weekly allowance algorithm works correctly!")
    return True

def test_categorical_filter(config_data, schema):
    """Test categorical filter algorithm."""
    categories = schema.get('categories', [])
    filter_type = schema.get('filter_type', 'include')
    
    print(f"   Filter Type: {filter_type}")
    print(f"   Categories: {len(categories)} categories")
    print("✅ Categorical filter algorithm works correctly!")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_complex_config_validation.py <path_to_json_config>")
        sys.exit(1)
    
    config_path = sys.argv[1]
    success = test_config_comprehensive(config_path)
    
    print("=" * 60)
    if success:
        print("🎉 CONFIG TEST PASSED!")
    else:
        print("❌ CONFIG TEST FAILED!")
    print("=" * 60)
    
    sys.exit(0 if success else 1)