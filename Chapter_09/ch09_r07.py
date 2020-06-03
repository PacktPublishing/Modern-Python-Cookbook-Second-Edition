"""Python Cookbook 2nd ed.

Chapter 9, recipe 7, Implementing "there exists" processing.
"""
from itertools import takewhile, dropwhile
from typing import Iterable, Iterator, TypeVar, Callable

T_ = TypeVar("T_")
Predicate = Callable[[T_], bool]


def find_first(fn: Predicate, source: Iterable[T_]) -> Iterator[T_]:
    for item in source:
        if fn(item):
            yield item
            break


import math


def prime(n: int) -> bool:
    """
    >>> p = {2, 3, 5, 7, 11, 13, 17, 19}
    >>> tests = (prime(n) == (n in p)
    ...     for n in range(2, 21)
    ... )
    >>> all(tests)
    True
    >>> prime(9973)
    True
    >>> prime(9997)
    False
    """
    factors = find_first(lambda i: n % i == 0, range(2, int(math.sqrt(n) + 1)))
    return len(list(factors)) == 0


def prime_t(n: int) -> bool:
    """
    >>> p = {2, 3, 5, 7, 11, 13, 17, 19}
    >>> tests = (prime_t(n) == (n in p)
    ...     for n in range(2, 21)
    ... )
    >>> all(tests)
    True
    >>> prime_t(9973)
    True
    >>> prime_t(9997)
    False
    """
    tests = set(range(2, int(math.sqrt(n) + 1)))
    non_factors = set(takewhile(lambda i: n % i != 0, tests))
    return tests == non_factors


def prime_any(n: int) -> bool:
    """
    >>> p = {2, 3, 5, 7, 11, 13, 17, 19}
    >>> tests = (prime_any(n) == (n in p)
    ...     for n in range(2, 21)
    ... )
    >>> all(tests)
    True
    >>> prime_any(9973)
    True
    >>> prime_any(9997)
    False

    """
    tests = range(2, int(math.sqrt(n) + 1))
    has_factors = any(n % t == 0 for t in tests)
    return not has_factors

def primeset(source: Iterable[int]) -> Iterator[int]:
    """
    >>> list(primeset(range(2, 21)))
    [2, 3, 5, 7, 11, 13, 17, 19]
    """
    for i in source:
        if prime(i):
            yield i


import random


def fermat_prime(n: int, k: int) -> int:
    """
    >>> fermat_prime(9973, 5)
    True
    >>> fermat_prime(9997, 5)
    False
    >>> random.seed(42)
    >>> for k in range(1, 5):
    ...     print(f"{k=}, {fermat_prime(96709, k)=}")
    k=1, fermat_prime(96709, k)=False
    k=2, fermat_prime(96709, k)=False
    k=3, fermat_prime(96709, k)=False
    k=4, fermat_prime(96709, k)=False
    >>> fermat_prime(9967009, k=2)
    False
    >>> fermat_prime(9999991, k=2)
    True
    """
    assert n > 3 and k >= 1
    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:  # (a**(n-1)%n) != 1:
            return False
    return True


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
