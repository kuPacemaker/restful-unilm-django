from preprocess.text import passaginate

# Create your models here.
class BaseKnowledge:
    
    def __init__(self, text):
        self.passages = passaginate(text, noun_sorting=True)
        
    def attach_aqset(self, index, aqset):
        self.passages[index].aqset = aqset

    def jsonate(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, indent = 4))