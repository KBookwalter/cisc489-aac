import nltk
from nltk.corpus import nps_chat
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

# words = [word.upper() for word in WORDS.words()]

# with open('words.txt', 'w') as f:
#     original_stdout = sys.stdout
#     sys.stdout = f
#     for w in words:
#         print(w)
#     sys.stdout = original_stdout

#     for i in range(10):
#         print(words[i])

