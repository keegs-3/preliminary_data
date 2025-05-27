import re

def sanitize_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        # Quote range values if not already quoted
        if line.strip().startswith("range:"):
            match = re.search(r'range:\s*(.+)', line)
            if match:
                val = match.group(1).strip()
                if not (val.startswith('"') or val.startswith("'")):
                    val = f'"{val}"'
                    line = f'  range: {val}\n'

        # Quote unit values if needed
        elif line.strip().startswith("unit:"):
            match = re.search(r'unit:\s*(.+)', line)
            if match:
                val = match.group(1).strip()
                if any(ch in val for ch in ['%', '°', 'µ', '≥', '≤']) and not (val.startswith('"') or val.startswith("'")):
                    val = f'"{val}"'
                    line = f'  unit: {val}\n'

        new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print("✅ YAML sanitized. Percent signs, symbols, and ranges now quoted properly.")

sanitize_yaml("Markers.yaml")
