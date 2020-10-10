from django.db import models
from textblob import TextBlob
import time, math, json
import nltk
from .qgcall import call_qg_interface

# Create your models here.
class BaseKnowledge:
    
    def __init__(self, text):
        self.passages = list(map(Passage, self.passginate(text)))
        for p in self.passages:
            p.noun_sort(self.passages)
        
    def passginate(self, text, wc_limit=412):
        psgs = []
        raw_psgs = [p for p in text.split('\n') if p != '']
        word_count = [1 + p.count(' ') for p in raw_psgs]
        
        for psg, wc in zip(raw_psgs, word_count):
            if wc <= wc_limit:
                psgs.append(psg)
            else:
                long_psg_toks = psg.split(' ')
                self.passaginate_recur(long_psg_toks, wc_limit, psgs)
        return psgs
                
    def passaginate_recur(self, long_psg_toks, wc_limit, psgs):
        wc = len(long_psg_toks)
        if wc > wc_limit:

            end_pos = wc_limit
            for pos in range(wc_limit - 1, wc):
                if long_psg_toks[pos][-1] == '.':
                    end_pos = pos + 1
                    break
                    
            trimmed_psg_toks = long_psg_toks[0: end_pos]
            psgs.append(' '.join(trimmed_psg_toks))
            
            next_psg_toks = long_psg_toks[end_pos: wc]
            self.passaginate_recur(next_psg_toks, wc_limit, psgs)
        else:
            psgs.append(' '.join(long_psg_toks))
        
    def attach_question(self):
        for passage in self.passages:
            print(passage.attach_question())
            
    def jsonate(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, indent = 4))
        
class Passage:
    
    def __init__(self, text):
        self.text = text
        self.nouns = self._noun_extract(text)
        self.aqset = list()
        
    def _noun_extract(self, text):
        tokenized = nltk.word_tokenize(text)
        nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if pos[:2]=='NN']
        noun_phrases = TextBlob(text).noun_phrases
        return nouns + noun_phrases
    
    def noun_sort(self, passages):
        sorted_nouns = sorted(self.noun_tfidf(passages), key=lambda item: item[1], reverse=True)
        self.nouns = [item[0] for item in sorted_nouns]       

    def noun_tfidf(self, passages):
        noun_set = set(self.nouns)
        tf = [self.nouns.count(noun) for noun in noun_set]
        idf = [sum([noun in p.nouns for p in passages]) for noun in noun_set]
        tfidf = [tf*math.log(len(passages)/idf) for tf, idf in zip(tf, idf)]
        
        return zip(noun_set, tfidf)
    
    def attach_question(self):
        request, answers = self.qg_query_formatted(6)
        questions = call_qg_interface(request)
        print(questions)
        
        self.aqset = list(zip(answers, questions))
        return True
    
    def qg_query_formatted(self, limit=5):
        answer_limit = min(limit, len(self.nouns))
        answer_send = [answer for num, answer in enumerate(self.nouns) if num < answer_limit]
        paset = "".join([self._seperated(self.text, answer) for answer in answer_send])
        return paset + '*', answer_send
    
    def _seperated(self, msg1, msg2):
        return "{} [SEP] {}\n".format(msg1, msg2)
    
    def jsonate(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent = 4)
