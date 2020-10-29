from collections import Counter
import math

class TfIdfLen:
    def __init__(self, word_lists):
        self.idf = dict()
        self.num_docs = max(len(word_lists), 2)
        for i, word_list in enumerate(word_lists):
            for noun in word_list:
                self.idf[noun] = i+1
    
    def fit_transform(self, word_list):
        tf = Counter(word_list)
        tfidf_score = {noun: tf_score * math.log(self.num_docs / self.idf[noun]) * math.log(len(noun)) / math.log(3.3) for noun, tf_score in tf.items()}
        return tfidf_score
