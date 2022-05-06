
import nltk
from nltk.corpus import nps_chat
from nltk.util import ngrams
from nltk.corpus import words as WORDS
import sys

START_SYMBOL = '<START>'
END_SYMBOL = '<END>'

def train_bigrams(training_data):
    train_unigrams(training_data)
    bigrams = {}
    prev = START_SYMBOL
    # bigrams[prev] = {}
    # doc = doc[1:]

    for char in training_data:
        if prev not in bigrams:
            bigrams[prev] = {}
        if char not in bigrams[prev]:
            bigrams[prev][char] = 0
        bigrams[prev][char] += 1
        prev = char

    # Handle end of file
    # This might have to be removed if I try to do text generation
    if prev not in bigrams:
        bigrams[prev] = {}
    bigrams[prev][END_SYMBOL] = 1

    with open("bigrams.txt", "w") as f:
        original_stdout = sys.stdout
        sys.stdout = f
        for b1 in bigrams:
            for b2 in bigrams[b1]:
                print(b1, b2, bigrams[b1][b2])
        sys.stdout = original_stdout

    return bigrams


def train_unigrams(training_data):
    unigrams = {}

    for char in training_data:
        if char not in unigrams:
            unigrams[char] = 0
        unigrams[char] += 1

    with open("unigrams.txt", "w") as f:
        original_stdout = sys.stdout
        sys.stdout = f
        for u in unigrams:
            print(u, unigrams[u])
        sys.stdout = original_stdout

    return unigrams

def dynamic_ngram_helper(data, grams, n):
    n_grams = list(ngrams(data, n))
    new_char = n_grams[-1]
    for n in n_grams:
        prev = grams
        for char in n:
            prev = prev[char]
        if new_char not in prev:
            prev[new_char] = {}
            prev[new_char]['count'] = 0
        prev[new_char]['count'] += 1


