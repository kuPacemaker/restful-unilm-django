import pickle

class SquadTfidfVectorizer:

    src = 'preprocess/squad_tfidf_vectorizer.skl'
    instance = None

    @classmethod
    def load(cls):
        if cls.instance is None:
            cls.instance = pickle.load(open(cls.src, 'rb'))
        return cls.instance