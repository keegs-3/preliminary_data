#!/usr/bin/env python3
"""
Python JSON Updater Script
Updates recommendations_list.json with new marker/metric categorizations from CSV
"""

import json
import csv
import sys
import os

def load_json_data(filename):
    """Load JSON data from file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{filename}': {e}")
        return None

def load_csv_data(filename):
    """Load CSV data from file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
    except Exception as e:
        print(f"Error reading CSV file '{filename}': {e}")
        return None

def get_csv_to_json_mapping():
    """Returns the complete mapping from CSV column names to JSON marker names"""
    return {
        # Blood lipids and cardiovascular
        'Total Cholesterol': 'total_cholesterol',
        'LDL': 'ldl',
        'HDL': 'hdl',
        'Lp(a)': 'lp_a',
        'Triglycerides': 'triglycerides',
        'ApoB': 'apob',
        'Omega-3 Index': 'omega_3_index',
        
        # Blood chemistry and markers
        'RDW': 'rdw',
        'Magnesium (RBC)': 'magnesium_rbc',
        'Vitamin D': 'vitamin_d',
        'Serum Ferritin': 'serum_ferritin',
        'Total Iron Binding Capacity (TIBC)': 'tibc',
        'Transferrin Saturation': 'transferrin_saturation',
        'hsCRP': 'hscrp',
        
        # Blood cell counts
        'White Blood Cell Count': 'white_blood_cell_count',
        'Neutrophils': 'neutrophils',
        'Lymphocytes': 'lymphocytes',
        'Neutrocyte/Lymphocyte Ratio': 'neutrocyte_lymphocyte_ratio',
        'Eosinophils': 'eosinophils',
        'Red Blood Cell Count': 'red_blood_cell_count',
        'Platelet Count': 'platelet_count',
        
        # Glucose and insulin
        'HbA1c': 'hba1c',
        'Fasting Glucose': 'fasting_glucose',
        'Fasting Insulin': 'fasting_insulin',
        'HOMA-IR': 'homa_ir',
        
        # Liver function
        'ALT': 'alt',
        'GGT': 'ggt',
        'AST': 'ast',
        'ALP': 'alp',
        'Albumin': 'albumin',
        
        # Hormones
        'Testosterone': 'testosterone',
        'Free Testosterone': 'free_testosterone',
        'Cortisol': 'cortisol',
        'Estradiol': 'estradiol',
        'Progesterone': 'progesterone',
        'TSH': 'tsh',
        'DHEA-S': 'dhea_s',
        'SHBG': 'shbg',
        
        # Other blood chemistry
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
        
        # Kidney function
        'eGFR': 'egfr',
        'Cystatin C': 'cystatin_c',
        'BUN': 'bun',
        'Creatinine': 'creatinine',
        
        # Minerals
        'Calcium (Serum)': 'calcium_serum',
        'Calcium (Ionized)': 'calcium_ionized',
        
        # Physical metrics
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
        
        # Sleep metrics
        'REM Sleep': 'rem_sleep',
        'Deep Sleep': 'deep_sleep',
        'Total Sleep': 'total_sleep',
        
        # Activity metrics
        'Steps/Day': 'steps_day'
    }

def parse_and_convert_markers(marker_string, csv_to_json_mapping):
    """Parse CSV marker string and convert to JSON format"""
    if not marker_string or marker_string.strip() == '':
        return []
    
    # Split by comma and clean up whitespace
    csv_markers = [marker.strip() for marker in marker_string.split(',') if marker.strip()]
    
    # Convert CSV names to JSON format
    json_markers = []
    for csv_marker in csv_markers:
        if csv_marker in csv_to_json_mapping:
            json_markers.append(csv_to_json_mapping[csv_marker])
        else:
            print(f"Warning: No mapping found for CSV marker: '{csv_marker}'")
            # Fallback: convert to snake_case
            fallback = csv_marker.lower().replace(' ', '_').replace('-', '_')
            fallback = ''.join(c for c in fallback if c.isalnum() or c == '_')
            fallback = '_'.join(part for part in fallback.split('_') if part)
            json_markers.append(fallback)
    
    return json_markers

