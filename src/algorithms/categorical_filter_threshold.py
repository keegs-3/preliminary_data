"""
Categorical Filter Threshold Algorithm

Applies filtering based on categorical criteria before threshold evaluation.
Supports category-specific thresholds and scoring rules.
"""

from typing import Dict, Any, Union, List
from dataclasses import dataclass
from enum import Enum
from .binary_threshold import EvaluationPeriod, SuccessCriteria, CalculationMethod, ComparisonOperator


@dataclass
class CategoryFilter:
    """Represents a category filter with its criteria and thresholds."""
    category_name: str
    category_values: List[str]  # Values that match this category
    threshold: Union[float, int, bool]
    success_value: float = 100
    failure_value: float = 0
    comparison_operator: ComparisonOperator = ComparisonOperator.GTE
    weight: float = 1.0  # Weight for this category in composite scoring


@dataclass
class CategoricalFilterThresholdConfig:
    category_field: str  # Field name containing the category
    category_filters: List[CategoryFilter]
    default_threshold: Union[float, int, bool] = 0
    default_success_value: float = 50
    default_failure_value: float = 0
    measurement_type: str = "categorical"
    evaluation_period: EvaluationPeriod = EvaluationPeriod.DAILY
    success_criteria: SuccessCriteria = SuccessCriteria.SIMPLE_TARGET
    calculation_method: CalculationMethod = CalculationMethod.LAST_VALUE
    calculation_fields: Union[str, Dict[str, Any]] = "value"
    aggregation_method: str = "weighted_average"  # How to combine multiple category scores
    frequency_requirement: str = "daily"
    description: str = ""


