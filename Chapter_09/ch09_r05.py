"""Python Cookbook 2nd ed.

Chapter 9, recipe 5, Summarizing a collection – how to reduce.
"""
from typing import Iterable


from functools import reduce


def mul(a: int, b: int) -> int:
    return a * b


def prod(values: Iterable[int]) -> int:
    """
    >>> prod(range(1, 5+1))
    120
    """
    return reduce(mul, values, 1)


def factorial(n: int) -> int:
    """
    >>> factorial(52)
    80658175170943878571660636856403766975289505440883277824000000000000
    """
    return prod(range(1, n + 1))


test_factorial = """
>>> factorial(52)//(factorial(5)*factorial(52-5))
2598960
"""

from typing import Callable

l_add: Callable[[int, int], int] = lambda a, b: a + b
l_mul: Callable[[int, int], int] = lambda a, b: a * b

# Or use
# from operator import add, mul


def prod2(values: Iterable[int]) -> int:
    """
    >>> prod2(range(1, 5+1))
    120
    """
    return reduce(l_mul, values, 1)


def prod3(values: Iterable[int]) -> int:
    """
    >>> prod3(range(1, 5+1))
    120
    """
    return reduce(lambda a, b: a * b, values, 1)


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
