from functools import lru_cache
import matplotlib.pyplot as plt


@lru_cache(maxsize=None)
def fibonacci_generator(num):
    first, second, third = 0, 1, 1
    count = 1
    while count <= num:
        yield third
        third = second + first
        first = second
        second = third
        count += 1


fib_array = []
for number in fibonacci_generator(500):
    fib_array.append(number)
print(fib_array)

plt.scatter(fib_array, range(len(fib_array)))
plt.show()
