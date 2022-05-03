from predictive_keyboard import PredictiveKeyboard
from nltk.corpus import gutenberg
from time import time

test_sent = "Your mother was a hamster and your father smelt of elderberries!"

def main():

    kb = PredictiveKeyboard()

    # kb.print_keyboard()


    moby = prep_data()

    data = moby

    static_scans = kb.type_sentence_static(data.upper())
    print("Static Scans: ", static_scans)
    
    time_start = time()
    dynamic_scans = kb.type_sentence_dynamic(data.upper())
    time_end = time()

    print("Dynamic Scans: ", dynamic_scans)

    diff = (static_scans - dynamic_scans) / static_scans

    print("Difference: ", diff * 100, "% faster")

    print("Time taken: ", time_end - time_start)

    # print("Time per character: " (time_end - time_start) / len(test_sent), "seconds")

def prep_data():
    moby = gutenberg.raw("melville-moby_dick.txt")[:1000]
    moby.replace("  ", " ")
    moby.replace("\n", " ")
    return moby.upper()




if __name__ == '__main__':
    main()
