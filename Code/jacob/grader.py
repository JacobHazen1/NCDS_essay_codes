import pandas as pd
import ollama
import json
import time  # optional: to pause between requests

# Load the corrected essays
path = "/home/semipro321/OneDrive/School/McGill/Research Projects/Essay/"
df_essay = pd.read_csv(path + "essays_corrected_60.csv")

df_essay = df_essay.sample(5)
# Scoring prompt for llama
SCORING_PROMPT = (
    "You are a research assistant helping analyze historical essays written by 11-year-old children in 1958 United Kingdom. "
    "Each child was asked this: Imagine you are now 25 years old. Write about the life you are leading, your interests, your home life and your work at the age of 25."
    "Your job is to read the essay carefully and assign scores (from 1 to 5) on the following five traits:\n\n"
    
    "1. Life Goal Specificity:\n"
    "   - Score 1 = No clear goals or vague ideas (e.g., 'I might do something')\n"
    "   - Score 3 = Some general career ideas or lifestyle plans\n"
    "   - Score 5 = Clear and detailed life plan (job, living situation, family, etc.)\n\n"

    "2. Agency and Initiative:\n"
    "   - Score 1 = Passive language, life 'just happens'\n"
    "   - Score 3 = Some personal decisions mentioned\n"
    "   - Score 5 = Strong personal control, plans made and acted upon\n\n"

    "3. Delayed Gratification and Financial Planning:\n"
    "   - Score 1 = No mention of saving or long-term thinking\n"
    "   - Score 3 = Some awareness of working/saving for future\n"
    "   - Score 5 = Mentions saving, banking, investing, or education as future preparation\n\n"

    "4. Educational Aspiration:\n"
    "   - Score 1 = No mention of learning or schooling\n"
    "   - Score 3 = Mentions training or general schooling\n"
    "   - Score 5 = Clear intent to pursue college, university, or specific study path\n\n"

    "5. Career Prestige:\n"
    "   - Score 1 = No job or low-skill/undesired job\n"
    "   - Score 3 = Mid-level or common profession\n"
    "   - Score 5 = Highly skilled, professional, or ambitious job\n\n"

    "Return the result in this exact JSON format (do not explain your scores):\n"
    "{{\n"
    "  \"specificity\": <score>,\n"
    "  \"agency\": <score>,\n"
    "  \"planning\": <score>,\n"
    "  \"education\": <score>,\n"
    "  \"career\": <score>\n"
    "}}\n\n"
    "Essay:\n\n"
    "{essay}"
)

# Function to send essay to model and return scores
def score_essay(text):
    prompt = SCORING_PROMPT.format(essay=text)
    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response["message"]["content"].strip()
        return content
    except Exception as e:
        print("Error:", e)
        return None

# Apply scoring to each essay
results = []
for idx, row in df_essay.iterrows():
    print(f"Scoring essay {idx+1}/{len(df_essay)}...")
    scored = score_essay(row["corrected"])
    results.append(scored)
    time.sleep(1)  # optional pause to avoid overloading model

# Save raw scores
df_essay["score_json"] = results

# Parse JSON safely
def parse_json_safe(x):
    try:
        return json.loads(x)
    except:
        return {"specificity": None, "agency": None, "planning": None, "education": None, "career": None}

df_scores = df_essay["score_json"].apply(parse_json_safe).apply(pd.Series)

# Combine scores with original dataframe
df_final = pd.concat([df_essay, df_scores], axis=1)

# Save result
df_final.to_csv(path + "essays_scored_60.csv", index=False)
print("Saved to essays_scored_60.csv")
