"""
Recommendation Configuration Generator

Analyzes recommendations and generates appropriate algorithm configurations
using the units_v3 and metric_types_v3 data for proper metric and unit linking.
"""

import csv
import json
import re
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum


class AlgorithmType(Enum):
    BINARY_THRESHOLD = "binary_threshold"
    PROPORTIONAL = "proportional"
    ZONE_BASED_3TIER = "zone_based_3tier"
    ZONE_BASED_5TIER = "zone_based_5tier"
    COMPOSITE_WEIGHTED = "composite_weighted"
    CONSTRAINED_WEEKLY_ALLOWANCE = "constrained_weekly_allowance"
    CATEGORICAL_FILTER = "categorical_filter_threshold"


@dataclass
class RecommendationAnalysis:
    """Analysis of a recommendation to determine best algorithm."""
    algorithm_type: AlgorithmType
    evaluation_pattern: str  # "daily" or "frequency"
    tier_count: Optional[int] = None
    confidence: float = 0.0
    reasoning: str = ""


class RecommendationConfigGenerator:
    """Generates algorithm configurations from recommendations."""
    
    def __init__(self):
        self.units_data = self._load_units_data()
        self.metrics_data = self._load_metrics_data()
        self.generated_configs = []
    
    def _load_units_data(self) -> Dict[str, Dict]:
        """Load units data from CSV."""
        units = {}
        csv_path = Path(__file__).parent / "ref_csv_files_airtable" / "units_v3.csv"
        
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                units[row['identifier']] = {
                    'ui_display': row['ui_display'],
                    'symbol': row['symbol'],
                    'unit_type': row['unit_type'],
                    'metric_types': row.get('metric_types', '').split(',') if row.get('metric_types') else []
                }
        
        return units
    
    def _load_metrics_data(self) -> Dict[str, Dict]:
        """Load metrics data from CSV."""
        metrics = {}
        csv_path = Path(__file__).parent / "ref_csv_files_airtable" / "metric_types_v3.csv"
        
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                metrics[row['identifier']] = {
                    'name': row['name'],
                    'description_general': row['description_general'],
                    'description_frontend': row['description_frontend'],
                    'base_type': row['base_type'],
                    'units_v3': row['units_v3'],
                    'aggregation_style': row['aggregation_style'],
                    'validation_schema': self._safe_parse_json(row.get('validation_schema', '{}')),
                    'recommendations_v2': row.get('recommendations_v2', '').split(',') if row.get('recommendations_v2') else []
                }
        
        return metrics
    
    def _safe_parse_json(self, json_string: str) -> Dict[str, Any]:
        """Safely parse JSON string, handling malformed JSON."""
        if not json_string or json_string.strip() == '':
            return {}
        
        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            try:
                # Try to fix common JSON issues
                fixed = json_string.replace("'", '"')  # Single quotes to double quotes
                fixed = re.sub(r'(\w+):', r'"\1":', fixed)  # Add quotes around keys
                
                # Fix incomplete JSON arrays (missing closing brace)
                if '"allowed_values":' in fixed and not fixed.strip().endswith('}'):
                    if fixed.strip().endswith(','):
                        fixed = fixed.strip().rstrip(',') + '}'
                    elif not fixed.strip().endswith('}'):
                        fixed = fixed.strip() + '}'
                
                return json.loads(fixed)
            except:
                # Silently return empty dict for malformed JSON
                return {}
    
    def analyze_recommendation(self, recommendation_text: str, recommendation_id: str = None) -> RecommendationAnalysis:
        """Analyze a recommendation to determine the best algorithm type."""
        
        text_lower = recommendation_text.lower()
        
        # Keywords for different algorithm types
        binary_keywords = [
            "avoid", "eliminate", "stop", "don't", "never", "always", "must", 
            "complete", "finish", "achieve", "reach", "hit", "yes/no", "true/false",
            "meet", "exceed", "pass", "fail", "threshold", "minimum"
        ]
        
        # High-priority binary patterns (exact matches get bonus weight)
        binary_priority_patterns = [
            "add one", "take one", "include one", "have one", "consume one", "replace one",
            "one daily", "one serving", "single serving", "single daily",
            "as default", "as the default", "eliminate most", "eliminate all",
            "no more than", "eliminate entirely", "eliminate alcohol", "eliminate"
        ]
        
        # Remove "every main meal" from binary patterns - should be proportional
        proportional_priority_patterns = [
            "every main meal", "at every meal", "each meal"
        ]
        
        proportional_keywords = [
            "increase", "decrease", "reduce", "more", "less", "percent", "%", 
            "ratio", "proportion", "target", "goal", "aim for", "strive for",
            "grams", "servings", "minutes", "hours", "times", "days", "at least"
        ]
        
        zone_keywords = [
            "optimal", "range", "between", "zone", "tier", "level", "grade",
            "excellent", "good", "fair", "poor", "low", "medium", "high",
            "category", "classification"
        ]
        
        frequency_keywords = [
            "weekly", "daily", "times per", "days per", "frequency", "often",
            "regularly", "consistently", "habit", "routine", "schedule"
        ]
        
        composite_keywords = [
            "overall", "combined", "multiple", "both", "and", "together",
            "comprehensive", "holistic", "total", "composite", "weighted",
            "plus", "maintain", "consistent", "schedule", "variation", "variance",
            "with at least", "different", "sources", "variety"
        ]
        
        weekly_allowance_keywords = [
            "per week", "weekly", "across", "days", "week across", 
            "drinks per week", "week across 2 days"
        ]
        
        # Count keyword matches with priority weighting
        binary_score = sum(1 for keyword in binary_keywords if keyword in text_lower)
        
        # Check for high-priority binary patterns and add significant weight
        priority_matches = sum(1 for pattern in binary_priority_patterns if pattern in text_lower)
        if priority_matches > 0:
            binary_score += priority_matches * 5  # Give 5x weight to priority patterns
        
        proportional_score = sum(1 for keyword in proportional_keywords if keyword in text_lower)
        
        # Check for proportional priority patterns and add weight
        prop_priority_matches = sum(1 for pattern in proportional_priority_patterns if pattern in text_lower)
        if prop_priority_matches > 0:
            proportional_score += prop_priority_matches * 3  # Give 3x weight to proportional patterns
        
        zone_score = sum(1 for keyword in zone_keywords if keyword in text_lower)
        frequency_score = sum(1 for keyword in frequency_keywords if keyword in text_lower)
        composite_score = sum(1 for keyword in composite_keywords if keyword in text_lower)
        
        # Check for high-priority composite patterns
        if ("every" in text_lower and "different" in text_lower) or ("with at least" in text_lower and "sources" in text_lower):
            composite_score += 5  # Give high priority to multi-component patterns
        
        weekly_allowance_score = sum(1 for keyword in weekly_allowance_keywords if keyword in text_lower)
        
        # Check for range patterns like "7-9 hours", "20-30 minutes" and boost zone score
        import re
        range_pattern = r'\d+[-–]\d+\s*(hours?|minutes?|grams?|mg|servings?)'
        if re.search(range_pattern, text_lower):
            zone_score += 3  # Give zone scoring high priority for range patterns
        
        # Determine evaluation pattern - check for frequency and weekly patterns
        if "per week" in text_lower or "weekly" in text_lower:
            eval_pattern = "weekly"
        elif frequency_score > 1 or "of 7" in text_lower or "nights" in text_lower:
            eval_pattern = "frequency" 
        else:
            eval_pattern = "daily"
        
        # Determine algorithm type
        scores = {
            'binary': binary_score,
            'proportional': proportional_score,
            'zone': zone_score,
            'composite': composite_score,
            'weekly_allowance': weekly_allowance_score
        }
        
        max_score = max(scores.values())
        tier_count = None  # Initialize tier_count
        
        if max_score == 0:
            # Default to proportional for unrecognized patterns
            algorithm_type = AlgorithmType.PROPORTIONAL
            confidence = 0.3
            reasoning = "Default choice - no clear pattern detected"
        
        elif scores['weekly_allowance'] == max_score and weekly_allowance_score >= 3:
            algorithm_type = AlgorithmType.CONSTRAINED_WEEKLY_ALLOWANCE
            confidence = 0.9
            reasoning = f"Weekly allowance pattern detected (weekly allowance score: {weekly_allowance_score})"
        
        elif scores['composite'] == max_score and composite_score >= 2:
            algorithm_type = AlgorithmType.COMPOSITE_WEIGHTED
            confidence = 0.8
            reasoning = f"Multiple elements detected (composite score: {composite_score})"
        
        elif scores['zone'] == max_score and zone_score >= 2:
            # Determine tier count based on text - default to 5-tier for sleep ranges
            if any(tier in text_lower for tier in ['excellent', 'good', 'fair', 'poor', 'critical']) or "hours" in text_lower:
                algorithm_type = AlgorithmType.ZONE_BASED_5TIER
                tier_count = 5
            else:
                algorithm_type = AlgorithmType.ZONE_BASED_3TIER  
                tier_count = 3
            confidence = 0.8
            reasoning = f"Zone/tier language detected (zone score: {zone_score})"
        
        elif scores['binary'] == max_score and binary_score >= 2:
            algorithm_type = AlgorithmType.BINARY_THRESHOLD
            confidence = 0.9
            reasoning = f"Binary/threshold language detected (binary score: {binary_score})"
        
        else:
            algorithm_type = AlgorithmType.PROPORTIONAL
            confidence = 0.7
            reasoning = f"Proportional scoring best fit (proportional score: {proportional_score})"
        
        return RecommendationAnalysis(
            algorithm_type=algorithm_type,
            evaluation_pattern=eval_pattern,
            tier_count=tier_count,
            confidence=confidence,
            reasoning=reasoning
        )
    
    def find_related_metric(self, recommendation_text: str, recommendation_id: str = None) -> Optional[str]:
        """Find the most appropriate metric type for this recommendation."""
        
        # First try to find by recommendation ID
        if recommendation_id:
            for metric_id, metric_data in self.metrics_data.items():
                if recommendation_id in metric_data['recommendations_v2']:
                    return metric_id
        
        # Then try keyword matching
        text_lower = recommendation_text.lower()
        
        best_match = None
        best_score = 0
        
        for metric_id, metric_data in self.metrics_data.items():
            score = 0
            
            # Check name match
            if metric_data['name'].lower() in text_lower:
                score += 10
            
            # Check description matches
            desc_words = metric_data['description_general'].lower().split()
            for word in desc_words:
                if len(word) > 3 and word in text_lower:
                    score += 1
            
            # Check identifier parts
            id_parts = metric_id.replace('_', ' ').split()
            for part in id_parts:
                if len(part) > 3 and part in text_lower:
                    score += 2
            
            if score > best_score:
                best_score = score
                best_match = metric_id
        
        return best_match if best_score > 2 else None
    
    def get_unit_for_metric(self, metric_id: str) -> str:
        """Get the appropriate unit for a metric."""
        if metric_id in self.metrics_data:
            return self.metrics_data[metric_id]['units_v3']
        return 'points'  # Default unit
    
    def generate_config(self, recommendation_text: str, recommendation_id: str = None) -> Dict[str, Any]:
        """Generate a complete algorithm configuration for a recommendation."""
        
        # Analyze the recommendation
        analysis = self.analyze_recommendation(recommendation_text, recommendation_id)
        
        # Find related metric and unit
        metric_id = self.find_related_metric(recommendation_text, recommendation_id)
        unit = self.get_unit_for_metric(metric_id) if metric_id else 'points'
        
        # Get validation schema for target values
        validation = self.metrics_data.get(metric_id, {}).get('validation_schema', {}) if metric_id else {}
        default_target = validation.get('target_daily', 100)
        max_value = validation.get('range', {}).get('max', 200)
        
        # Try to extract specific target from recommendation text
        extracted_target = self._extract_threshold_from_text(recommendation_text)
        target_daily = extracted_target if extracted_target is not None else default_target
        
        # Generate base config ID
        config_id = self._generate_config_id(analysis.algorithm_type, analysis.evaluation_pattern, metric_id)
        
        # Generate configuration based on algorithm type
        if analysis.algorithm_type == AlgorithmType.BINARY_THRESHOLD:
            config = self._generate_binary_config(
                config_id, recommendation_text, analysis, metric_id, unit, target_daily
            )
        
        elif analysis.algorithm_type == AlgorithmType.PROPORTIONAL:
            config = self._generate_proportional_config(
                config_id, recommendation_text, analysis, metric_id, unit, target_daily, max_value
            )
        
        elif analysis.algorithm_type in [AlgorithmType.ZONE_BASED_3TIER, AlgorithmType.ZONE_BASED_5TIER]:
            config = self._generate_zone_config(
                config_id, recommendation_text, analysis, metric_id, unit, target_daily
            )
        
        elif analysis.algorithm_type == AlgorithmType.COMPOSITE_WEIGHTED:
            config = self._generate_composite_config(
                config_id, recommendation_text, analysis, metric_id, unit
            )
        
        elif analysis.algorithm_type == AlgorithmType.CONSTRAINED_WEEKLY_ALLOWANCE:
            config = self._generate_weekly_allowance_config(
                config_id, recommendation_text, analysis, metric_id, unit, target_daily
            )
        
        else:
            # Default to proportional
            config = self._generate_proportional_config(
                config_id, recommendation_text, analysis, metric_id, unit, target_daily, max_value
            )
        
        # Add metadata
        config['metadata'] = {
            'recommendation_text': recommendation_text,
            'recommendation_id': recommendation_id,
            'analysis': {
                'algorithm_type': analysis.algorithm_type.value,
                'confidence': analysis.confidence,
                'reasoning': analysis.reasoning
            },
            'metric_id': metric_id,
            'generated_at': self._get_timestamp()
        }
        
        return config
    
    def _generate_config_id(self, algorithm_type: AlgorithmType, eval_pattern: str, metric_id: str) -> str:
        """Generate a unique configuration ID."""
        algo_prefix = {
            AlgorithmType.BINARY_THRESHOLD: "BIN",
            AlgorithmType.PROPORTIONAL: "PROP", 
            AlgorithmType.ZONE_BASED_3TIER: "Z3T",
            AlgorithmType.ZONE_BASED_5TIER: "Z5T",
            AlgorithmType.COMPOSITE_WEIGHTED: "COMP",
            AlgorithmType.CONSTRAINED_WEEKLY_ALLOWANCE: "ALLOW",
            AlgorithmType.CATEGORICAL_FILTER: "CAT"
        }
        
        pattern_suffix = "FREQ" if eval_pattern == "frequency" else "DAILY"
        metric_suffix = metric_id[:8].upper() if metric_id else "GENERIC"
        
        return f"SC-{algo_prefix[algorithm_type]}-{pattern_suffix}-{metric_suffix}"
    
    def _generate_binary_config(self, config_id: str, rec_text: str, analysis: RecommendationAnalysis, 
                               metric_id: str, unit: str, target: float) -> Dict[str, Any]:
        """Generate binary threshold configuration."""
        
        # Extract threshold from text or use target
        threshold = self._extract_threshold_from_text(rec_text) or target
        
        return {
            "config_id": config_id,
            "config_name": f"Binary Threshold - {metric_id or 'Generic'}",
            "scoring_method": "binary_threshold", 
            "configuration_json": {
                "method": "binary_threshold",
                "formula": "if (actual_value >= threshold) then success_value else failure_value",
                "evaluation_pattern": analysis.evaluation_pattern,
                "schema": {
                    "measurement_type": "binary",
                    "evaluation_period": "weekly" if analysis.evaluation_pattern == "weekly" else ("rolling_7_day" if analysis.evaluation_pattern == "frequency" else "daily"),
                    "success_criteria": "weekly_target" if analysis.evaluation_pattern == "weekly" else ("frequency_target" if analysis.evaluation_pattern == "frequency" else "simple_target"),
                    "calculation_method": "weekly_sum" if analysis.evaluation_pattern == "weekly" else ("exists" if analysis.evaluation_pattern != "frequency" else "exists"),
                    "tracked_metrics": [metric_id] if metric_id else ["generic_metric"],
                    "threshold": threshold,
                    "success_value": 100,
                    "failure_value": 0,
                    "unit": unit,
                    "frequency_requirement": "weekly threshold compliance" if analysis.evaluation_pattern == "weekly" else ("5 successful days out of 7-day window" if analysis.evaluation_pattern == "frequency" else "daily"),
                    "description": f"Binary threshold scoring for: {rec_text[:100]}..."
                }
            }
        }
    
    def _generate_proportional_config(self, config_id: str, rec_text: str, analysis: RecommendationAnalysis,
                                     metric_id: str, unit: str, target: float, max_val: float) -> Dict[str, Any]:
        """Generate proportional configuration."""
        
        return {
            "config_id": config_id,
            "config_name": f"Proportional Achievement - {metric_id or 'Generic'}",
            "scoring_method": "proportional",
            "configuration_json": {
                "method": "proportional", 
                "formula": "(actual_value / target) * 100",
                "evaluation_pattern": analysis.evaluation_pattern,
                "schema": {
                    "measurement_type": "quantity",
                    "evaluation_period": "rolling_7_day" if analysis.evaluation_pattern == "frequency" else "daily",
                    "success_criteria": "frequency_target" if analysis.evaluation_pattern == "frequency" else "simple_target", 
                    "calculation_method": "sum",
                    "tracked_metrics": [metric_id] if metric_id else ["generic_metric"],
                    "target": target,
                    "unit": unit,
                    "minimum_threshold": 0,
                    "maximum_cap": 100,
                    "partial_credit": True,
                    "frequency_requirement": "achieve target 5 of 7 days" if analysis.evaluation_pattern == "frequency" else "daily",
                    "description": f"Proportional scoring for: {rec_text[:100]}..."
                }
            }
        }
    
    def _generate_zone_config(self, config_id: str, rec_text: str, analysis: RecommendationAnalysis,
                             metric_id: str, unit: str, target: float) -> Dict[str, Any]:
        """Generate zone-based configuration."""
        
        # Create zones based on tier count
        if analysis.tier_count == 5:
            zones = self._create_5_tier_zones(target)
        else:
            zones = self._create_3_tier_zones(target)
        
        return {
            "config_id": config_id,
            "config_name": f"{analysis.tier_count}-Tier Zone Scoring - {metric_id or 'Generic'}",
            "scoring_method": "zone_based",
            "configuration_json": {
                "method": "zone_based",
                "formula": "score based on which zone actual_value falls into",
                "evaluation_pattern": analysis.evaluation_pattern,
                "tier_count": analysis.tier_count,
                "schema": {
                    "measurement_type": "quantity",
                    "evaluation_period": "rolling_7_day" if analysis.evaluation_pattern == "frequency" else "daily",
                    "success_criteria": "frequency_target" if analysis.evaluation_pattern == "frequency" else "simple_target",
                    "calculation_method": "average",
                    "tracked_metrics": [metric_id] if metric_id else ["generic_metric"],
                    "zones": zones,
                    "unit": unit,
                    "frequency_requirement": "hit optimal zone 5 of 7 days" if analysis.evaluation_pattern == "frequency" else "daily",
                    "description": f"Zone-based scoring for: {rec_text[:100]}..."
                }
            }
        }
    
    def _generate_composite_config(self, config_id: str, rec_text: str, analysis: RecommendationAnalysis,
                                  metric_id: str, unit: str) -> Dict[str, Any]:
        """Generate composite weighted configuration."""
        
        # Check for different types of composite algorithms
        if "sleep" in rec_text.lower() and ("schedule" in rec_text.lower() or "variation" in rec_text.lower()):
            # Sleep schedule composite (duration + consistency)
            components = [
                {
                    "name": "Sleep Duration Zone",
                    "weight": 0.55,
                    "target_range": [7, 9],
                    "unit": "hour",
                    "scoring_method": "zone_based_5tier",
                    "field_name": "sleep_duration",
                    "zones": [
                        {"range": [0, 5], "score": 20, "label": "Critical"},
                        {"range": [5, 6], "score": 40, "label": "Poor"},
                        {"range": [6, 7], "score": 60, "label": "Fair"},
                        {"range": [7, 9], "score": 100, "label": "Optimal"},
                        {"range": [9, 12], "score": 80, "label": "Excessive"}
                    ]
                },
                {
                    "name": "Sleep Time Consistency", 
                    "weight": 0.225,
                    "tolerance_minutes": 60,
                    "unit": "minute",
                    "scoring_method": "rolling_average_tolerance",
                    "field_name": "sleep_time",
                    "calculation_method": "daily_rolling_avg_check",
                    "algorithm_logic": "For each night: abs(sleep_time - current_rolling_avg) < 60 min",
                    "weekly_scoring": "(compliant_nights / 7) * 100",
                    "examples": {
                        "7_of_7": "100%",
                        "6_of_7": "85.7%", 
                        "5_of_7": "71.4%",
                        "4_of_7": "57.1%"
                    }
                },
                {
                    "name": "Wake Time Consistency",
                    "weight": 0.225, 
                    "tolerance_minutes": 60,
                    "unit": "minute",
                    "scoring_method": "rolling_average_tolerance",
                    "field_name": "wake_time", 
                    "calculation_method": "daily_rolling_avg_check",
                    "algorithm_logic": "For each night: abs(wake_time - current_rolling_avg) < 60 min",
                    "weekly_scoring": "(compliant_nights / 7) * 100",
                    "examples": {
                        "7_of_7": "100%",
                        "6_of_7": "85.7%", 
                        "5_of_7": "71.4%",
                        "4_of_7": "57.1%"
                    }
                }
            ]
        elif ("vegetables" in rec_text.lower() or "fruit" in rec_text.lower() or "grain" in rec_text.lower()) and "different" in rec_text.lower():
            # Parse vegetable/fruit/grain composite patterns
            text_lower = rec_text.lower()
            
            if "every" in text_lower and "main meal" in text_lower:
                # Pattern: 1 serving at every main meal + variety (REC0007.2/REC0008.2/REC0011.2)
                serving_target = 3  # breakfast, lunch, dinner
                variety_target = self._extract_threshold_from_text(rec_text.replace("servings", "").replace("serving", ""))
                if variety_target is None:
                    variety_target = 2  # default
                
                if "vegetables" in text_lower:
                    food_type = "vegetables"
                elif "fruit" in text_lower:
                    food_type = "fruit"
                else:
                    food_type = "whole_grain"
                components = [
                    {
                        "name": f"{food_type.title()} Servings at Meals",
                        "weight": 0.7,
                        "target": serving_target,
                        "unit": "serving",
                        "scoring_method": "proportional",
                        "field_name": f"dietary_{food_type}_meals",
                        "description": f"1 serving at each main meal (breakfast, lunch, dinner)"
                    },
                    {
                        "name": f"{food_type.title()} Variety",
                        "weight": 0.3,
                        "target": variety_target,
                        "unit": "sources",
                        "scoring_method": "proportional", 
                        "field_name": f"dietary_{food_type}_variety",
                        "description": f"At least {variety_target} different {food_type} types per day"
                    }
                ]
            else:
                # Pattern: X+ servings + Y+ variety (REC0007.3/REC0008.3/REC0011.3)
                serving_target = self._extract_threshold_from_text(rec_text)
                if serving_target is None:
                    serving_target = 5  # default
                
                # Extract variety target from "at least X different" pattern
                variety_match = re.search(r'at least (\d+) different', text_lower)
                variety_target = int(variety_match.group(1)) if variety_match else 3
                
                if "vegetables" in text_lower:
                    food_type = "vegetables"
                elif "fruit" in text_lower:
                    food_type = "fruit"
                else:
                    food_type = "whole_grain"
                
                # Check if variety is across the week or daily
                variety_period = "weekly" if "across the week" in text_lower else "daily"
                components = [
                    {
                        "name": f"Daily {food_type.title()} Servings",
                        "weight": 0.7,
                        "target": serving_target,
                        "unit": "serving",
                        "scoring_method": "proportional",
                        "field_name": f"dietary_{food_type}_daily",
                        "description": f"Reach {serving_target} or more servings of {food_type} daily"
                    },
                    {
                        "name": f"{food_type.title()} Variety",
                        "weight": 0.3,
                        "target": variety_target,
                        "unit": "sources",
                        "scoring_method": "proportional", 
                        "field_name": f"dietary_{food_type}_variety_{variety_period}",
                        "description": f"At least {variety_target} different {food_type} types {variety_period}"
                    }
                ]
        else:
            # Default composite components
            components = [
                {
                    "name": "Primary Component",
                    "weight": 0.7,
                    "target": 100,
                    "unit": unit,
                    "scoring_method": "proportional",
                    "field_name": metric_id or "primary_metric"
                },
                {
                    "name": "Secondary Component", 
                    "weight": 0.3,
                    "target": 80,
                    "unit": "points",
                    "scoring_method": "proportional",
                    "field_name": "secondary_metric"
                }
            ]
        
        return {
            "config_id": config_id,
            "config_name": f"Composite Weighted - {metric_id or 'Generic'}",
            "scoring_method": "composite_weighted",
            "configuration_json": {
                "method": "composite_weighted",
                "formula": "weighted average of multiple components",
                "evaluation_pattern": analysis.evaluation_pattern,
                "schema": {
                    "measurement_type": "composite",
                    "evaluation_period": "rolling_7_day" if analysis.evaluation_pattern == "frequency" else "daily",
                    "success_criteria": "frequency_target" if analysis.evaluation_pattern == "frequency" else "simple_target",
                    "calculation_method": "weighted_average",
                    "tracked_metrics": [metric_id] if metric_id else ["generic_metric"],
                    "components": components,
                    "minimum_threshold": 0,
                    "maximum_cap": 100,
                    "frequency_requirement": "meet composite target weekly" if analysis.evaluation_pattern == "frequency" else "daily",
                    "description": f"Composite scoring for: {rec_text[:100]}..."
                }
            }
        }
    
    def _generate_weekly_allowance_config(self, config_id: str, rec_text: str, analysis: RecommendationAnalysis,
                                        metric_id: str, unit: str, weekly_allowance: float) -> Dict[str, Any]:
        """Generate constrained weekly allowance configuration."""
        
        # Extract day constraint from text (default to 2 for "across 2 days")
        import re
        day_pattern = r'across (\d+) days?'
        day_match = re.search(day_pattern, rec_text.lower())
        max_days = int(day_match.group(1)) if day_match else 2
        
        return {
            "config_id": config_id,
            "config_name": f"Constrained Weekly Allowance - {metric_id or 'Generic'}",
            "scoring_method": "constrained_weekly_allowance",
            "configuration_json": {
                "method": "constrained_weekly_allowance",
                "formula": "if (weekly_total <= allowance AND days_used <= max_days) then 100 else 0",
                "evaluation_pattern": "weekly",
                "schema": {
                    "measurement_type": "constrained",
                    "evaluation_period": "rolling_7_day",
                    "success_criteria": "dual_constraint",
                    "calculation_method": "weekly_constraint_check",
                    "tracked_metrics": [metric_id] if metric_id else ["generic_metric"],
                    "weekly_allowance": weekly_allowance,
                    "max_days_per_week": max_days,
                    "unit": unit,
                    "constraints": {
                        "total_weekly_limit": weekly_allowance,
                        "max_consumption_days": max_days,
                        "min_consumption_days": 0
                    },
                    "scoring_logic": {
                        "success_conditions": [
                            f"weekly_total <= {weekly_allowance}",
                            f"consumption_days <= {max_days}"
                        ],
                        "success_value": 100,
                        "failure_value": 0,
                        "examples": {
                            "pass_scenarios": [
                                f"2+1 {unit}s on 2 days = PASS",
                                f"1+2 {unit}s on 2 days = PASS",
                                f"3+0 {unit}s on 1 day = FAIL (exceeds day limit)",
                                f"1+1+1 {unit}s on 3 days = FAIL (exceeds day limit)"
                            ]
                        }
                    },
                    "description": f"Weekly allowance with day constraints for: {rec_text[:100]}..."
                }
            }
        }
    
    def _create_5_tier_zones(self, target: float) -> List[Dict[str, Any]]:
        """Create 5-tier zones around a target value."""
        return [
            {"range": [0, target * 0.3], "score": 20, "label": "Critical"},
            {"range": [target * 0.3, target * 0.6], "score": 40, "label": "Poor"},
            {"range": [target * 0.6, target * 0.8], "score": 60, "label": "Fair"},
            {"range": [target * 0.8, target * 1.2], "score": 100, "label": "Good"},
            {"range": [target * 1.2, target * 2.0], "score": 80, "label": "Excessive"}
        ]
    
    def _create_3_tier_zones(self, target: float) -> List[Dict[str, Any]]:
        """Create 3-tier zones around a target value."""
        return [
            {"range": [0, target * 0.7], "score": 33, "label": "Below Target"},
            {"range": [target * 0.7, target * 1.3], "score": 100, "label": "On Target"},
            {"range": [target * 1.3, target * 2.0], "score": 66, "label": "Above Target"}
        ]
    
    def _extract_threshold_from_text(self, text: str) -> Optional[float]:
        """Extract numeric threshold from recommendation text."""
        
        # Special handling for "one" patterns - these should always be 1
        text_lower = text.lower()
        one_patterns = [
            "add one", "take one", "include one", "have one", "consume one",
            "one daily", "one serving", "single serving", "single daily"
        ]
        
        if any(pattern in text_lower for pattern in one_patterns):
            return 1.0
        
        # Handle word numbers first
        word_numbers = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
        }
        
        # Check for "no more than [word]" patterns first
        for word, num in word_numbers.items():
            if f'no more than {word}' in text_lower:
                return float(num)
        
        # Look for patterns like "at least 8", "minimum 5", "goal of 30", "reach 38g", "no more than 2"
        patterns = [
            r'no more than (\d+(?:\.\d+)?)',  # "no more than 2 drinks"
            r'(\d+(?:\.\d+)?) or more',  # "5 or more servings" - prioritize this pattern
            r'reach (\d+(?:\.\d+)?)',
            r'at least (\d+(?:\.\d+)?)',
            r'minimum (\d+(?:\.\d+)?)',
            r'goal of (\d+(?:\.\d+)?)',
            r'target (\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?) of \d+',  # Captures "3 of 7", "5 of 7", etc.
            r'add (\d+(?:\.\d+)?)',
            r'take (\d+(?:\.\d+)?)',
            r'have (\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)g\b',  # Captures "38g", "21g", etc. - moved lower priority
            r'(\d+(?:\.\d+)?) grams?',  # Captures "38 grams", "21 gram"
            r'one daily' # Special case for "one daily serving"
        ]
        
        # Special handling for "every main meal" = 3 meals
        if 'every main meal' in text_lower:
            return 3.0
        
        # Special handling for "one daily serving" type patterns
        if 'one daily' in text.lower() or 'add one' in text.lower():
            return 1.0
        
        for pattern in patterns:
            if pattern == r'one daily':
                if re.search(pattern, text.lower()):
                    return 1.0
            else:
                match = re.search(pattern, text.lower())
                if match:
                    return float(match.group(1))
        
        return None
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def save_config(self, config: Dict[str, Any], output_dir: str = None) -> str:
        """Save configuration to file."""
        if output_dir is None:
            output_dir = Path(__file__).parent / "generated_configs"
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Generate filename using recommendation ID + algorithm type
        rec_id = config['metadata'].get('recommendation_id', 'UNKNOWN')
        algorithm_type = config['metadata']['analysis']['algorithm_type'].upper().replace('_', '-')
        config_id = config['config_id']  # Always get config_id for master list
        
        if rec_id and rec_id != 'UNKNOWN':
            filename = f"{rec_id}-{algorithm_type}.json"
        else:
            # Fallback to original config_id if no rec_id
            filename = f"{config_id}.json"
            
        filepath = output_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Also add to master list
        master_file = output_path / "all_generated_configs.json"
        if master_file.exists():
            with open(master_file, 'r') as f:
                master_data = json.load(f)
                all_configs = master_data.get('configurations', [])
        else:
            all_configs = []
            master_data = {
                "project_name": "WellPath Recommendation Algorithm Configurations",
                "description": "Generated algorithm configurations for health recommendations",
                "configurations": []
            }
        
        # Update or append based on recommendation_id (not config_id)
        rec_id = config['metadata'].get('recommendation_id')
        updated = False
        
        if rec_id:
            for i, existing in enumerate(all_configs):
                if existing.get('metadata', {}).get('recommendation_id') == rec_id:
                    all_configs[i] = config
                    updated = True
                    break
        
        if not updated:
            all_configs.append(config)
        
        # Update master data
        master_data['configurations'] = all_configs
        master_data['total_configs'] = len(all_configs)
        
        # Sort by recommendation_id for consistent ordering
        all_configs.sort(key=lambda x: x.get('metadata', {}).get('recommendation_id', 'ZZZ'))
        
        with open(master_file, 'w') as f:
            json.dump(master_data, f, indent=2)
        
        self.generated_configs.append(config)
        return str(filepath)


def process_recommendation(recommendation_text: str, recommendation_id: str = None) -> Tuple[Dict[str, Any], str]:
    """Process a single recommendation and return config + file path."""
    generator = RecommendationConfigGenerator()
    config = generator.generate_config(recommendation_text, recommendation_id)
    filepath = generator.save_config(config)
    
    return config, filepath