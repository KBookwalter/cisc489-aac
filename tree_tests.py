from tree import NgramTree
from nltk.corpus import words as WORDS
from nltk.util import ngrams
import pickle

def predictions_test():
    words = ['ABCD', 'ABCE', 'BCD', 'BCD', 'BCF', 'BCG', 'CH']
    t = NgramTree('<S>')
    t.add_words(words)
    print(t.get_predictions('ABC'))

def word_tree_test():
    sent = "YOUR MOTHER WAS A HAMSTER AND YOUR FATHER SMELT OF ELDERBERRIES".split()
    t = NgramTree('<S>')
    t.add_word(sent, 4)
    print(t.get_ngram_count(['YOUR', 'HAMSTER']))

def ngram_length_test():
    t = pickle.load(open("character_ngram_tree.p", "rb"))
    print(t.get_ngram_count("AARDVARK"))

ngram_length_test()
