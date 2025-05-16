import ollama
import pandas as pd

path = "/Users/xuefeicheng/Desktop/essay/NCDS_essay_codes/"
df_essay = pd.read_csv(path + 'Data/essay11/raw_all_essays.csv')

df_sample = df_essay.sample(1)

#original_text = df_sample.iloc[0, 0]

original_text = "Iam 25 years old. YEsterday I got a car for myseLF and The FamiLy. I was marrid at the age of 21 my wiFe is caLLed Jane. We have a 4 year old son. Iam STiLL going To CoLLage when I go to work I hope To become a Teacher and in spare Time an aThLeTic. Iam sTiLL iNTeresTed in bird waTching. I Live in a bungalow NEAR [estate] oFTen I TAKE My son To [estate] gardens. NEXT weekwe are geTTing a dog we do not know whaT To caLL iT. THe car is an ASTIN MARTiN. On SATURDays I oFTen go To FooTbaLL maTches. AbouT a week ago I TaughT my son now To swim someTimes he is very obSTinaTe. My wiFe is a very good swimmer she has swam 5 times for Leeds. We have goT a clour Television. I hope To Teach French and Spanish. THe school I hope To Teach aT is [school name]. I have JusT Learned ThaT we are having anoTher baby!we do noT Know whaT he is a boy or a girL we have a siLver Tea seT. I have JuST heard ThaT Iam wanted back aT coLLage anyway ThaT is my LiFe STory aT 25 bye hope you enjoyed IT.  Words: 208"

prompt = (
    "This is a historical writing sample from a child back in 1958 United Kingdom."
    "Correct spelling only. Do not change grammar, punctuation, or sentence order.\n"
    "If you see “xxx” or “****” as a misspelled word: If followed by a number (e.g. “xxx120”) it often refers to “£” – if this fits the context of the sentence, simply replace “xxx120” with “120 pounds”\n"
    "If 'xxx' or '****' are not followed by a number, keep them as-is.\n"
    "Expand short forms: e.g., write 'centimetres' instead of 'cm'.\n"
    "Avoid using symbols.\n"
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