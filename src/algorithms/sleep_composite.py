"""
Sleep Composite Scoring Algorithm

Specialized algorithm for comprehensive sleep quality assessment combining:
- Sleep duration (zone-based scoring): 55% weight
- Sleep time consistency (variance-based): 22.5% weight  
- Wake time consistency (variance-based): 22.5% weight

Algorithm Type: sleep_composite
Pattern: Daily composite assessment
Evaluation: Daily with multi-component scoring
Logic: Weighted average of duration zones + consistency variance scoring
"""

from typing import Dict, Any, Union, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class SleepCompositeConfig:
    """Configuration for sleep composite scoring"""
    # Duration component (55% weight)
    duration_weight: float = 0.55
    duration_zones: List[Dict[str, Any]] = None
    
    # Consistency components (22.5% each)
    sleep_consistency_weight: float = 0.225
    wake_consistency_weight: float = 0.225
    variance_thresholds: List[Dict[str, Any]] = None
    
    # Metadata
    unit: str = "composite_score"
    description: str = ""
    
    def __post_init__(self):
        # Default sleep duration zones
        if self.duration_zones is None:
            self.duration_zones = [
                {"range": [0, 6], "score": 0, "label": "Insufficient"},
                {"range": [6, 7], "score": 50, "label": "Low"},
                {"range": [7, 9], "score": 100, "label": "Optimal"},
                {"range": [9, 10], "score": 75, "label": "Long"},
                {"range": [10, 24], "score": 25, "label": "Excessive"}
            ]
        
        # Default variance thresholds for consistency
        if self.variance_thresholds is None:
            self.variance_thresholds = [
                {"max_variance": 60, "score": 100},   # <60 min = 100%
                {"max_variance": 90, "score": 75},    # 60-90 min = 75%
                {"max_variance": 120, "score": 50},   # 90-120 min = 50%
                {"max_variance": 150, "score": 25},   # 120-150 min = 25%
                {"max_variance": float('inf'), "score": 0}  # >150 min = 0%
            ]


class SleepCompositeAlgorithm:
    """Sleep composite algorithm implementation with duration + consistency scoring"""
    
    def __init__(self, config: SleepCompositeConfig):
        self.config = config
    
    def calculate_score(self, sleep_data: Dict[str, Union[float, int]]) -> float:
        """
        Calculate composite sleep score from duration and consistency data.
        
        Args:
            sleep_data: Dict containing:
                - sleep_duration: Hours of sleep (float)
                - sleep_time_consistency: Variance in minutes (float) 
                - wake_time_consistency: Variance in minutes (float)
                
        Returns:
            Composite sleep score (0-100)
        """
        duration = sleep_data.get('sleep_duration', 0)
        sleep_variance = sleep_data.get('sleep_time_consistency', 0)
        wake_variance = sleep_data.get('wake_time_consistency', 0)
        
        # Calculate component scores
        duration_score = self._calculate_duration_score(duration)
        sleep_consistency_score = self._calculate_consistency_score(sleep_variance)
        wake_consistency_score = self._calculate_consistency_score(wake_variance)
        
        # Calculate weighted composite
        composite_score = (
            (duration_score * self.config.duration_weight) +
            (sleep_consistency_score * self.config.sleep_consistency_weight) +
            (wake_consistency_score * self.config.wake_consistency_weight)
        )
        
        # Ensure score is within bounds
        return max(0.0, min(100.0, composite_score))
    
    def _calculate_duration_score(self, duration: float) -> float:
        """Calculate score for sleep duration using zone-based logic"""
        for zone in self.config.duration_zones:
            min_val, max_val = zone["range"]
            if min_val <= duration < max_val:
                return float(zone["score"])
        
        # Handle edge case: exactly at max value of optimal zone
        if duration == 9.0:  # Exactly 9 hours
            return 100.0
        
        # Fallback to last zone for values beyond defined ranges
        return float(self.config.duration_zones[-1]["score"])
    
    def _calculate_consistency_score(self, variance_minutes: float) -> float:
        """Calculate score for sleep/wake consistency using variance thresholds"""
        for threshold in self.config.variance_thresholds:
            if variance_minutes < threshold["max_variance"]:
                return float(threshold["score"])
        
        # Fallback to 0 for extreme variance
        return 0.0
    
    def calculate_progressive_scores(self, daily_sleep_data: List[Dict[str, Union[float, int]]]) -> List[float]:
        """
        Calculate progressive adherence scores for sleep composite assessment.
        
        Args:
            daily_sleep_data: List of daily sleep data dicts (7 days)
            
        Returns:
            List of daily composite scores
        """
        progressive_scores = []
        
        for daily_data in daily_sleep_data:
            score = self.calculate_score(daily_data)
            progressive_scores.append(score)
        
        return progressive_scores
    
    def get_component_breakdown(self, sleep_data: Dict[str, Union[float, int]]) -> Dict[str, Any]:
        """
        Get detailed breakdown of component scores for analysis.
        
        Returns:
            Dict with component scores and composite calculation
        """
        duration = sleep_data.get('sleep_duration', 0)
        sleep_variance = sleep_data.get('sleep_time_consistency', 0)
        wake_variance = sleep_data.get('wake_time_consistency', 0)
        
        # Calculate individual components
        duration_score = self._calculate_duration_score(duration)
        sleep_consistency_score = self._calculate_consistency_score(sleep_variance)
        wake_consistency_score = self._calculate_consistency_score(wake_variance)
        
        # Calculate weighted contributions
        duration_contribution = duration_score * self.config.duration_weight
        sleep_contribution = sleep_consistency_score * self.config.sleep_consistency_weight
        wake_contribution = wake_consistency_score * self.config.wake_consistency_weight
        
        composite_score = duration_contribution + sleep_contribution + wake_contribution
        
        return {
            "components": {
                "duration": {
                    "value": duration,
                    "score": duration_score,
                    "weight": self.config.duration_weight,
                    "contribution": duration_contribution
                },
                "sleep_consistency": {
                    "value": sleep_variance,
                    "score": sleep_consistency_score,
                    "weight": self.config.sleep_consistency_weight,
                    "contribution": sleep_contribution
                },
                "wake_consistency": {
                    "value": wake_variance,
                    "score": wake_consistency_score,
                    "weight": self.config.wake_consistency_weight,
                    "contribution": wake_contribution
                }
            },
            "composite_score": composite_score,
            "algorithm": "sleep_composite"
        }
    
    def validate_config(self) -> bool:
        """Validate the configuration parameters"""
        # Check weights sum to 1.0
        total_weight = (self.config.duration_weight + 
                       self.config.sleep_consistency_weight + 
                       self.config.wake_consistency_weight)
        
        if abs(total_weight - 1.0) > 0.001:  # Allow small floating point errors
            raise ValueError(f"Component weights must sum to 1.0, got {total_weight}")
        
        # Validate duration zones
        if not self.config.duration_zones:
            raise ValueError("Duration zones cannot be empty")
        
        # Validate variance thresholds
        if not self.config.variance_thresholds:
            raise ValueError("Variance thresholds cannot be empty")
        
        # Check variance thresholds are in ascending order
        prev_max = 0
        for threshold in self.config.variance_thresholds[:-1]:  # Exclude infinity
            if threshold["max_variance"] <= prev_max:
                raise ValueError("Variance thresholds must be in ascending order")
            prev_max = threshold["max_variance"]
        
        return True
    
    def get_formula(self) -> str:
        """Return the algorithm formula as a string"""
        return (f"({self.config.duration_weight} × duration_zone_score) + "
                f"({self.config.sleep_consistency_weight} × sleep_consistency_score) + "
                f"({self.config.wake_consistency_weight} × wake_consistency_score)")


