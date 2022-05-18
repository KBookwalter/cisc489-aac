from email.policy import default
import re

from torch import default_generator
from tree import NgramTree
import pickle
import csv

class PredictiveKeyboard:

    def __init__(self):
        self.static_keyboard = [ [' ', '.', ',', '?', '!', ';', ':', '-', '"'],
                            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '$'],
                            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '*', '(', ')'],
                            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
                            ['&', '@', '\'', '%', '/', '[', ']', '{', '}', '#'] ]


        # use this for starting a new word
        # first letters of 5 most common words with unique starting characters
        self.default_row = ['T', 'B', 'O', 'A', 'I']
        
        self.dynamic_row = self.default_row

        self.prev = ''

        self.character_ngram_tree = pickle.load(open("character_ngram_tree.p", "rb"))

        self.word_ranks = self.init_word_ranks()

        self.word_predictions_default = ['THE', 'OF', 'AND', 'TO', 'A']

        self.word_predictions_row = self.word_predictions_default

    def init_word_ranks(self):
        file = open('unigram_freq.csv')
        csvreader = csv.reader(file)
        header = next(csvreader)
        word_ranks = {}
        for row in csvreader:
            word_ranks[row[0]] = row[1]
        return word_ranks


    def print_keyboard(self):
        print(self.dynamic_row)
        for row in self.static_keyboard:
            print(row)


    # add to this method a way to handle characters not in keyboard
    def get_static_char_location(self, char):
        found = False
        char = char.upper()
        char_row = 0
        char_col = 0
        i = -1

        for row in self.static_keyboard:
            i += 1
            if char in row:
                char_row = i
                found = True

        # Output index if the character exists on the keyboard
        if found:
            char_col = self.static_keyboard[char_row].index(char)

            # Add 1 since list index from 0 but we want indexing from 1 for time calculation
            return char_row + 1, char_col + 1

        # Ignore characters that don't exist on the keyboard
        else:
            return 0, 0

    def get_char_location(self, char):
        in_dynamic = False
        char = char.upper()
        char_row = 0
        char_col = 0

        if char in self.dynamic_row:
            char_row = 1
            char_col = self.dynamic_row.index(char) + 1
            in_dynamic = True
        else:
            char_row, char_col= self.get_static_char_location(char)
        
        if(in_dynamic):
            return char_row, char_col
        elif char_row != 0 and char_col != 0:
            # add 1 to account for dynamic row
            char_row += 1

        # returns 0, 0 if the character wasn't in dynamic row and
        # return from get_static_char_location indicates the
        # character isn't in the keyboard
        return char_row, char_col

    def type_sentence_dynamic(self, sent):
        sent = list(sent)
        scan_time = 0

        for char in sent:
            char = char.upper()
            char_row, char_col = self.get_char_location(char)
            scan_time = scan_time + char_row + char_col
            if re.match(r'[A-Z]+', char):
                self.update_prev(char)
                self.update_dynamic_row()
            elif re.match(r' ', char):
                self.reset_prev()
                self.reset_dynamic_row()

        return scan_time

    def type_sentence_dynamic_with_word_predictions(self, sent):
        sent_original = sent
        words = sent.upper().split(" ")
        next_word = words[0]
        sent = list(sent.upper())
        scan_time = 0
        i = 0

        while i < len(sent):
            char = sent[i]

            if next_word in self.word_predictions_row:
                row = 7
                col = self.word_predictions_row.index(next_word) + 1
                scan_time += row + col
                self.reset_prev()
                self.reset_dynamic_row()
                self.reset_word_predictions
                words = words[1:]
                next_word = words[0]
                i = sent_original.index(next_word, i) - 1      
            else:
                char = char.upper()
                char_row, char_col = self.get_char_location(char)
                # char_row += 1 # account for extra row at top
                scan_time = scan_time + char_row + char_col
                if re.match(r'[A-Z]+', char):
                    self.update_prev(char)
                    self.update_dynamic_row()
                    self.update_word_predictions
                elif re.match(r' ', char):
                    self.reset_prev()
                    self.reset_dynamic_row()
                    self.reset_word_predictions
                    words = words[1:]
                    next_word = words[0]

            i += 1

        return scan_time


    def type_sentence_static(self, sent):
        sent = list(sent)
        scan_time = 0

        for char in sent:
            char = char.upper()
            char_row, char_col = self.get_static_char_location(char)
            scan_time = scan_time + char_row + char_col

        return scan_time

    def update_prev(self, char):
        self.prev = self.prev + char

    def reset_prev(self):
        self.prev = ''

    def reset_dynamic_row(self):
        self.dynamic_row = self.default_row

    def update_dynamic_row(self):
        self.dynamic_row = self.character_ngram_tree.get_predictions(self.prev)

    def reset_word_predictions(self):
        self.word_predictions_row = self.word_predictions_default

    def get_more_word_predictions(self, preds):
        i = 5 - len(preds)
        for word in self.word_predictions_default:
            if word not in preds:
                preds.append(word)
                i -= 1
                if i== 0:
                    break

        return preds


    def update_word_predictions(self):
        if self.character_ngram_tree.get_ngram_count(self.prev) > 0:
            all_preds = self.character_ngram_tree.get_word_predictions(self.prev)
            sorted_pred_ranks = [(word, self.word_ranks[word]) for word in all_preds].sort(key = lambda x: x[1])
            if len(sorted_pred_ranks >= 5):
                new_preds = [pred[1] for pred in sorted_pred_ranks[:5]]
            else:
                new_preds = [pred[1] for pred in sorted_pred_ranks]
                new_preds = self.get_more_word_predictions(new_preds)
        else:
            new_preds = self.word_predictions_default

        self.word_predictions_row = new_preds
        return new_preds