import yaml
import pandas as pd

# Load the YAML file
with open("Markers.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

output = []

# Iterate over each marker
for marker, details in data.items():
    ranges = details.get("ranges", [])
    for item in ranges:
        label = item.get("label")
        score = item.get("score")
        
        if label is not None and score is not None:
            output.append({
                "marker/metric": marker,
                "Range": label,
                "Score": score
            })

# Export to CSV
df = pd.DataFrame(output)
df.to_csv("output_marker_scores.csv", index=False)
print("✅ Done: output_marker_scores.csv saved.")
