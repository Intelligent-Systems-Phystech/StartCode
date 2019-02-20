import numpy as np
from nltk import tokenize
import pymorphy2
from sklearn.feature_extraction.text import TfidfTransformer

tokenizer = tokenize.RegexpTokenizer(r'\w+')
morph = pymorphy2.MorphAnalyzer()
transformer = TfidfTransformer(smooth_idf=False)

def get_docs_words_matrix(texts):
    """
    Function returns a matrix with frequences of words in rows 
    in which number of rows is equal to the number of documents in collection.

    Parameters
    ----------
    texts : list of str
        list of documents
    Returns
    -------
    numpy.matrix
        matrix "documents-words"
    """
    tokenized_texts = [[morph.parse(word)[0].normal_form for word in tokenizer.tokenize(text)] for text in texts]
    dictionary = set(sum(tokenized_texts, []))
    return np.matrix([[words_in_text.count(word) for word in dictionary] for words_in_text in tokenized_texts])

def get_decomposition(texts):
    """
    Function returns a matrix "documents-topics" and a matrix "topics-words" 
    using a matrix "documents-words" as an input.
    Frequency metric is improved by using the tf-idf metric 
    instead of a simple frequency of word in a document.

    Parameters
    ----------
    texts : list of str
        list of documents
    Returns
    -------
    tuple(numpy.matrix, numpy.matrix)
        matrix "documents-topics", matrix "topics-words"
    """
    docs_words_matrix = transformer.fit_transform(get_docs_words_matrix(texts)).toarray() 
    u, s, vh = np.linalg.svd(docs_words_matrix, full_matrices=False)
    return u, vh
