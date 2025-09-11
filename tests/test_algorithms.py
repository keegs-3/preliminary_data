"""
Test suite for all scoring algorithms.

Tests functionality, edge cases, and validation for each algorithm type.
"""

import sys
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
    create_daily_binary_threshold,
    create_frequency_binary_threshold,
    create_daily_proportional,
    create_frequency_proportional,
    create_daily_zone_based,
    create_frequency_zone_based,
    create_daily_composite,
    create_sleep_quality_composite,
    create_sleep_duration_zones,
    ComparisonOperator,
    EvaluationPeriod,
    SuccessCriteria,
    CalculationMethod
)


class TestBinaryThresholdAlgorithm:
    """Test binary threshold algorithm."""
    
    def test_basic_threshold_met(self):
        """Test basic threshold evaluation when met."""
        algo = create_daily_binary_threshold(threshold=50, success_value=100, failure_value=0)
        
        assert algo.calculate_score(60) == 100
        assert algo.calculate_score(50) == 100  # Equal should pass with >=
        assert algo.calculate_score(40) == 0
    
    def test_comparison_operators(self):
        """Test different comparison operators."""
        config = BinaryThresholdConfig(
            threshold=50,
            success_value=100,
            failure_value=0,
            comparison_operator=ComparisonOperator.GT
        )
        algo = BinaryThresholdAlgorithm(config)
        
        assert algo.calculate_score(51) == 100
        assert algo.calculate_score(50) == 0  # Equal should fail with >
        assert algo.calculate_score(49) == 0
    
    def test_boolean_threshold(self):
        """Test boolean threshold evaluation."""
        config = BinaryThresholdConfig(
            threshold=True,
            success_value=100,
            failure_value=0,
            comparison_operator=ComparisonOperator.EQ
        )
        algo = BinaryThresholdAlgorithm(config)
        
        assert algo.calculate_score(True) == 100
        assert algo.calculate_score(False) == 0
    
    def test_validation(self):
        """Test configuration validation."""
        config = BinaryThresholdConfig(threshold=50)
        algo = BinaryThresholdAlgorithm(config)
        
        assert algo.validate_config() == True
        
        # Test invalid operator
        try:
            config.comparison_operator = "invalid"
            algo._meets_threshold(50)
            assert False, "Should have raised ValueError for invalid operator"
        except ValueError:
            pass  # Expected


class TestProportionalAlgorithm:
    """Test proportional algorithm."""
    
    def test_basic_proportional_scoring(self):
        """Test basic proportional scoring."""
        algo = create_daily_proportional(target=100, unit="points")
        
        assert algo.calculate_score(100) == 100  # 100% of target
        assert algo.calculate_score(50) == 50    # 50% of target
        assert algo.calculate_score(150) == 100  # Capped at 100
        assert algo.calculate_score(0) == 0      # 0% of target
    
    def test_minimum_threshold(self):
        """Test minimum threshold functionality."""
        config = ProportionalConfig(
            target=100,
            unit="points",
            minimum_threshold=10,
            partial_credit=True
        )
        algo = ProportionalAlgorithm(config)
        
        assert algo.calculate_score(5) == 10   # Below threshold but partial credit
        assert algo.calculate_score(50) == 50  # Normal scoring
        
        # Test without partial credit
        config.partial_credit = False
        algo = ProportionalAlgorithm(config)
        assert algo.calculate_score(5) == 0    # Below threshold, no partial credit
    
    def test_maximum_cap(self):
        """Test maximum cap functionality."""
        config = ProportionalConfig(
            target=100,
            unit="points",
            maximum_cap=75
        )
        algo = ProportionalAlgorithm(config)
        
        assert algo.calculate_score(100) == 75  # Capped at 75
        assert algo.calculate_score(200) == 75  # Still capped at 75
        assert algo.calculate_score(50) == 50   # Normal scoring below cap
    
    def test_validation_errors(self):
        """Test validation error cases."""
        # Test zero target
        config = ProportionalConfig(target=0, unit="points")
        algo = ProportionalAlgorithm(config)
        
        try:
            algo.calculate_score(50)
            assert False, "Should have raised ValueError for zero target"
        except ValueError as e:
            assert "Target must be greater than 0" in str(e)
        
        try:
            algo.validate_config()
            assert False, "Should have raised ValueError for zero target"
        except ValueError as e:
            assert "Target must be greater than 0" in str(e)


