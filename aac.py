from predictive_keyboard import PredictiveKeyboard
from nltk.corpus import gutenberg
from time import time
from tree import NgramTree

test_sent = "Your mother was a hamster and your father smelt of elderberries!"

def main():

    kb = PredictiveKeyboard()

    # kb.print_keyboard()


    data = prep_data()

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

    diff = (static_scans - dynamic_scans) / static_scans
    print("Difference (scans): ", diff * 100, "% faster\n")



    # print("Time per character: " (time_end - time_start) / len(test_sent), "seconds")

def prep_data():
    text = gutenberg.raw("carroll-alice.txt")
    text.replace("  ", " ")
    text.replace("\n", " ")
    return text.upper()




if __name__ == '__main__':
    main()
