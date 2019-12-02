"""Python Cookbook 2nd ed.

Chapter 8, recipe 7.
"""
from itertools import takewhile
from typing import Iterable, Iterator, TypeVar, Callable

T_ = TypeVar("T_")
Predicate = Callable[[T_], bool]


def find_first(predicate: Predicate, source: Iterable[T_]) -> Iterator[T_]:
    for item in source:
        if predicate(item):
            yield item
            break


import math


def prime(n: int) -> bool:
    """
    >>> p = [2, 3, 5, 7, 11, 13, 17, 19]
    >>> tests = (prime(n) == (n in p)
    ...     for n in range(2, 21)
    ... )
    >>> all(tests)
    True
    """
    factors = find_first(lambda i: n % i == 0, range(2, int(math.sqrt(n) + 1)))
    return len(list(factors)) == 0


def prime_t(n: int) -> bool:
    """
    >>> p = [2, 3, 5, 7, 11, 13, 17, 19]
    >>> tests = (prime_t(n) == (n in p)
    ...     for n in range(2, 21)
    ... )
    >>> all(tests)
    True
    """
    tests = set(range(2, int(math.sqrt(n) + 1)))
    non_factors = set(takewhile(lambda i: n % i != 0, tests))
    return tests == non_factors
