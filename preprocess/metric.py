from collections import Counter
import math
from .pretrained import SquadTfidfVectorizer, BibleTfidfVectorizer

class SquadTfIdf:

    def __init__(self):
        self.vectorizer = SquadTfidfVectorizer.load()
        self.vocab = set(self.vectorizer.get_feature_names())

    def transform(self, docs):
        vectors = self.vectorizer.transform(docs)
        words = self.vectorizer.inverse_transform(vectors)

        tfidfs = []
        for doc_id, vector in enumerate(vectors):
            tfidf = {}
            be = vector.indptr.tolist()
            begin, end = be[0], be[1]
            for feature_id in range(begin, end):
                tfidf[words[doc_id][feature_id]] = vector.data[feature_id]
            tfidfs.append(tfidf)
        return tfidfs

class BibleTfIdf(SquadTfIdf):
    
    def __init__(self):
        self.vectorizer = BibleTfidfVectorizer.load()
        self.vocab = set(self.vectorizer.get_feature_names())

# class TfIdfLen:

#     def __init__(self, word_lists):
#         self.idf = dict()
#         self.num_docs = max(len(word_lists), 2)

#         for i, word_list in enumerate(word_lists):
#             for noun in word_list:
#                 self.idf[noun] = i+1
    
#     def fit_transform(self, word_list):
#         tf = Counter(word_list)
#         tfidf_score = {noun: tf_score * math.log(self.num_docs / self.idf[noun]) * math.log(len(noun)) / math.log(3.3) for noun, tf_score in tf.items()}
#         return tfidf_score
