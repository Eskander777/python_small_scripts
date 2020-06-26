class Calculator:
    opers = {
        '+': '__add__',
        '-': '__sub__',
        '*': '__mul__',
        '/': '__truediv__',
        '**': '__pow__',
        '//': '__floordiv__',
        '%': '__mod__'

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

    def __pow__(self, other):
        res = self.first ** other
        return res

    def __floordiv__(self, other):
        res = self.first // other
        return res

    def __mod__(self, other):
        res = self.first % other
        return res

    def turn_to_int(self):
        self.first = int(self.first)

    def make_calculations(self):
        try:
            self.turn_to_int()
            oper_str = input('Enter operator: > ')
            if oper_str not in self.opers.keys():
                raise ValueError
            second_num = int(input('Enter second number: > '))
            oper = getattr(self, self.opers.get(oper_str))
            result = oper(second_num)
        except ZeroDivisionError:
            print("\nYou can't divide by zero. Try again!\n")
        except (TypeError, ValueError):
            print('\nWrong input. Try again!\n')
            raise
        else:
            print(f'Operation: {self.first} {oper_str} {second_num}')
            print(f'\nThe answer is: {result}\n')


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
