"""
API Endpoints for Unit Conversion Integration
============================================

Flask/FastAPI endpoints that integrate unit conversion into the WellPath API.
Handles user input, conversion, scoring, and display formatting.
"""

from flask import Flask, request, jsonify
from typing import Dict, Any, Optional
import json
from datetime import datetime
import uuid

from ..core_systems.unit_conversion_service import UnitConversionService
from ..core_systems.recommendation_engine_with_units import RecommendationEngineWithUnits


app = Flask(__name__)
converter = UnitConversionService()
engine = RecommendationEngineWithUnits()


@app.route('/api/metrics/entry', methods=['POST'])
def create_metric_entry_with_conversion():
    """
    Create a metric entry with automatic unit conversion
    
    Request Body:
    {
        "user_id": "user123",
        "metric_id": "dietary_water", 
        "value": 8,
        "unit": "cup",
        "timestamp": "2024-01-15T10:30:00Z" (optional)
    }
    
    Response:
    {
        "success": true,
        "entry_id": "entry_456",
        "conversion": {
            "original_value": 8,
            "original_unit": "cup",
            "converted_value": 1893.0,
            "base_unit": "milliliter"
        },
        "scores": {
            "REC0020.2": {"score": 85.1, "method": "proportional"}
        },
        "display": {
            "formatted_display": "8.0 cups",
            "achievement_message": "Great job! You're 85% of the way to your goal."
        }
    }
    """
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['user_id', 'metric_id', 'value', 'unit']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False, 
                    'error': f'Missing required field: {field}'
                }), 400
                
        # Validate input
        validation = engine.validate_user_input(
            data['value'], 
            data['unit'], 
            data['metric_id']
        )
        
        if not validation['is_valid']:
            return jsonify({
                'success': False,
                'error': 'Invalid input',
                'validation_errors': validation['messages']
            }), 400
            
        # Generate session ID for audit trail
        session_id = str(uuid.uuid4())
        
        # Process the input with conversion and scoring
        result = engine.process_user_input(
            user_id=data['user_id'],
            metric_id=data['metric_id'],
            value=data['value'],
            input_unit=data['unit'],
            session_id=session_id
        )
        
        # Store in database (implementation would go here)
        entry_id = store_metric_entry(result, data.get('timestamp'))
        
        # Get display formatting
        display_format = engine.get_user_display_format(
            user_id=data['user_id'],
            base_value=result['conversion']['converted_value'],
            base_unit=result['conversion']['base_unit'],
            metric_id=data['metric_id']
        )
        
        # Generate achievement message
        achievement_msg = generate_achievement_message(result['scores'])
        
        return jsonify({
            'success': True,
            'entry_id': entry_id,
            'conversion': result['conversion'],
            'scores': {k: {'score': v['score'], 'method': v['method']} 
                      for k, v in result['scores'].items()},
            'display': {
                'formatted_display': display_format['formatted_display'],
                'achievement_message': achievement_msg
            },
            'validation_warnings': validation.get('warnings', [])
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/units/supported/<metric_id>', methods=['GET'])
def get_supported_units(metric_id: str):
    """
    Get supported units for a metric
    
    Response:
    {
        "metric_id": "dietary_water",
        "unit_type": "volume", 
        "supported_units": {
            "cup": {"display_name": "Cup", "symbol": "cup", "is_base": false},
            "milliliter": {"display_name": "Milliliter", "symbol": "mL", "is_base": true}
        }
    }
    """
    try:
        supported = engine.get_supported_units_for_metric(metric_id)
        return jsonify(supported)
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/units/convert', methods=['POST'])
def convert_units():
    """
    Convert between units (utility endpoint)
    
    Request Body:
    {
        "value": 8,
        "from_unit": "cup", 
        "to_unit": "milliliter"
    }
    
    Response:
    {
        "success": true,
        "original_value": 8,
        "original_unit": "cup",
        "converted_value": 1893.0,
        "converted_unit": "milliliter"
    }
    """
    try:
        data = request.json
        
        # Convert to base unit first
        base_conversion = converter.convert_to_base(data['value'], data['from_unit'])
        
        # Then convert to target unit
        if data['to_unit'] == base_conversion['base_unit']:
            # Target is already base unit
            final_value = base_conversion['converted_value']
        else:
            # Convert from base to target
            display_conversion = converter.convert_from_base(
                base_conversion['converted_value'],
                base_conversion['base_unit'],
                data['to_unit']
            )
            final_value = display_conversion['value']
            
        return jsonify({
            'success': True,
            'original_value': data['value'],
            'original_unit': data['from_unit'],
            'converted_value': final_value,
            'converted_unit': data['to_unit']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/users/<user_id>/preferences/units', methods=['GET', 'POST'])
def manage_unit_preferences(user_id: str):
    """
    Get or set user's unit preferences
    
    GET Response:
    {
        "user_id": "user123",
        "preferences": {
            "volume": "cup",
            "mass": "pound", 
            "length": "feet_inches",
            "temperature": "fahrenheit"
        }
    }
    
    POST Request Body:
    {
        "preferences": {
            "volume": "liter",
            "mass": "kilogram"
        }
    }
    """
    if request.method == 'GET':
        # Get current preferences
        preferences = get_user_unit_preferences(user_id)
        return jsonify({
            'user_id': user_id,
            'preferences': preferences
        })
        
    elif request.method == 'POST':
        # Update preferences
        data = request.json
        new_preferences = data.get('preferences', {})
        
        # Validate unit types and units
        for unit_type, unit in new_preferences.items():
            supported_units = converter.get_supported_units_for_type(unit_type)
            if unit not in supported_units:
                return jsonify({
                    'success': False,
                    'error': f'Unsupported unit "{unit}" for type "{unit_type}"'
                }), 400
                
        # Save preferences
        updated_preferences = save_user_unit_preferences(user_id, new_preferences)
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'preferences': updated_preferences
        })


@app.route('/api/metrics/history/<user_id>/<metric_id>', methods=['GET'])
def get_metric_history_with_units(user_id: str, metric_id: str):
    """
    Get metric history with unit conversion for display
    
    Query Parameters:
    - display_unit: Preferred unit for display (optional)
    - limit: Number of entries to return (default: 100)
    
    Response:
    {
        "user_id": "user123",
        "metric_id": "dietary_water",
        "display_unit": "cup",
        "entries": [
            {
                "entry_id": "entry_456",
                "timestamp": "2024-01-15T10:30:00Z",
                "original_value": 8,
                "original_unit": "cup", 
                "base_value": 1893.0,
                "base_unit": "milliliter",
                "display_value": 8.0,
                "display_unit": "cup",
                "display_formatted": "8.0 cups",
                "scores": {
                    "REC0020.2": 85.1
                }
            }
        ]
    }
    """
    try:
        display_unit = request.args.get('display_unit')
        limit = int(request.args.get('limit', 100))
        
        # Get raw entries from database
        raw_entries = get_metric_entries_from_db(user_id, metric_id, limit)
        
        # If no display unit specified, use user's preference
        if not display_unit:
            unit_type = engine._get_unit_type_for_metric(metric_id)
            display_unit = engine._get_user_preferred_unit(user_id, unit_type)
        
        # Process entries for display
        processed_entries = []
        for entry in raw_entries:
            # Convert to display unit if different from stored original unit
            if display_unit != entry['original_unit']:
                display_conversion = converter.convert_from_base(
                    entry['base_value'],
                    entry['base_unit'],
                    display_unit
                )
                display_value = display_conversion['value']
                display_formatted = display_conversion['formatted_display']
            else:
                display_value = entry['original_value']
                display_formatted = f"{entry['original_value']} {entry['original_unit']}"
                
            processed_entries.append({
                'entry_id': entry['entry_id'],
                'timestamp': entry['timestamp'].isoformat(),
                'original_value': entry['original_value'],
                'original_unit': entry['original_unit'],
                'base_value': entry['base_value'],
                'base_unit': entry['base_unit'],
                'display_value': display_value,
                'display_unit': display_unit,
                'display_formatted': display_formatted,
                'scores': entry.get('scores', {})
            })
            
        return jsonify({
            'user_id': user_id,
            'metric_id': metric_id,
            'display_unit': display_unit,
            'entries': processed_entries
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/conversion/validate', methods=['POST'])
def validate_conversion_input():
    """
    Validate user input before conversion
    
    Request Body:
    {
        "value": "5'10\"",
        "unit": "feet_inches",
        "metric_id": "height"
    }
    
    Response:
    {
        "is_valid": true,
        "messages": [],
        "warnings": ["Height seems unusually tall"],
        "preview_conversion": {
            "converted_value": 177.8,
            "base_unit": "centimeter"
        }
    }
    """
    try:
        data = request.json
        
        validation = engine.validate_user_input(
            data['value'],
            data['unit'], 
            data['metric_id']
        )
        
        # If valid, include preview conversion
        if validation['is_valid']:
            try:
                preview = converter.convert_to_base(data['value'], data['unit'])
                validation['preview_conversion'] = {
                    'converted_value': preview['converted_value'],
                    'base_unit': preview['base_unit']
                }
            except:
                pass  # Preview conversion failed, but validation passed
                
        return jsonify(validation)
        
    except Exception as e:
        return jsonify({
            'is_valid': False,
            'messages': [str(e)],
            'warnings': []
        }), 500


# Helper functions (these would be implemented based on your database setup)

def store_metric_entry(conversion_result: Dict, timestamp: Optional[str] = None) -> str:
    """Store metric entry in database and return entry ID"""
    # Implementation would insert into metric_entries table
    # with both original and converted values
    entry_id = str(uuid.uuid4())
    # ... database insertion logic ...
    return entry_id


def generate_achievement_message(scores: Dict[str, Any]) -> str:
    """Generate encouraging achievement message based on scores"""
    if not scores:
        return "Entry recorded successfully!"
        
    max_score = max(score_info['score'] for score_info in scores.values())
    
    if max_score >= 90:
        return "Excellent work! You're crushing your health goals! 🎉"
    elif max_score >= 75:
        return "Great job! You're making solid progress toward your goals. 👏"
    elif max_score >= 50:
        return "Good effort! Keep building on this momentum. 💪"
    else:
        return "Every step counts! You're building healthy habits. 🌱"


def get_user_unit_preferences(user_id: str) -> Dict[str, str]:
    """Get user's unit preferences from database"""
    # Implementation would query user_unit_preferences table
    # For now, return defaults
    return {
        'volume': 'cup',
        'mass': 'pound',
        'length': 'feet_inches',
        'temperature': 'fahrenheit'
    }


def save_user_unit_preferences(user_id: str, new_preferences: Dict[str, str]) -> Dict[str, str]:
    """Save user's unit preferences to database"""
    # Implementation would insert/update user_unit_preferences table
    current_prefs = get_user_unit_preferences(user_id)
    current_prefs.update(new_preferences)
    # ... database update logic ...
    return current_prefs


def get_metric_entries_from_db(user_id: str, metric_id: str, limit: int) -> list:
    """Get metric entries from database"""
    # Implementation would query metric_entries table
    # Return list of entries with conversion information
    return []


if __name__ == '__main__':
    app.run(debug=True)