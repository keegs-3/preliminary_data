import pandas as pd
import json
import os

def build_recommendation_subset(recommendations_json_path, csv_input_path, subset_json_output_path):
    # Step 1: Load the full recommendations list (expects dict with 'recommendations' key)
    with open(recommendations_json_path, 'r', encoding='utf-8') as f:
        full_data = json.load(f)
    
    if 'recommendations' not in full_data:
        raise ValueError("JSON file does not contain 'recommendations' key")

    full_recs = full_data['recommendations']
    print(f"Loaded {len(full_recs)} total recommendations")

    # Step 2: Load the recommendation IDs from the CSV (column F = index 5)
    if not os.path.exists(csv_input_path):
        raise FileNotFoundError(f"CSV not found at path: {csv_input_path}")

    csv_df = pd.read_csv(csv_input_path)

    if csv_df.shape[1] < 6:
        raise ValueError("CSV does not have at least 6 columns; check that column F exists.")

    rec_ids = csv_df.iloc[:, 5].dropna().astype(str).str.strip().unique()
    print(f"Found {len(rec_ids)} unique rec IDs from CSV")

    # Step 3: Filter the recommendations list to only those in the CSV
    filtered_recs = [rec for rec in full_recs if str(rec.get('id')).strip() in rec_ids]
    print(f"✅ Matched {len(filtered_recs)} recommendations")

    # Step 4: Write to a new JSON file for impact scorer
    with open(subset_json_output_path, 'w', encoding='utf-8') as f:
        json.dump({"recommendations": filtered_recs}, f, indent=2)


    print(f"📝 Subset written to: {subset_json_output_path}")

# Example usage
if __name__ == "__main__":
    # Calculate base directory properly
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    build_recommendation_subset(
        recommendations_json_path=os.path.join(base_dir, "recommendations_list.json"),
        csv_input_path=os.path.join(base_dir, "archive", "OpenAI_Recs", "recommendation_output (1).csv"),
        subset_json_output_path=os.path.join(base_dir, "subset_recommendations.json")
    )
