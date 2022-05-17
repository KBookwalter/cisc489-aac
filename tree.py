from logging import root
from nltk.util import ngrams
import copy

class NgramTree:

    def __init__(self, val):
        self.val = val
        self.count = 1
        self.children = []

    def get_child(node, val):
        for c in node.children:
            if c.val == val:
                return c
        return None

    def add_ngram(self, ngram):
        prev = self
        vals = ngram
        while len(vals) > 1:
            prev = prev.get_child(vals[0])
            vals = vals[1:]
        if prev.has_child(vals[0]):
            prev.get_child(vals[0]).count += 1
        else:
             prev.children.append(NgramTree(vals[0]))
        prev.children.sort(key=lambda n: n.count, reverse=True)
        
                
    def has_child(node, val):
        for n in node.children:
            if n.val == val:
                return True
        return False

    def get_ngram_count(self, ngram):
        prev = self
        vals = ngram
        while(len(vals) > 0):
            if prev.has_child(vals[0]):
                prev = prev.get_child(vals[0])
                vals = vals[1:]
            else:
                return 0

        return prev.count

    def generate_ngrams(self, vals, limit):
        for i in range(1, limit):
            n_grams = ngrams(vals, i)
            for n in n_grams:
                self.add_ngram(n)

    def generate_ngrams_from_list(self, vals):
        for val in vals:
            self.generate_ngrams(val, len(val) + 1)

    def get_children(self, ngram):
        if self.get_ngram_count(ngram) > 0:
            vals = ngram
            prev = self
            while len(vals) > 0:
                prev = prev.get_child(vals[0])
                vals = vals[1:]
            return prev.children
        else:
            return []


    def get_more_predictions(self, pattern, preds):
        while(len(preds) < 5):
            pattern = pattern[1:]
            new_preds = [p.val for p in self.get_children(pattern)]
            i = 5 - len(preds)
            for val in new_preds:
                if val not in preds:
                    preds.append(val)
                    i -= 1
                    if i==0:
                        break
        return preds


    def get_predictions(self, pattern):
        preds = [p.val for p in self.get_children(pattern)]
        if len(preds) >= 5:
            return preds[:5]
        else:
            return self.get_more_predictions(pattern, preds)
