
import re
import spacy
import contextualSpellCheck
import ollama

nlp = spacy.load("en_core_web_md")
contextualSpellCheck.add_to_pipe(nlp)


def llama_fix(text: str) -> str:
   
    prompt = (
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
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    )
    return response["message"]["content"].strip()


def correct(text: str) -> str:
    """
    1. Split text into sentences.
    2. run through llama
    3. Run each through spaCy + contextualSpellCheck.
    4. If spellCheck applied, use outcome; else keep original.
    5. Rejoin and return the corrected text.
    """
# 1
    sentences = re.split(r'(?<=[.!?])\s+', text)
    corrected = []

    for sent in sentences:
        # 2
        llama_out = llama_fix(sent)
        # 3
        doc = nlp(llama_out)
        # 4
        final = doc._.outcome_spellCheck if doc._.performed_spellCheck else llama_out
        corrected.append(final)

    # 5
    return " ".join(corrected)



original_text = (
        "I am 25 years old and my life is good. I work in a police startoin and I have to beark up crowds of people and scounte the Cife in socer to is Head Qunes and everey were he go and I see my wife and chines once a years in the poilce Fores it is hear* and you have to be bave and to have muntse. and you get pay onec verey to mothes it is good in the Poilce Fose and you can Ingean and be talk to Hopiesel.The End."
        #"I woad Be a carcanh**h and I woad like to lvie on a farm and have a lor I got my own tea nea***y and whare Ihas"
    )

print(correct(original_text))

