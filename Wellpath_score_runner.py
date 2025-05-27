import yaml
import re
import csv

# Load YAML file
def load_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# Parse score value from string
def parse_score(value, range_str, score_raw):
    try:
        if '-' in range_str and not range_str.startswith('linear'):
            low, high = map(float, range_str.split('-'))
            if low <= value <= high:
                if isinstance(score_raw, str) and score_raw.startswith('linear:'):
                    s1, s2 = map(float, score_raw.replace('linear:', '').split('-'))
                    return round(s1 + (s2 - s1) * ((value - low) / (high - low)), 2)
                return float(score_raw)
        elif range_str.startswith('<'):
            if value < float(range_str[1:]):
                return float(score_raw) if isinstance(score_raw, (int, float)) else float(score_raw.replace('linear:', '').split('-')[0])
        elif range_str.startswith('>'):
            if value > float(range_str[1:]):
                return float(score_raw) if isinstance(score_raw, (int, float)) else float(score_raw.replace('linear:', '').split('-')[-1])
    except Exception as e:
        return None
    return None

# Normalize keys to lowercase underscore format
def normalize_key(key):
    return key.lower().replace(" ", "_")

# Extract all unique pillar names
def extract_all_pillars(config):
    pillars = set()
    for marker in config.values():
        for p in marker.get("pillars", []):
            pillars.add(p)
    return sorted(pillars)

# Main evaluation function
def evaluate_marker(marker_name, value, config):
    normalized_keys = {normalize_key(k): k for k in config}
    true_key = normalized_keys.get(normalize_key(marker_name))

    if not true_key:
        return None, "Marker not found", "N/A", []

    marker = config[true_key]
    for tier in marker.get('ranges', []):
        score = parse_score(value, tier['range'], tier['score'])
        if score is not None:
            return score, tier['label'], marker['type'], marker.get('pillars', [])

    return None, "Out of range", marker['type'], marker.get('pillars', [])

# Sample data
SAMPLE_TESTS = {
    "total_cholesterol": 201,
    "ldl": 140,
    "hdl_male": 60,
    "lp_a": 50,
    "triglycerides": 150,
    "apob": 100,
    "omega3_index": 8.0,

    "hba1c": 5.6,
    "fasting_glucose": 100,
    "fasting_insulin": 10.0,
    "homa_ir": 2.5,

    "alt_male": 40.0,
    "ggt_male": 30.0,
    "hscrp": 3.0,

    "wbc": 10.0,
    "neutrophils": 5.5,
    "lymphocytes": 3.5,
    "neut_lymph_ratio": 2.5,
    "eosinophils": 500,

    "tsh": 2.5,
    "estradiol_men": 40.0,
    "testosterone_male": 800,
    "free_testosterone_male": 12.0,
    "shbg_male": 35,

    "cortisol_morning": 16.0,
    "cortisol_afternoon": 10.0,
    "cortisol_midnight": 5.0,

    "albumin": 5.0,
    "ast_male": 25,
    "creatine_kinase_ck": 350,
    "sodium": 142,
    "potassium": 4.7,

    "ferritin": 100,
    "hematocrit": 45.0,
    "hemoglobin": 15.5,
    "iron": 130,
    "total_iron_binding_capacity": 310,
    "transferrin_saturation": 35.0,
    "mch": 33.0,
    "mchc": 35.5,
    "mcv": 95,
    "rbc": 5.0,
    "platelets": 300,
    "vo2_max": 44,
    "percent_body_fat_male": 20,
    "lbm_male": 80,
    "waist_hip_male": 0.90,
    "bmi": 24.9
}

# Main process
if __name__ == "__main__":
    print("🧠 Loading Markers.yaml...")
    config = load_yaml("Markers.yaml")

    print("\n🧪 Running evaluation on SAMPLE_TESTS...\n")

    all_pillars = extract_all_pillars(config)
    output_rows = []

    for marker, val in SAMPLE_TESTS.items():
        score, label, mtype, pillars = evaluate_marker(marker, val, config)

        print(f"🧬 {marker.upper():<25} | Value: {val}")
        print(f"   📘 Type: {mtype}")
        print(f"   🧱 Pillars: {', '.join(pillars) if pillars else 'N/A'}")
        print(f"   🏷️  Label: {label}")
        print(f"   🧮 Score: {score}\n")

        row = {
            "marker": marker,
            "value": val,
            "type": mtype,
            "label": label,
            "score": score
        }

        for p in all_pillars:
            row[p.lower()] = 1 if p in pillars else 0

        output_rows.append(row)

    # Output CSV file
    csv_columns = ["marker", "value", "type", "label", "score"] + [p.lower() for p in all_pillars]
    with open("sample_results.csv", mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(output_rows)

    print("✅ CSV export complete: sample_results.csv")