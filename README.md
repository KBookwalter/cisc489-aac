Final Project for CISC 489 - Intro to NLP
Kevin Bookwalter

RUNNING THE PROGRAM:

    The setup of this program is a bit confusing because I had to adjust things to get it to work
    with the perl script after I had already written most of the code. Running main() in aac.py will
    run all of my tests and put the results in results.txt.

    There are a few things that have to be checked for the perl script to run properly.
    1) Lines 22 through 32 must be commented out in aac.py. These lines run all of my
        tests and will mess up predictions.txt.
    2) Lines 93 and 98 must not be commented out in predictive_keyboard.py. These lines
        write out the predictions as they are made. They can be commented for other runs
        because I don't use the predicitons file in my own tests.

    Run main() in aac.py with the above conditions met and predictions.txt will be right.
    I submitted the assignment with these conditions met, so it should be running fine.

    Run the perl script with a static keyboard with:
        % perl GetScanTime.pl -k Keyboard.txt -t testfile.txt -r report.txt

    Run the perl script with a dynamic keyboard with:
        perl GetScanTime.pl -k Keyboard.txt -t testfile.txt -p predictions.txt -r report.txt    

FILE DESCRIPTIONS (Python/Perl Files):
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

    GetScanTime.pl:
        Perl script for checking scan times

FILE DESCRIPTIONS (Data Files):
    character_ngram_tree.p:
        Serialized character-level NgramTree

    overheard.txt:
        Data file used for static vs dynamic typing tests. Transcribed conversations
        heard on the street. Copied from NLTK corpora.

    switchboard.txt:
        Data file used for static vs dynamic typing tests. Transcribed phone conversations.
        Copied from NLTK corpora.

    all-results.txt:
        *** These are the results for running test on all testing data ***
        Results of main() in aac.py are printed into this file. Contains number of scans
        taken for static and dynamic typing, time taken, and differences between static
        and dynamic typing.

    results.txt:
        This file is rewritten to contain results whatever tests are run.

    report.txt:
        Output of perl script

    predictions.txt:
        All predictions made by the dynamic keyboard. This gets overwritten

    predicitons-copy.txt:
        A copy of the predictions for the provided test file. This doesn't get overwritten,
        and is here so that my original predcitions output doesn't get lost.
        
    testfile.txt:
        Final test file provided by Dr. McCoy.

    Keyboard.txt:
        Keyboard used for Perl script

    unigram_freq.csv:
        Ngram tree training file. Contains 333,333 most common English words

    words.txt
        Old training file. Copy of NLTK words corpus containing ~240,000 English words

    

333,333 word data set:
    https://www.kaggle.com/datasets/rtatman/english-word-frequency?resource=download