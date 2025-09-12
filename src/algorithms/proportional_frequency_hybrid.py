"""
Proportional Frequency Hybrid Algorithm

Combines proportional daily scoring with frequency-based weekly evaluation.
Solves the issue where partial progress gets no credit in frequency patterns.
"""

from typing import Dict, Any, List, Union, Tuple
from dataclasses import dataclass
from .binary_threshold import EvaluationPeriod, SuccessCriteria, CalculationMethod


@dataclass
class ProportionalFrequencyHybridConfig:
    daily_target: float
    required_qualifying_days: int
    unit: str
    measurement_type: str = "hybrid_quantity_frequency"
    evaluation_period: EvaluationPeriod = EvaluationPeriod.ROLLING_7_DAY
    success_criteria: SuccessCriteria = SuccessCriteria.FREQUENCY_TARGET
    calculation_method: CalculationMethod = CalculationMethod.SUM
    daily_minimum_threshold: float = 0
    total_days: int = 7
    minimum_threshold: float = 0
    maximum_cap: float = 100
    partial_credit: bool = True
    progress_direction: str = "buildup"
    description: str = ""


class ProportionalFrequencyHybridAlgorithm:
    """Proportional Frequency Hybrid scoring algorithm implementation."""
    
    def __init__(self, config: ProportionalFrequencyHybridConfig):
        self.config = config
        self._validate_config()
    
    def _validate_config(self):
        """Validate configuration parameters."""
        if self.config.daily_target <= 0:
            raise ValueError("daily_target must be greater than 0")
        
        if self.config.required_qualifying_days <= 0:
            raise ValueError("required_qualifying_days must be greater than 0")
        
        if self.config.required_qualifying_days > self.config.total_days:
            raise ValueError("required_qualifying_days cannot exceed total_days")
        
        if self.config.daily_minimum_threshold < 0:
            raise ValueError("daily_minimum_threshold must be >= 0")
    
    def calculate_daily_score(self, actual_value: Union[float, int]) -> float:
        """
        Calculate proportional score for a single day.
        
        Args:
            actual_value: The measured value to evaluate for one day
            
        Returns:
            Score as percentage of daily target (0-100)
        """
        if actual_value <= 0:
            return 0.0
        
        # Calculate base percentage
        percentage = (actual_value / self.config.daily_target) * 100
        
        # Apply maximum cap
        return min(percentage, self.config.maximum_cap)
    
    def calculate_weekly_score(self, daily_values: List[Union[float, int]]) -> float:
        """
        Calculate weekly score using proportional frequency hybrid method.
        
        Args:
            daily_values: List of measured values for each day (length should match total_days)
            
        Returns:
            Weekly score as percentage (0-100)
        """
        if len(daily_values) != self.config.total_days:
            raise ValueError(f"Expected {self.config.total_days} daily values, got {len(daily_values)}")
        
        # Calculate daily scores
        daily_scores = [self.calculate_daily_score(value) for value in daily_values]
        
        # Filter qualifying days (above minimum threshold)
        qualifying_data = [
            (score, value) 
            for score, value in zip(daily_scores, daily_values) 
            if value >= self.config.daily_minimum_threshold
        ]
        
        # Check if we have enough qualifying days
        if len(qualifying_data) < self.config.required_qualifying_days:
            return self.config.minimum_threshold
        
        # Sort by score descending and take top N
        qualifying_data.sort(key=lambda x: x[0], reverse=True)
        top_scores = [score for score, _ in qualifying_data[:self.config.required_qualifying_days]]
        
        # Calculate average of top qualifying days
        weekly_score = sum(top_scores) / len(top_scores)
        
        # Apply minimum threshold and maximum cap
        weekly_score = max(weekly_score, self.config.minimum_threshold)
        weekly_score = min(weekly_score, self.config.maximum_cap)
        
        return weekly_score
    
    def calculate_progressive_scores(self, daily_values: List[Union[float, int]]) -> List[float]:
        """
        Calculate progressive adherence scores as they would appear each day to the user.
        
        For proportional frequency hybrid: Shows 100% as long as weekly goal is still achievable.
        
        Args:
            daily_values: List of daily measured values (7 days)
            
        Returns:
            List of progressive scores (what user sees each day)
        """
        progressive_scores = []
        
        for day_idx in range(len(daily_values)):
            # Calculate current qualifying days up to this point
            current_values = daily_values[:day_idx + 1]
            qualifying_count = sum(1 for value in current_values if value >= self.config.daily_minimum_threshold)
            
            remaining_days = len(daily_values) - (day_idx + 1)
            can_still_achieve = (qualifying_count + remaining_days) >= self.config.required_qualifying_days
            
            if qualifying_count >= self.config.required_qualifying_days:
                progressive_scores.append(100.0)  # Already achieved
            elif can_still_achieve:
                progressive_scores.append(100.0)  # Still possible
            else:
                progressive_scores.append(0.0)   # Impossible now
        
        return progressive_scores
    
    def get_daily_breakdown(self, daily_values: List[Union[float, int]]) -> Dict[str, Any]:
        """
        Get detailed breakdown of daily and weekly scoring.
        
        Args:
            daily_values: List of measured values for each day
            
        Returns:
            Dictionary with daily scores, qualifying days, and weekly result
        """
        if len(daily_values) != self.config.total_days:
            raise ValueError(f"Expected {self.config.total_days} daily values, got {len(daily_values)}")
        
        # Calculate daily scores
        daily_scores = [self.calculate_daily_score(value) for value in daily_values]
        
        # Identify qualifying days
        qualifying_days = []
        for i, (score, value) in enumerate(zip(daily_scores, daily_values)):
            if value >= self.config.daily_minimum_threshold:
                qualifying_days.append({
                    'day': i + 1,
                    'value': value,
                    'score': score,
                    'qualifies': True
                })
            else:
                qualifying_days.append({
                    'day': i + 1,
                    'value': value,
                    'score': score,
                    'qualifies': False
                })
        
        # Sort qualifying days by score and identify top performers
        qualifying_only = [day for day in qualifying_days if day['qualifies']]
        qualifying_only.sort(key=lambda x: x['score'], reverse=True)
        top_days = qualifying_only[:self.config.required_qualifying_days]
        
        # Calculate weekly score
        weekly_score = self.calculate_weekly_score(daily_values)
        
        return {
            'daily_breakdown': qualifying_days,
            'total_qualifying_days': len(qualifying_only),
            'required_qualifying_days': self.config.required_qualifying_days,
            'top_performing_days': top_days,
            'weekly_score': weekly_score,
            'target_met': len(qualifying_only) >= self.config.required_qualifying_days
        }


