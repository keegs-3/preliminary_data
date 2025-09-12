"""
SC-WEEKLY-ELIMINATION Algorithm Implementation
============================================

Scores based on complete elimination of unwanted behaviors across entire weeks.
Any violation during the week results in failure for the entire weekly period.

Algorithm Type: SC-WEEKLY-ELIMINATION
Pattern: Weekly Elimination Block
Evaluation: Weekly (7 days) or other time blocks  
Scoring: Binary (100 or 0)
Logic: Zero tolerance - any violation fails entire week
"""

from typing import List, Dict, Any, Union
import logging

logger = logging.getLogger(__name__)


def calculate_weekly_elimination_score(
    daily_values: List[float],
    elimination_threshold: float = 0,
    elimination_comparison: str = "==",
    **kwargs
) -> Dict[str, Any]:
    """
    Calculate SC-WEEKLY-ELIMINATION score for daily elimination pattern
    
    Args:
        daily_values: List of 7 daily measurements [Mon, Tue, Wed, Thu, Fri, Sat, Sun]
        elimination_threshold: Target value for elimination (usually 0)
        elimination_comparison: Comparison operator ("==", "<=", ">=")
        **kwargs: Additional parameters from config schema
        
    Returns:
        Dict with score and violation details
        
    Examples:
        # Complete ultra-processed food elimination (0 every day)
        calculate_weekly_elimination_score(
            daily_values=[0, 0, 1, 0, 0, 0, 0],  # Wednesday violation
            elimination_threshold=0,
            elimination_comparison="=="
        )
        # Returns: {"score": 0, "violations": 1, "violation_days": [3]}
        
        # Complete smoking cessation
        calculate_weekly_elimination_score(
            daily_values=[0, 0, 0, 0, 0, 0, 0],  # Clean week
            elimination_threshold=0,
            elimination_comparison="=="
        ) 
        # Returns: {"score": 100, "violations": 0, "violation_days": []}
    """
    
    if len(daily_values) != 7:
        raise ValueError(f"Expected 7 daily values for weekly calculation, got {len(daily_values)}")
        
    if elimination_comparison not in ["==", "<=", ">="]:
        raise ValueError(f"Unsupported comparison operator: {elimination_comparison}")
    
    # Check each day for violations
    violations = 0
    violation_days = []
    daily_results = []
    
    for i, daily_value in enumerate(daily_values):
        day_meets_elimination = False
        
        if elimination_comparison == "==":
            day_meets_elimination = daily_value == elimination_threshold
        elif elimination_comparison == "<=":
            day_meets_elimination = daily_value <= elimination_threshold
        elif elimination_comparison == ">=":
            day_meets_elimination = daily_value >= elimination_threshold
            
        if not day_meets_elimination:
            violations += 1
            violation_days.append(i + 1)  # 1-indexed day numbers
            
        daily_results.append({
            'day': i + 1,
            'value': daily_value,
            'meets_elimination': day_meets_elimination,
            'comparison': f"{daily_value} {elimination_comparison} {elimination_threshold}",
            'status': 'CLEAN' if day_meets_elimination else 'VIOLATION'
        })
    
    # Zero tolerance: any violation = entire week fails
    score = 100 if violations == 0 else 0
    
    result = {
        'score': score,
        'violations': violations,
        'violation_days': violation_days,
        'clean_days': 7 - violations,
        'elimination_achieved': violations == 0,
        'details': f"{'SUCCESS' if violations == 0 else 'FAILED'} - {violations} violation(s) in week",
        'daily_breakdown': daily_results,
        'algorithm': 'SC-WEEKLY-ELIMINATION'
    }
    
    logger.info(f"SC-WEEKLY-ELIMINATION: {violations} violations, score: {score}")
    
    return result


def calculate_weekly_limit_score(
    daily_values: List[float],
    weekly_limit: int,
    **kwargs
) -> Dict[str, Any]:
    """
    Calculate SC-WEEKLY-ELIMINATION score for weekly sum limits
    
    Args:
        daily_values: List of 7 daily measurements
        weekly_limit: Maximum allowed total for the week
        **kwargs: Additional parameters
        
    Returns:
        Dict with score and weekly total
        
    Examples:
        # Takeout meals: ≤1 per week
        calculate_weekly_limit_score(
            daily_values=[1, 0, 0, 0, 0, 0, 1],  # 2 meals total
            weekly_limit=1
        )
        # Returns: {"score": 0, "weekly_total": 2, "limit_exceeded": True}
        
        # Takeout meals: ≤1 per week (success)
        calculate_weekly_limit_score(
            daily_values=[0, 0, 1, 0, 0, 0, 0],  # 1 meal total
            weekly_limit=1
        )
        # Returns: {"score": 100, "weekly_total": 1, "limit_exceeded": False}
    """
    
    if len(daily_values) != 7:
        raise ValueError(f"Expected 7 daily values for weekly calculation, got {len(daily_values)}")
    
    weekly_total = sum(daily_values)
    limit_exceeded = weekly_total > weekly_limit
    
    # Binary scoring: success if within limit
    score = 100 if not limit_exceeded else 0
    
    result = {
        'score': score,
        'weekly_total': weekly_total,
        'weekly_limit': weekly_limit,
        'limit_exceeded': limit_exceeded,
        'remaining_allowance': max(0, weekly_limit - weekly_total),
        'details': f"{'SUCCESS' if not limit_exceeded else 'EXCEEDED'} - {weekly_total}/{weekly_limit} weekly limit",
        'daily_values': daily_values,
        'algorithm': 'SC-WEEKLY-ELIMINATION (weekly limit)'
    }
    
    logger.info(f"SC-WEEKLY-ELIMINATION (limit): {weekly_total}/{weekly_limit}, score: {score}")
    
    return result