'''

import re
import spacy
import contextualSpellCheck
import ollama
import language_tool_python

# Load spaCy model and add contextual spell-checker\ nlp = spacy.load("en_core_web_md")
nlp = spacy.load("en_core_web_md")
contextualSpellCheck.add_to_pipe(nlp)

# Load UK dictionary for post-filter
DICT_PATH = "/Users/xuefeicheng/Downloads/hunspell-en_GB-ise-2020.12.07/en_GB-ise.dic"
uk_words = set()
with open(DICT_PATH, encoding="utf-8") as f:
    for line in f:
        if line.strip() and not line[0].isdigit():
            uk_words.add(line.split('/')[0].strip().lower())

# Initialize LanguageTool for grammar checking
from language_tool_python import LanguageToolPublicAPI
tool = LanguageToolPublicAPI('en-GB')


def llama_fix(text: str) -> str:
    """
    2. Run sentence through LLaMA to fix misspellings only,
    without changing grammar, punctuation, or word order.
    """
    prompt = (
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
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    )
    return resp["message"]["content"].strip()


def post_filter_dictionary(corrected: str, original: str) -> str:
    """
    Replace any token in 'corrected' not found in uk_words
    with its counterpart from 'original'.
    """
    corr_tokens = corrected.split()
    orig_tokens = original.split()
    filtered = []
    for ctok, otok in zip(corr_tokens, orig_tokens):
        clean = re.sub(r'[^\w\[\]]', '', ctok).lower()
        if clean and clean not in uk_words:
            filtered.append(otok)
        else:
            filtered.append(ctok)
    return ' '.join(filtered)


def correct(text: str) -> str:
    """
    1. Split text into sentences.
    2. Run each through LLaMA.
    3. Run that output through spaCy + contextualSpellCheck.
    4. If contextualSpellCheck applied, use its result; else keep LLaMA output.
    5. Rejoin sentences.
    6. Post-filter against UK dictionary.
    7. Run final text through LanguageTool for grammar corrections.
    8. Return the fully corrected text.
    """
    # 1. Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    corrected_sentences = []

    for sent in sentences:
        # 2. LLaMA pass
        llama_out = llama_fix(sent)
        # 3. spaCy + contextualSpellCheck
        doc = nlp(llama_out)
        # 4. Choose contextual outcome if available
        base = doc._.outcome_spellCheck if doc._.performed_spellCheck else llama_out
        corrected_sentences.append(base)

    # 5. Rejoin sentences
    joined = ' '.join(corrected_sentences)
    # 6. Post-filter dictionary
    #filtered = post_filter_dictionary(joined, text)
    # 7. Grammar check
    final = tool.correct(joined)
    return final


if __name__ == "__main__":
    original_text = (
        "I am 25 years old and my life is good. I work in a police startoin and I have to beark up crowds of people and scounte the Cife in socer to is Head Qunes and everey were he go and I see my wife and chines once a years in the poilce Fores it is hear* and you have to be bave and to have muntse. and you get pay onec verey to mothes it is good in the Poilce Fose and you can Ingean and be talk to Hopiesel.The End."
    )
    print(correct(original_text))


import re
import spacy
import ollama
import language_tool_python

# Load spaCy model
nlp = spacy.load("en_core_web_md")

# Load UK dictionary for post-filtering
DICT_PATH = "/Users/xuefeicheng/Downloads/hunspell-en_GB-ise-2020.12.07/en_GB-ise.dic"
uk_words = set()
with open(DICT_PATH, encoding="utf-8") as f:
    for line in f:
        if line.strip() and not line[0].isdigit():
            uk_words.add(line.split('/')[0].strip().lower())

# Initialize LanguageTool for grammar checking
tool = language_tool_python.LanguageToolPublicAPI('en-GB')


def llama_fix(text: str) -> str:
    """
    "This is a historical writing sample from a child."
        "Correct spelling only. Do not change grammar, punctuation, or sentence order.\n"
        "Replace 'xxx' or '****' followed by a number with the number and the word 'pounds'.\n"
        "If 'xxx' or '****' are not followed by a number, keep them as-is.\n"
        "Avoid using symbols like '£' — write 'pounds'.\n"
        "Expand short forms: e.g., write 'centimetres' instead of 'cm'.\n"
        "DO NOT replace or modify anything inside square brackets (e.g. [male name], [street name]).\n"
        "DO NOT invent names or proper nouns.\n"
        "Only return the corrected sentence. Do not explain anything.\n"
    """
    system_prompt = (
        "You are a precise spelling assistant. "
        "Fix misspellings only. Do NOT change grammar, punctuation, or word order."
    )
    resp = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
    )
    return resp["message"]["content"].strip()


def post_filter_dictionary(corrected: str, original: str) -> str:
    """
    Replace any token in 'corrected' not found in uk_words
    with its counterpart from 'original'.
    """
    corr_tokens = corrected.split()
    orig_tokens = original.split()
    filtered = []
    for ctok, otok in zip(corr_tokens, orig_tokens):
        clean = re.sub(r'[^\w\[\]]', '', ctok).lower()
        if clean and clean not in uk_words:
            filtered.append(otok)
        else:
            filtered.append(ctok)
    return ' '.join(filtered)


def correct(text: str) -> str:
    """
    1. Split text into sentences.
    2. Run each through LLaMA.
    3. Rejoin sentences.
    4. Post-filter against UK dictionary.
    5. Run final text through LanguageTool for grammar corrections.
    6. Return the fully corrected text.
    """
    # 1. Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    corrected_sentences = []

    for sent in sentences:
        # 2. LLaMA pass
        llama_out = llama_fix(sent)
        corrected_sentences.append(llama_out)

    # 3. Rejoin sentences
    joined = ' '.join(corrected_sentences)
    # 4. Post-filter dictionary
    filtered = post_filter_dictionary(joined, text)
    # 5. Grammar check
    final = tool.check(filtered)
    return language_tool_python.utils.correct(filtered, final)


original_text = (
        "I am 25 years old and my life is good. I work in a police startoin and I have to beark up crowds of people and scounte the Cife in socer to is Head Qunes and everey were he go and I see my wife and chines once a years in the poilce Fores it is hear* and you have to be bave and to have muntse. and you get pay onec verey to mothes it is good in the Poilce Fose and you can Ingean and be talk to Hopiesel.The End."
        #"I woad Be a carcanh**h and I woad like to lvie on a farm and have a lor I got my own tea nea***y and whare Ihas"
    )

print(correct(original_text))

'''