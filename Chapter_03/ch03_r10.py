"""Python Cookbook 2nd ed.

Chapter 3, Recipe 10, Designing recursive functions around Python's stack limits
"""

import timeit
import doctest
from typing import Iterable, Iterator


def prod(int_iter: Iterable[int]) -> int:
    p = 1
    for i in int_iter:
        p *= i
    return p


def fact_s(n: int) -> int:
    """
    >>> fact_s(5)
    120
    """
    return prod(range(1, n + 1))


def fact_o(n: int) -> int:
    """
    >>> fact_o(5)
    120
    """
    p = 1
    for i in range(2, n + 1):
        p *= i
    return p


def fact_w(n: int) -> int:
    """
    >>> fact_w(5)
    120
    """
    p = n
    while n != 1:
        n = n - 1
        p *= n
    return p


def fibo(n: int) -> int:
    """
    >>> fibo(7)
    21
    """
    if n <= 1:
        return 1
    else:
        return fibo(n - 1) + fibo(n - 2)


from functools import lru_cache


@lru_cache(128)
def fibo_r(n: int) -> int:
    """
    >>> fibo_r(0)
    1
    >>> fibo_r(1)
    1
    >>> fibo_r(2)
    2
    >>> fibo_r(3)
    3
    >>> fibo_r(4)
    5
    >>> fibo_r(7)
    21
    """
    if n < 2:
        return 1
    else:
        return fibo_r(n - 1) + fibo_r(n - 2)


def fibo_iter() -> Iterator[int]:
    a = 1
    b = 1
    yield a
    while True:
        yield b
        a, b = b, a + b


def fibo_i(n: int) -> int:
    """
    >>> fibo_i(0)
    1
    >>> fibo_i(1)
    1
    >>> fibo_i(2)
    2
    >>> fibo_i(3)
    3
    >>> fibo_i(4)
    5
    >>> fibo_i(7)
    21
    """
    for i, f_i in enumerate(fibo_iter()):
        if i == n:
            break
    return f_i


def test_fact():
    assert prod(range(2, 6)) == 120
    assert fact_s(5) == 120
    assert fact_o(5) == 120
    assert fact_w(5) == 120


def test_fibo():
    assert fibo_r(7) == 21
    assert fibo_i(7) == 21


def timing_factorial():
    simple = timeit.timeit(
        "fact_s(52)",
        """
from ch03_r07 import fact_s
""",
    )

    optimized = timeit.timeit(
        "fact_o(52)",
        """
from ch03_r07 import fact_o
""",
    )

    while_statement = timeit.timeit(
        "fact_w(52)",
        """
from ch03_r07 import fact_w
""",
    )

    print(f"Simple    {simple:.4f}")
    print(f"Optimized {optimized:.4f}")
    print(f"While     {while_statement:.4f}")


def timing_fibonacci():
    cached = timeit.timeit(
        "fibo_r(20)",
        """
from ch03_r07 import fibo_r
""",
    )

    iterative = timeit.timeit(
        "fibo_i(20)",
        """
from ch03_r07 import fibo_i
""",
    )

    print(f"Cached     {cached:.4f}")
    print(f"Interative {iterative:.4f}")


if __name__ == "__main__":
    timing_factorial()
    timing_fibonacci()
