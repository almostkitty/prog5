import functools


##########ЗАДАНИЕ 1###########
def my_genn():
    """Сопрограмма"""

    while True:
        number_of_fib_elem = yield
        fib = [0, 1]
        for i in range(2, number_of_fib_elem):
            fib.append(fib[-1] + fib[-2])
        yield fib[:number_of_fib_elem]


def fib_coroutine(g):
    @functools.wraps(g)
    def inner(*args, **kwargs):
        gen = g(*args, **kwargs)
        gen.send(None)
        return gen
    return inner


my_genn = fib_coroutine(my_genn)
gen = my_genn()
print(gen.send(5))



##########ЗАДАНИЕ 2##########
class FibonacciLst:
    def __init__(self, lst):
        self.lst = lst
        self.idx = 0
        self.fib = [0, 1]
    

    def __iter__(self):
        return self
    

    def __next__(self):
        while self.idx < len(self.lst):
            num = self.lst[self.idx]
            self.idx += 1

            while self.fib[-1] < num:
                self.fib.append(self.fib[-1] + self.fib[-2])
            if num in self.fib:
                return num
        raise StopIteration





lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
fib_iterator = FibonacciLst(lst)
print(list(fib_iterator))