class TestZoneBasedAlgorithm:
    """Test zone-based algorithm."""
    
    def test_basic_zone_scoring(self):
        """Test basic zone scoring."""
        zones = create_sleep_duration_zones()
        algo = create_daily_zone_based(zones=zones, unit="hours")
        
        assert algo.calculate_score(3) == 20   # Very Poor zone
        assert algo.calculate_score(5.5) == 40 # Poor zone
        assert algo.calculate_score(6.5) == 60 # Fair zone
        assert algo.calculate_score(8) == 100  # Good zone
        assert algo.calculate_score(10) == 80  # Excessive zone
        assert algo.calculate_score(15) == 0   # Outside all zones
    
    def test_zone_boundaries(self):
        """Test zone boundary handling."""
        zones = create_sleep_duration_zones()
        algo = create_daily_zone_based(zones=zones, unit="hours")
        
        # Test exact boundary values
        assert algo.calculate_score(5) == 40   # Boundary between Very Poor and Poor
        assert algo.calculate_score(6) == 60   # Boundary between Poor and Fair
        assert algo.calculate_score(7) == 100  # Boundary between Fair and Good
        assert algo.calculate_score(9) == 80   # Boundary between Good and Excessive
    
    def test_graduated_scoring(self):
        """Test graduated boundary scoring."""
        zones = create_sleep_duration_zones()
        config = ZoneBasedConfig(
            zones=zones,
            unit="hours",
            grace_range=True,
            boundary_handling="graduated"
        )
        algo = ZoneBasedAlgorithm(config)
        
        # Graduated scoring should give slightly different scores within zone
        score_start = algo.calculate_score(7.0)   # Start of Good zone
        score_end = algo.calculate_score(8.9)     # End of Good zone
        
        assert score_start <= score_end  # Score should increase through zone
        assert 95 <= score_start <= 100  # Should be close to base score
    
    def test_zone_validation(self):
        """Test zone validation."""
        # Test wrong number of zones
        try:
            ZoneBasedAlgorithm(ZoneBasedConfig(zones=[], unit="hours"))
            assert False, "Should have raised ValueError for wrong number of zones"
        except ValueError as e:
            assert "exactly 5 zones" in str(e)
        
        # Test overlapping zones
        overlapping_zones = [
            Zone(0, 5, 20, "Zone1"),
            Zone(4, 8, 40, "Zone2"),  # Overlap with Zone1
            Zone(8, 10, 60, "Zone3"),
            Zone(10, 12, 80, "Zone4"),
            Zone(12, 15, 100, "Zone5")
        ]
        
        try:
            ZoneBasedAlgorithm(ZoneBasedConfig(zones=overlapping_zones, unit="hours"))
            assert False, "Should have raised ValueError for overlapping zones"
        except ValueError as e:
            assert "Overlap between zones" in str(e)


class TestCompositeWeightedAlgorithm:
    """Test composite weighted algorithm."""
    
    def test_basic_composite_scoring(self):
        """Test basic composite scoring."""
        components = [
            Component(
                name="Component1",
                weight=0.6,
                target=100,
                unit="points",
                scoring_method="proportional",
                field_name="comp1"
            ),
            Component(
                name="Component2",
                weight=0.4,
                target=50,
                unit="points",
                scoring_method="proportional",
                field_name="comp2"
            )
        ]
        
        algo = create_daily_composite(components=components)
        
        # Test perfect scores (both components at 100%)
        result = algo.calculate_score({"comp1": 100, "comp2": 50})
        assert result == 100
        
        # Test mixed scores
        result = algo.calculate_score({"comp1": 50, "comp2": 25})  # Both at 50%
        assert result == 50
        
        # Test weighted impact
        result = algo.calculate_score({"comp1": 100, "comp2": 0})  # Only first component
        assert result == 60  # 0.6 * 100 + 0.4 * 0 = 60
    
    def test_binary_component(self):
        """Test binary scoring component."""
        components = [
            Component(
                name="BinaryComp",
                weight=1.0,
                target=50,
                unit="points",
                scoring_method="binary",
                field_name="binary_field",
                parameters={
                    "threshold": 50,
                    "success_value": 100,
                    "failure_value": 0,
                    "comparison_operator": ">="
                }
            )
        ]
        
        algo = create_daily_composite(components=components)
        
        assert algo.calculate_score({"binary_field": 60}) == 100
        assert algo.calculate_score({"binary_field": 50}) == 100
        assert algo.calculate_score({"binary_field": 40}) == 0
    
    def test_zone_component(self):
        """Test zone-based scoring component."""
        components = [
            Component(
                name="ZoneComp",
                weight=1.0,
                target=8,
                unit="hours",
                scoring_method="zone",
                field_name="zone_field",
                parameters={
                    "zones": [
                        {"min": 0, "max": 5, "score": 20},
                        {"min": 5, "max": 6, "score": 40},
                        {"min": 6, "max": 7, "score": 60},
                        {"min": 7, "max": 9, "score": 100},
                        {"min": 9, "max": 12, "score": 80}
                    ]
                }
            )
        ]
        
        algo = create_daily_composite(components=components)
        
        assert algo.calculate_score({"zone_field": 8}) == 100
        assert algo.calculate_score({"zone_field": 5.5}) == 40
        assert algo.calculate_score({"zone_field": 15}) == 0  # Outside zones
    
    def test_sleep_quality_composite(self):
        """Test the predefined sleep quality composite."""
        algo = create_sleep_quality_composite()
        
        # Test perfect sleep (8 hours duration, good consistency)
        result = algo.calculate_score({
            "sleep_duration": 8,
            "schedule_variance": 30  # 30 minutes variance (good)
        })
        assert result == 100  # 0.7 * 100 + 0.3 * 100 = 100
        
        # Test poor sleep (4 hours duration, poor consistency)
        result = algo.calculate_score({
            "sleep_duration": 4,
            "schedule_variance": 120  # 2 hours variance (poor)
        })
        assert result == 14  # 0.7 * 20 + 0.3 * 0 = 14
    
    def test_missing_component_value(self):
        """Test error handling for missing component values."""
        components = [
            Component(
                name="TestComp",
                weight=1.0,
                target=100,
                unit="points",
                scoring_method="proportional",
                field_name="missing_field"
            )
        ]
        
        algo = create_daily_composite(components=components)
        
        try:
            algo.calculate_score({"wrong_field": 100})
            assert False, "Should have raised ValueError for missing component"
        except ValueError as e:
            assert "Missing value for component" in str(e)
    
    def test_weight_validation(self):
        """Test component weight validation."""
        # Test zero total weight
        components = [
            Component(
                name="TestComp",
                weight=0,
                target=100,
                unit="points",
                scoring_method="proportional",
                field_name="test_field"
            )
        ]
        
        try:
            CompositeWeightedAlgorithm(CompositeWeightedConfig(components=components))
            assert False, "Should have raised ValueError for zero total weight"
        except ValueError as e:
            assert "Total component weights must be greater than 0" in str(e)


