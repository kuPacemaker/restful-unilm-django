class TfIdf:
    from collections import Counter
    
    def __init__(self, word_lists):
        self.idf = dict()
        self.num_docs = len(word_lists)
        for i, word_list in enumerate(word_lists):
            for noun in word_list:
                self.idf[noun] = i+1
    
    def fit_transform(self, word_list):
        tf = Counter(word_list)
        tfidf_score = {noun: tf_score * math.log(self.num_docs / self.idf[noun]) for noun, tf_score in tf.items()}
        return tfidf_score