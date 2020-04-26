"""Python Cookbook 2nd ed.

Chapter 11, recipes 1 and 2, Using docstrings for testing and
Testing functions that raise exceptions
"""

from math import factorial
from typing import List, Tuple


def binom(n: int, k: int) -> int:
    """
    Computes the binomial coefficient.
    This shows how many combinations of
    *n* things taken in groups of size *k*.

    :param n: size of the universe
    :param k: size of each subset

    :returns: the number of combinations

    >>> binom(52, 5)
    2598960
    >>> binom(52, 0)
    1
    >>> binom(52, 52)
    1
    """
    return factorial(n) // (factorial(k) * factorial(n - k))


test_GIVEN_n_5_k_52_THEN_ValueError = """
GIVEN n=5, k=52 WHEN binom(n, k) THEN exception
>>> binom(5, 52)  # doctest: +IGNORE_EXCEPTION_DETAIL 
Traceback (most recent call last):
  File "/Users/slott/miniconda3/envs/cookbook/lib/python3.8/doctest.py", line 1328, in __run
    compileflags, 1), test.globs)
  File "<doctest __main__.__test__.GIVEN_binom_WHEN_wrong_relationship_THEN_error[0]>", line 1, in <module>
    binom(5, 52)
  File "/Users/slott/Documents/Python/Python Cookbook 2e/Code/ch11_r01.py", line 24, in binom
    return factorial(n) // (factorial(k) * factorial(n-k))
ValueError: factorial() not defined for negative values
"""

test_GIVEN_negative_THEN_ValueError = """
GIVEN n=52, k=-5 WHEN binom(n, k) THEN exception
>>> binom(52, -5)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
ValueError: factorial() not defined for negative values
"""

test_GIVEN_str_THEN_TypeError = """
GIVEN n='a', k='b' WHEN binom(n, k) THEN exception
>>> binom('a', 'b')  # doctest: +IGNORE_EXCEPTION_DETAIL 
Traceback (most recent call last):
  File "/Users/slott/miniconda3/envs/cookbook/lib/python3.8/doctest.py", line 1328, in __run
    exec(compile(example.source, filename, "single",
  File "<doctest ch11_r01.__test__.GIVEN n='a', k='b' WHEN binom(n, k) THEN exception[0]>", line 1, in <module>
    binom('a', 'b')
  File "Chapter_11.ch11_r01.py", line 24, in binom
    return factorial(n) // (factorial(k) * factorial(n-k))
TypeError: 'str' object cannot be interpreted as an integer
"""

import collections
from statistics import median
from typing import Counter


class Summary:
    """
    Computes summary statistics.

    >>> s = Summary()
    >>> s.add(8)
    >>> s.add(9)
    >>> s.add(9)
    >>> round(s.mean, 2)
    8.67
    >>> s.median
    9
    >>> print(str(s))
    mean = 8.67
    median = 9
    """

    def __init__(self) -> None:
        self.counts: Counter[int] = collections.Counter()

    def __str__(self) -> str:
        return f"mean = {self.mean:.2f}\nmedian = {self.median:d}"

    def add(self, value: int) -> None:
        """
        Adds a value to be summarized.

        :param value: Adds a new value to the collection.
        """
        self.counts[value] += 1

    @property
    def mean(self) -> float:
        """
        Returns the mean of the collection.
        """
        s0 = sum(f for v, f in self.counts.items())
        s1 = sum(v * f for v, f in self.counts.items())
        return s1 / s0

    @property
    def median(self) -> float:
        """
        Returns the median of the collection.
        """
        return median(self.counts.elements())

    @property
    def count(self) -> int:
        s0 = sum(f for v, f in self.counts.items())
        return s0

    @property
    def mode(self) -> List[Tuple[int, int]]:
        """Returns the items in the collection in decreasing
        order by frequency.
        """
        return self.counts.most_common()


__test__ = {
    n: v
    for n, v in locals().items()
    if n.startswith("test_")
}
