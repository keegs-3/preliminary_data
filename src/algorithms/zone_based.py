"""
Zone-Based Scoring Algorithm

Assigns scores based on which zone the actual value falls into.
Supports 5-tier zone system with configurable ranges and scores.
"""

from typing import Dict, Any, Union, List
from dataclasses import dataclass
from .binary_threshold import EvaluationPeriod, SuccessCriteria, CalculationMethod


@dataclass
class Zone:
    """Represents a scoring zone with range and score."""
    min_value: Union[float, int]
    max_value: Union[float, int]
    score: float
    label: str
    
    def contains(self, value: Union[float, int]) -> bool:
        """Check if value falls within this zone (inclusive of boundaries)."""
        return self.min_value <= value <= self.max_value


@dataclass
class ZoneBasedConfig:
    zones: List[Zone]
    unit: str
    measurement_type: str = "duration"
    evaluation_period: EvaluationPeriod = EvaluationPeriod.DAILY
    success_criteria: SuccessCriteria = SuccessCriteria.SIMPLE_TARGET
    calculation_method: CalculationMethod = CalculationMethod.SUM
    calculation_fields: Union[str, Dict[str, Any]] = "value"
    grace_range: bool = False
    boundary_handling: str = "strict"
    frequency_requirement: str = "daily"
    description: str = ""


class ZoneBasedAlgorithm:
    """Zone-based scoring algorithm implementation."""
    
    def __init__(self, config: ZoneBasedConfig, frequency_target: int = None):
        self.config = config
        self.frequency_target = frequency_target  # For frequency-based evaluation
        self._validate_zones()
    
    def calculate_score(self, actual_value: Union[float, int]) -> float:
        """
        Calculate score based on which zone the value falls into.
        
        Args:
            actual_value: The measured value to evaluate
            
        Returns:
            Score based on the zone the value falls into
        """
        # Sort zones by min_value to ensure we find the first matching zone
        sorted_zones = sorted(self.config.zones, key=lambda z: z.min_value)
        
        for zone in sorted_zones:
            if zone.contains(actual_value):
                if self.config.grace_range and self.config.boundary_handling == "graduated":
                    return self._apply_graduated_scoring(actual_value, zone)
                return zone.score
        
        # Value doesn't fall in any zone - return 0
        return 0.0
    
    def _apply_graduated_scoring(self, value: Union[float, int], zone: Zone) -> float:
        """Apply graduated scoring near zone boundaries."""
        zone_width = zone.max_value - zone.min_value
        if zone_width == 0:
            return zone.score
        
        # Calculate position within zone (0.0 to 1.0)
        position = (value - zone.min_value) / zone_width
        
        # Apply a small gradient based on position
        gradient_factor = 0.95 + (0.05 * position)  # 95% to 100% of zone score
        return zone.score * gradient_factor
    
    def _validate_zones(self):
        """Validate zone configuration."""
        if not self.config.zones:
            raise ValueError("Zone-based algorithm requires zones to be defined")
        
        # Allow both 3-tier and 5-tier zones
        valid_zone_counts = [3, 5]
        if len(self.config.zones) not in valid_zone_counts:
            raise ValueError(f"Zone-based algorithm requires {valid_zone_counts} zones, got {len(self.config.zones)}")
        
        # Sort zones by min_value for validation
        sorted_zones = sorted(self.config.zones, key=lambda z: z.min_value)
        
        # Check for gaps or overlaps (allow adjacent zones where max = next min)
        for i in range(len(sorted_zones) - 1):
            current_zone = sorted_zones[i]
            next_zone = sorted_zones[i + 1]
            
            if current_zone.max_value < next_zone.min_value:
                raise ValueError(f"Gap between zones: {current_zone.label} and {next_zone.label}")
            
            if current_zone.max_value > next_zone.min_value:
                raise ValueError(f"Overlap between zones: {current_zone.label} and {next_zone.label}")
    
    def validate_config(self) -> bool:
        """Validate the configuration parameters."""
        required_fields = [
            "zones", "unit", "measurement_type", "evaluation_period",
            "success_criteria", "calculation_method", "calculation_fields"
        ]
        
        for field in required_fields:
            if not hasattr(self.config, field):
                raise ValueError(f"Missing required field: {field}")
        
        self._validate_zones()
        return True
    
    def calculate_weekly_frequency_score(self, daily_values: List[Union[float, int]], target_zone_score: float = 100) -> float:
        """Calculate weekly score based on frequency of hitting target zone."""
        if not self.frequency_target:
            # No frequency requirement, return average of daily scores
            daily_scores = [self.calculate_score(value) for value in daily_values]
            return sum(daily_scores) / len(daily_scores)
        
        # Count days that hit the target zone (e.g., optimal sleep = 100 points)
        target_days = 0
        for value in daily_values:
            if self.calculate_score(value) >= target_zone_score:
                target_days += 1
        
        # Calculate achievement ratio
        if target_days >= self.frequency_target:
            return 100.0  # Full achievement
        else:
            return (target_days / self.frequency_target) * 100
    
    def get_formula(self) -> str:
        """Return the algorithm formula as a string."""
        if self.frequency_target:
            return f"frequency-based: score based on hitting target zone {self.frequency_target} days per week"
        return "score based on which zone actual_value falls into"
    
    def calculate_progressive_scores(self, daily_values: List[Union[float, int]]) -> List[float]:
        """
        Calculate progressive adherence scores as they would appear each day to the user.
        
        For zone-based algorithms: Each day is independent, shows that day's zone score.
        
        Args:
            daily_values: List of daily measured values (7 days)
            
        Returns:
            List of progressive scores (what user sees each day)
        """
        progressive_scores = []
        
        for value in daily_values:
            score = self.calculate_score(value)
            progressive_scores.append(score)
        
        return progressive_scores
    
    def get_zone_info(self) -> str:
        """Return information about all zones."""
        info = []
        for zone in self.config.zones:
            info.append(f"{zone.label}: [{zone.min_value}-{zone.max_value}] {zone.score} points")
        return "\n".join(info)


def create_sleep_duration_zones() -> List[Zone]:
    """Create standard sleep duration zones (in hours)."""
    return [
        Zone(0, 5, 20, "Very Poor"),
        Zone(5, 6, 40, "Poor"),
        Zone(6, 7, 60, "Fair"),
        Zone(7, 9, 100, "Good"),
        Zone(9, 12, 80, "Excessive")
    ]


def create_daily_zone_based(
    zones: List[Zone],
    unit: str,
    grace_range: bool = False,
    boundary_handling: str = "strict",
    description: str = ""
) -> ZoneBasedAlgorithm:
    """Create a daily zone-based algorithm."""
    config = ZoneBasedConfig(
        zones=zones,
        unit=unit,
        grace_range=grace_range,
        boundary_handling=boundary_handling,
        evaluation_period=EvaluationPeriod.DAILY,
        description=description
    )
    return ZoneBasedAlgorithm(config)


def create_frequency_zone_based(
    zones: List[Zone],
    unit: str,
    frequency_requirement: str,
    grace_range: bool = False,
    boundary_handling: str = "strict",
    description: str = ""
) -> ZoneBasedAlgorithm:
    """Create a frequency-based zone-based algorithm."""
    config = ZoneBasedConfig(
        zones=zones,
        unit=unit,
        grace_range=grace_range,
        boundary_handling=boundary_handling,
        evaluation_period=EvaluationPeriod.ROLLING_7_DAY,
        success_criteria=SuccessCriteria.FREQUENCY_TARGET,
        frequency_requirement=frequency_requirement,
        description=description
    )
    return ZoneBasedAlgorithm(config)