from tree import NgramTree
from nltk.corpus import words as WORDS
from nltk.util import ngrams
import pickle
import csv

def train_character_tree_nltk_words():
    t = NgramTree('<S>')
    all_words = [word.upper() for word in WORDS.words()]
    t.generate_ngrams_from_list(all_words)
    pickle.dump(t, open("character_ngram_tree.p", "wb"))

def train_character_tree_frequent_words():
    t = NgramTree('<S>')
    file = open('unigram_freq.csv')
    csvreader = csv.reader(file)
    header = next(csvreader)
    words = [row[0].upper() for row in csvreader]
    t.generate_ngrams_from_list(words)
    pickle.dump(t, open("character_ngram_tree.p", "wb"))


train_character_tree_frequent_words()
