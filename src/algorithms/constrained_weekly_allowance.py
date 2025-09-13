"""
Constrained Weekly Allowance Algorithm

Manages weekly allowances with constraints and rollover rules.
Tracks weekly budgets and spending patterns.
"""

from typing import Dict, Any, Union, List
from dataclasses import dataclass
from datetime import datetime, timedelta
from .binary_threshold import EvaluationPeriod, SuccessCriteria, CalculationMethod


@dataclass
class ConstrainedWeeklyAllowanceConfig:
    weekly_allowance: float
    unit: str
    rollover_enabled: bool = False
    max_rollover_percentage: float = 50.0
    minimum_weekly_usage: float = 0.0
    penalty_for_overage: float = 0.0
    measurement_type: str = "count"
    evaluation_period: str = "weekly_constraint"
    success_criteria: SuccessCriteria = SuccessCriteria.SIMPLE_TARGET
    calculation_method: CalculationMethod = CalculationMethod.SUM
    calculation_fields: Union[str, Dict[str, Any]] = "weekly_usage"
    max_days_per_week: int = None  # Maximum days per week constraint
    description: str = ""


class ConstrainedWeeklyAllowanceAlgorithm:
    """Constrained weekly allowance algorithm implementation."""
    
    def __init__(self, config: ConstrainedWeeklyAllowanceConfig):
        self.config = config
        self.weekly_history = {}  # Track usage history by week
    
    def calculate_score(self, daily_values: List[Union[float, int]] = None, weekly_usage: float = None, week_identifier: str = None) -> Dict[str, Any]:
        """
        Calculate score based on weekly allowance constraints.
        
        Args:
            daily_values: List of daily values (7 days) for dual constraint checking
            weekly_usage: Amount used this week (if daily_values not provided)
            week_identifier: Unique identifier for the week (e.g., "2024-W01")
            
        Returns:
            Dict containing score, allowance status, and details
        """
        if week_identifier is None:
            week_identifier = self._get_current_week_id()
        
        # Calculate weekly usage and days used from daily values
        if daily_values is not None:
            weekly_usage = sum(daily_values)
            days_used = sum(1 for value in daily_values if value > 0)
        else:
            days_used = None  # Can't determine days used from total only
        
        # Get available allowance for this week
        available_allowance = self._calculate_available_allowance(week_identifier)
        
        # Check dual constraints if max_days_per_week is specified
        if self.config.max_days_per_week is not None and days_used is not None:
            if days_used > self.config.max_days_per_week:
                # Violates max days constraint - immediate failure
                compliance_score = 0.0
                status = "exceeds_max_days"
                overage = weekly_usage - available_allowance if weekly_usage > available_allowance else 0.0
                
                # Update history
                self.weekly_history[week_identifier] = {
                    "usage": weekly_usage,
                    "allowance": available_allowance,
                    "overage": overage,
                    "score": compliance_score,
                    "days_used": days_used,
                    "max_days": self.config.max_days_per_week
                }
                
                return {
                    "score": compliance_score,
                    "status": status,
                    "weekly_usage": weekly_usage,
                    "available_allowance": available_allowance,
                    "overage": overage,
                    "remaining_allowance": max(0.0, available_allowance - weekly_usage),
                    "days_used": days_used,
                    "max_days_allowed": self.config.max_days_per_week
                }
        
        # Calculate base compliance score
        if weekly_usage <= available_allowance:
            compliance_score = 100.0
            overage = 0.0
            status = "within_allowance"
        else:
            overage = weekly_usage - available_allowance
            # Penalty for going over allowance
            penalty = min(overage * self.config.penalty_for_overage, 100.0)
            compliance_score = max(0.0, 100.0 - penalty)
            status = "over_allowance"
        
        # Check minimum usage requirement
        if weekly_usage < self.config.minimum_weekly_usage:
            compliance_score = max(0.0, compliance_score - 20.0)  # Penalty for under-usage
            status = "under_minimum"
        
        # Update history
        history_data = {
            "usage": weekly_usage,
            "allowance": available_allowance,
            "overage": overage,
            "score": compliance_score
        }
        if days_used is not None:
            history_data["days_used"] = days_used
            history_data["max_days"] = self.config.max_days_per_week
            
        self.weekly_history[week_identifier] = history_data
        
        result = {
            "score": compliance_score,
            "status": status,
            "weekly_usage": weekly_usage,
            "available_allowance": available_allowance,
            "overage": overage,
            "remaining_allowance": max(0.0, available_allowance - weekly_usage)
        }
        if days_used is not None:
            result["days_used"] = days_used
            result["max_days_allowed"] = self.config.max_days_per_week
            
        return result
    
    def _calculate_available_allowance(self, week_identifier: str) -> float:
        """Calculate available allowance including any rollovers."""
        base_allowance = self.config.weekly_allowance
        
        if not self.config.rollover_enabled:
            return base_allowance
        
        # Calculate rollover from previous week
        previous_week = self._get_previous_week_id(week_identifier)
        if previous_week in self.weekly_history:
            prev_data = self.weekly_history[previous_week]
            unused_amount = max(0.0, prev_data["allowance"] - prev_data["usage"])
            
            # Apply rollover limits
            max_rollover = base_allowance * (self.config.max_rollover_percentage / 100.0)
            rollover_amount = min(unused_amount, max_rollover)
            
            return base_allowance + rollover_amount
        
        return base_allowance
    
    def _get_current_week_id(self) -> str:
        """Get current week identifier."""
        now = datetime.now()
        year, week, _ = now.isocalendar()
        return f"{year}-W{week:02d}"
    
    def _get_previous_week_id(self, week_identifier: str) -> str:
        """Get previous week identifier."""
        try:
            year, week_str = week_identifier.split("-W")
            week = int(week_str)
            
            if week == 1:
                # Handle year rollover
                prev_year = int(year) - 1
                # Get last week of previous year
                last_week = datetime(prev_year, 12, 31).isocalendar()[1]
                return f"{prev_year}-W{last_week:02d}"
            else:
                return f"{year}-W{week-1:02d}"
        except:
            return "unknown"
    
    def get_weekly_summary(self, week_identifier: str = None) -> Dict[str, Any]:
        """Get summary for a specific week."""
        if week_identifier is None:
            week_identifier = self._get_current_week_id()
        
        if week_identifier not in self.weekly_history:
            return {"error": "No data for specified week"}
        
        return self.weekly_history[week_identifier]
    
    def get_usage_trend(self, num_weeks: int = 4) -> List[Dict[str, Any]]:
        """Get usage trend over recent weeks."""
        sorted_weeks = sorted(self.weekly_history.keys(), reverse=True)
        recent_weeks = sorted_weeks[:num_weeks]
        
        trend = []
        for week in reversed(recent_weeks):  # Chronological order
            data = self.weekly_history[week]
            trend.append({
                "week": week,
                "usage": data["usage"],
                "allowance": data["allowance"],
                "score": data["score"],
                "utilization_percentage": (data["usage"] / data["allowance"]) * 100
            })
        
        return trend
    
    def validate_config(self) -> bool:
        """Validate the configuration parameters."""
        if self.config.weekly_allowance <= 0:
            raise ValueError("Weekly allowance must be greater than 0")
        
        if self.config.max_rollover_percentage < 0 or self.config.max_rollover_percentage > 100:
            raise ValueError("Max rollover percentage must be between 0 and 100")
        
        if self.config.minimum_weekly_usage < 0:
            raise ValueError("Minimum weekly usage cannot be negative")
        
        if self.config.penalty_for_overage < 0:
            raise ValueError("Penalty for overage cannot be negative")
        
        return True
    
    def calculate_progressive_scores(self, daily_values: List[Union[float, int]]) -> List[float]:
        """
        Calculate progressive adherence scores as they would appear each day to the user.
        
        For weekly allowance: Shows cumulative usage against weekly allowance.
        
        Args:
            daily_values: List of daily measured values (7 days)
            
        Returns:
            List of progressive scores (what user sees each day)
        """
        progressive_scores = []
        cumulative_usage = 0
        
        for value in daily_values:
            cumulative_usage += value
            
            if cumulative_usage <= self.config.weekly_allowance:
                progressive_scores.append(100.0)
            else:
                # Calculate penalty for exceeding allowance
                overage = cumulative_usage - self.config.weekly_allowance
                penalty = min(overage * self.config.penalty_for_overage, 100.0)
                score = max(0.0, 100.0 - penalty)
                progressive_scores.append(score)
        
        return progressive_scores
    
    def get_formula(self) -> str:
        """Return the algorithm formula as a string."""
        if self.config.max_days_per_week is not None:
            return f"(weekly_usage <= {self.config.weekly_allowance} AND days_used <= {self.config.max_days_per_week}) ? 100 : 0"
        return "weekly_usage <= allowance ? 100 : max(0, 100 - overage_penalty)"


def create_weekly_allowance(
    weekly_allowance: float,
    unit: str,
    rollover_enabled: bool = False,
    max_rollover_percentage: float = 50.0,
    penalty_for_overage: float = 10.0,
    max_days_per_week: int = None,
    description: str = ""
) -> ConstrainedWeeklyAllowanceAlgorithm:
    """Create a constrained weekly allowance algorithm."""
    config = ConstrainedWeeklyAllowanceConfig(
        weekly_allowance=weekly_allowance,
        unit=unit,
        rollover_enabled=rollover_enabled,
        max_rollover_percentage=max_rollover_percentage,
        penalty_for_overage=penalty_for_overage,
        max_days_per_week=max_days_per_week,
        description=description
    )
    return ConstrainedWeeklyAllowanceAlgorithm(config)