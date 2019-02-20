import numpy as np
from nltk import tokenize
import pymorphy2
from sklearn.feature_extraction.text import TfidfTransformer

tokenizer = tokenize.RegexpTokenizer(r'\w+')
morph = pymorphy2.MorphAnalyzer()
transformer = TfidfTransformer(smooth_idf=False)

def get_docs_words_matrix(texts):
    tokenized_texts = [[morph.parse(word)[0].normal_form for word in tokenizer.tokenize(text)] for text in texts]
    dictionary = set(sum(tokenized_texts, []))
    return np.matrix([[words_in_text.count(word) for word in dictionary] for words_in_text in tokenized_texts])

def get_decomposition(texts):
    docs_words_matrix = transformer.fit_transform(get_docs_words_matrix(texts)).toarray() 
    u, s, vh = np.linalg.svd(docs_words_matrix, full_matrices=False)
    return u, vh