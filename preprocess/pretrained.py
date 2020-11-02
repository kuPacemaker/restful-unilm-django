import pickle

class SquadTfidfVectorizer:

    src = 'preprocess/squad_tfidf_vectorizer.skl'
    instance = None

    @classmethod
    def load(cls):
        if cls.instance is None:
            with open(cls.src, 'rb') as f:
                cls.instance = pickle.loads(f)
        return cls.instance