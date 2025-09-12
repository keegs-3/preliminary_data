"""
SC-MINIMUM-FREQUENCY Algorithm Implementation
===========================================

Scores based on achieving a threshold on a minimum number of days within 
a weekly evaluation period. Success requires meeting criteria on at least X days per week.

Algorithm Type: SC-MINIMUM-FREQUENCY
Pattern: Minimum Achievement Frequency  
Evaluation: Weekly (7 days)
Scoring: Binary (100 or 0)
"""

from typing import List, Dict, Any, Union
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class MinimumFrequencyConfig:
    daily_threshold: float
    daily_comparison: str
    required_days: int
    total_days: int = 7
    description: str = ""


class MinimumFrequencyAlgorithm:
    """Minimum frequency algorithm implementation with progressive scoring."""
    
    def __init__(self, config: MinimumFrequencyConfig):
        self.config = config
    
    def calculate_score(self, daily_values: List[float]) -> float:
        """Calculate weekly score based on frequency requirement."""
        result = calculate_minimum_frequency_score(
            daily_values=daily_values,
            daily_threshold=self.config.daily_threshold,
            daily_comparison=self.config.daily_comparison,
            required_days=self.config.required_days
        )
        return result['score']
    
    def calculate_progressive_scores(self, daily_values: List[Union[float, int]]) -> List[float]:
        """
        Calculate progressive adherence scores as they would appear each day to the user.
        
        Shows 100% as long as the weekly frequency goal is still achievable.
        
        Args:
            daily_values: List of daily measured values (7 days)
            
        Returns:
            List of progressive scores (what user sees each day)
        """
        progressive_scores = []
        successes = 0
        
        for day_idx, value in enumerate(daily_values):
            # Check if this day meets threshold
            if self.config.daily_comparison == "<=":
                day_pass = value <= self.config.daily_threshold
            elif self.config.daily_comparison == ">=":
                day_pass = value >= self.config.daily_threshold
            else:  # "=="
                day_pass = value == self.config.daily_threshold
            
            if day_pass:
                successes += 1
            
            remaining_days = len(daily_values) - (day_idx + 1)
            can_still_achieve = (successes + remaining_days) >= self.config.required_days
            
            if successes >= self.config.required_days:
                progressive_scores.append(100)  # Already achieved
            elif can_still_achieve:
                progressive_scores.append(100)  # Still possible
            else:
                progressive_scores.append(0)   # Impossible now
        
        return progressive_scores


def calculate_minimum_frequency_score(
    daily_values: List[float], 
    daily_threshold: float,
    daily_comparison: str,
    required_days: int,
    **kwargs
) -> Dict[str, Any]:
    """
    Calculate SC-MINIMUM-FREQUENCY score for weekly data
    
    Args:
        daily_values: List of 7 daily measurements [Mon, Tue, Wed, Thu, Fri, Sat, Sun]
        daily_threshold: The threshold value each day must meet
        daily_comparison: Comparison operator ("<=", ">=", "==")
        required_days: Minimum number of days that must meet threshold (e.g., 2, 5)
        **kwargs: Additional parameters from config schema
        
    Returns:
        Dict with score and calculation details
        
    Examples:
        # Ultra-processed foods: ≤1 serving on at least 2 days/week
        calculate_minimum_frequency_score(
            daily_values=[5, 0, 10, 1, 3, 2, 1],
            daily_threshold=1,
            daily_comparison="<=", 
            required_days=2
        )
        # Returns: {"score": 100, "successful_days": 3, "details": "3 ≥ 2 days met criteria"}
        
        # Water intake: ≥8 cups on at least 5 days/week  
        calculate_minimum_frequency_score(
            daily_values=[6, 8, 9, 7, 8, 10, 8],
            daily_threshold=8,
            daily_comparison=">=",
            required_days=5
        )
        # Returns: {"score": 100, "successful_days": 5, "details": "5 ≥ 5 days met criteria"}
    """
    
    if len(daily_values) != 7:
        raise ValueError(f"Expected 7 daily values for weekly calculation, got {len(daily_values)}")
        
    if daily_comparison not in ["<=", ">=", "=="]:
        raise ValueError(f"Unsupported comparison operator: {daily_comparison}")
        
    # Count days that meet the threshold
    successful_days = 0
    daily_results = []
    
    for i, daily_value in enumerate(daily_values):
        day_meets_threshold = False
        
        if daily_comparison == "<=":
            day_meets_threshold = daily_value <= daily_threshold
        elif daily_comparison == ">=":
            day_meets_threshold = daily_value >= daily_threshold  
        elif daily_comparison == "==":
            day_meets_threshold = daily_value == daily_threshold
            
        if day_meets_threshold:
            successful_days += 1
            
        daily_results.append({
            'day': i + 1,
            'value': daily_value,
            'meets_threshold': day_meets_threshold,
            'comparison': f"{daily_value} {daily_comparison} {daily_threshold}"
        })
    
    # Binary scoring: success if we meet minimum required days
    score = 100 if successful_days >= required_days else 0
    
    # Detailed results
    result = {
        'score': score,
        'successful_days': successful_days,
        'required_days': required_days, 
        'total_days': len(daily_values),
        'success_rate': successful_days / len(daily_values),
        'threshold_met': successful_days >= required_days,
        'details': f"{successful_days} {'≥' if successful_days >= required_days else '<'} {required_days} days met criteria",
        'daily_breakdown': daily_results,
        'algorithm': 'SC-MINIMUM-FREQUENCY'
    }
    
    logger.info(f"SC-MINIMUM-FREQUENCY: {successful_days}/{len(daily_values)} days met threshold, "
                f"required {required_days}, score: {score}")
    
    return result


