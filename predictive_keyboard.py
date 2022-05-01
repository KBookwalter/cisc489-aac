
class PredictiveKeyboard():

    static_keyboard = [ [' ', '.', ',', '?', '!', ';', ':', '-', '"'],
                        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '$'],
                        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '*', '(', ')'],
                        ['&', '@', '\'', '%', '/', '[', ']', '{', '}', '#'] ]

    # starts as 5 most frequent letters
    dynamic_row = ['E', 'A', 'R', 'I', 'O']

    def print_keyboard(self):
        print(self.dynamic_row)
        for row in self.static_keyboard:
            print(row)


    # add to this method a way to handle characters not in keyboard
    def get_static_char_location(self, char):
        char = char.upper()
        char_row = 0
        char_col = 0
        i = -1

        for row in self.static_keyboard:
            i += 1
            if char in row:
                char_row = i

        char_col = self.static_keyboard[char_row].index(char)

        # Add 1 since list index from 0 but we want indexing from 1 for time calculation
        return char_row + 1, char_col + 1

    def get_char_location(self, char):
        char = char.upper()
        char_row = 0
        char_col = 0

        if char in self.dynamic_row:
            char_row = 1
            char_col = self.dynamic_row.index(char) + 1
        else:
            char_row, char_col= self.get_static_char_location(char)
            # add 1 to account for dynamic row
            char_row += 1

        return char_row, char_col

    def type_sentence_dynamic(self, sent):
        sent = list(sent)
        scan_time = 0

        for char in sent:
            char_row, char_col = self.get_char_location(char)
            scan_time = scan_time + char_row + char_col

        return scan_time

    def type_sentence_static(self, sent):
        sent = list(sent)
        scan_time = 0

        for char in sent:
            char_row, char_col = self.get_static_char_location(char)
            scan_time = scan_time + char_row + char_col

        return scan_time
