from tree import NgramTree
from nltk.corpus import words as WORDS
from nltk.corpus import brown
from nltk.corpus import wordnet2021
from nltk.corpus import switchboard
from nltk.util import ngrams
import pickle
import sys

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

def switch_board_test():
    convs = switchboard.words()
    original_stdout = sys.stdout
    with open("switchboard.txt", "w") as f:
        sys.stdout = f
        for word in convs:
            print(word)

    sys.stdout = original_stdout

def tmp_test():
    words = wordnet2021.words()
    print(len(words))



tmp_test()