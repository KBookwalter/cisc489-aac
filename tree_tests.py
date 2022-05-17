from tree import NgramTree
from nltk.corpus import words as WORDS
from nltk.corpus import brown
from nltk.corpus import wordnet2021
from nltk.corpus import switchboard
from nltk.util import ngrams
import pickle
import sys
import copy
import csv

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

def word_predictions_test():
    t = NgramTree('<S>')
    t.generate_ngrams_from_list(['CAR', 'CAT', 'CAB', 'COLD', 'COLORFUL', 'COD', 'COLOR'])
    print(t.get_word_predictions('CO'))

def word_predictions_test2():
    t = pickle.load(open("character_ngram_tree.p", "rb"))
    print("HORSE" in t.get_word_predictions("HORS"))

def word_list_test():
    file = open('unigram_freq.csv')
    csvreader = csv.reader(file)
    header = next(csvreader)
    word_ranks = {}
    for row in csvreader:
        word_ranks[row[0]] = row[1]

    print(len(word_ranks))

word_predictions_test2()