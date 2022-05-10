from tree import NgramTree
from nltk.corpus import words as WORDS
from nltk.util import ngrams
import pickle

def train_character_tree():
    t = NgramTree('<S>')
    all_words = [word.upper() for word in WORDS.words()]
    t.generate_ngrams_from_list(all_words)
    pickle.dump(t, open("character_ngram_tree.p", "wb"))


train_character_tree()
