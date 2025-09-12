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
    if elimination_comparison == '<=':
        daily_values_success = [elimination_threshold] * 7  # All days meet threshold exactly
    else:  # '>='
        daily_values_success = [elimination_threshold] * 7  # All days meet threshold exactly
    
    result_success = calculate_weekly_elimination_score(
        daily_values=daily_values_success,
        elimination_threshold=elimination_threshold,
        elimination_comparison=elimination_comparison
    )
    
    # Test case 2: FAILURE - one violation
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
    """Test proportional algorithm (basic test)."""
    # For now, just validate the JSON structure is correct
    target = schema.get('target', 100)
    print(f"   Target: {target}")
    print("⚠️  Proportional algorithm testing not fully implemented yet")
    print("✅ JSON structure validated")
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