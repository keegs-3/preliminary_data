#!/usr/bin/env python3
"""
Python JSON Creator Script - Build JSON from Excel
Creates a new recommendations_list.json from Excel data using the original JSON structure
Now replaces the existing file and creates backup in Recommendations_List_Old folder
"""

import json
import sys
import os
import shutil
from datetime import datetime

def create_backup_folder_and_move_original():
    """Create backup folder and move original file there"""
    backup_folder = "Recommendations_List_Old"
    original_file = "recommendations_list.json"
    
    # Create backup folder if it doesn't exist
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
        print(f"Created backup folder: {backup_folder}")
    
    # If original file exists, move it to backup folder with timestamp
    if os.path.exists(original_file):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"recommendations_list_backup_{timestamp}.json"
        backup_path = os.path.join(backup_folder, backup_filename)
        
        try:
            shutil.move(original_file, backup_path)
            print(f"Moved original file to: {backup_path}")
            return True
        except Exception as e:
            print(f"Warning: Could not move original file to backup: {e}")
            return False
    else:
        print("No existing recommendations_list.json found to backup")
        return True

def load_excel_data(filename):
    """Load Excel data from file"""
    try:
        import pandas as pd
        
        print(f"Loading Excel file: {filename}")
        df = pd.read_excel(filename)
        
        print(f"Successfully loaded Excel file with {len(df)} rows")
        print(f"Excel columns found: {list(df.columns)}")
        
        # Convert to list of dictionaries
        data = df.to_dict('records')
        
        # Show first few rows
        print(f"First few rows:")
        for i, row in enumerate(data[:3]):
            print(f"  Row {i+1}: ID={row.get('ID', 'N/A')}, Title={str(row.get('Title', 'N/A'))[:50]}...")
        
        return data
        
    except ImportError:
        print("Error: pandas library not found. Install with: pip install pandas openpyxl")
        return None
    except Exception as e:
        print(f"Error reading Excel file '{filename}': {e}")
        return None

def get_csv_to_json_mapping():
    """Returns the complete mapping from CSV column names to JSON marker names"""
    return {
        'Total Cholesterol': 'total_cholesterol',
        'LDL': 'ldl',
        'HDL': 'hdl',
        'Lp(a)': 'lp_a',
        'Triglycerides': 'triglycerides',
        'ApoB': 'apob',
        'Omega-3 Index': 'omega_3_index',
        'RDW': 'rdw',
        'Magnesium (RBC)': 'magnesium_rbc',
        'Vitamin D': 'vitamin_d',
        'Serum Ferritin': 'serum_ferritin',
        'Total Iron Binding Capacity (TIBC)': 'tibc',
        'Transferrin Saturation': 'transferrin_saturation',
        'hsCRP': 'hscrp',
        'White Blood Cell Count': 'white_blood_cell_count',
        'Neutrophils': 'neutrophils',
        'Lymphocytes': 'lymphocytes',
        'Neutrocyte/Lymphocyte Ratio': 'neutrocyte_lymphocyte_ratio',
        'Eosinophils': 'eosinophils',
        'Red Blood Cell Count': 'red_blood_cell_count',
        'Platelet Count': 'platelet_count',
        'HbA1c': 'hba1c',
        'Fasting Glucose': 'fasting_glucose',
        'Fasting Insulin': 'fasting_insulin',
        'HOMA-IR': 'homa_ir',
        'ALT': 'alt',
        'GGT': 'ggt',
        'AST': 'ast',
        'ALP': 'alp',
        'Albumin': 'albumin',
        'Testosterone': 'testosterone',
        'Free Testosterone': 'free_testosterone',
        'Cortisol': 'cortisol',
        'Estradiol': 'estradiol',
        'Progesterone': 'progesterone',
        'TSH': 'tsh',
        'DHEA-S': 'dhea_s',
        'SHBG': 'shbg',
        'Uric Acid': 'uric_acid',
        'Hemoglobin': 'hemoglobin',
        'Hematocrit': 'hematocrit',
        'Vitamin B12': 'vitamin_b12',
        'Folate Serum': 'folate_serum',
        'Folate (RBC)': 'folate_rbc',
        'Homocysteine': 'homocysteine',
        'Creatine Kinase': 'creatine_kinase',
        'Sodium': 'sodium',
        'Potassium': 'potassium',
        'Ferritin': 'ferritin',
        'Mean Corpuscular Hemoglobin (MCH)': 'mch',
        'Mean Corpuscular Hemoglobin Concentration (MCHC)': 'mchc',
        'eGFR': 'egfr',
        'Cystatin C': 'cystatin_c',
        'BUN': 'bun',
        'Creatinine': 'creatinine',
        'Calcium (Serum)': 'calcium_serum',
        'Calcium (Ionized)': 'calcium_ionized',
        'VO2 Max': 'vo2_max',
        '% Bodyfat': 'bodyfat',
        'Skeletal Muscle Mass to Fat-Free Mass': 'skeletal_muscle_mass_to_fat_free_mass',
        'Hip-to-Waist Ratio': 'hip_to_waist_ratio',
        'BMI': 'bmi',
        'Resting Heart Rate': 'resting_heart_rate',
        'Blood Pressure - Systolic': 'blood_pressure_systolic',
        'Blood Pressure - Diastolic': 'blood_pressure_diastolic',
        'Visceral Fat': 'visceral_fat',
        'Grip Strength': 'grip_strength',
        'HRV': 'hrv',
        'REM Sleep': 'rem_sleep',
        'Deep Sleep': 'deep_sleep',
        'Total Sleep': 'total_sleep',
        'Steps/Day': 'steps_day',
        'Weight': 'weight',
        'Height': 'height'
    }