def create_sleep_composite(
    duration_weight: float = 0.55,
    sleep_consistency_weight: float = 0.225,
    wake_consistency_weight: float = 0.225,
    description: str = ""
) -> SleepCompositeAlgorithm:
    """Create a sleep composite algorithm with standard weights"""
    config = SleepCompositeConfig(
        duration_weight=duration_weight,
        sleep_consistency_weight=sleep_consistency_weight,
        wake_consistency_weight=wake_consistency_weight,
        description=description
    )
    return SleepCompositeAlgorithm(config)


# Example usage and testing
if __name__ == "__main__":
    # Example 1: Good sleep duration, good consistency
    good_sleep = {
        "sleep_duration": 8.0,          # 8 hours (optimal zone) = 100 points
        "sleep_time_consistency": 15,   # 15 min variance (<60) = 100 points
        "wake_time_consistency": 20     # 20 min variance (<60) = 100 points
    }
    
    algorithm = create_sleep_composite()
    score1 = algorithm.calculate_score(good_sleep)
    breakdown1 = algorithm.get_component_breakdown(good_sleep)
    print("Good sleep example:", score1)
    print("Breakdown:", breakdown1)
    
    # Example 2: Suboptimal sleep duration, poor consistency
    poor_sleep = {
        "sleep_duration": 6.5,          # 6.5 hours (low zone) = 50 points
        "sleep_time_consistency": 45,   # 45 min variance (<60) = 100 points  
        "wake_time_consistency": 75     # 75 min variance (60-90) = 75 points
    }
    
    score2 = algorithm.calculate_score(poor_sleep)
    breakdown2 = algorithm.get_component_breakdown(poor_sleep)
    print("Poor sleep example:", score2)
    print("Breakdown:", breakdown2)
    
    # Example 3: Insufficient sleep, high variance
    bad_sleep = {
        "sleep_duration": 5.5,          # 5.5 hours (insufficient) = 0 points
        "sleep_time_consistency": 180,  # 180 min variance (>150) = 0 points
        "wake_time_consistency": 120    # 120 min variance (90-120) = 50 points
    }
    
    score3 = algorithm.calculate_score(bad_sleep)
    breakdown3 = algorithm.get_component_breakdown(bad_sleep)
    print("Bad sleep example:", score3)
    print("Breakdown:", breakdown3)