def calculate_single_day_minimum_frequency_score(
    daily_value: float,
    daily_threshold: float, 
    daily_comparison: str,
    required_days: int,
    **kwargs
) -> Dict[str, Any]:
    """
    Calculate contribution of a single day to SC-MINIMUM-FREQUENCY score
    
    This is a helper for real-time scoring when you only have one day's data.
    The full weekly score requires all 7 days.
    
    Args:
        daily_value: Single day's measurement
        daily_threshold: The threshold this day must meet
        daily_comparison: Comparison operator
        required_days: Target minimum days (for reference)
        
    Returns:
        Dict indicating if this day contributes to weekly goal
    """
    
    # Check if this day meets threshold
    day_meets_threshold = False
    if daily_comparison == "<=":
        day_meets_threshold = daily_value <= daily_threshold
    elif daily_comparison == ">=":
        day_meets_threshold = daily_value >= daily_threshold
    elif daily_comparison == "==":
        day_meets_threshold = daily_value == daily_threshold
        
    return {
        'day_contribution': 100 if day_meets_threshold else 0,
        'meets_threshold': day_meets_threshold,
        'comparison_result': f"{daily_value} {daily_comparison} {daily_threshold}",
        'required_days_target': required_days,
        'note': f"This day {'contributes to' if day_meets_threshold else 'does not contribute to'} weekly goal of {required_days} days",
        'algorithm': 'SC-MINIMUM-FREQUENCY (single day)'
    }


def validate_minimum_frequency_config(config: Dict[str, Any]) -> List[str]:
    """
    Validate SC-MINIMUM-FREQUENCY configuration
    
    Args:
        config: Algorithm configuration dictionary
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    required_fields = [
        'daily_threshold',
        'daily_comparison', 
        'required_days'
    ]
    
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")
            
    if 'daily_comparison' in config:
        if config['daily_comparison'] not in ["<=", ">=", "=="]:
            errors.append(f"Invalid daily_comparison: {config['daily_comparison']}")
            
    if 'required_days' in config:
        if not isinstance(config['required_days'], int) or config['required_days'] < 1:
            errors.append("required_days must be a positive integer")
        if config['required_days'] > 7:
            errors.append("required_days cannot exceed 7 for weekly evaluation")
            
    if 'total_days' in config and config.get('total_days', 7) != 7:
        errors.append("total_days must be 7 for weekly SC-MINIMUM-FREQUENCY")
        
    return errors


# Example usage and testing
if __name__ == "__main__":
    # Example 1: Ultra-processed foods - limit to ≤1 serving on at least 2 days/week
    ultra_processed_week = [5, 0, 10, 1, 3, 2, 1]  # 3 days meet ≤1 threshold
    result1 = calculate_minimum_frequency_score(
        daily_values=ultra_processed_week,
        daily_threshold=1,
        daily_comparison="<=", 
        required_days=2
    )
    print("Ultra-processed foods result:", result1)
    
    # Example 2: Water intake - ≥8 cups on at least 5 days/week
    water_week = [6, 8, 9, 7, 8, 10, 8]  # 5 days meet ≥8 threshold
    result2 = calculate_minimum_frequency_score(
        daily_values=water_week,
        daily_threshold=8,
        daily_comparison=">=",
        required_days=5
    )
    print("Water intake result:", result2)
    
    # Example 3: Single day assessment
    single_day = calculate_single_day_minimum_frequency_score(
        daily_value=1,
        daily_threshold=1,
        daily_comparison="<=",
        required_days=2
    )
    print("Single day assessment:", single_day)