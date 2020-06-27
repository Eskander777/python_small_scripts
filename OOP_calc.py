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

    def __init__(self):
        # self.first = input('Enter first number (press "Enter" to exit): > ')
        self.expr = input(
            'Enter operation you want to perform (example: "2 + 2" / press "ENTER" to quit): > ')
        separ_array = []
        separ = ''
        if self.expr != '':
            for sym in self.expr:
                if sym in self.opers.keys():
                    separ_array.append(sym)
            separ = separ.join(separ_array)
            if separ in self.opers.keys():
                operation_tuple = self.expr.partition(separ)
                self.first, self.oper_str, self.second = operation_tuple

    def __add__(self):
        res = self.first + self.second
        return res

    def __sub__(self):
        res = self.first - self.second
        return res

    def __mul__(self):
        res = self.first * self.second
        return res

    def __truediv__(self):
        res = self.first / self.second
        return res

    def __pow__(self):
        res = self.first ** self.second
        return res

    def __floordiv__(self):
        res = self.first // self.second
        return res

    def __mod__(self):
        res = self.first % self.second
        return res

    def turn_to_num(self):
        self.first = float(self.first)
        self.second = float(self.second)

    def make_calculations(self):
        try:
            self.turn_to_num()
            # oper_str = input('Enter operator: > ')
            if self.oper_str not in self.opers.keys():
                raise ValueError
            # second_num = float(input('Enter second number: > '))
            oper = getattr(self, self.opers.get(self.oper_str))
            result = oper()
        except ZeroDivisionError:
            print("\nYou can't divide by zero. Try again!\n")
        except AttributeError:
            print('\nWrong input. Try again!\n')
        except (TypeError, ValueError):
            print('\nWrong input. Try again!\n')
        else:
            print(f'Operation: {self.first} {self.oper_str} {self.second}')
            print(f'\nThe answer is: {result}\n')


def main():
    while True:
        calc = Calculator()
        if calc.expr == '':
            break
        try:
            calc.make_calculations()
        except ValueError:
            continue


if __name__ == '__main__':
    main()