def create_proportional_frequency_hybrid(
    daily_target: float,
    required_qualifying_days: int,
    unit: str,
    daily_minimum_threshold: float = 0,
    total_days: int = 7,
    maximum_cap: float = 100,
    minimum_threshold: float = 0,
    description: str = ""
) -> ProportionalFrequencyHybridAlgorithm:
    """
    Factory function to create a proportional frequency hybrid algorithm.
    
    Args:
        daily_target: Target value for 100% daily score
        required_qualifying_days: Number of top days to average for weekly score
        unit: Measurement unit
        daily_minimum_threshold: Minimum value to qualify as valid day
        total_days: Total evaluation period length
        maximum_cap: Maximum weekly score cap
        minimum_threshold: Minimum weekly score floor
        description: Description of the algorithm instance
        
    Returns:
        Configured ProportionalFrequencyHybridAlgorithm instance
    """
    config = ProportionalFrequencyHybridConfig(
        daily_target=daily_target,
        required_qualifying_days=required_qualifying_days,
        unit=unit,
        daily_minimum_threshold=daily_minimum_threshold,
        total_days=total_days,
        minimum_threshold=minimum_threshold,
        maximum_cap=maximum_cap,
        description=description
    )
    
    return ProportionalFrequencyHybridAlgorithm(config)