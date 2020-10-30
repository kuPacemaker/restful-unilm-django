from preprocess.text import passaginate
from functools import reduce
import json

# Create your models here.
class BaseKnowledge:
    
    def __init__(self, text, passage_num_words=120):
        text = text.replace('\n', '')
        self.passages = passaginate(text, noun_sorting=True, max_words=passage_num_words)
        self.nouns = list(reduce(lambda x, y: set(x) | set(y), 
                            [p.nouns for p in self.passages]))

    def all_text(self):
        return [passage.text for passage in self.passages]
        
    def attach_aqset(self, index, aqset):
        self.passages[index].aqset = aqset

    def jsonate(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, indent = 4))
