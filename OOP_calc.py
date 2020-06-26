class Calculator:
    opers = {
        '+': '__add__',
        '-': '__sub__',
        '*': '__mul__',
        '/': '__truediv__',
    }

    def __init__(self, first):
        self.first = first

    def __add__(self, other):
        res = self.first + other
        return res

    def __sub__(self, other):
        res = self.first - other
        return res

    def __mul__(self, other):
        res = self.first * other
        return res

    def __truediv__(self, other):
        res = self.first / other
        return res

    def turn_to_int(self):
        self.first = int(self.first)

    def make_calculations(self):
        while True:
            try:
                self.turn_to_int()
                oper_str = input('Enter operator: > ')
                if oper_str not in self.opers.keys():
                    raise ValueError
                second_num = int(input('Enter second number: > '))
                oper = getattr(self, self.opers.get(oper_str))
            except (TypeError, ValueError):
                print('\nWrong input. Try again!\n')
                raise
            else:
                print(f'\nThe answer is: {oper(second_num)}\n')
                break


def main():
    while True:
        calc = Calculator(
            input('Enter first number (press "Enter" to exit): > '))
        if calc.first == '':
            break
        try:
            calc.make_calculations()
        except ValueError:
            continue


if __name__ == '__main__':
    main()
