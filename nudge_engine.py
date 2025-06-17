import datetime
import yaml
import re

# 📦 Load Nudges YAML
def load_nudges(filepath="nudges.yaml"):
    with open(filepath, "r") as f:
        return yaml.safe_load(f)

# 🧠 Trigger Engine
def evaluate_nudges(user_data, rec_id, nudges):
    triggered = []

    for nudge in nudges:
        trigger = nudge.get("trigger", {})
        if trigger.get("rec_id") != rec_id:
            continue

        t_type = trigger.get("type", "")
        condition = trigger.get("condition", "")

        if t_type == "missed_days":
            match = re.match(r"(\d+)\s.*of\s(\d+)", condition)
            if match:
                x = int(match.group(1))
                y = int(match.group(2))
                history = user_data.get("step_history", [])[-y:]
                missed = sum(1 for d in history if not d.get("completed", False))
                if missed >= x:
                    triggered.append(nudge)

        elif t_type == "goal_success":
            streak = user_data.get("streaks", {}).get(rec_id, 0)
            required = int(condition.replace("-day streak", "").strip())
            if streak >= required:
                triggered.append(nudge)

        elif t_type == "inactivity":
            steps = user_data.get("steps_today", 0)
            now = user_data.get("time", datetime.datetime.now())
            cutoff_hour = int(condition) if condition.isdigit() else 14
            if now.hour >= cutoff_hour and steps < 1000:
                triggered.append(nudge)

        elif t_type == "cross_domain":
            if rec_id in user_data.get("success_recs", []):
                triggered.append(nudge)

        elif t_type == "biomarker_change":
            biomarker = trigger.get("biomarker")
            expected = trigger.get("trend")
            actual = user_data.get("biomarker_trends", {}).get(biomarker)
            if actual == expected:
                triggered.append(nudge)

        elif t_type == "struggle_detected":
            failures = user_data.get("challenge_failures", 0)
            adherence = user_data.get("adherence", {}).get(rec_id, 1.0)
            if failures >= 2 and adherence < 0.5:
                triggered.append(nudge)

        elif t_type == "weather_event":
            expected = trigger.get("forecast", "").lower()
            actual = user_data.get("weather", "").lower()
            if actual == expected:
                triggered.append(nudge)

    return triggered

# 🧪 TEST ENTRYPOINT
if __name__ == "__main__":
    rec_id = "REC001"

    user_data = {
        "step_history": [
            {"date": "2024-06-01", "completed": False},
            {"date": "2024-06-02", "completed": True},
            {"date": "2024-06-03", "completed": False},
            {"date": "2024-06-04", "completed": False},
            {"date": "2024-06-05", "completed": True}
        ],
        "streaks": {"REC001": 5},
        "steps_today": 750,
        "time": datetime.datetime.now(),
        "success_recs": ["REC001"],
        "biomarker_trends": {"vo2_max": "improving"},
        "challenge_failures": 3,
        "adherence": {"REC001": 0.4},
        "weather": "Rain"
    }

    nudges = load_nudges("nudges.yaml")
    matched = evaluate_nudges(user_data, rec_id, nudges)

    print(f"\n✅ Matching Nudges for {rec_id} ({len(matched)}):")
    for n in matched:
        print(f"\n• {n['title']}\n  → {n['message']}")
