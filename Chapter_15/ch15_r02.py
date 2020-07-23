"""Python Cookbook 2nd ed.

Chapter 15, recipe 2, Average of values in a Counter
"""
import collections
import json
from pathlib import Path
from typing import (
    Any,  Callable, cast, Dict, Iterable, Iterator, List,
    Counter, Union, TypedDict)


Point = Dict[str, float]
class Series(TypedDict):
    series: str
    data: List[Point]

def get_series(data: List[Series], series_name: str) -> Series:
    series = next(
        s for s in data
           if s["series"] == series_name
        )
    return series


def data_counter(
        series: Series, variable_name: str) -> Counter[float]:
    return collections.Counter(
        item[variable_name]
        for item in cast(List[Point], series["data"])
    )

def counter_sum(counter: Counter[float]) -> float:
    return sum(f*v for v, f in counter.items())

test_counter_sum = """
>>> import collections 
>>> raw_data = [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8] 
>>> series_4_x = collections.Counter(raw_data) 
>>> counter_sum(series_4_x)
99
"""

def counter_len(counter: Counter[float]) -> int:
    return sum(f for v, f in counter.items())

test_counter_len = """
>>> import collections 
>>> raw_data = [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8] 
>>> series_4_x = collections.Counter(raw_data) 
>>> counter_len(series_4_x)
11
"""

def counter_mean(counter: Counter[float]) -> float:
    return counter_sum(counter)/counter_len(counter)

test_counter_mean = """
>>> import collections 
>>> raw_data = [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8] 
>>> series_4_x = collections.Counter(raw_data) 
>>> counter_mean(series_4_x)
9.0
"""

def counter_sum_2(counter: Counter[float]) -> float:
    return sum(f*v**2 for v, f in counter.items())

test_counter_sum_2 = """
>>> import collections 
>>> raw_data = [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8] 
>>> series_4_x = collections.Counter(raw_data) 
>>> counter_sum_2(series_4_x)
1001
"""

def counter_variance(counter: Counter[float]) -> float:
   n = counter_len(counter)
   return (
       1/(n-1) *
       (counter_sum_2(counter) - (counter_sum(counter)**2)/n)
   )


import math
def counter_stdev(counter: Counter[float]) -> float:
   return math.sqrt(counter_variance(counter))

test_variance_stdev = """
>>> import collections 
>>> raw_data = [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8] 
>>> series_4_x = collections.Counter(raw_data) 
>>> counter_variance(series_4_x)
11.0
>>> round(counter_stdev(series_4_x), 2)
3.32
"""

def main():
    data: List[Series] = json.loads(
        source_path.read_text(),
    )
    s_4 = get_series(data, 'IV')
    s_4_x = collections.Counter(data_counter(s_4, 'x'))
    print(
        f"Series IV, variable x: "
        f"mean={counter_mean(s_4_x)} "
        f"variance={counter_variance(s_4_x)} "
        f"stdev={counter_stdev(s_4_x)}"
    )

test_main = """
>>> source_path = Path('data/anscombe.json')
>>> data: List[Series] = json.loads(
...     source_path.read_text(),
... )
>>> s_4 = get_series(data, 'IV')
>>> s_4_x = collections.Counter(data_counter(s_4, 'x'))
>>> s_4_x
Counter({8.0: 10, 19.0: 1})
>>> print(
...     f"Series IV, variable x: "
...     f"mean={counter_mean(s_4_x)} "
...     f"variance={round(counter_variance(s_4_x), 2)} "
...     f"stdev={round(counter_stdev(s_4_x), 2)}"
... )
Series IV, variable x: mean=9.0 variance=11.0 stdev=3.32
"""


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
