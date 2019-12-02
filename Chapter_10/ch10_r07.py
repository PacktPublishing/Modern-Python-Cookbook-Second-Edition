"""Python Cookbook 2nd ed.

Chapter 10, recipe 7.
"""

from pathlib import Path
import json
import statistics
from typing import Iterable, Iterator, Optional, List


def absdev(data: Iterable[float], median: Optional[float] = None) -> Iterator[float]:
    if median is None:
        median = statistics.median(data)
    return (abs(x - median) for x in data)


def median_absdev(data: Iterable[float], median: Optional[float] = None) -> float:
    if median is None:
        median = statistics.median(data)
    return statistics.median(absdev(data, median=median))


def z_mod(data: Iterable[float]) -> Iterator[float]:
    median = statistics.median(data)
    mad = median_absdev(data, median)
    return (0.6745 * (x - median) / mad for x in data)


import itertools


def pass_outliers(data: List[float]) -> Iterator[float]:
    return itertools.compress(data, (z >= 3.5 for z in z_mod(data)))


def reject_outliers(data: List[float]) -> Iterator[float]:
    return itertools.compress(data, (z < 3.5 for z in z_mod(data)))


from pprint import pprint

# for series in data:
#     pprint(series)


def examine_anscombe(source_path: Path) -> None:
    raw_data = json.loads(source_path.read_text())

    data = {series["series"]: series["data"] for series in raw_data}
    for series_name in data:
        print(series_name)
        series_data = data[series_name]
        for variable_name in series_data:
            variable = [item[variable_name] for item in series_data]
            print(variable_name, variable, end=" ")
            try:
                print("outliers", list(pass_outliers(variable)))
            except ZeroDivisionError:
                print("Data Appears Linear")
        print()


__test__ = {
    "demo": """
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
  File "Chapter_10/ch10_r07.py", line 34, in <genexpr>
    return itertools.compress(data, (z >= 3.5 for z in z_mod(data)))
  File "Chapter_10/ch10_r07.py", line 27, in <genexpr>
    0.6745*(x - median)/mad for x in data
ZeroDivisionError: float division by zero
>>> list(pass_outliers([item['y'] for item in series]))  # IV
[]
""",
}

if __name__ == "__main__":
    source_path = Path("data") / "anscombe.json"
    examine_anscombe(source_path)
