"""Python Cookbook 2nd ed.

Coupon Collector sources of biased data.
"""
import collections
import random
from typing import Dict, Iterable, DefaultDict, Counter
from Chapter_15.collector import samples, arrival1, arrival2


def example_1(source: Iterable[int]) -> Dict[int, int]:
    histogram: Dict[int, int] = {}
    for item in source:
        if item not in histogram:
            histogram[item] = 0
        histogram[item] += 1
    return histogram


def example_2(source: Iterable[int]) -> Dict[int, int]:
    histogram: Dict[int, int] = {}
    for item in source:
        histogram.setdefault(item, 0)
        histogram[item] += 1
    return histogram


def example_3(source: Iterable[int]) -> Dict[int, int]:
    histogram: DefaultDict[int, int] = collections.defaultdict(int)
    for item in source:
        histogram[item] += 1
    return histogram


def example_4(source: Iterable[int]) -> Dict[int, int]:
    histogram: Counter[int] = collections.Counter(source)
    return histogram


def show(histogram: Dict[int, int]) -> None:
    """
    >>> random.seed(1)
    >>> data = collections.Counter(
    ...     int(5+5*random.gauss(0, .3)) for _ in range(100))
    >>> show(data)
      0 | *
      1 | *
      2 | **********
      3 | *****************************
      4 | *****************************************
      5 | **************************************************
      6 | ***************************
      7 | ********
      8 | *
    """
    limit = max(histogram.values())
    for k in sorted(histogram):
        bar = int(50 * histogram[k] / limit) * "*"
        print(f"{k:3d} | {bar:s}")


def test_histograms():
    data = [2, 2, 2, 3, 3, 3, 3, 5]
    assert example_1(data) == {2: 3, 3: 4, 5: 1}
    assert example_2(data) == {2: 3, 3: 4, 5: 1}
    assert example_3(data) == {2: 3, 3: 4, 5: 1}
    assert example_4(data) == {2: 3, 3: 4, 5: 1}


test_counter_histogram = """
>>> import random
>>> from Chapter_04.ch04_r07 import samples, arrival2
>>> random.seed(1)
>>> list(samples(10, arrival2(8)))
[1, 0, 1, 1, 2, 2, 2, 2, 1, 1]

>>> from collections import Counter
>>> def summarize_4(source):
...    histogram = Counter(source)
...    return histogram

>>> from pprint import pprint
>>> random.seed(1)
>>> histogram = summarize_4(samples(1000, arrival2(8)))
>>> pprint(histogram)
Counter({1: 150, 0: 130, 2: 129, 4: 128, 5: 127, 6: 118, 3: 117, 7: 101})

>>> for key in sorted(histogram):
...    print(key, histogram[key])
0 130
1 150
2 129
3 117
4 128
5 127
6 118
7 101
"""

if __name__ == "__main__":
    print("\narrival1")
    show(example_1(samples(1000, arrival1(8))))
    print("\narrival1")
    show(example_2(samples(1000, arrival1(8))))
    print("\narrival1")
    show(example_3(samples(1000, arrival1(8))))
    print("\narrival1")
    show(example_4(samples(1000, arrival1(8))))

    print("\narrival2")
    show(example_1(samples(1000, arrival2(8))))

    from pprint import pprint

    random.seed(1)
    pprint(example_4(samples(1000, arrival1(8))))
