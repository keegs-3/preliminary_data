import yaml
import pandas as pd

with open("survey.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

output = []

for item in data:
    question_text = item.get("question")
    answers = item.get("answers", [])

    if question_text and isinstance(answers, list):
        for ans in answers:
            if isinstance(ans, dict):
                answer_text = ans.get("text")
                score = ans.get("score")

                if answer_text is not None and score is not None:
                    output.append({
                        "question": question_text,
                        "answer": str(answer_text),  # ensure numeric text is stringified
                        "score": score
                    })

df = pd.DataFrame(output)
df.to_csv("survey_question_answers_with_scores.csv", index=False)
print("✅ Done: survey_question_answers_with_scores.csv saved.")
