from email.policy import default
import re

from torch import default_generator
from tree import NgramTree
import pickle

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
            if re.match(r'[A-Z]+', char):
                char_row, char_col = self.get_char_location(char)
                scan_time = scan_time + char_row + char_col
                self.update_prev(char)
                self.update_dynamic_row()
            elif re.match(r' ', char):
                self.reset_prev()
                self.reset_dynamic_row()


        return scan_time

    def type_sentence_static(self, sent):
        sent = list(sent)
        scan_time = 0

        for char in sent:
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
        # print(self.prev)
        self.dynamic_row = self.character_ngram_tree.get_predictions(self.prev)
