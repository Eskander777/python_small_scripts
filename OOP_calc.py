OPERS = {
    '+': '__add__',
    '-': '__sub__',
    '*': '__mul__',
    '/': '__truediv__',
}


class Calculator:
    def __init__(self, first):
        self.first = first

    def turn_to_int(self):
        self.first = int(self.first)

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


def main():
    while True:
        calc = Calculator(input('Enter first number: > '))
        if calc.first == '':
            break
        calc.turn_to_int()
        oper_str = input('Enter operator: > ')
        second_num = int(input('Enter second number: > '))
        oper = getattr(calc, OPERS.get(oper_str))
        print(f'\nThe answer is: {oper(second_num)}\n')


if __name__ == '__main__':
    main()
