import ollama
import pandas as pd

# path = "/Users/xuefeicheng/Desktop/essay/NCDS_essay_codes/"

path = "/home/semipro321/OneDrive/School/McGill/Research Projects/Essay/"
df_essay = pd.read_csv(path + 'Data/essay11/raw_all_essays.csv')

df_sample = df_essay.sample(1)

original_text = df_sample.iloc[0, 0]

#original_text = "I am 25 years old and my life is good. I work in a police startoin and I have to beark up crowds of people and scounte the Cife in socer to is Head Qunes and everey were he go and I see my wife and chines once a years in the poilce Fores it is hear* and you have to be bave and to have muntse. and you get pay onec verey to mothes it is good in the Poilce Fose and you can Ingean and be talk to Hopiesel.The End."

prompt = (
    "This is a historical writing sample from a child back in 1958 United Kingdom."
    "Correct spelling only. Do not change grammar, punctuation, or sentence order.\n"
    "Replace 'xxx' or '****' followed by a number with the number and the word 'pounds'.\n"
    "If 'xxx' or '****' are not followed by a number, keep them as-is.\n"
    "Avoid using symbols like '£' — write 'pounds'.\n"
    "Expand short forms: e.g., write 'centimetres' instead of 'cm'.\n"
    "DO NOT replace or modify anything inside square brackets (e.g. [male name], [street name]).\n"
    "DO NOT invent names or proper nouns.\n"
    "Only return the corrected sentence. Do not explain anything.\n"
    f"{original_text}"
)

response = ollama.chat(
    model='llama3.2',
    messages=[{'role': 'user', 'content': prompt}]
)

corrected_text = response['message']['content'].strip()


print("\n Original:")
print(original_text)
print("\n Corrected:")
print(corrected_text)

"""
df_sample = df_essay.sample(3).iloc[:, 0].tolist()

instruction = (
    "This is a historical writing sample from a child. "
    "Correct spelling only. Do not change grammar, punctuation, or sentence order.\n"
    "Replace 'xxx' or '****' followed by a number with the number and the word 'pounds'.\n"
    "If 'xxx' or '****' are not followed by a number, keep them as-is.\n"
    "Avoid using symbols like '£' — write 'pounds'.\n"
    "Expand short forms: e.g., write 'centimetres' instead of 'cm'.\n"
    "DO NOT replace or modify anything inside square brackets (e.g. [male name], [street name]).\n"
    "DO NOT invent names or proper nouns.\n"
    "Only return the corrected sentences, numbered to match the input. Do not explain anything.\n"
)

batch_text = "\n\n".join(f"{i+1}. {essay}" for i, essay in enumerate(df_sample))
prompt = instruction + batch_text

response = ollama.chat(
    model='llama3.2',
    messages=[{'role': 'user', 'content': prompt}]
)
corrected_batch = response['message']['content'].strip()

print(corrected_batch)
"""