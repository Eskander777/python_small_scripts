class Calculator:
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
