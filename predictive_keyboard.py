import re
from nltk.corpus import words as WORDS
from tree import NgramTree

class PredictiveKeyboard:

    def __init__(self):
        self.static_keyboard = [ [' ', '.', ',', '?', '!', ';', ':', '-', '"'],
                            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '$'],
                            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '*', '(', ')'],
                            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
                            ['&', '@', '\'', '%', '/', '[', ']', '{', '}', '#'] ]

        # first letters of 5 most frequent English words with unique first characters
        # 'the', 'be', 'of', 'and', 'in'
        self.dynamic_row = ['T', 'B', 'O', 'A', 'I']

        # use this for starting a new word
        self.default_row = ['T', 'B', 'O', 'A', 'I']

        # temporary work around for when no predictions can be made, just use 5 most frequent letters
        self.most_frequent = ['E', 'A', 'R', 'I', 'O']

        self.all_words = [word.upper() for word in WORDS.words()]
        self.possible_words = self.all_words

        self.prev = ''


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

        # i = 0
        # length = len(sent)
        for char in sent:
            # i += 1
            # if(i % 1000 == 0):
            #     print(i, '/', length)
            char = char.upper()
            if re.match(r'[A-Z]+', char):
                char_row, char_col = self.get_char_location(char)
                scan_time = scan_time + char_row + char_col
                self.update_prev(char)
                self.update_possible_words()
                self.update_dynamic_row()
            elif re.match(r' ', char):
                self.reset_prev()
                self.reset_dynamic_row()
                self.reset_words()


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

    def reset_words(self):
        self.possible_words = self.all_words

    def update_possible_words(self):
        pattern = r'\b' + self.prev + r'.+'
        new_words = [word for word in self.possible_words if re.match(pattern, word)]
        self.possible_words = new_words

    def update_dynamic_row(self):
        # print(self.prev)
        next = {}
        self.dynamic_row = []
        for word in self.possible_words:
            next_char = word[len(self.prev)]
            if next_char not in next:
                next[next_char] = 0
            next[next_char] += 1

        top5 = sorted(next.items(), key=lambda x: x[1], reverse=True)[:5]
        
        for k,v in top5:
            self.dynamic_row.append(k)

        # if dynamic row is not full, fill it with most frequent English characters
        if len(self.dynamic_row) < 5:
            i = 5 - len(self.dynamic_row)
            for char in self.most_frequent:
                if char not in self.dynamic_row:
                    self.dynamic_row.append(char)
                    i -= 1
                if i == 0:
                    break


    
        

    # def update_prev(self, char):
    #     if char.isalpha():
    #         self.prev = char
    
    # def update_dynamic_row(self):
    #     # d.items(), key=lambda x: x[1], reverse=True
    #     top5 = sorted(self.bigrams[self.prev].items(), key=lambda x: x[1])[:5]
    #     # print(top5)
    #     self.dynamic_row = []
    #     for k,v in top5:
    #         self.dynamic_row.append(k)
    #     print(self.dynamic_row)
