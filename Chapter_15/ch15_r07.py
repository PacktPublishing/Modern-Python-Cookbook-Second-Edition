"""Python Cookbook 2nd ed.

Chapter 15, recipe 7, Are there outliers?
"""

from pathlib import Path
import json
import statistics
from typing import (
    Iterable, Iterator, Optional, Sequence, Dict, TypedDict, Callable, List
)


def absdev(
        data: Sequence[float],
        median: Optional[float] = None) -> Iterator[float]:
    if median is None:
        median = statistics.median(data)
    return (abs(x - median) for x in data)


def median_absdev(
        data: Sequence[float],
        median: Optional[float] = None) -> float:
    if median is None:
        median = statistics.median(data)
    return statistics.median(absdev(data, median=median))


def z_mod(data: Sequence[float]) -> Iterator[float]:
    median = statistics.median(data)
    mad = median_absdev(data, median)
    return (0.6745 * (x - median) / mad for x in data)


import itertools


def pass_outliers(data: Sequence[float]
                  ) -> Iterator[float]:
    return itertools.compress(
        data, (z >= 3.5 for z in z_mod(data)))


def reject_outliers(data: Sequence[float]
                    ) -> Iterator[float]:
    return itertools.compress(
        data, (z < 3.5 for z in z_mod(data)))


Point = Dict[str, float]
class Series(TypedDict):
    series: str
    data: List[Point]


def examine_all_series(source_path: Path) -> None:
    raw_data: Sequence[Series] = json.loads(source_path.read_text())

    series_map = {
        series["series"]: series["data"]
        for series in raw_data}
    for series_name in series_map:
        print(series_name)
        series_data = series_map[series_name]
        for variable_name in 'x', 'y':
            values = [item[variable_name] for item in series_data]
            print(variable_name, values, end=" ")
            try:
                print("outliers", list(pass_outliers(values)))
            except ZeroDivisionError:
                print("Data Appears Linear")
        print()


test_demo = """
>>> source_path = Path('data') / 'anscombe.json'
>>> raw_data = json.loads(source_path.read_text())
>>> data = {series['series']: series['data'] for series in raw_data}
>>> series = data['I']
>>> list(pass_outliers([item['x'] for item in series]))  # I
[]
>>> list(pass_outliers([item['y'] for item in series]))  # I
[]
>>> series = data['II']
>>> list(pass_outliers([item['x'] for item in series]))  # II
[]
>>> list(pass_outliers([item['y'] for item in series]))  # II
[]
>>> series = data['III']
>>> list(pass_outliers([item['x'] for item in series]))  # III
[]
>>> list(pass_outliers([item['y'] for item in series]))  # III
[12.74]
>>> series = data['IV']
>>> list(pass_outliers([item['x'] for item in series]))  # IV
Traceback (most recent call last):
  File "/Users/slott/miniconda3/envs/cookbook/lib/python3.8/doctest.py", line 1328, in __run
    exec(compile(example.source, filename, "single",
  File "<doctest ch10_r07.__test__.demo[13]>", line 1, in <module>
    list(pass_outliers([item['x'] for item in series]))
  File "Chapter_15/ch10_r07.py", line 34, in <genexpr>
    return itertools.compress(data, (z >= 3.5 for z in z_mod(data)))
  File "Chapter_15/ch10_r07.py", line 27, in <genexpr>
    0.6745*(x - median)/mad for x in data
ZeroDivisionError: float division by zero
>>> list(pass_outliers([item['y'] for item in series]))  # IV
[]
"""

outlier = lambda z: z >= 3.5

def pass_outliers_2(data: Sequence[float]) -> Iterator[float]:
    return itertools.compress(
        data, (outlier(z) for z in z_mod(data)))


def reject_outliers_2(data: Sequence[float]) -> Iterator[float]:
    return itertools.compress(
        data, (not outlier(z) for z in z_mod(data)))


def filter_outlier(mad: float, median_x: float, x: float) -> bool:
    return 0.6745*(x - median_x)/mad >= 3.5


from functools import partial


def make_filter_outlier_partial(
        data: Sequence[float]) -> Callable[[float], bool]:
    population_median = statistics.median(data)
    mad = median_absdev(data, population_median)
    outlier_partial = partial(
        filter_outlier, mad, population_median)
    return outlier_partial


def pass_outliers_3(data: Sequence[float]) -> Iterator[float]:
    outlier_partial = make_filter_outlier_partial(data)
    return filter(outlier_partial, data)


def reject_outliers_3(data: Sequence[float]) -> Iterator[float]:
    outlier_partial = make_filter_outlier_partial(data)
    return itertools.filterfalse(outlier_partial, data)

test_outliers = """
>>> data =  [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73] 
>>> list(pass_outliers(data))
[12.74]
>>> set(reject_outliers(data)) == set(data) - set([12.74])
True
"""

test_outliers_2 = """
>>> data =  [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73] 
>>> list(pass_outliers_2(data))
[12.74]
>>> set(reject_outliers_2(data)) == set(data) - set([12.74])
True
"""

test_outliers_3 = """
>>> data =  [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73] 
>>> list(pass_outliers_3(data))
[12.74]
>>> set(reject_outliers_3(data)) == set(data) - set([12.74])
True
"""


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}

if __name__ == "__main__":
    source_path = Path("data") / "anscombe.json"
    examine_all_series(source_path)
