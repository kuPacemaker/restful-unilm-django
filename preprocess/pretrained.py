import pickle

class SquadTfidfVectorizer:

    src = 'preprocess/squad_tfidf_vectorizer.skl'
    instance = None

    @classmethod
    def load(cls):
        if cls.instance is None:
            with open(cls.src, 'rb') as f:
                cls.instance = pickle.load(f)
        return cls.instance

class BibleTfidfVectorizer:

    src = 'preprocess/bible_tfidf_vectorizer.skl'
    instance = None

    @classmethod
    def load(cls):
        if cls.instance is None:
            with open(cls.src, 'rb') as f:
                cls.instance = pickle.load(f)
        return cls.instance