class CategoricalFilterThresholdAlgorithm:
    """Categorical filter threshold algorithm implementation."""
    
    def __init__(self, config: CategoricalFilterThresholdConfig):
        self.config = config
        self._validate_categories()
    
    def calculate_score(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate score based on categorical filtering and thresholds.
        
        Args:
            data: Dictionary containing category field and value field
            
        Returns:
            Dict containing score and detailed breakdown
        """
        category_value = data.get(self.config.category_field)
        measured_value = data.get("value", 0)
        
        if category_value is None:
            raise ValueError(f"Missing category field: {self.config.category_field}")
        
        # Find matching category filter
        matching_filter = self._find_matching_filter(category_value)
        
        if matching_filter:
            # Apply category-specific threshold
            score = self._calculate_threshold_score(
                measured_value, 
                matching_filter.threshold,
                matching_filter.success_value,
                matching_filter.failure_value,
                matching_filter.comparison_operator
            )
            
            return {
                "score": score,
                "matched_category": matching_filter.category_name,
                "category_value": category_value,
                "threshold_used": matching_filter.threshold,
                "measured_value": measured_value,
                "filter_applied": True
            }
        else:
            # Use default threshold
            score = self._calculate_threshold_score(
                measured_value,
                self.config.default_threshold,
                self.config.default_success_value,
                self.config.default_failure_value,
                ComparisonOperator.GTE
            )
            
            return {
                "score": score,
                "matched_category": "default",
                "category_value": category_value,
                "threshold_used": self.config.default_threshold,
                "measured_value": measured_value,
                "filter_applied": False
            }
    
    def calculate_multi_category_score(self, data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate score for multiple categorical data points.
        
        Args:
            data_list: List of data dictionaries
            
        Returns:
            Aggregated score and breakdown
        """
        if not data_list:
            return {"score": 0, "breakdown": [], "error": "No data provided"}
        
        category_scores = []
        breakdown = []
        
        for data in data_list:
            result = self.calculate_score(data)
            category_scores.append({
                "score": result["score"],
                "weight": self._get_category_weight(result["matched_category"])
            })
            breakdown.append(result)
        
        # Aggregate scores based on method
        if self.config.aggregation_method == "weighted_average":
            total_weighted_score = sum(cs["score"] * cs["weight"] for cs in category_scores)
            total_weight = sum(cs["weight"] for cs in category_scores)
            final_score = total_weighted_score / total_weight if total_weight > 0 else 0
        
        elif self.config.aggregation_method == "simple_average":
            final_score = sum(cs["score"] for cs in category_scores) / len(category_scores)
        
        elif self.config.aggregation_method == "minimum":
            final_score = min(cs["score"] for cs in category_scores)
        
        elif self.config.aggregation_method == "maximum":
            final_score = max(cs["score"] for cs in category_scores)
        
        else:
            final_score = sum(cs["score"] for cs in category_scores) / len(category_scores)
        
        return {
            "score": final_score,
            "aggregation_method": self.config.aggregation_method,
            "categories_processed": len(data_list),
            "breakdown": breakdown
        }
    
    def _find_matching_filter(self, category_value: str) -> CategoryFilter:
        """Find the filter that matches the given category value."""
        for filter_config in self.config.category_filters:
            if category_value in filter_config.category_values:
                return filter_config
        return None
    
    def _calculate_threshold_score(
        self, 
        actual_value: Union[float, int, bool], 
        threshold: Union[float, int, bool],
        success_value: float,
        failure_value: float,
        comparison_operator: ComparisonOperator
    ) -> float:
        """Calculate binary threshold score."""
        meets_threshold = False
        
        if comparison_operator == ComparisonOperator.GTE:
            meets_threshold = actual_value >= threshold
        elif comparison_operator == ComparisonOperator.GT:
            meets_threshold = actual_value > threshold
        elif comparison_operator == ComparisonOperator.EQ:
            meets_threshold = actual_value == threshold
        elif comparison_operator == ComparisonOperator.LT:
            meets_threshold = actual_value < threshold
        elif comparison_operator == ComparisonOperator.LTE:
            meets_threshold = actual_value <= threshold
        
        return success_value if meets_threshold else failure_value
    
    def _get_category_weight(self, category_name: str) -> float:
        """Get weight for a category."""
        if category_name == "default":
            return 1.0
        
        for filter_config in self.config.category_filters:
            if filter_config.category_name == category_name:
                return filter_config.weight
        
        return 1.0
    
    def _validate_categories(self):
        """Validate category filter configuration."""
        if not self.config.category_filters:
            raise ValueError("At least one category filter must be defined")
        
        # Check for duplicate category values across filters
        all_values = set()
        for filter_config in self.config.category_filters:
            for value in filter_config.category_values:
                if value in all_values:
                    raise ValueError(f"Duplicate category value: {value}")
                all_values.add(value)
        
        # Validate weights
        for filter_config in self.config.category_filters:
            if filter_config.weight < 0:
                raise ValueError(f"Category weight cannot be negative: {filter_config.category_name}")
    
    def validate_config(self) -> bool:
        """Validate the configuration parameters."""
        required_fields = ["category_field", "category_filters"]
        
        for field in required_fields:
            if not hasattr(self.config, field):
                raise ValueError(f"Missing required field: {field}")
        
        self._validate_categories()
        return True
    
    def get_formula(self) -> str:
        """Return the algorithm formula as a string."""
        return "filter_by_category(data) then apply_threshold(filtered_value)"
    
    def get_category_info(self) -> str:
        """Return information about all category filters."""
        info = []
        for filter_config in self.config.category_filters:
            values_str = ", ".join(filter_config.category_values)
            info.append(f"{filter_config.category_name}: [{values_str}] threshold={filter_config.threshold}")
        return "\n".join(info)


def create_daily_categorical_filter(
    category_field: str,
    category_filters: List[CategoryFilter],
    default_threshold: Union[float, int, bool] = 0,
    aggregation_method: str = "weighted_average",
    description: str = ""
) -> CategoricalFilterThresholdAlgorithm:
    """Create a daily categorical filter threshold algorithm."""
    config = CategoricalFilterThresholdConfig(
        category_field=category_field,
        category_filters=category_filters,
        default_threshold=default_threshold,
        aggregation_method=aggregation_method,
        evaluation_period=EvaluationPeriod.DAILY,
        description=description
    )
    return CategoricalFilterThresholdAlgorithm(config)


def create_frequency_categorical_filter(
    category_field: str,
    category_filters: List[CategoryFilter],
    frequency_requirement: str,
    default_threshold: Union[float, int, bool] = 0,
    aggregation_method: str = "weighted_average",
    description: str = ""
) -> CategoricalFilterThresholdAlgorithm:
    """Create a frequency-based categorical filter threshold algorithm."""
    config = CategoricalFilterThresholdConfig(
        category_field=category_field,
        category_filters=category_filters,
        default_threshold=default_threshold,
        aggregation_method=aggregation_method,
        evaluation_period=EvaluationPeriod.ROLLING_7_DAY,
        success_criteria=SuccessCriteria.FREQUENCY_TARGET,
        frequency_requirement=frequency_requirement,
        description=description
    )
    return CategoricalFilterThresholdAlgorithm(config)