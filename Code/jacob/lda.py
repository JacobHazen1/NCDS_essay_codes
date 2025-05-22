#!/usr/bin/env python3
"""
lda_essays.py  – Train an LDA topic model on 11-year-old NCDS essays
Usage:  python lda_essays.py --file path/to/essays.csv --col essay_text --k 10
"""

import argparse, re, string, logging, pickle
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim import corpora, models
import os

###############################################################################
# 1. CLI arguments
###############################################################################
parser = argparse.ArgumentParser()
parser.add_argument("--file", required=True, help="CSV file with essays")
parser.add_argument("--col",  default="essay", help="column holding raw text")
parser.add_argument("--k",    type=int, default=10, help="number of topics")
parser.add_argument("--passes", type=int, default=10, help="training passes")
parser.add_argument("--seed", type=int, default=42, help="random seed")
args = parser.parse_args()

###############################################################################
# 2. Load data
###############################################################################
df = pd.read_csv(args.file)
texts_raw = df[args.col].astype(str).tolist()

###############################################################################
# 3. Pre-processing helpers
###############################################################################
nltk.download("stopwords", quiet=True)
nltk.download("wordnet",   quiet=True)

stop_set = set(stopwords.words("english"))
punct_pat = re.compile(f"[{re.escape(string.punctuation)}]")

lemm   = WordNetLemmatizer()
def clean(text:str) -> list[str]:
    text   = punct_pat.sub(" ", text.lower())   # rm punctuation + lower
    tokens = [lemm.lemmatize(tok) for tok in text.split() if tok not in stop_set]
    return [tok for tok in tokens if len(tok) > 2]          # drop short tokens

texts_tok = [clean(t) for t in texts_raw]

###############################################################################
# 4. Build dictionary & corpus
###############################################################################
dictionary = corpora.Dictionary(texts_tok)
dictionary.filter_extremes(no_below=5, no_above=0.6)  # keep common terms
corpus = [dictionary.doc2bow(toks) for toks in texts_tok]

###############################################################################
# 5. Fit LDA
###############################################################################
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
lda = models.LdaModel(
    corpus=corpus,
    id2word=dictionary,
    num_topics=args.k,
    random_state=args.seed,
    passes=args.passes,
    alpha="auto",
)

###############################################################################
# 6. Show topics
###############################################################################
print(f"\nTop words per topic (K={args.k}):\n" + "-"*40)
for i, topic in lda.show_topics(num_topics=args.k, num_words=10, formatted=False):
    words = "  ".join([w for w, _ in topic])
    print(f"Topic {i:2d}:  {words}")

###############################################################################
# 7. Save artefacts for later use
###############################################################################
folder = "/home/semipro321/OneDrive/School/McGill/Research Projects/Essay/Code/jacob/LDA_model/"
os.makedirs(folder, exist_ok=True)
dictionary.save(os.path.join(folder, "lda_dictionary.dict"))
lda.save(os.path.join(folder, "lda_model.gensim"))
pickle.dump(corpus, open(os.path.join(folder, "lda_corpus.pkl"), "wb"))
# Save the dictionary, model, and corpus to disk

print("\nDictionary, model, and corpus saved to disk.")


#python lda_essays.py --file raw_all_essays.csv --col cleaned_text --k 12 --passes 20
# This prints the 12 topics, saves

# lda_dictionary.dict

# lda_model.gensim

# lda_corpus.pkl

# theta = [lda.get_document_topics(bow, minimum_probability=0.0) for bow in corpus]
# doc_topic_df = pd.DataFrame([{f"topic_{k}": p for k, p in dist} for dist in theta])
# python lda.py --file "/home/semipro321/OneDrive/School/McGill/Research Projects/Essay/essays_corrected_60.csv" --col corrected --k 12 --passes 20