def parse_and_convert_markers(marker_string, mapping):
    """Parse marker string and convert to JSON format"""
    if not marker_string or str(marker_string).strip() == '' or str(marker_string).lower() == 'nan':
        return []
    
    # Split by comma and clean up whitespace
    csv_markers = [marker.strip() for marker in str(marker_string).split(',') if marker.strip()]
    
    # Convert CSV names to JSON format
    json_markers = []
    for csv_marker in csv_markers:
        if csv_marker in mapping:
            json_markers.append(mapping[csv_marker])
        else:
            print(f"Warning: No mapping found for marker: '{csv_marker}'")
            # Fallback: convert to snake_case
            fallback = csv_marker.lower().replace(' ', '_').replace('-', '_')
            fallback = ''.join(c for c in fallback if c.isalnum() or c == '_')
            fallback = '_'.join(part for part in fallback.split('_') if part)
            json_markers.append(fallback)
    
    return json_markers

def clean_value(value):
    """Clean values from pandas (handles NaN, None, etc.)"""
    if value is None:
        return ''
    if str(value).lower() == 'nan':
        return ''
    return str(value)

def create_recommendations_json(excel_data):
    """Create new JSON structure from Excel data"""
    
    mapping = get_csv_to_json_mapping()
    recommendations = []
    
    print(f"\nCreating JSON structure from {len(excel_data)} Excel rows...")
    
    for i, row in enumerate(excel_data):
        if not row.get('ID'):
            continue
            
        # Show progress for first few and every 50th row
        if i < 5 or i % 50 == 0:
            print(f"Processing row {i+1}: {row.get('ID')}")
        
        # Clean values
        row_id = str(row.get('ID', ''))
        title = clean_value(row.get('Title', ''))
        raw_impact_val = clean_value(row.get('Raw_impact', 0))
        
        # Convert raw_impact to integer
        try:
            raw_impact = int(float(raw_impact_val)) if raw_impact_val and raw_impact_val != '' else 0
        except (ValueError, TypeError):
            raw_impact = 0
        
        # Create recommendation object matching original JSON structure
        recommendation = {
            "id": row_id,
            "title": title,
            "raw_impact": raw_impact,
            "primary_markers": parse_and_convert_markers(row.get('Primary Markers', ''), mapping),
            "secondary_markers": parse_and_convert_markers(row.get('Secondary Markers', ''), mapping),
            "tertiary_markers": parse_and_convert_markers(row.get('Tertiary Markers', ''), mapping),
            "primary_metrics": parse_and_convert_markers(row.get('Primary Metrics', ''), mapping),
            "secondary_metrics": parse_and_convert_markers(row.get('Secondary Metrics', ''), mapping),
            "tertiary_metrics": parse_and_convert_markers(row.get('Tertiary Metrics', ''), mapping)
        }
        
        recommendations.append(recommendation)
    
    # Create the complete JSON structure with metadata
    json_structure = {
        "recommendations": recommendations,
        "metadata": {
            "total_recommendations": len(recommendations),
            "creation_date": datetime.now().strftime("%Y-%m-%d"),
            "creation_time": datetime.now().strftime("%H:%M:%S"),
            "source": "WellPath recommendations database",
            "description": "Complete WellPath recommendations with markers and metrics for impact scoring",
            "excel_source": "WellPath Tiered Markers.xlsx"
        }
    }
    
    return json_structure

def main():
    """Main execution function"""
    
    excel_filename = 'WellPath Tiered Markers.xlsx'
    output_filename = 'recommendations_list.json'  # Now replaces the original file
    
    print("=" * 60)
    print("Python JSON Creator Script - Excel to JSON Converter")
    print("=" * 60)
    print(f"Looking for Excel file: {excel_filename}")
    
    # Check if Excel file exists
    if not os.path.exists(excel_filename):
        print(f"Error: Excel file '{excel_filename}' not found in current directory")
        print("Please ensure the Excel file is in the same folder as this script")
        return
    
    # Check if pandas is available
    try:
        import pandas as pd
        print("✓ Pandas library found - ready to read Excel files")
    except ImportError:
        print("Error: pandas library not found.")
        print("Install with: pip install pandas openpyxl")
        return
    
    # Create backup and move original file
    print(f"\n--- Backup Process ---")
    backup_success = create_backup_folder_and_move_original()
    if not backup_success:
        print("Warning: Backup process encountered issues, but continuing...")
    
    # Load Excel data
    print(f"\n--- Loading Excel Data ---")
    excel_data = load_excel_data(excel_filename)
    if not excel_data:
        return
    
    # Create new JSON structure
    print(f"\n--- Creating JSON Structure ---")
    json_data = create_recommendations_json(excel_data)
    
    # Show sample recommendation
    if json_data['recommendations']:
        sample = json_data['recommendations'][0]
        print(f"\nSample recommendation:")
        print(f"  ID: {sample['id']}")
        print(f"  Title: {sample['title']}")
        print(f"  Raw Impact: {sample['raw_impact']}")
        print(f"  Primary Markers: {sample['primary_markers']}")
        print(f"  Primary Metrics: {sample['primary_metrics']}")
    
    # Save the new JSON file (replaces original)
    print(f"\n--- Saving New JSON File ---")
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Successfully replaced: {output_filename}")
        print(f"  Total recommendations: {len(json_data['recommendations'])}")
        print(f"  Creation date: {json_data['metadata']['creation_date']}")
        print(f"  Creation time: {json_data['metadata']['creation_time']}")
        print(f"\n🎉 Success! Your recommendations_list.json file has been updated.")
        print(f"   Original file backed up to: Recommendations_List_Old/")
        
    except Exception as e:
        print(f"❌ Error saving JSON file: {e}")
        return

    print("\n" + "=" * 60)
    print("Process completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
