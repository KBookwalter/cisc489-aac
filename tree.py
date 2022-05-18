from logging import root
from nltk.util import ngrams
import copy

class NgramTree:

    def __init__(self, val):
        self.val = val
        self.count = 1
        self.children = []

    """
    Gets the child node of 'node' with value 'val'
    Returns None if no such node exists
    """
    def get_child(node, val):
        for c in node.children:
            if c.val == val:
                return c
        return None

    """
    Adds an ngram to the tree. If the ngram exists, it's count is updated.
    If not, a new node is created for the ngram.
    """
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
        
    """
    Checks if a node 'node' has a child with value 'val'
    """    
    def has_child(node, val):
        for n in node.children:
            if n.val == val:
                return True
        return False

    """
    Gets the count of a given ngram.
    Traverses the tree through the characters of the ngram
    and returns count of final charcacter, which is the count of
    that entire character pattern.
    """
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

    """
    Adds all ngrams of length 1 to 'limit' in a single word 'vals'
    """
    def generate_ngrams(self, vals, limit):
        for i in range(1, limit):
            n_grams = ngrams(vals, i)
            for n in n_grams:
                self.add_ngram(n)

    """
    Adds all ngrams of any length for all words in the list 'vals'
    """
    def generate_ngrams_from_list(self, vals):
        for val in vals:
            self.generate_ngrams(val, len(val) + 1)

    """
    Returns the children of the last character in an ngram.
    These children are all the characters that follow the ngram.
    """
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

    """
    Generates more predictions. Takes a pattern and the predicitons
    it generated and fills the predictions list up to 5
    """
    def get_more_predictions(self, pattern, preds):
        while(len(preds) < 5):
            # shorten pattern by cutting off oldest character
            pattern = pattern[1:]
            # find new predicitons based on new, shorter pattern
            new_preds = [p.val for p in self.get_children(pattern)]
            i = 5 - len(preds)
            for val in new_preds:
                if val not in preds:
                    preds.append(val)
                    i -= 1
                    if i==0:
                        break
        return preds


    """
    Generates character predictions based on a pattern.
    """
    def get_predictions(self, pattern):
        preds = [p.val for p in self.get_children(pattern)]
        if len(preds) >= 5:
            # 5 most likely if 5 predictions exist
            return preds[:5]
        else:
            # Find more predictions if 5 aren't generated
            return self.get_more_predictions(pattern, preds)
