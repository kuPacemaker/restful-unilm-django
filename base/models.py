from preprocess.text import passaginate
from functools import reduce
import json

# Create your models here.
class BaseKnowledge:
    
    def __init__(self, text, passage_num_words=120, vectorizer='squad'):
        text = text.replace('\n', '')
        self.passages = passaginate(text, passage_num_words, vectorizer, noun_sorting=True)
        self.nouns = list(reduce(lambda x, y: set(x) | set(y), 
                            [p.nouns for p in self.passages]))

    def all_text(self):
        return [passage.text for passage in self.passages]
        
    def attach_aqset(self, index, aqset):
        self.passages[index].aqset = aqset

    def prune_passage(self):
        for i, passage in enumerate(self.passages):
            _, _, score = passage.aqset[0]
            if i == 0 or (i > 0 and top_score < score):
                top_passage, top_score = passage, score
        self.passages = [top_passage]
        
    def prune_nouns(self):
        global_amount = self.prune_nouns_amount()
        for passage in self.passages:
            amount = min(len(passage.nouns), global_amount)
            passage.nouns = passage.nouns[:amount]
            
        self.nouns = list(reduce(lambda x, y: set(x) | set(y), 
                            [p.nouns for p in self.passages]))
    
    def prune_nouns_amount(self):
        return 3 + int(3 / len(self.passages))

    def jsonate(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, indent = 4))
