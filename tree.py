from copyreg import pickle
from nltk.util import ngrams
from nltk.corpus import words as WORDS
import pickle

class NgramTree:

    def __init__(self, char):
        self.char = char
        self.count = 1
        self.children = []

    def get_child(node, char):
        for c in node.children:
            if c.char == char:
                return c
        return None

    def add_ngram(self, ngram):
        prev = self
        chars = ngram
        while len(chars) > 1:
            prev = prev.get_child(chars[0])
            chars = chars[1:]
        if prev.has_child(chars[0]):
            prev.get_child(chars[0]).count += 1
        else:
             prev.children.append(NgramTree(chars[0]))
        prev.children.sort(key=lambda n: n.count, reverse=True)
        
                
    def has_child(node, char):
        for n in node.children:
            if n.char == char:
                return True
        return False

    def get_ngram_count(self, ngram):
        prev = self
        chars = ngram
        while(len(chars) > 0):
            if prev.has_child(chars[0]):
                prev = prev.get_child(chars[0])
                chars = chars[1:]
            else:
                return 0

        return prev.count

    def add_word(self, word):
        for i in range(1, len(word) + 1):
            n_grams = ngrams(word, i)
            for n in n_grams:
                self.add_ngram(n)

    def add_words(self, words):
        for word in words:
            self.add_word(word)

    def get_children(self, ngram):
        if self.get_ngram_count(ngram) > 0:
            chars = ngram
            prev = self
            while len(chars) > 0:
                prev = prev.get_child(chars[0])
                chars = chars[1:]
            return prev.children
        else:
            return []


    def get_predictions(self, pattern):
        preds = [p.char for p in self.get_children(pattern)]
        if len(preds) >= 5:
            return preds[:5]
        else:
            i = 5 - len(preds)
            for char in ['E', 'A', 'R', 'I', 'O']:
                if char not in preds:
                    preds.append(char)
                    i -= 1
                if i == 0:
                    return preds


            



# def test():
#     t = NgramTree('<S>')
#     all_words = [word.upper() for word in WORDS.words()]
#     t.add_words(all_words[:1000])
#     print(t.get_ngram_count('A'))
#     print(t.get_ngram_count('AB'))
#     print(t.get_ngram_count('AARDVARK'))
#     children = t.get_child('A').children

#     pickle.dump(children, open("children.p", "wb"))

#     asdf = pickle.load(open("children.p", "rb"))

#     for c in asdf:
#         print(c.char, c.count)

# def test2():
#         t = NgramTree('<S>')
#         all_words = [word.upper() for word in WORDS.words()]
#         t.add_words(all_words[:1000])
#         preds = t.get_predictions('AARDVA')
#         for p in preds:
#             print(p)

# def train_ngrams():
#     t = NgramTree('<S>')
#     all_words = [word.upper() for word in WORDS.words()]
#     t.add_words(all_words)

#     pickle.dump(t, open("ngrams.p", "wb"))

# def test3():
#     t = pickle.load(open("ngrams.p", "rb"))
#     print(t.get_predictions("KEV"))
#     print(t.get_predictions("KEV"))
#     print(t.get_predictions("KEV"))
#     print(t.get_predictions("KEV"))
#     print(t.get_predictions("KEV"))
#     print(t.get_predictions("KEV"))



# test3()




    