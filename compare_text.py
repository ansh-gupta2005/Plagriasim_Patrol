# Updated compare_text.py with code comparison support
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tokenize
from io import BytesIO

STOPWORDS = {
    'the', 'is', 'in', 'a', 'an', 'and', 'of', 'to', 'it', 'on', 'for', 'with', 'that', 'this',
    'as', 'are', 'was', 'were', 'by', 'be', 'am', 'at', 'or', 'from', 'but', 'not', 'have', 'has',
    'had', 'do', 'does', 'did', 'so', 'if', 'out', 'up', 'down', 'about', 'into', 'over', 'then',
    'its', "it's"
}

def preprocess(text):
    return [word.strip('.,()').lower() for word in text.split() if word.lower().strip('.,()') not in STOPWORDS]

def combined_similarity(words_a, words_b):
    a = " ".join(words_a)
    b = " ".join(words_b)
    vec = CountVectorizer().fit_transform([a, b])
    cosine_sim = cosine_similarity(vec)[0, 1] * 100
    difflib_sim = SequenceMatcher(None, words_a, words_b).ratio() * 100
    return round((cosine_sim + difflib_sim) / 2, 2)

def compare_all_submissions(texts):
    results = []
    keys = list(texts.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            t1 = preprocess(texts[keys[i]])
            t2 = preprocess(texts[keys[j]])
            score = combined_similarity(t1, t2)
            results.append({"file1": keys[i], "file2": keys[j], "similarity": score})
    return results

def tokenize_code(code):
    try:
        tokens = tokenize.tokenize(BytesIO(code.encode('utf-8')).readline)
        return [tok.string for tok in tokens if tok.type in (1, 3)]
    except:
        return []

def compare_code_submissions(code_texts):
    results = []
    keys = list(code_texts.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            t1 = tokenize_code(code_texts[keys[i]])
            t2 = tokenize_code(code_texts[keys[j]])
            score = combined_similarity(t1, t2)
            results.append({"file1": keys[i], "file2": keys[j], "similarity": score})
    return results
