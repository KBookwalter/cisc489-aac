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


    def get_pattern_last_node(self, pattern):
        prev = self
        while(len(pattern) > 0):
            if prev.has_child(pattern[0]):
                prev = prev.get_child(pattern[0])
                pattern = pattern[1:]
            else:
                return None
        return prev

    def get_word_predictions_helper(self, root, pattern, preds):
        if root.children == []:
            preds.append(pattern)
        else:
            while root.count > 0 and root.children != []:
                trim = False
                trim_parent = None
                trim_node = None
                prev = root
                next = root.children[0]
                pred = pattern + next.val
                root.count -= 1
                while next.children != []:
                    next.count -= 1
                    if(next.count == 0 and trim == False):
                        trim = True
                        trim_parent  = prev
                        trim_node = next
                    prev = next
                    next = next.children[0]
                    pred += next.val
                preds.append(pred)
                prev.children.remove(next)   
                if trim is True:
                    trim_parent.children.remove(trim_node)
                    trim_parent = None
                    trim_node = None
                    trim = False   

        return preds

    def get_word_predictions(self, pattern):
        root_node = copy.deepcopy(self.get_pattern_last_node(pattern))
        preds = []
        # for c in root_node.children:
        #     preds += self.get_word_predictions_helper(c, pattern + c.val, [])
        preds += self.get_word_predictions_helper(root_node, pattern, [])
        
        return preds
