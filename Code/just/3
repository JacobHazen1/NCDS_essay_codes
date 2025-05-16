import re
import spacy
import ollama
import language_tool_python
from spellchecker import SpellChecker

nlp = spacy.load("en_core_web_md")
spell = SpellChecker(language='en', case_sensitive=False)

#DICT_PATH = "/Users/xuefeicheng/Downloads/hunspell-en_GB-ise-2020.12.07/en_GB-ise.dic"
DICT_PATH = "/Users/xuefeicheng/Desktop/essay/NCDS_essay_codes/Code/uk_english_dictionary.txt"
uk_words = set()
with open(DICT_PATH, encoding="utf-8") as f:
    for line in f:
        if line.strip() and not line[0].isdigit():
            uk_words.add(line.split('/')[0].strip().lower())

tool = language_tool_python.LanguageToolPublicAPI('en-GB')


def llama_fix(text: str) -> str:
    system_prompt = (
        "This is a historical writing sample from a child."
        "Correct spelling only. Do not change grammar, punctuation, or sentence order.\n"
        "Replace 'xxx' or '****' followed by a number with the number and the word 'pounds'.\n"
        "If 'xxx' or '****' are not followed by a number, keep them as-is.\n"
        "Avoid using symbols like '£' — write 'pounds'.\n"
        "Expand short forms: e.g., write 'centimetres' instead of 'cm'.\n"
        "DO NOT replace or modify anything inside square brackets (e.g. [male name], [street name]).\n"
        "DO NOT invent names or proper nouns.\n"
        "Only return the corrected sentence. Do not explain anything.\n"
    )
    resp = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
    )
    return resp["message"]["content"].strip()


'''def dictionary_spell_check(text: str) -> str:
    tokens = re.findall(r"\w+|\W+", text)
    corrected = []
    for tok in tokens:
        if tok.isalpha():
            clean = tok
            if clean.lower() in spell:
                corrected.append(tok)
            else:
                suggestion = spell.correction(clean)
                if suggestion:
                    if tok.istitle():
                        suggestion = suggestion.capitalize()
                    elif tok.isupper():
                        suggestion = suggestion.upper()
                    corrected.append(suggestion)
                else:
                    corrected.append(tok)
        else:
            corrected.append(tok)
    return ''.join(corrected)
'''

def correct(text: str) -> str:
    """
    1. Split text into sentences.
    2. Post-filter original sentence with UK dictionary.
    3. Run dictionary-filtered sentence through LLaMA.
    4. Rejoin sentences.
    5. Run the full text through LanguageTool for grammar.
    6. Return the fully corrected text.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    processed = []
    for sent in sentences:
        dict_checked = dictionary_spell_check(sent)
        llama_out = llama_fix(dict_checked)
        processed.append(llama_out)

    joined = ' '.join(processed)
    matches = tool.check(joined)
    final = language_tool_python.utils.correct(joined, matches)

    print("Dictionary Changes:",dict_checked)

    print("LLaMA Spelling Changes:",joined)

    final = language_tool_python.utils.correct(joined, matches)
    return final



original_text = (
         "I am 25 years old and my life is good. I work in a police startoin and I have to beark up crowds of people and scounte the Cife in socer to is Head Qunes and everey were he go and I see my wife and chines once a years in the poilce Fores it is hear* and you have to be bave and to have muntse. and you get pay onec verey to mothes it is good in the Poilce Fose and you can Ingean and be talk to Hopiesel.The End."

    )
print(correct(original_text))
