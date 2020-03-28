"""Python Cookbook 2nd ed.

Chapter B, Bonus, recipe 8.
"""

from pathlib import Path
import json
from typing import Any, Iterable, Dict

# from collections import OrderedDict

import math


class SimpleStats:
    def __init__(self, name: str) -> None:
        self.name = name
        self.count = 0
        self.sum = 0
        self.sum_2 = 0

    def cleanse(self, value: Any) -> float:
        return float(value)

    def add(self, value: Any) -> None:
        value = self.cleanse(value)
        self.count += 1
        self.sum += value
        self.sum_2 += value * value

    @property
    def mean(self) -> float:
        return self.sum / self.count

    @property
    def stdev(self) -> float:
        return math.sqrt(
            (self.count * self.sum_2 - self.sum ** 2) / (self.count * (self.count - 1))
        )


def analyze(series_data: Iterable[Dict[str, Any]]) -> Dict[str, SimpleStats]:
    x_stats = SimpleStats("x")
    y_stats = SimpleStats("y")
    column_stats = {"x": x_stats, "y": y_stats}

    for item in series_data:
        for column_name in column_stats:
            column_stats[column_name].add(item[column_name])

    return column_stats


def stat_summary(source_path: Path) -> None:
    raw_data = json.loads(source_path.read_text())
    data = {series["series"]: series["data"] for series in raw_data}

    for series_name in data:
        print(series_name)
        column_stats = analyze(data[series_name])
        for column_key in column_stats:
            print(
                " ",
                column_key,
                column_stats[column_key].mean,
                column_stats[column_key].stdev,
            )


test_demo = """
>>> source_path = Path('data')/'anscombe.json'
>>> raw_data = json.loads(source_path.read_text())
>>> data = {series['series']: series['data'] for series in raw_data}
>>> for series_name in data:
...         print(series_name)
...         column_stats = analyze(data[series_name])
...         for column_key in column_stats:
...             print(' ', column_key,
...                  round(column_stats[column_key].mean, 2),
...                  round(column_stats[column_key].stdev, 3))
I
  x 9.0 3.317
  y 7.5 2.032
II
  x 9.0 3.317
  y 7.5 2.032
III
  x 9.0 3.317
  y 7.5 2.03
IV
  x 9.0 3.317
  y 7.5 2.031
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}

if __name__ == "__main__":
    source_path = Path("data") / "anscombe.json"
    stat_summary(source_path)
