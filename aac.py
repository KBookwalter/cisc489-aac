from predictive_keyboard import PredictiveKeyboard

test_sent = "Your mother was a hamster and your father smelt of elderberries!"

def main():
    print('here')

    kb = PredictiveKeyboard()

    kb.print_keyboard()

    print('Static Time: ', kb.type_sentence_static(test_sent), 'scans')
    print('Dynamic Time: ', kb.type_sentence_dynamic(test_sent), 'scans')

if __name__ == '__main__':
    main()
