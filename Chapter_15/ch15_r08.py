"""Python Cookbook 2nd ed.

Chapter 15, recipe 8, Many variables one pass
"""

import collections
import json
import math
from pathlib import Path
from typing import (
    Any, Iterable, Dict, TypedDict, List, Tuple, Counter, Union
)


Sample = Dict[str, str]
class Series(TypedDict):
    series: str
    data: List[Sample]

from abc import abstractmethod

class StatsGather:
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def add(self, value: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def summary(self) -> str:
        raise NotImplementedError


class SimpleStats(StatsGather):
    def __init__(self, name: str) -> None:
        super().__init__(name)
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
            (self.count * self.sum_2 - self.sum ** 2)
            /
            (self.count * (self.count - 1))
        )

    def summary(self) -> str:
        return (
            f"{self.name} "
            f"mean={self.mean:.1f} stdev={self.stdev:.3f}"
        )


test_simple_stats = """
>>> s = SimpleStats("X")
>>> for i in range(10):
...     s.add(i)
>>> s.mean
4.5
>>> round(s.stdev, 3)
3.028
"""

def analyze(
        series_data: Iterable[Sample],
        names: List[str]
) -> Dict[str, SimpleStats]:
    column_stats = {
        key: SimpleStats(key) for key in names
    }
    for row in series_data:
        for column_name in column_stats:
            column_stats[column_name].add(row[column_name])

    return column_stats


def stat_summary_xy(source_path: Path) -> None:
    raw_data: List[Series] = json.loads(
        source_path.read_text())
    series_map = {
        series["series"]: series["data"]
        for series in raw_data}

    for series_name in series_map:
        data_stream: Iterable[Sample] = iter(series_map[series_name])
        print(f"{series_name:}")
        column_stats = analyze(data_stream, ["x", "y"])
        for column_key in column_stats:
            print(" ", column_stats[column_key].summary())

test_stat_summary_xy = """
>>> source_path = Path('data')/'anscombe.json'
>>> stat_summary_xy(source_path)
I
  x mean=9.0 stdev=3.317
  y mean=7.5 stdev=2.032
II
  x mean=9.0 stdev=3.317
  y mean=7.5 stdev=2.032
III
  x mean=9.0 stdev=3.317
  y mean=7.5 stdev=2.030
IV
  x mean=9.0 stdev=3.317
  y mean=7.5 stdev=2.031


"""

class IntegerDiscreteStats(StatsGather):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.counts: Counter[int] = collections.Counter()

    def cleanse(self, value: Any) -> float:
        return int(value)

    def add(self, value: Any) -> None:
        value = self.cleanse(value)
        self.counts[value] += 1

    @property
    def mode(self) -> Tuple[int, int]:
        return self.counts.most_common(1)[0]

    @property
    def fq_dist(self) -> Counter[int]:
        return self.counts

    def summary(self) -> str:
        return f"{self.name} mode={self.mode}"


test_integer_discrete_stats = """
>>> s = IntegerDiscreteStats("X")
>>> for i in range(5):
...     s.add(i)
>>> for i in range(5):
...     s.add(i)
>>> s.add(2)
>>> s.mode
(2, 3)
>>> s.fq_dist
Counter({2: 3, 0: 2, 1: 2, 3: 2, 4: 2})
"""


def analyze2(
        series_data: Iterable[Sample],
        column_stats: Dict[str, StatsGather]
) -> Dict[str, StatsGather]:
    for row in series_data:
        for column_name in column_stats:
            column_stats[column_name].add(row[column_name])
    return column_stats

from Chapter_15.ch15_r05 import non_comment_iter, raw_data_iter

def stats_summary_co2(source_path: Path) -> None:
    column_stats: Dict[str, StatsGather] = {
        "year": IntegerDiscreteStats("year"),
        "month":  IntegerDiscreteStats("month"),
        "decimal_date": SimpleStats("decimal_date"),
        "average": SimpleStats("average"),
        "interpolated": SimpleStats("interpolated"),
        "trend": SimpleStats("trend"),
        "days": IntegerDiscreteStats("days"),
    }

    with source_path.open() as source_file:
        non_comment_data = non_comment_iter(source_file)
        raw_data = raw_data_iter(non_comment_data)
        column_stats = analyze2(raw_data, column_stats)

    for column_key in column_stats:
        print(column_stats[column_key].summary())

test_stats_summary_co2 = """
>>> source_path = Path('data')/'co2_mm_mlo.txt'
>>> stats_summary_co2(source_path)
year mode=(1959, 12)
month mode=(3, 59)
decimal_date mean=1987.3 stdev=16.827
average mean=347.3 stdev=51.803
interpolated mean=351.5 stdev=25.806
trend mean=351.5 stdev=25.719
days mode=(-1, 194)
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}

if __name__ == "__main__":
    source_path = Path("data") / "anscombe.json"
    stat_summary_xy(source_path)
