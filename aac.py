from predictive_keyboard import PredictiveKeyboard
from nltk.corpus import gutenberg, switchboard
from time import time
from tree import NgramTree
import re
import sys

def main():

    kb = PredictiveKeyboard()

    static_scans = 0
    dynamic_scans = 0
    dynamic_scans_with_word_preds = 0

    original_stdout = sys.stdout
    with open("results.txt", "w") as f:
        sys.stdout = f
        # s, d, w= run_gutenberg(kb)
        # static_scans += s
        # dynamic_scans += d
        # dynamic_scans_with_word_preds += w

        s, d, w = run_switchboard(kb)
        static_scans += s
        dynamic_scans += d
        dynamic_scans_with_word_preds += w

        s, d, w = run_overheard(kb)
        static_scans += s
        dynamic_scans += d
        dynamic_scans_with_word_preds += w

        s, d, w= run_test_file(kb)
        static_scans += s
        dynamic_scans += d
        dynamic_scans_with_word_preds += w

        dynamic_diff = (static_scans - dynamic_scans) / static_scans
        print("\n==================================================================\n")
        print("Total Difference Dynamic: ", dynamic_diff * 100, "% faster\n")

        word_pred_diff = (static_scans - dynamic_scans_with_word_preds) / static_scans
        print("\n==================================================================\n")
        print("Total Difference Dynamic with Word Predictions: ", word_pred_diff * 100, "% faster\n")
    
    sys.stdout = original_stdout


def run_gutenberg(kb):
    static_scans = 0
    dynamic_scans = 0

    gutenberg_texts = ["bible-kjv", "carroll-alice", "melville-moby_dick", "austen-sense"]

    for title in gutenberg_texts:
        data = prep_gutenberg(title)
        s, d = run_test(kb, data, title)
        static_scans += s
        dynamic_scans += d

    return static_scans, dynamic_scans

def run_switchboard(kb):
    static_scans = 0
    dynamic_scans = 0
    word_pred_scans = 0

    sb_words = prep_switchboard()
    s, d, w = run_test(kb, sb_words, "switchboard")

    static_scans += s
    dynamic_scans += d
    word_pred_scans += w

    return static_scans, dynamic_scans, word_pred_scans

def run_overheard(kb):
    static_scans = 0
    dynamic_scans = 0
    word_pred_scans = 0

    overheard = prep_overheard()
    s, d, w = run_test(kb, overheard, "overheard")

    static_scans += s
    dynamic_scans += d
    word_pred_scans += w

    return static_scans, dynamic_scans, word_pred_scans

def run_test_file(kb):
    test_file = open("testfile.txt", "r", encoding="utf-8")
    text = test_file.read()
    s,d,w = run_test(kb, text, "test file")
    return s,d,w

    

def run_test(kb, data, title):
    print("\n==================================================================\n")
    print("Typing " + title)
    time_start = time()
    static_scans = kb.type_sentence_static(data.upper())
    time_end = time()
    print("\nStatic Scans: ", static_scans)
    print("Time taken: ", time_end - time_start, "seconds")
    print("\n")
    
    time_start = time()
    dynamic_scans = kb.type_sentence_dynamic(data.upper())
    time_end = time()

    print("Dynamic Scans: ", dynamic_scans)
    print("Time taken: ", time_end - time_start, "seconds")
    print("\n")

    time_start = time()
    word_pred_scans = kb.type_sentence_dynamic_with_word_predictions(data.upper())
    time_end = time()
    print("Dynamic Scans with Word Predictions: ", word_pred_scans)
    print("Time taken: ", time_end - time_start, "seconds")
    print("\n")

    dynamic_diff = (static_scans - dynamic_scans) / static_scans
    print("Dynamic Scanning: ", dynamic_diff * 100, "% faster\n")

    word_diff = (static_scans - word_pred_scans) / static_scans
    print("Dynamic Scanning with Word Prediction: ", word_diff * 100, "% faster\n")

    return static_scans, dynamic_scans, word_pred_scans

def prep_gutenberg(title):
    text = gutenberg.raw(title + '.txt')
    text.replace("  ", " ")
    text.replace("\n", " ")
    return text.upper()

def prep_switchboard():
    words = switchboard.words()
    words_str = ""
    for word in words:
        words_str += word + " "
    return words_str

def prep_overheard():
    file = open('overheard.txt', 'r', encoding='utf-8')
    lines_raw = file.readlines()
    lines = [re.sub(r".*: ", r"", line) for line in lines_raw]

    str_text = ""
    for line in lines:
        str_text += re.sub(r'\n', '', line) + " "

    return str_text

if __name__ == '__main__':
    main()