def calculate_monthly_limit_score(
    daily_values: List[float],
    monthly_limit: int,
    **kwargs  
) -> Dict[str, Any]:
    """
    Calculate SC-WEEKLY-ELIMINATION score for monthly sum limits
    
    Args:
        daily_values: List of daily measurements for the month (28-31 values)
        monthly_limit: Maximum allowed total for the month
        **kwargs: Additional parameters
        
    Returns:
        Dict with score and monthly total
    """
    
    if len(daily_values) < 28 or len(daily_values) > 31:
        raise ValueError(f"Expected 28-31 daily values for monthly calculation, got {len(daily_values)}")
    
    monthly_total = sum(daily_values)
    limit_exceeded = monthly_total > monthly_limit
    
    score = 100 if not limit_exceeded else 0
    
    result = {
        'score': score,
        'monthly_total': monthly_total,
        'monthly_limit': monthly_limit,
        'limit_exceeded': limit_exceeded,
        'remaining_allowance': max(0, monthly_limit - monthly_total),
        'days_in_month': len(daily_values),
        'details': f"{'SUCCESS' if not limit_exceeded else 'EXCEEDED'} - {monthly_total}/{monthly_limit} monthly limit",
        'algorithm': 'SC-WEEKLY-ELIMINATION (monthly limit)'
    }
    
    logger.info(f"SC-WEEKLY-ELIMINATION (monthly): {monthly_total}/{monthly_limit}, score: {score}")
    
    return result


def calculate_single_day_elimination_score(
    daily_value: float,
    elimination_threshold: float = 0,
    elimination_comparison: str = "==",
    **kwargs
) -> Dict[str, Any]:
    """
    Calculate single day contribution to SC-WEEKLY-ELIMINATION score
    
    This is a helper for real-time scoring. The full weekly score requires all 7 days,
    and any single violation fails the entire week.
    
    Args:
        daily_value: Single day's measurement
        elimination_threshold: Target for elimination
        elimination_comparison: Comparison operator
        
    Returns:
        Dict indicating if this day violates elimination criteria
    """
    
    # Check if this day meets elimination criteria
    day_meets_elimination = False
    if elimination_comparison == "==":
        day_meets_elimination = daily_value == elimination_threshold
    elif elimination_comparison == "<=":
        day_meets_elimination = daily_value <= elimination_threshold  
    elif elimination_comparison == ">=":
        day_meets_elimination = daily_value >= elimination_threshold
        
    return {
        'day_score': 100 if day_meets_elimination else 0,
        'meets_elimination': day_meets_elimination,
        'is_violation': not day_meets_elimination,
        'comparison_result': f"{daily_value} {elimination_comparison} {elimination_threshold}",
        'week_impact': 'CLEAN DAY' if day_meets_elimination else 'WEEK FAILED',
        'note': f"{'Success' if day_meets_elimination else 'Violation'} - any violation fails entire week",
        'algorithm': 'SC-WEEKLY-ELIMINATION (single day)'
    }


def validate_weekly_elimination_config(config: Dict[str, Any]) -> List[str]:
    """
    Validate SC-WEEKLY-ELIMINATION configuration
    
    Args:
        config: Algorithm configuration dictionary
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    calculation_method = config.get('calculation_method')
    
    if calculation_method == 'weekly_sum_limit':
        if 'weekly_limit' not in config:
            errors.append("weekly_limit required for weekly_sum_limit method")
        elif not isinstance(config['weekly_limit'], (int, float)) or config['weekly_limit'] < 0:
            errors.append("weekly_limit must be a non-negative number")
            
    elif calculation_method == 'monthly_sum_limit':
        if 'monthly_limit' not in config:
            errors.append("monthly_limit required for monthly_sum_limit method")
        elif not isinstance(config['monthly_limit'], (int, float)) or config['monthly_limit'] < 0:
            errors.append("monthly_limit must be a non-negative number")
            
    else:
        # Default daily elimination method
        required_fields = ['elimination_threshold', 'elimination_comparison']
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")
                
        if 'elimination_comparison' in config:
            if config['elimination_comparison'] not in ["==", "<=", ">="]:
                errors.append(f"Invalid elimination_comparison: {config['elimination_comparison']}")
    
    return errors


# Example usage and testing
if __name__ == "__main__":
    # Example 1: Complete elimination (ultra-processed foods)
    ultra_processed_clean = [0, 0, 0, 0, 0, 0, 0]  # Perfect week
    result1 = calculate_weekly_elimination_score(
        daily_values=ultra_processed_clean,
        elimination_threshold=0,
        elimination_comparison="=="
    )
    print("Clean elimination week:", result1)
    
    # Example 2: Violation in elimination
    ultra_processed_violation = [0, 0, 1, 0, 0, 0, 0]  # Wednesday violation
    result2 = calculate_weekly_elimination_score(
        daily_values=ultra_processed_violation,
        elimination_threshold=0,
        elimination_comparison="=="
    )
    print("Week with violation:", result2)
    
    # Example 3: Weekly limit (takeout meals)
    takeout_within_limit = [0, 0, 1, 0, 0, 0, 0]  # 1 meal, limit is 1
    result3 = calculate_weekly_limit_score(
        daily_values=takeout_within_limit,
        weekly_limit=1
    )
    print("Within weekly limit:", result3)
    
    # Example 4: Weekly limit exceeded
    takeout_over_limit = [1, 0, 0, 0, 0, 0, 1]  # 2 meals, limit is 1
    result4 = calculate_weekly_limit_score(
        daily_values=takeout_over_limit,
        weekly_limit=1
    )
    print("Weekly limit exceeded:", result4)