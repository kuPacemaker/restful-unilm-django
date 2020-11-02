import nltk
from textblob import TextBlob
from .metric import SquadTfIdf

def passaginate(text, max_words, noun_sorting=False):
    psgs = psg_split(text, max_words)
    passages = list(map(Passage, psgs))
    metric = SquadTfIdf()
    vocab = metric.vocab

    if noun_sorting:
        scores = metric.transform(passages)
        for i, passage in enumerate(passages):
            passage.noun_sort(scores[i], vocab=vocab, inplace=True, reverse=True)
    return passages

class Passage:

    def __init__(self, text):
        self.text = text
        self.nouns = noun_extract(text)
    
    def noun_sort(self, score, vocab=None, inplace=True, reverse=True):
        nouns = set(self.nouns)
        if vocab is not None :
            nouns &= vocab

        noun_score = [(noun, score[noun]) for noun in nouns]
        sorted_noun_score = sorted(noun_score, key=lambda x: x[1], reverse=reverse)
        sorted_nouns = [noun for noun, score in sorted_noun_score]

        if inplace:
            self.nouns = sorted_nouns
            return None
        return sorted_nouns

def noun_extract(text):
    tokenized = nltk.word_tokenize(text)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if pos[:2]=='NN']
    noun_phrases = [phrase for phrase in TextBlob(text).noun_phrases]
    result = []
    
    for noun in nouns+noun_phrases:
        trimmed_noun = noun_trim(noun)
        if trimmed_noun != '':
            result.append(trimmed_noun)
    return result

def noun_trim(noun):
    return noun.strip("\'“”. ")

def psg_split(text, max_words):
    psgs = [p for p in text.split('\n') if p != '']
    w_counter = [1 + p.count(' ') for p in psgs]
    result_psgs = []

    for psg, n_words in zip(psgs, w_counter):
        if n_words <= max_words:
            result_psgs.append(psg)
        else:
            psg_toks = psg.split(' ')
            recursive_psg_split(psg_toks, max_words, result_psgs)
    return result_psgs

def recursive_psg_split(psg_toks, max_words, result_psgs):
    n_words = len(psg_toks)
    if n_words > max_words:
        end_pos = max_words

        for pos in range(max_words - 1, n_words):
            if len(psg_toks[pos]) > 0:
                if psg_toks[pos][-1] == '.':
                    end_pos = pos + 1
                    break
                
        trimmed_psg_toks = psg_toks[0: end_pos]
        result_psgs.append(' '.join(trimmed_psg_toks))
        
        next_psg_toks = psg_toks[end_pos: n_words]
        recursive_psg_split(next_psg_toks, max_words, result_psgs)
    elif n_words > 0:
        result_psgs.append(' '.join(psg_toks))