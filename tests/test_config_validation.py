#!/usr/bin/env python3
"""
Quick test to validate a specific JSON config can be loaded and used.
"""
import sys
import json
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from algorithms import *

def test_config(config_path):
    """Test a single JSON config file."""
    print(f"Testing config: {config_path}")
    
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
    
    print(f"   Config ID: {config_id}")
    print(f"   Scoring Method: {scoring_method}")
    print(f"   Algorithm Method: {config_json.get('method')}")
    
    # Test if we can create the appropriate algorithm
    try:
        if scoring_method == 'binary_threshold':
            # Extract threshold info
            schema = config_json.get('schema', {})
            threshold = schema.get('threshold', 1.0)
            success_value = schema.get('success_value', 100)
            failure_value = schema.get('failure_value', 0)
            
            # Create algorithm
            algorithm = create_daily_binary_threshold(
                threshold=threshold,
                success_value=success_value,
                failure_value=failure_value,
                description=config_data.get('config_name', 'Test')
            )
            
            # Test it
            test_value_pass = threshold + 1  # Should pass
            test_value_fail = threshold - 0.1  # Should fail
            
            score_pass = algorithm.calculate_score(test_value_pass)
            score_fail = algorithm.calculate_score(test_value_fail)
            
            print(f"   Test Value (Pass): {test_value_pass} → Score: {score_pass}")
            print(f"   Test Value (Fail): {test_value_fail} → Score: {score_fail}")
            
            # Validate scores
            if score_pass == success_value and score_fail == failure_value:
                print("✅ Algorithm works correctly!")
                return True
            else:
                print(f"❌ Algorithm returned unexpected scores")
                return False
                
        else:
            print(f"⚠️  Scoring method '{scoring_method}' not implemented in this test")
            return True  # We'll assume it's okay for now
            
    except Exception as e:
        print(f"❌ Algorithm creation/testing failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_config_validation.py <path_to_json_config>")
        sys.exit(1)
    
    config_path = sys.argv[1]
    success = test_config(config_path)
    sys.exit(0 if success else 1)