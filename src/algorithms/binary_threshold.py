"""
Binary Threshold Scoring Algorithm

Evaluates whether a measured value meets or exceeds a threshold.
Returns success_value if threshold is met, failure_value otherwise.
"""

from typing import Dict, Any, Union, List
from dataclasses import dataclass
from enum import Enum


class ComparisonOperator(Enum):
    GTE = ">="
    GT = ">"
    EQ = "="
    LT = "<"
    LTE = "<="


class EvaluationPeriod(Enum):
    DAILY = "daily"
    ROLLING_7_DAY = "rolling_7_day"


class SuccessCriteria(Enum):
    SIMPLE_TARGET = "simple_target"
    FREQUENCY_TARGET = "frequency_target"


class CalculationMethod(Enum):
    SUM = "sum"
    AVERAGE = "average"
    DIFFERENCE = "difference"
    COUNT = "count"
    MAX = "max"
    MIN = "min"
    LAST_VALUE = "last_value"
    EXISTS = "exists"


@dataclass
class BinaryThresholdConfig:
    threshold: Union[float, int, bool]
    success_value: float = 100
    failure_value: float = 0
    measurement_type: str = "binary"
    evaluation_period: EvaluationPeriod = EvaluationPeriod.DAILY
    success_criteria: SuccessCriteria = SuccessCriteria.SIMPLE_TARGET
    calculation_method: CalculationMethod = CalculationMethod.EXISTS
    calculation_fields: Union[str, Dict[str, Any]] = "value"
    comparison_operator: ComparisonOperator = ComparisonOperator.GTE
    frequency_requirement: str = "daily"
    description: str = ""


class BinaryThresholdAlgorithm:
    """Binary threshold scoring algorithm implementation."""
    
    def __init__(self, config: BinaryThresholdConfig):
        self.config = config
    
    def calculate_score(self, actual_value: Union[float, int, bool]) -> float:
        """
        Calculate score based on binary threshold logic.
        
        Args:
            actual_value: The measured value to evaluate
            
        Returns:
            Score (success_value or failure_value)
        """
        if self._meets_threshold(actual_value):
            return self.config.success_value
        else:
            return self.config.failure_value
    
    def _meets_threshold(self, actual_value: Union[float, int, bool]) -> bool:
        """Check if actual value meets the threshold criteria."""
        threshold = self.config.threshold
        operator = self.config.comparison_operator
        
        if operator == ComparisonOperator.GTE:
            return actual_value >= threshold
        elif operator == ComparisonOperator.GT:
            return actual_value > threshold
        elif operator == ComparisonOperator.EQ:
            return actual_value == threshold
        elif operator == ComparisonOperator.LT:
            return actual_value < threshold
        elif operator == ComparisonOperator.LTE:
            return actual_value <= threshold
        else:
            raise ValueError(f"Unknown comparison operator: {operator}")
    
    def validate_config(self) -> bool:
        """Validate the configuration parameters."""
        required_fields = [
            "threshold", "success_value", "failure_value", 
            "measurement_type", "evaluation_period", "success_criteria",
            "calculation_method", "calculation_fields"
        ]
        
        for field in required_fields:
            if not hasattr(self.config, field):
                raise ValueError(f"Missing required field: {field}")
        
        return True
    
    def calculate_progressive_scores(self, daily_values: List[Union[float, int]]) -> List[float]:
        """
        Calculate progressive adherence scores as they would appear each day to the user.
        
        For buildup goals (>=): Shows that day's performance.
        For countdown/limit goals (<=): Shows 100% as long as weekly goal is still achievable.
        
        Args:
            daily_values: List of daily measured values (7 days)
            
        Returns:
            List of progressive scores (what user sees each day)
        """
        progressive_scores = []
        
        # Check if this is a countdown/limit goal (like alcohol limits)
        is_countdown = (self.config.comparison_operator in [ComparisonOperator.LTE, ComparisonOperator.LT])
        
        if is_countdown:
            # For countdown goals, show 100% as long as weekly goal is still achievable
            # Assume 5/7 days compliance requirement for limits
            successes = 0
            required_successes = 5  # Standard assumption for limits
            
            for day_idx, value in enumerate(daily_values):
                day_pass = self._meets_threshold(value)
                if day_pass:
                    successes += 1
                
                remaining_days = len(daily_values) - (day_idx + 1)
                can_still_achieve = (successes + remaining_days) >= required_successes
                
                if successes >= required_successes:
                    progressive_scores.append(self.config.success_value)  # Already achieved
                elif can_still_achieve:
                    progressive_scores.append(self.config.success_value)  # Still possible
                else:
                    progressive_scores.append(self.config.failure_value)  # Impossible now
        else:
            # For buildup goals, show that day's performance
            for value in daily_values:
                score = self.calculate_score(value)
                progressive_scores.append(score)
        
        return progressive_scores
    
    def get_formula(self) -> str:
        """Return the algorithm formula as a string."""
        op = self.config.comparison_operator.value
        return f"if (actual_value {op} {self.config.threshold}) then {self.config.success_value} else {self.config.failure_value}"


def create_daily_binary_threshold(
    threshold: Union[float, int, bool],
    success_value: float = 100,
    failure_value: float = 0,
    comparison_operator: str = ">=",
    description: str = ""
) -> BinaryThresholdAlgorithm:
    """Create a daily binary threshold algorithm."""
    config = BinaryThresholdConfig(
        threshold=threshold,
        success_value=success_value,
        failure_value=failure_value,
        comparison_operator=ComparisonOperator(comparison_operator),
        evaluation_period=EvaluationPeriod.DAILY,
        description=description
    )
    return BinaryThresholdAlgorithm(config)


def create_frequency_binary_threshold(
    threshold: Union[float, int, bool],
    frequency_requirement: str,
    success_value: float = 100,
    failure_value: float = 0,
    comparison_operator: str = ">=",
    description: str = ""
) -> BinaryThresholdAlgorithm:
    """Create a frequency-based binary threshold algorithm."""
    config = BinaryThresholdConfig(
        threshold=threshold,
        success_value=success_value,
        failure_value=failure_value,
        comparison_operator=ComparisonOperator(comparison_operator),
        evaluation_period=EvaluationPeriod.ROLLING_7_DAY,
        success_criteria=SuccessCriteria.FREQUENCY_TARGET,
        frequency_requirement=frequency_requirement,
        description=description
    )
    return BinaryThresholdAlgorithm(config)