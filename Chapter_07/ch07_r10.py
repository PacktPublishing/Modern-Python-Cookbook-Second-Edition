"""Python Cookbook 2nd ed.

Chapter 7, recipe 10, Using properties for lazy attributes
"""
from Chapter_15.collector import arrival1, samples, coupon_collector, expected
import collections
import math
import statistics
from typing import Counter, Iterator, Callable, Optional, cast


class LazyCounterStatistics:
    """
    >>> data = collections.Counter( [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5] )
    >>> cs = LazyCounterStatistics(data)
    >>> round(cs.mean,1)
    9.0
    >>> round(cs.stddev**2,1)
    11.0
    """

    def __init__(self, raw_counter: Counter) -> None:
        self.raw_counter = raw_counter

    @property
    def sum(self) -> float:
        return sum(f * v for v, f in self.raw_counter.items())

    @property
    def count(self) -> int:
        return sum(f for v, f in self.raw_counter.items())

    @property
    def mean(self) -> float:
        return self.sum / self.count

    @property
    def sum2(self) -> float:
        return sum(f * v ** 2 for v, f in self.raw_counter.items())

    @property
    def variance(self) -> float:
        return (self.sum2 - self.sum ** 2 / self.count) / (self.count - 1)

    @property
    def stddev(self) -> float:
        return math.sqrt(self.variance)


# An example, using the data generator from chapter 4.

ArrivalF = Callable[[int], Iterator[int]]


def raw_data(
    n: int = 8, limit: int = 1000, arrival_function: ArrivalF = arrival1
) -> Counter[int]:
    """
    >>> import random
    >>> random.seed(1)
    >>> data = raw_data(n=2, limit=8, arrival_function=arrival1)
    >>> data
    Counter({3: 1, 2: 1})
    """
    data = samples(limit, arrival_function(n))
    wait_times = collections.Counter(coupon_collector(n, data))
    return wait_times


test_expected = """
>>> expected(8)
Fraction(761, 35)
"""

test_raw_data = """
>>> import random
>>> random.seed(1)
>>> data = raw_data(8)
>>> round(statistics.mean(data.elements()), 2)
20.81
>>> round(statistics.stdev(data.elements()), 2)
7.02
"""

test_LazyCounterStatistics = """
>>> import random
>>> random.seed(1)
>>> data = raw_data(8)
>>> stats = LazyCounterStatistics(data)
>>> round(stats.mean, 2)
20.81
>>> round(stats.stddev, 2)
7.02
"""


class CachingLazyCounterStatistics:
    def __init__(self, raw_counter: Counter) -> None:
        self.raw_counter = raw_counter
        self._sum: Optional[float] = None
        self._count: Optional[float] = None

    @property
    def sum(self) -> float:
        if self._sum is None:
            self._sum = sum(f * v for v, f in self.raw_counter.items())
        return cast(float, self._sum)

    @property
    def count(self) -> float:
        if self._count is None:
            self._count = sum(f for v, f in self.raw_counter.items())
        return cast(float, self._count)

    @property
    def mean(self) -> float:
        return self.sum / self.count


test_caching = """
>>> import random
>>> random.seed(1)
>>> data = raw_data(8)
>>> stats = CachingLazyCounterStatistics(data)
>>> round(stats.mean, 2)
20.81
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}


if __name__ == "__main__":

    import random

    random.seed(1)
    data = raw_data(8)

    print("expected_time", float(expected(8)))
    print("expected mean", statistics.mean(data.elements()))
    print("expected stddev", statistics.stdev(data.elements()))

    stats = LazyCounterStatistics(data)
    print("Mean: {stats.mean:.2f}")
    print("Standard Deviation: {stats.stddev:.3f}")