def update_recommendations(json_filename, csv_filename, output_filename=None):
    """Main function to update recommendations from CSV data"""
    
    print("Starting recommendation update process...")
    print(f"Reading JSON file: {json_filename}")
    print(f"Reading CSV file: {csv_filename}")
    
    # Load data files
    recommendations_data = load_json_data(json_filename)
    if not recommendations_data:
        return False
    
    csv_data = load_csv_data(csv_filename)
    if not csv_data:
        return False
    
    print(f"Found {len(recommendations_data['recommendations'])} recommendations in JSON")
    print(f"Found {len(csv_data)} records in CSV")
    
    # Get mapping
    csv_to_json_mapping = get_csv_to_json_mapping()
    
    # Create CSV mapping by ID
    csv_mapping = {}
    for row in csv_data:
        if row.get('ID'):
            csv_mapping[row['ID']] = {
                'primary_markers': parse_and_convert_markers(row.get('Primary Markers', ''), csv_to_json_mapping),
                'secondary_markers': parse_and_convert_markers(row.get('Secondary Markers', ''), csv_to_json_mapping),
                'tertiary_markers': parse_and_convert_markers(row.get('Tertiary Markers', ''), csv_to_json_mapping),
                'primary_metrics': parse_and_convert_markers(row.get('Primary Metrics', ''), csv_to_json_mapping),
                'secondary_metrics': parse_and_convert_markers(row.get('Secondary Metrics', ''), csv_to_json_mapping),
                'tertiary_metrics': parse_and_convert_markers(row.get('Tertiary Metrics', ''), csv_to_json_mapping)
            }
    
    # Update recommendations
    updated_count = 0
    not_found_count = 0
    
    for rec in recommendations_data['recommendations']:
        if rec['id'] in csv_mapping:
            csv_rec_data = csv_mapping[rec['id']]
            
            # Update with CSV data
            rec['primary_markers'] = csv_rec_data['primary_markers']
            rec['secondary_markers'] = csv_rec_data['secondary_markers']
            rec['tertiary_markers'] = csv_rec_data['tertiary_markers']
            rec['primary_metrics'] = csv_rec_data['primary_metrics']
            rec['secondary_metrics'] = csv_rec_data['secondary_metrics']
            rec['tertiary_metrics'] = csv_rec_data['tertiary_metrics']
            
            updated_count += 1
        else:
            not_found_count += 1
            print(f"Warning: No CSV data found for recommendation ID: {rec['id']}")
    
    print(f"Updated {updated_count} recommendations")
    print(f"{not_found_count} recommendations had no matching CSV data")
    
    # Show sample of updated data
    sample_rec = None
    for rec in recommendations_data['recommendations']:
        if rec['primary_markers'] or rec['primary_metrics']:
            sample_rec = rec
            break
    
    if sample_rec:
        print("\nSample of updated recommendation:")
        print(f"ID: {sample_rec['id']}")
        print(f"Title: {sample_rec['title']}")
        print(f"Primary Markers: {sample_rec['primary_markers']}")
        print(f"Primary Metrics: {sample_rec['primary_metrics']}")
    
    # Save updated JSON
    if not output_filename:
        output_filename = 'updated_' + json_filename
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(recommendations_data, f, indent=2, ensure_ascii=False)
        print(f"\nUpdated JSON saved to: {output_filename}")
        return True
    except Exception as e:
        print(f"Error saving updated JSON: {e}")
        return False

def main():
    """Main execution function"""
    
    # Default file names
    json_filename = 'recommendations_list.json'
    csv_filename = 'recommendationsGrid view 9.csv'
    
    # Check if files exist
    if not os.path.exists(json_filename):
        print(f"Error: JSON file '{json_filename}' not found in current directory")
        print(f"Current directory: {os.getcwd()}")
        return
    
    if not os.path.exists(csv_filename):
        print(f"Error: CSV file '{csv_filename}' not found in current directory")
        print(f"Current directory: {os.getcwd()}")
        return
    
    # Run the update
    success = update_recommendations(json_filename, csv_filename)
    
    if success:
        print("\nUpdate completed successfully!")
    else:
        print("\nUpdate failed. Check the error messages above.")

if __name__ == "__main__":
    main()
