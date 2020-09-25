from django.db import models
from textblob import TextBlob
import time, math, json
import nltk
from .qgcall import call_qg_interface

# Create your models here.
class BaseKnowledge:
    
    def __init__(self, text):
        self.passages = list(map(Passage, self._passaginate(text)))
        for p in self.passages:
            p.noun_sort(self.passages)
        
    def _passaginate(self, text, wcount_limit=412):
        raw_psgs = text.split("\n")
        new_psgs = []
        
        for psg in raw_psgs:
            psg_wcount = len(nltk.word_tokenize(psg))
            
            if psg_wcount > wcount_limit:
                psg_tmp = ""
                psg_tmp_wcount = 0
                
                for sent in nltk.sent_tokenize(psg):
                    sent_wcount = len(nltk.word_tokenize(sent))
                    if psg_tmp_wcount + sent_wcount <= wcount_limit:
                        psg_tmp += sent
                        psg_tmp_wcount += sent_wcount
                    else:
                        new_psgs.append(psg_tmp)
                        psg_tmp_wcount = 0
                        psg_tmp = sent
                        
                if psg_tmp != "":
                    new_psgs.append(psg_tmp)
            else:
                if psg != "":
                    new_psgs.append(psg)
        return new_psgs
        
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
        noun_set = set(self.nouns)
        
        tf = list(map(self.nouns.count, noun_set))
        idf = [sum(map(lambda p: noun in p.nouns, passages)) for noun in noun_set]
        tfidf = list(map(lambda i: tf[i]*math.log(len(passages)/idf[i]), range(0, len(noun_set))))

        nouns_with_tfidf = zip(noun_set, tfidf)
        sorted_nouns = sorted(nouns_with_tfidf, key=lambda item: item[1], reverse=True)
        self.nouns = list(map(lambda item: item[0], sorted_nouns))
        
        #print(self.nouns)
    
    def attach_question(self):
        request, answers = self.qg_query_formatted(6)
        questions = call_qg_interface(request)
        print(questions)
        
        self.aqset = list(zip(answers, questions))
        return True
    
    def qg_query_formatted(self, limit=5):
        answer_limit = min(limit, len(self.nouns))
        answer_send = [answer for num, answer in enumerate(self.nouns) if num < answer_limit]
        return "".join([self._seperated(self.text, answer) for answer in answer_send]), answer_send
    
    def _seperated(self, msg1, msg2):
        return "{} [SEP] {}\n".format(msg1, msg2)
    
    def jsonate(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent = 4)