"""
Proportional Scoring Algorithm

Calculates score as (actual_value / target) * 100
Supports minimum thresholds, maximum caps, and partial credit.
"""

from typing import Dict, Any, Union
from dataclasses import dataclass
from .binary_threshold import EvaluationPeriod, SuccessCriteria, CalculationMethod


@dataclass
class ProportionalConfig:
    target: float
    unit: str
    measurement_type: str = "count"
    evaluation_period: EvaluationPeriod = EvaluationPeriod.DAILY
    success_criteria: SuccessCriteria = SuccessCriteria.SIMPLE_TARGET
    calculation_method: CalculationMethod = CalculationMethod.SUM
    calculation_fields: Union[str, Dict[str, Any]] = "value"
    minimum_threshold: float = 0
    maximum_cap: float = 100
    partial_credit: bool = True
    frequency_requirement: str = "daily"
    description: str = ""


class ProportionalAlgorithm:
    """Proportional scoring algorithm implementation."""
    
    def __init__(self, config: ProportionalConfig):
        self.config = config
    
    def calculate_score(self, actual_value: Union[float, int]) -> float:
        """
        Calculate proportional score.
        
        Args:
            actual_value: The measured value to evaluate
            
        Returns:
            Score as percentage of target (0-100, or up to maximum_cap)
        """
        if self.config.target <= 0:
            raise ValueError("Target must be greater than 0")
        
        # Calculate base percentage
        percentage = (actual_value / self.config.target) * 100
        
        # Apply minimum threshold
        if percentage < self.config.minimum_threshold:
            return self.config.minimum_threshold if self.config.partial_credit else 0
        
        # Apply maximum cap
        return min(percentage, self.config.maximum_cap)
    
    def validate_config(self) -> bool:
        """Validate the configuration parameters."""
        required_fields = [
            "target", "unit", "measurement_type", "evaluation_period",
            "success_criteria", "calculation_method", "calculation_fields"
        ]
        
        for field in required_fields:
            if not hasattr(self.config, field):
                raise ValueError(f"Missing required field: {field}")
        
        if self.config.target <= 0:
            raise ValueError("Target must be greater than 0")
        
        if self.config.minimum_threshold < 0:
            raise ValueError("Minimum threshold cannot be negative")
        
        if self.config.maximum_cap < self.config.minimum_threshold:
            raise ValueError("Maximum cap cannot be less than minimum threshold")
        
        return True
    
    def get_formula(self) -> str:
        """Return the algorithm formula as a string."""
        return f"(actual_value / {self.config.target}) * 100"


def create_daily_proportional(
    target: float,
    unit: str,
    minimum_threshold: float = 0,
    maximum_cap: float = 100,
    partial_credit: bool = True,
    description: str = ""
) -> ProportionalAlgorithm:
    """Create a daily proportional algorithm."""
    config = ProportionalConfig(
        target=target,
        unit=unit,
        minimum_threshold=minimum_threshold,
        maximum_cap=maximum_cap,
        partial_credit=partial_credit,
        evaluation_period=EvaluationPeriod.DAILY,
        description=description
    )
    return ProportionalAlgorithm(config)


def create_frequency_proportional(
    target: float,
    unit: str,
    frequency_requirement: str,
    minimum_threshold: float = 0,
    maximum_cap: float = 100,
    partial_credit: bool = True,
    description: str = ""
) -> ProportionalAlgorithm:
    """Create a frequency-based proportional algorithm."""
    config = ProportionalConfig(
        target=target,
        unit=unit,
        minimum_threshold=minimum_threshold,
        maximum_cap=maximum_cap,
        partial_credit=partial_credit,
        evaluation_period=EvaluationPeriod.ROLLING_7_DAY,
        success_criteria=SuccessCriteria.FREQUENCY_TARGET,
        frequency_requirement=frequency_requirement,
        description=description
    )
    return ProportionalAlgorithm(config)