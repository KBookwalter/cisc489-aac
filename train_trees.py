from tree import NgramTree
from nltk.corpus import words as WORDS
from nltk.util import ngrams
import pickle

def train_character_tree():
    t = NgramTree('<S>')
    all_words = [word.upper() for word in WORDS.words()]
    t.add_words(all_words)
    pickle.dump(t, open("character_tree.p", "wb"))

def word_tree_test():
    test_sentence = 'THE DOG WITH SPOTS RUNS FASTER THAN THE DOG WITH STRIPES'.split()
    t = NgramTree('<S>')
    fourgrams = ngrams(test_sentence, 4)
    t.add_words(fourgrams)
    children = t.children
    for c in children:
        print(c.char)
    print(t.get_ngram_count(['DOG']))

def character_tree_test():
    t = pickle.load(open("ngrams.p", "rb"))
    children = t.children
    for c in children:
        print(c.char)
    print(t.get_ngram_count('Z'))

character_tree_test()
