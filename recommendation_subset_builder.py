import pandas as pd
import json
import os

def build_recommendation_subset(recommendations_json_path, csv_output_path, subset_json_output_path):
    # Step 1: Load the full recommendations list
    with open(recommendations_json_path, 'r') as f:
        full_recs = json.load(f)

    # Step 2: Load the recommendation IDs from the CSV (column F = index 5)
    csv_df = pd.read_csv(csv_output_path)
    if csv_df.shape[1] < 6:
        raise ValueError("CSV does not have at least 6 columns; check that column F exists.")

    rec_ids = csv_df.iloc[:, 5].dropna().astype(str).str.strip().unique()

    # Step 3: Filter the recommendations list to only those in the CSV
    filtered_recs = [rec for rec in full_recs if rec.get('id') in rec_ids]

    # Step 4: Ensure output directory exists
    os.makedirs(os.path.dirname(subset_json_output_path), exist_ok=True)

    # Step 5: Write to a new JSON file for impact scorer
    with open(subset_json_output_path, 'w') as f:
        json.dump(filtered_recs, f, indent=2)

    print(f"✅ Subset created: {len(filtered_recs)} recommendations written to {subset_json_output_path}")

# Example usage:
if __name__ == "__main__":
    build_recommendation_subset(
        recommendations_json_path="./recommendations_list.json",
        csv_output_path="./recommendation_output (1).csv",
        subset_json_output_path="./OpenAI_Recs/subset_recommendations.json"
    )
