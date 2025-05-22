import ollama
import pandas as pd

DATA_PATH = "/Users/xuefeicheng/Desktop/essay/NCDS_essay_codes/Data/essay11/raw_all_essays.csv"
OUT_PATH  = "/Users/xuefeicheng/Library/CloudStorage/OneDrive-SharedLibraries-McGillUniversity/Jacob Hazen - Data/Essay11/200_essays_corrected.csv"
#OUT_PATH  = "/Users/xuefeicheng/Desktop/essays_corrected.csv"

df = pd.read_csv(DATA_PATH)

text_col = df.columns[3]

df_200 = df.head(200).copy()
df_200['ID'] = df['Text'].str.extract(r'ID:\s*(\w+)')
df_200['Word Count'] = df['Text'].str.extract(r'Words:\s*(\d+)')
df_200 = df_200.rename(columns={text_col: "original"})

df_200["processed"] = ""

instruction = (
    "This is a historical writing sample from a child in 1958 United Kingdom. \n"
    "Correct spelling only. Do not change grammar, punctuation, or sentence order.\n"
    "ABSOLUTELY DO NOT add or delete any words, numbers, or phrases that are not already present in the original sentence. No guessing or inferring missing content.\n"
    "DO NOT invent names or proper nouns.\n"
    "Replace a pattern of three or more 'x' or '*' followed by a number with the number and the word 'pounds'. For example replace “xxxx120” with “120 pounds”. \n"
    "Avoid using symbols. For example change '£' to pounds. \n"
    "Expand short forms: e.g., write 'centimetres' instead of 'cm'.\n"
    "DO NOT replace or modify anything inside square brackets (e.g. [name], [address]).\n"
    "Only return the corrected sentence. Do not explain anything.\n"
)

for idx, row in df_200.iterrows():
    prompt = instruction + f"1. {row['original']}"
    resp = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': prompt}],
        options={
        'temperature': 0.0,
        'top_p': 1.0,
        'repeat_penalty': 1.0
    }
        ]
    )
    corrected = resp['message']['content'].strip()
    if corrected.startswith("1. "):
        corrected = corrected[3:]
    df_200.at[idx, 'processed'] = corrected

df_out = df_200[['ID', 'original', 'processed','Word Count']]
df_out.to_csv(OUT_PATH, index=False)
print(f"Processed 200 essays saved to {OUT_PATH}")
