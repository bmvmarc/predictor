import regex
from random import choices


class Predictor:

    def __init__(self):
        self.string = ''
        self.triads = {bin(x)[2:].rjust(3, '0'): 0 for x in range(8)}
        self.money = 1000

    def __str__(self):
        return self.string

    def start(self):
        self.get_patterns()

        print('\nYou have $1000. Every time the system successfully predicts your next press, you lose $1.'
              'Otherwise, you earn $1. Print "enough" to leave the game. Let\'s go!\n')

        while True:
            inp = input('Print a random string containing 0 or 1:\n')
            if inp == 'enough':
                break
            else:
                inp = ''.join(x for x in inp if x in '01')
                if inp != '':
                    self.game(inp)
                    self.string += inp
                    self.count_triads()

        print('Game over!\n')

    def get_patterns(self):
        length = 0
        while length < 100:
            inp = input('Print a random string containing 0 or 1:\n\n')
            self.string += ''.join(x for x in inp if x in '01')
            length = len(self.string)
            if length < 100:
                print(f'Current data length is {length}, {100 - length} symbols left')

        print('\nFinal data string:\n' + self.string)
        self.count_triads()

    def game(self, test_string):
        numbers_to_guess = len(test_string) - 3
        predicted = ''.join(choices('01', k=3))
        for i in range(3, len(test_string)):
            predicted += self.get_next_prediction(test_string[i - 3:i])

        print(f'prediction:\n{predicted}')

        guessed = sum(1 for i in range(3, len(test_string)) if test_string[i] == predicted[i])
        pro_cent = round(guessed * 100 / numbers_to_guess, 2)

        print(f'\nComputer guessed right {guessed} out of {numbers_to_guess} symbols ({pro_cent} %)')

        self.money -= (guessed + guessed - numbers_to_guess)
        print(f'Your capital is now ${self.money}\n')

    def get_next_prediction(self, sequence):
        if self.triads[sequence][0] > self.triads[sequence][1]:
            return '0'
        elif self.triads[sequence][0] < self.triads[sequence][1]:
            return '1'
        else:
            return choices('01', k=1)[0]

    def count_triads(self):
        self.triads = {k: (len(regex.findall(k + '0', self.string, overlapped=True)),
                           len(regex.findall(k + '1', self.string, overlapped=True))) for k in self.triads}


predictor = Predictor()
predictor.start()
