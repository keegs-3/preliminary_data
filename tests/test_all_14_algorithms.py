"""
Test suite for all 14 algorithm configurations from the CSV file.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from algorithms import *


def test_sc_binary_daily():
    """Test SC-BINARY-DAILY: Binary Daily Threshold"""
    print("Testing SC-BINARY-DAILY...")
    
    algo = create_daily_binary_threshold(
        threshold=50,
        success_value=100,
        failure_value=0,
        description="Binary daily threshold for goal completion"
    )
    
    assert algo.calculate_score(60) == 100  # Above threshold
    assert algo.calculate_score(50) == 100  # At threshold  
    assert algo.calculate_score(40) == 0    # Below threshold
    assert algo.validate_config() == True
    print("  ✓ SC-BINARY-DAILY - PASSED")


def test_sc_binary_frequency():
    """Test SC-BINARY-FREQUENCY: Binary Frequency Window"""
    print("Testing SC-BINARY-FREQUENCY...")
    
    algo = create_frequency_binary_threshold(
        threshold=1,
        frequency_requirement="5 successful days out of 7-day window",
        success_value=100,
        failure_value=0,
        description="Binary frequency threshold for weekly goals"
    )
    
    assert algo.calculate_score(1) == 100  # Meets threshold
    assert algo.calculate_score(0) == 0    # Below threshold
    assert algo.validate_config() == True
    print("  ✓ SC-BINARY-FREQUENCY - PASSED")


def test_sc_proportional_daily():
    """Test SC-PROPORTIONAL-DAILY: Proportional Daily Achievement"""
    print("Testing SC-PROPORTIONAL-DAILY...")
    
    algo = create_daily_proportional(
        target=100,
        unit="points",
        maximum_cap=150,
        description="Proportional daily achievement scoring"
    )
    
    assert algo.calculate_score(100) == 100  # 100% of target
    assert algo.calculate_score(50) == 50    # 50% of target
    assert algo.calculate_score(150) == 150  # 150% of target (capped at max_cap)
    assert algo.validate_config() == True
    print("  ✓ SC-PROPORTIONAL-DAILY - PASSED")


def test_sc_proportional_frequency():
    """Test SC-PROPORTIONAL-FREQUENCY: Proportional Frequency Window"""
    print("Testing SC-PROPORTIONAL-FREQUENCY...")
    
    algo = create_frequency_proportional(
        target=75,
        unit="minutes",
        frequency_requirement="achieve target on 5 of 7 days",
        description="Proportional frequency achievement scoring"
    )
    
    assert algo.calculate_score(75) == 100   # 100% of target
    assert algo.calculate_score(37.5) == 50  # 50% of target
    assert algo.validate_config() == True
    print("  ✓ SC-PROPORTIONAL-FREQUENCY - PASSED")


def test_sc_zone_5tier_daily():
    """Test SC-ZONE-5TIER-DAILY: 5-Tier Zone Daily Scoring"""
    print("Testing SC-ZONE-5TIER-DAILY...")
    
    zones = create_sleep_duration_zones()  # Creates 5-tier zones
    algo = create_daily_zone_based(
        zones=zones,
        unit="hours",
        description="5-tier zone daily scoring for sleep duration"
    )
    
    assert algo.calculate_score(8) == 100   # Good zone
    assert algo.calculate_score(4) == 20    # Very Poor zone
    assert algo.calculate_score(10) == 80   # Excessive zone
    assert len(algo.config.zones) == 5      # Verify 5 tiers
    assert algo.validate_config() == True
    print("  ✓ SC-ZONE-5TIER-DAILY - PASSED")


def test_sc_zone_5tier_frequency():
    """Test SC-ZONE-5TIER-FREQUENCY: 5-Tier Zone Frequency Window"""
    print("Testing SC-ZONE-5TIER-FREQUENCY...")
    
    zones = create_sleep_duration_zones()  # Creates 5-tier zones
    algo = create_frequency_zone_based(
        zones=zones,
        unit="hours",
        frequency_requirement="hit optimal zone on 5 of 7 days",
        description="5-tier zone frequency scoring"
    )
    
    assert algo.calculate_score(8) == 100   # Good zone
    assert len(algo.config.zones) == 5      # Verify 5 tiers
    assert algo.validate_config() == True
    print("  ✓ SC-ZONE-5TIER-FREQUENCY - PASSED")


def test_sc_zone_3tier_daily():
    """Test SC-ZONE-3TIER-DAILY: 3-Tier Zone Daily Scoring"""
    print("Testing SC-ZONE-3TIER-DAILY...")
    
    # Create 3-tier zones
    zones_3tier = [
        Zone(0, 33, 25, "Low"),
        Zone(33, 67, 75, "Medium"),
        Zone(67, 100, 100, "High")
    ]
    
    algo = create_daily_zone_based(
        zones=zones_3tier,
        unit="percentage",
        description="3-tier zone daily scoring"
    )
    
    assert algo.calculate_score(20) == 25   # Low zone
    assert algo.calculate_score(50) == 75   # Medium zone  
    assert algo.calculate_score(80) == 100  # High zone
    assert len(algo.config.zones) == 3     # Verify 3 tiers
    assert algo.validate_config() == True
    print("  ✓ SC-ZONE-3TIER-DAILY - PASSED")


def test_sc_zone_3tier_frequency():
    """Test SC-ZONE-3TIER-FREQUENCY: 3-Tier Zone Frequency Window"""
    print("Testing SC-ZONE-3TIER-FREQUENCY...")
    
    # Create 3-tier zones
    zones_3tier = [
        Zone(0, 33, 25, "Low"),
        Zone(33, 67, 75, "Medium"),
        Zone(67, 100, 100, "High")
    ]
    
    algo = create_frequency_zone_based(
        zones=zones_3tier,
        unit="percentage",
        frequency_requirement="hit medium+ zone on 5 of 7 days",
        description="3-tier zone frequency scoring"
    )
    
    assert algo.calculate_score(50) == 75   # Medium zone
    assert len(algo.config.zones) == 3     # Verify 3 tiers
    assert algo.validate_config() == True
    print("  ✓ SC-ZONE-3TIER-FREQUENCY - PASSED")


def test_sc_composite_daily():
    """Test SC-COMPOSITE-DAILY: Composite Weighted Daily"""
    print("Testing SC-COMPOSITE-DAILY...")
    
    components = [
        Component(
            name="Exercise",
            weight=0.4,
            target=30,
            unit="minutes",
            scoring_method="proportional",
            field_name="exercise_minutes"
        ),
        Component(
            name="Nutrition",
            weight=0.6,
            target=5,
            unit="servings",
            scoring_method="proportional",
            field_name="fruit_veg_servings"
        )
    ]
    
    algo = create_daily_composite(
        components=components,
        description="Daily composite wellness score"
    )
    
    # Test perfect scores
    result = algo.calculate_score({"exercise_minutes": 30, "fruit_veg_servings": 5})
    assert result == 100
    
    # Test partial scores
    result = algo.calculate_score({"exercise_minutes": 15, "fruit_veg_servings": 2.5})
    assert result == 50  # Both at 50%
    
    assert algo.validate_config() == True
    print("  ✓ SC-COMPOSITE-DAILY - PASSED")


def test_sc_composite_frequency():
    """Test SC-COMPOSITE-FREQUENCY: Composite Weighted Frequency Window"""
    print("Testing SC-COMPOSITE-FREQUENCY...")
    
    components = [
        Component(
            name="Weekly Exercise",
            weight=0.7,
            target=150,
            unit="minutes",
            scoring_method="proportional",
            field_name="weekly_exercise"
        ),
        Component(
            name="Consistency",
            weight=0.3,
            target=5,
            unit="days",
            scoring_method="binary",
            field_name="active_days",
            parameters={"threshold": 5, "success_value": 100, "failure_value": 0}
        )
    ]
    
    algo = create_frequency_composite(
        components=components,
        frequency_requirement="meet composite target weekly",
        description="Weekly composite fitness score"
    )
    
    # Test perfect week
    result = algo.calculate_score({"weekly_exercise": 150, "active_days": 5})
    assert result == 100
    
    assert algo.validate_config() == True
    print("  ✓ SC-COMPOSITE-FREQUENCY - PASSED")


def test_sc_composite_sleep_advanced():
    """Test SC-COMPOSITE-SLEEP-ADVANCED: Composite Sleep Duration + Schedule Consistency"""
    print("Testing SC-COMPOSITE-SLEEP-ADVANCED...")
    
    algo = create_sleep_quality_composite()  # Predefined advanced sleep composite
    
    # Test excellent sleep
    result = algo.calculate_score({
        "sleep_duration": 8,
        "schedule_variance": 30
    })
    assert result == 100
    
    # Test poor sleep
    result = algo.calculate_score({
        "sleep_duration": 4,
        "schedule_variance": 120
    })
    assert result == 14  # 0.7 * 20 + 0.3 * 0
    
    assert algo.validate_config() == True
    print("  ✓ SC-COMPOSITE-SLEEP-ADVANCED - PASSED")


def test_sc_constrained_weekly_allowance():
    """Test SC-CONSTRAINED-WEEKLY-ALLOWANCE: Constrained Weekly Allowance"""
    print("Testing SC-CONSTRAINED-WEEKLY-ALLOWANCE...")
    
    algo = create_weekly_allowance(
        weekly_allowance=100,
        unit="points",
        rollover_enabled=True,
        max_rollover_percentage=25,
        penalty_for_overage=5.0,
        description="Weekly allowance with rollover"
    )
    
    # Test within allowance
    result = algo.calculate_score(80, "2024-W01")
    assert result["score"] == 100
    assert result["status"] == "within_allowance"
    
    # Test over allowance (accounting for rollover from previous week)
    # Previous week had 20 points remaining, so available allowance = 100 + 20 = 120
    # But let's test with a fresh week that has no rollover
    result = algo.calculate_score(130, "2024-W03")  # Over base allowance + any rollover
    assert result["status"] == "over_allowance"
    assert result["score"] < 100  # Should have penalty
    
    assert algo.validate_config() == True
    print("  ✓ SC-CONSTRAINED-WEEKLY-ALLOWANCE - PASSED")


def test_sc_categorical_filter_daily():
    """Test SC-CATEGORICAL-FILTER-DAILY: Categorical Filter Daily Threshold"""
    print("Testing SC-CATEGORICAL-FILTER-DAILY...")
    
    # Create category filters
    filters = [
        CategoryFilter(
            category_name="High Impact",
            category_values=["cardio", "strength", "HIIT"],
            threshold=30,
            success_value=100,
            failure_value=0,
            weight=1.5
        ),
        CategoryFilter(
            category_name="Low Impact", 
            category_values=["yoga", "walking", "stretching"],
            threshold=45,
            success_value=80,
            failure_value=0,
            weight=1.0
        )
    ]
    
    algo = create_daily_categorical_filter(
        category_field="exercise_type",
        category_filters=filters,
        default_threshold=20,
        description="Exercise type-specific thresholds"
    )
    
    # Test high impact exercise
    result = algo.calculate_score({
        "exercise_type": "cardio",
        "value": 35
    })
    assert result["score"] == 100
    assert result["matched_category"] == "High Impact"
    
    # Test low impact exercise
    result = algo.calculate_score({
        "exercise_type": "yoga", 
        "value": 50
    })
    assert result["score"] == 80
    assert result["matched_category"] == "Low Impact"
    
    # Test unknown category (uses default)
    result = algo.calculate_score({
        "exercise_type": "swimming",
        "value": 25
    })
    assert result["score"] == 50  # Uses default success value
    assert result["matched_category"] == "default"
    
    assert algo.validate_config() == True
    print("  ✓ SC-CATEGORICAL-FILTER-DAILY - PASSED")


def test_sc_categorical_filter_frequency():
    """Test SC-CATEGORICAL-FILTER-FREQUENCY: Categorical Filter Frequency Threshold"""
    print("Testing SC-CATEGORICAL-FILTER-FREQUENCY...")
    
    filters = [
        CategoryFilter(
            category_name="Vegetables",
            category_values=["broccoli", "spinach", "carrots"],
            threshold=2,
            success_value=100,
            failure_value=0
        ),
        CategoryFilter(
            category_name="Fruits",
            category_values=["apple", "banana", "berries"],
            threshold=1,
            success_value=80,
            failure_value=0
        )
    ]
    
    algo = create_frequency_categorical_filter(
        category_field="food_type",
        category_filters=filters,
        frequency_requirement="meet category targets 5 of 7 days",
        description="Food type-specific frequency thresholds"
    )
    
    # Test vegetable consumption
    result = algo.calculate_score({
        "food_type": "broccoli",
        "value": 3
    })
    assert result["score"] == 100
    assert result["matched_category"] == "Vegetables"
    
    assert algo.validate_config() == True
    print("  ✓ SC-CATEGORICAL-FILTER-FREQUENCY - PASSED")


def run_all_14_algorithm_tests():
    """Run tests for all 14 algorithm configurations."""
    print("=" * 80)
    print("TESTING ALL 14 ALGORITHM CONFIGURATIONS")
    print("=" * 80)
    
    test_functions = [
        test_sc_binary_daily,
        test_sc_binary_frequency,
        test_sc_proportional_daily,
        test_sc_proportional_frequency,
        test_sc_zone_5tier_daily,
        test_sc_zone_5tier_frequency,
        test_sc_zone_3tier_daily,
        test_sc_zone_3tier_frequency,
        test_sc_composite_daily,
        test_sc_composite_frequency,
        test_sc_composite_sleep_advanced,
        test_sc_constrained_weekly_allowance,
        test_sc_categorical_filter_daily,
        test_sc_categorical_filter_frequency
    ]
    
    passed = 0
    total = len(test_functions)
    
    for test_func in test_functions:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"  ✗ {test_func.__name__}: {e}")
    
    print("\n" + "=" * 80)
    print(f"ALL 14 ALGORITHM TEST RESULTS: {passed}/{total} PASSED")
    print("=" * 80)
    
    if passed == total:
        print("🎉 ALL 14 ALGORITHM CONFIGURATIONS WORKING PERFECTLY!")
    else:
        print(f"❌ {total - passed} algorithms need fixes")
    
    return passed == total


if __name__ == "__main__":
    run_all_14_algorithm_tests()