"""Python Cookbook 2nd ed.

Chapter 7, recipe 3, Designing classes with lots of processing
"""
from Chapter_15.collector import samples, arrival1, coupon_collector
import collections
import math
import statistics
from typing import Optional, Counter, Callable, Iterator

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


class CounterStatistics:
    """
    >>> data = collections.Counter( [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5] )
    >>> cs = CounterStatistics(data)
    >>> round(cs.mean,1)
    9.0
    >>> round(cs.stddev**2,1)
    11.0
    """

    def __init__(self, raw_counter: Counter[int]) -> None:
        self.raw_counter = raw_counter

        self.mean: float = self.compute_mean()
        self.stddev: float = self.compute_stddev()

    def compute_mean(self) -> float:
        total, count = 0.0, 0
        for value, frequency in self.raw_counter.items():
            total += value * frequency
            count += frequency
        return total / count

    def compute_stddev(self) -> float:
        total, count = 0.0, 0
        for value, frequency in self.raw_counter.items():
            total += frequency * (value - self.mean) ** 2
            count += frequency
        return math.sqrt(total / (count - 1))


class UpdateableCounterStatistics:
    """
    >>> data = Counter([10, 8, 13, 9, 11, 14, 6, 4, 12])
    >>> cs = UpdateableCounterStatistics(data)
    >>> round(cs.mean,1)
    9.7
    >>> round(cs.stddev**2,1)
    10.7
    >>> cs.add(7)
    >>> round(cs.mean,1)
    9.4
    >>> round(cs.stddev**2,1)
    10.3
    >>> cs.add(5)
    >>> round(cs.mean,1)
    9.0
    >>> round(cs.stddev**2,1)
    11.0
    """

    def __init__(self, counter: Counter = None) -> None:
        if counter is not None:
            self.raw_counter = counter
            self.count = sum(self.raw_counter[k] for k in self.raw_counter)
            self.sum = sum(self.raw_counter[k] * k for k in self.raw_counter)
            self.sum2 = sum(self.raw_counter[k] * k ** 2 for k in self.raw_counter)
            self.mean: Optional[float] = self.sum / self.count
            self.stddev: Optional[float] = math.sqrt(
                (self.sum2 - self.sum ** 2 / self.count) / (self.count - 1)
            )
        else:
            self.raw_counter = collections.Counter()
            self.count = 0
            self.sum = 0
            self.sum2 = 0
            self.mean = None
            self.stddev = None

    def add(self, value: int) -> None:
        self.raw_counter[value] += 1
        self.count += 1
        self.sum += value
        self.sum2 += value ** 2
        self.mean = self.sum / self.count
        if self.count > 1:
            self.stddev = math.sqrt(
                (self.sum2 - self.sum ** 2 / self.count) / (self.count - 1)
            )


test_expected = """
>>> from Chapter_15.collector import expected
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

test_CounterStatistics = """
>>> import random
>>> random.seed(1)
>>> data = raw_data(8)
>>> stats = CounterStatistics(data)
>>> round(stats.mean, 2)
20.81
>>> round(stats.stddev, 2)
7.02
"""

test_UpdateableCounterStatistics = """
>>> import random
>>> random.seed(1)
>>> data = raw_data(8)
>>> stats = UpdateableCounterStatistics(data)
>>> round(stats.mean, 2)
20.81
>>> round(stats.stddev, 2)
7.02
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}

if __name__ == "__main__":

    import random
    from Chapter_15.collector import expected

    random.seed(1)
    data = raw_data(8)

    print(f"expected_time {float(expected(8))}")
    print(f"expected mean {statistics.mean(data.elements())}")
    print(f"expected stddev {statistics.stdev(data.elements())}")

    stats = CounterStatistics(data)
    print(f"Mean: {stats.mean:.2f}")
    print(f"Standard Deviation: {stats.stddev:.3f}")

    stats2 = UpdateableCounterStatistics(data)
    print(f"Mean: {stats.mean:.2f}")
    print(f"Standard Deviation: {stats.stddev:.3f}")
