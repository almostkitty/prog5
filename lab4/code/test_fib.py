import pytest
from main import my_genn


def test_fib_1():
    gen = my_genn()
    assert gen.send(3) == [0, 1, 1], "Тривиальный случай n = 3, список [0, 1, 1]"


def test_fib_2():
    gen = my_genn()
    assert gen.send(5) == [0, 1, 1, 2, 3], "Пять первых членов ряда"


def test_fib_3():
    gen = my_genn()
    assert gen.send(9) == [0, 1, 1, 2, 3, 5, 8, 13, 21], "Девять первых членов ряда"


def test_fib_uno():
    gen = my_genn()
    assert gen.send(1) == [0], "Для одного элемента ряда"


def test_fib_zero():
    gen = my_genn()
    assert gen.send(0) == [], "Для отсутствия элементов"