class TestAlgorithmFactories:
    """Test algorithm factory functions."""
    
    def test_frequency_algorithms(self):
        """Test frequency-based algorithm creation."""
        # Binary threshold frequency
        algo = create_frequency_binary_threshold(
            threshold=50,
            frequency_requirement="5 of 7 days"
        )
        assert algo.config.evaluation_period == EvaluationPeriod.ROLLING_7_DAY
        assert algo.config.success_criteria == SuccessCriteria.FREQUENCY_TARGET
        
        # Proportional frequency
        algo = create_frequency_proportional(
            target=100,
            unit="points",
            frequency_requirement="achieve target on 5 of 7 days"
        )
        assert algo.config.evaluation_period == EvaluationPeriod.ROLLING_7_DAY
        assert algo.config.success_criteria == SuccessCriteria.FREQUENCY_TARGET
    
    def test_algorithm_formulas(self):
        """Test algorithm formula generation."""
        binary_algo = create_daily_binary_threshold(threshold=50)
        assert "if (actual_value >= 50)" in binary_algo.get_formula()
        
        prop_algo = create_daily_proportional(target=100, unit="points")
        assert "(actual_value / 100) * 100" in prop_algo.get_formula()
        
        zones = create_sleep_duration_zones()
        zone_algo = create_daily_zone_based(zones=zones, unit="hours")
        assert "zone actual_value falls into" in zone_algo.get_formula()


def run_all_tests():
    """Run all algorithm tests and return results."""
    import traceback
    
    results = {
        "total_tests": 0,
        "passed_tests": 0,
        "failed_tests": 0,
        "errors": []
    }
    
    test_classes = [
        TestBinaryThresholdAlgorithm(),
        TestProportionalAlgorithm(),
        TestZoneBasedAlgorithm(),
        TestCompositeWeightedAlgorithm(),
        TestAlgorithmFactories()
    ]
    
    for test_class in test_classes:
        test_methods = [method for method in dir(test_class) if method.startswith('test_')]
        
        for test_method_name in test_methods:
            results["total_tests"] += 1
            test_method = getattr(test_class, test_method_name)
            
            try:
                test_method()
                results["passed_tests"] += 1
                print(f"✓ {test_class.__class__.__name__}.{test_method_name}")
            except Exception as e:
                results["failed_tests"] += 1
                error_msg = f"{test_class.__class__.__name__}.{test_method_name}: {str(e)}"
                results["errors"].append(error_msg)
                print(f"✗ {error_msg}")
                print(f"  {traceback.format_exc()}")
    
    return results


if __name__ == "__main__":
    print("Running algorithm tests...")
    results = run_all_tests()
    
    print(f"\nTest Results:")
    print(f"Total: {results['total_tests']}")
    print(f"Passed: {results['passed_tests']}")
    print(f"Failed: {results['failed_tests']}")
    
    if results["errors"]:
        print(f"\nErrors:")
        for error in results["errors"]:
            print(f"  - {error}")
    
    if results["failed_tests"] == 0:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n❌ {results['failed_tests']} tests failed")