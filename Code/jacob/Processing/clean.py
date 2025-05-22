# import pandas as pd
# import ollama

# # 1. load your essays
# path = "/home/semipro321/OneDrive/School/McGill/Research Projects/Essay/"
# df_essay = pd.read_csv(path + 'Data/essay11/raw_all_essays.csv')

# # 2. define a reusable prompt template
# PROMPT = (
#     "You are a spelling corrector reviewing a historical writing sample from a child in 1958 United Kingdom.\n\n"
#     "Instructions:\n"
#     "1. Correct **spelling only**. Do not change grammar, punctuation, sentence structure, or word order.\n"
#     "2. Do **not** alter the meaning or tone of the text.\n"
#     "3. Replace 'xxx' or '****' followed by a number with the number and the word 'pounds' (e.g., '****5' → '5 pounds').\n"
#     "4. If 'xxx' or '****' are **not** followed by a number, leave them unchanged.\n"
#     "5. Avoid using symbols. Write out abbreviations fully (e.g., use 'centimetres' instead of 'cm').\n"
#     "6. Do **not** modify or replace anything inside square brackets (e.g., [John Smith]).\n"
#     "7. Do **not** invent names or content.\n\n"
#     "Return only the corrected text, without any extra commentary or explanation.\n\n"
#     "{essay}"
# )

# def correct_essay(text):
#     prompt = PROMPT.format(essay=text)
#     resp = ollama.chat(
#         model="llama3.2",
#         messages=[{"role":"user", "content":prompt}]
#     )
#     return resp["message"]["content"].strip()

# df_essay = df_essay.sample(200, random_state=43)  # sample 60 essays
# # run over all essays
# df_essay["corrected"] = df_essay["cleaned_text"].apply(correct_essay)

# # save to a new file
# df_essay.to_csv(path+"essays_corrected_200.csv", index=False)
import pandas as pd
import ollama

# 1. Load your essays
path = "/home/semipro321/OneDrive/School/McGill/Research Projects/Essay/"
df_essay = pd.read_csv(path + 'Data/essay11/raw_all_essays.csv')

# 2. Define prompt
# PROMPT = (
#     "You are a spelling corrector reviewing a historical writing sample from a child in 1958 United Kingdom.\n\n"
#     "Instructions:\n"
#     "1. Correct **spelling only**. Do not change grammar, punctuation, sentence structure, or word order.\n"
#     "2. Do **not** alter the meaning or tone of the text.\n"
#     "3. Replace 'xxx' or '****' followed by a number with the number and the word 'pounds' (e.g., '****5' → '5 pounds').\n"
#     "4. If 'xxx' or '****' are **not** followed by a number, leave them unchanged.\n"
#     "5. Avoid using symbols. Write out abbreviations fully (e.g., use 'centimetres' instead of 'cm').\n"
#     "6. Do **not** modify or replace anything inside square brackets (e.g., [John Smith]).\n"
#     "7. Do **not** invent names or content.\n\n"
#     "Return only the corrected text, without any extra commentary or explanation.\n\n"
#     "{essay}"
# )

PROMPT = (
    "You are a spelling corrector reviewing a historical writing sample from a child in 1958 United Kingdom.\n\n"
    "Correct **spelling only**. Do not change grammar, punctuation, word order, or sentence structure.\n"
    "Do not rephrase or simplify. Preserve all original meaning and style.\n"
    "Leave all punctuation, word choices, and grammar errors untouched unless they are spelling-related.\n"
    "Leave anything in square brackets [like this] exactly as-is.\n"
    "If you see 'xxx' or '****' followed by a number (e.g., '****5'), replace it with '5 pounds'.\n"
    "If 'xxx' or '****' are not followed by a number, leave them unchanged.\n"
    "Avoid symbols. Expand abbreviations (e.g., use 'centimetres' instead of 'cm').\n"
    "Do **not** explain changes or provide notes. Only return the corrected version of the essay.\n\n"
    "{essay}"
)

# 3. Grammar/spell corrector
def correct_essay(text):
    prompt = PROMPT.format(essay=text)
    resp = ollama.chat(
        model="ifioravanti/mistral-grammar-checker:7b",  # swap model here
        messages=[{"role": "user", "content": prompt}]
    )
    return resp["message"]["content"].strip()

# 4. Run on a subset (optional)
df_essay = df_essay.sample(5, random_state=43)
df_essay["corrected"] = df_essay["cleaned_text"].apply(correct_essay)

# 5. Save
df_essay.to_csv(path + "essays_corrected_5.csv", index=False)

