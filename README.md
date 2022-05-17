Final Project for CISC 489 - Intro to NLP
Kevin Bookwalter

FILE DESCRIPTIONS (Python Files):
    aac.py:
        This is the main script. Running main() will type a few different documents on a static
        keyboard and a dynamic keyboard and compare how many scans are taken. Outputs are described
        below under OUTPUTS.

    predictive_keyboard.py:
        Contains the PredictiveKeyboard class. This contains the data and methods used for
        typing. Contains methods for static and dynamic typing.

    train_trees.py:
        Script for training ngram trees. Run the entire script or run individual
        methods with a python interpreter, depending on which trees need to be
        trained. Serializes trees with the pickle library so that they don't have
        to be re-trained between runs.

    tree_tests.py:
        This file is full of tests I used during development. None of them
        are necessary anymore.

    tree.py:
        Contains the NgramTree class. NgramTree is an implementation of a tree
        that contains ngram frequencies of every ngram of every length that occurs in a
        set of training data. For example, training on the word "python" stores the
        frequencies of every 1 through 6-gram that occurs in the word.

        A few useful methods:
            get_predictions(self, pattern):
                Predicts next characters based on a pattern of previous characters

            generate_ngrams(self, vals, limit):
                Generates all 1 to n-grams where n = limit for a
                single word

            generate_ngrams_from_list(self, vals):
                Generates all n-grams of all lengths for each
                word in vals

            gen_ngram_count(self, ngram):
                Gets the frequency of an ngram

FILE DESCRIPTIONS (Data Files):
    character_ngram_tree.p:
        Serialized character-level NgramTree

    first1000.txt:
        First 1000 words of NLTK's words corpus. Used for some development tests.

    overheard.txt:
        Data file used for static vs dynamic typing tests. Transcribed conversations
        heard on the street. Copied from NLTK corpora.

    results.txt:
        Results of main() in aac.py are printed into this file. Contains number of scans
        taken for static and dynamic typing, time taken, and differences between static
        and dynamic typing.

    testfile.txt:
        Final test file provided by Dr. McCoy.

OUTPUTS:
    

333,333 word data set:
    https://www.kaggle.com/datasets/rtatman/english-word-frequency?resource=download