from tree import NgramTree
from nltk.corpus import words as WORDS
from nltk.util import ngrams
import pickle

def predictions_test():
    words = ['ABCD', 'ABCE', 'BCD', 'BCD', 'BCF', 'BCG', 'CH']
    t = NgramTree('<S>')
    t.add_words(words)
    print(t.get_predictions('ABC'))

predictions_test()
