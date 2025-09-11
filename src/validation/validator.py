"""
Algorithm Configuration Validator

Validates algorithm configurations against JSON schemas and business rules.
"""

import json
import jsonschema
from typing import Dict, Any, List, Union
from pathlib import Path


class AlgorithmValidator:
    """Validates algorithm configurations."""
    
    def __init__(self, schema_file: str = None):
        """
        Initialize validator with schema file.
        
        Args:
            schema_file: Path to JSON schema file. If None, uses default schemas.
        """
        if schema_file is None:
            schema_file = Path(__file__).parent.parent / "schemas" / "algorithm_schemas.json"
        
        with open(schema_file, 'r') as f:
            self.schemas = json.load(f)
    
    def validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a single algorithm configuration.
        
        Args:
            config: Algorithm configuration dictionary
            
        Returns:
            Validation result with errors and warnings
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "method": config.get("method", "unknown")
        }
        
        method = config.get("method")
        if not method:
            result["valid"] = False
            result["errors"].append("Missing 'method' field")
            return result
        
        # Get appropriate schema
        schema_key = f"{method}_schema"
        if schema_key not in self.schemas:
            result["valid"] = False
            result["errors"].append(f"Unknown method: {method}")
            return result
        
        schema = self.schemas[schema_key]
        
        # Validate against JSON schema
        try:
            jsonschema.validate(config, schema)
        except jsonschema.ValidationError as e:
            result["valid"] = False
            result["errors"].append(f"Schema validation error: {e.message}")
            return result
        except jsonschema.SchemaError as e:
            result["valid"] = False
            result["errors"].append(f"Schema error: {e.message}")
            return result
        
        # Perform method-specific validation
        method_validator = getattr(self, f"_validate_{method}", None)
        if method_validator:
            method_result = method_validator(config)
            result["errors"].extend(method_result.get("errors", []))
            result["warnings"].extend(method_result.get("warnings", []))
            if method_result.get("errors"):
                result["valid"] = False
        
        return result
    
    def validate_multiple_configs(self, configs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate multiple algorithm configurations.
        
        Args:
            configs: List of algorithm configuration dictionaries
            
        Returns:
            Overall validation result
        """
        results = []
        overall_valid = True
        
        for i, config in enumerate(configs):
            result = self.validate_config(config)
            result["config_index"] = i
            results.append(result)
            
            if not result["valid"]:
                overall_valid = False
        
        return {
            "valid": overall_valid,
            "results": results,
            "summary": self._generate_summary(results)
        }
    
    def _validate_binary_threshold(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate binary threshold specific rules."""
        errors = []
        warnings = []
        
        schema_config = config.get("schema", {})
        
        # Check threshold value type consistency
        threshold = schema_config.get("threshold")
        measurement_type = schema_config.get("measurement_type")
        
        if measurement_type == "binary" and not isinstance(threshold, bool):
            warnings.append("Binary measurement type should use boolean threshold")
        
        if measurement_type in ["duration", "count"] and not isinstance(threshold, (int, float)):
            errors.append(f"Measurement type '{measurement_type}' requires numeric threshold")
        
        # Check success/failure values
        success_value = schema_config.get("success_value", 100)
        failure_value = schema_config.get("failure_value", 0)
        
        if success_value <= failure_value:
            warnings.append("Success value should be greater than failure value")
        
        return {"errors": errors, "warnings": warnings}
    
    def _validate_proportional(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate proportional specific rules."""
        errors = []
        warnings = []
        
        schema_config = config.get("schema", {})
        
        # Check target value
        target = schema_config.get("target", 0)
        if target <= 0:
            errors.append("Target must be greater than 0")
        
        # Check threshold and cap consistency
        min_threshold = schema_config.get("minimum_threshold", 0)
        max_cap = schema_config.get("maximum_cap", 100)
        
        if min_threshold < 0:
            errors.append("Minimum threshold cannot be negative")
        
        if max_cap < min_threshold:
            errors.append("Maximum cap cannot be less than minimum threshold")
        
        if max_cap < 100:
            warnings.append("Maximum cap below 100% may limit scoring potential")
        
        return {"errors": errors, "warnings": warnings}
    
    def _validate_zone_based(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate zone-based specific rules."""
        errors = []
        warnings = []
        
        schema_config = config.get("schema", {})
        zones = schema_config.get("zones", [])
        
        if len(zones) != 5:
            errors.append("Zone-based algorithm requires exactly 5 zones")
            return {"errors": errors, "warnings": warnings}
        
        # Validate zone ranges
        sorted_zones = sorted(zones, key=lambda z: z["range"][0])
        
        for i, zone in enumerate(sorted_zones):
            range_values = zone["range"]
            if len(range_values) != 2:
                errors.append(f"Zone {i} must have exactly 2 range values")
                continue
            
            min_val, max_val = range_values
            if min_val >= max_val:
                errors.append(f"Zone {i} min value must be less than max value")
            
            # Check for gaps or overlaps with next zone
            if i < len(sorted_zones) - 1:
                next_zone = sorted_zones[i + 1]
                next_min = next_zone["range"][0]
                
                if max_val < next_min:
                    warnings.append(f"Gap between zone {i} and zone {i+1}")
                elif max_val > next_min:
                    errors.append(f"Overlap between zone {i} and zone {i+1}")
        
        return {"errors": errors, "warnings": warnings}
    
    def _validate_composite_weighted(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate composite weighted specific rules."""
        errors = []
        warnings = []
        
        schema_config = config.get("schema", {})
        components = schema_config.get("components", [])
        
        if not components:
            errors.append("At least one component must be defined")
            return {"errors": errors, "warnings": warnings}
        
        # Validate component weights
        total_weight = sum(comp.get("weight", 0) for comp in components)
        
        if total_weight <= 0:
            errors.append("Total component weights must be greater than 0")
        
        # Check for duplicate field names
        field_names = [comp.get("field_name") for comp in components]
        if len(field_names) != len(set(field_names)):
            errors.append("Component field names must be unique")
        
        # Validate individual components
        for i, component in enumerate(components):
            weight = component.get("weight", 0)
            target = component.get("target", 0)
            
            if weight < 0:
                errors.append(f"Component {i} weight cannot be negative")
            
            if weight == 0:
                warnings.append(f"Component {i} has zero weight")
            
            if target <= 0:
                warnings.append(f"Component {i} target should be positive")
        
        return {"errors": errors, "warnings": warnings}
    
    def _generate_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of validation results."""
        total_configs = len(results)
        valid_configs = sum(1 for r in results if r["valid"])
        
        error_count = sum(len(r["errors"]) for r in results)
        warning_count = sum(len(r["warnings"]) for r in results)
        
        method_counts = {}
        for result in results:
            method = result["method"]
            method_counts[method] = method_counts.get(method, 0) + 1
        
        return {
            "total_configs": total_configs,
            "valid_configs": valid_configs,
            "invalid_configs": total_configs - valid_configs,
            "total_errors": error_count,
            "total_warnings": warning_count,
            "methods": method_counts
        }


def validate_original_config_file(file_path: str) -> Dict[str, Any]:
    """
    Validate the original rec_config.json file.
    
    Args:
        file_path: Path to the rec_config.json file
        
    Returns:
        Validation results
    """
    validator = AlgorithmValidator()
    
    # Parse the malformed JSON file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix quotes and parse objects
    content = content.replace('""', '"')
    objects = []
    current_obj = ''
    brace_count = 0
    
    for char in content:
        if char == '{':
            if brace_count == 0:
                current_obj = '{'
            else:
                current_obj += char
            brace_count += 1
        elif char == '}':
            current_obj += char
            brace_count -= 1
            if brace_count == 0:
                try:
                    parsed = json.loads(current_obj)
                    objects.append(parsed)
                except json.JSONDecodeError:
                    pass  # Skip invalid objects
                current_obj = ''
        elif brace_count > 0:
            current_obj += char
    
    return validator.validate_multiple_configs(objects)