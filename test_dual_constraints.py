#!/usr/bin/env python3
"""
Test the dual constraint logic for REC0005.2
Validate the examples: 1+1+1 fail, 2+1 succeed, 1+1 succeed, 1+2 succeed, 3+0 fail
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from algorithms.constrained_weekly_allowance import ConstrainedWeeklyAllowanceAlgorithm, ConstrainedWeeklyAllowanceConfig

def test_dual_constraints():
    """Test REC0005.2 dual constraint examples"""
    
    # Create algorithm with REC0005.2 constraints  
    config = ConstrainedWeeklyAllowanceConfig(
        weekly_allowance=3.0,  # Max 3 drinks per week
        max_days_per_week=2,   # Max 2 days of drinking
        penalty_for_overage=100.0,  # Zero tolerance for exceeding drink limit
        unit="drink"
    )
    algorithm = ConstrainedWeeklyAllowanceAlgorithm(config)
    
    test_cases = [
        {
            "name": "1+1+1 (3 days) - should FAIL",
            "daily_values": [1, 1, 1, 0, 0, 0, 0],
            "expected": "FAIL"
        },
        {
            "name": "2+1 (2 days) - should PASS", 
            "daily_values": [2, 1, 0, 0, 0, 0, 0],
            "expected": "PASS"
        },
        {
            "name": "1+1 (2 days) - should PASS",
            "daily_values": [1, 1, 0, 0, 0, 0, 0], 
            "expected": "PASS"
        },
        {
            "name": "1+2 (2 days) - should PASS",
            "daily_values": [1, 2, 0, 0, 0, 0, 0],
            "expected": "PASS"
        },
        {
            "name": "3+0 (1 day) - should PASS",
            "daily_values": [3, 0, 0, 0, 0, 0, 0],
            "expected": "PASS"
        },
        {
            "name": "4+0 (1 day) - should FAIL (exceeds drinks)",
            "daily_values": [4, 0, 0, 0, 0, 0, 0],
            "expected": "FAIL"
        }
    ]
    
    print("Testing Dual Constraint Logic for REC0005.2")
    print("Constraints: ≤3 drinks per week AND ≤2 days of drinking")
    print("=" * 60)
    
    for test in test_cases:
        result = algorithm.calculate_score(daily_values=test["daily_values"])
        
        total_drinks = sum(test["daily_values"])
        days_used = sum(1 for d in test["daily_values"] if d > 0)
        
        actual_result = "PASS" if result["score"] == 100.0 else "FAIL"
        status_icon = "✅" if actual_result == test["expected"] else "❌"
        
        print(f"{status_icon} {test['name']}")
        print(f"   Drinks: {total_drinks}/3, Days: {days_used}/2")
        print(f"   Score: {result['score']}%, Status: {result['status']}")
        print(f"   Expected: {test['expected']}, Got: {actual_result}")
        print()

if __name__ == "__main__":
    test_dual_constraints()