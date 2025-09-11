"""
Scoring Algorithms Package

Provides implementations for various scoring algorithms:
- Binary Threshold: Pass/fail scoring based on threshold
- Proportional: Percentage-based scoring relative to target
- Zone-Based: Score based on which zone value falls into
- Composite Weighted: Weighted average of multiple components
"""

from .binary_threshold import (
    BinaryThresholdAlgorithm,
    BinaryThresholdConfig,
    create_daily_binary_threshold,
    create_frequency_binary_threshold,
    ComparisonOperator
)

from .proportional import (
    ProportionalAlgorithm,
    ProportionalConfig,
    create_daily_proportional,
    create_frequency_proportional
)

from .zone_based import (
    ZoneBasedAlgorithm,
    ZoneBasedConfig,
    Zone,
    create_daily_zone_based,
    create_frequency_zone_based,
    create_sleep_duration_zones
)

from .composite_weighted import (
    CompositeWeightedAlgorithm,
    CompositeWeightedConfig,
    Component,
    create_daily_composite,
    create_frequency_composite,
    create_sleep_quality_composite
)

from .constrained_weekly_allowance import (
    ConstrainedWeeklyAllowanceAlgorithm,
    ConstrainedWeeklyAllowanceConfig,
    create_weekly_allowance
)

from .categorical_filter_threshold import (
    CategoricalFilterThresholdAlgorithm,
    CategoricalFilterThresholdConfig,
    CategoryFilter,
    create_daily_categorical_filter,
    create_frequency_categorical_filter
)

from .binary_threshold import (
    EvaluationPeriod,
    SuccessCriteria,
    CalculationMethod
)

__all__ = [
    # Binary Threshold
    "BinaryThresholdAlgorithm",
    "BinaryThresholdConfig",
    "create_daily_binary_threshold",
    "create_frequency_binary_threshold",
    "ComparisonOperator",
    
    # Proportional
    "ProportionalAlgorithm",
    "ProportionalConfig",
    "create_daily_proportional",
    "create_frequency_proportional",
    
    # Zone-Based
    "ZoneBasedAlgorithm",
    "ZoneBasedConfig",
    "Zone",
    "create_daily_zone_based",
    "create_frequency_zone_based",
    "create_sleep_duration_zones",
    
    # Composite Weighted
    "CompositeWeightedAlgorithm",
    "CompositeWeightedConfig",
    "Component",
    "create_daily_composite",
    "create_frequency_composite",
    "create_sleep_quality_composite",
    
    # Constrained Weekly Allowance
    "ConstrainedWeeklyAllowanceAlgorithm",
    "ConstrainedWeeklyAllowanceConfig",
    "create_weekly_allowance",
    
    # Categorical Filter Threshold
    "CategoricalFilterThresholdAlgorithm",
    "CategoricalFilterThresholdConfig",
    "CategoryFilter",
    "create_daily_categorical_filter",
    "create_frequency_categorical_filter",
    
    # Common Enums
    "EvaluationPeriod",
    "SuccessCriteria",
    "CalculationMethod"
]