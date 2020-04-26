"""Python Cookbook 2nd ed.

Chapter 9, recipe 8, Creating a partial function.
"""

from pprint import pprint
from typing import Callable, List, Iterator, Iterable

text_1 = """
10	8.04
8	6.95
13	7.58
9	8.81
11	8.33
14	9.96
6	7.24
4	4.26
12	10.84
7	4.82
5	5.68
"""

text_2 = """
10	9.14
8	8.14
13	8.74
9	8.77
11	9.26
14	8.1
6	6.13
4	3.1
12	9.13
7	7.26
5	4.74
"""

# LineBreaker = Callable[[str], Iterator[List[str]]]
# text_parse: LineBreaker = lambda text: (r.split() for r in filter(None, text.splitlines()))


def text_parse(text: str) -> Iterator[List[str]]:
    non_empty = filter(None, text.splitlines())
    return (r.split() for r in non_empty)


from dataclasses import dataclass


@dataclass
class Row:
    x: float
    y: float


# RowBuilder = Callable[[Iterable[List[str]]], Iterator[Row]]
# row_build: RowBuilder = lambda rows: (Row(x=float(x), y=float(y)) for x, y in rows)


def make_row(rows: Iterable[List[str]]) -> Iterator[Row]:
    return (Row(x=float(x), y=float(y)) for x, y in rows)


data_1 = list(make_row(text_parse(text_1)))
data_2 = list(make_row(text_parse(text_2)))


def standardize(mean: float, stdev: float, x: float) -> float:
    return (x - mean) / stdev


import statistics

mean_x = statistics.mean(item.x for item in data_1)
stdev_x = statistics.stdev(item.x for item in data_1)

from functools import partial

z_1 = partial(standardize, mean_x, stdev_x)

z_2 = lambda x: standardize(mean_x, stdev_x, x)

z_3 = lambda x, m=mean_x, s=stdev_x: standardize(m, s, x)


def prepare_z(data: List[Row]) -> Callable[[float], float]:
    mean_x = statistics.mean(item.x for item in data)
    stdev_x = statistics.stdev(item.x for item in data)
    return partial(standardize, mean_x, stdev_x)


z_4 = prepare_z(data_1)


test_parse = """
>>> pprint(list(text_parse(text_1)))
[['10', '8.04'],
 ['8', '6.95'],
 ['13', '7.58'],
 ['9', '8.81'],
 ['11', '8.33'],
 ['14', '9.96'],
 ['6', '7.24'],
 ['4', '4.26'],
 ['12', '10.84'],
 ['7', '4.82'],
 ['5', '5.68']]
"""

test_parse_cleanse = """
>>> pprint(list(make_row(text_parse(text_1))))
[Row(x=10.0, y=8.04),
 Row(x=8.0, y=6.95),
 Row(x=13.0, y=7.58),
 Row(x=9.0, y=8.81),
 Row(x=11.0, y=8.33),
 Row(x=14.0, y=9.96),
 Row(x=6.0, y=7.24),
 Row(x=4.0, y=4.26),
 Row(x=12.0, y=10.84),
 Row(x=7.0, y=4.82),
 Row(x=5.0, y=5.68)]
"""

test_standardize = """
>>> for row in data_1:
...     z_x = standardize(mean_x, stdev_x, row.x)
...     print(row, round(z_x,2))
Row(x=10.0, y=8.04) 0.3
Row(x=8.0, y=6.95) -0.3
Row(x=13.0, y=7.58) 1.21
Row(x=9.0, y=8.81) 0.0
Row(x=11.0, y=8.33) 0.6
Row(x=14.0, y=9.96) 1.51
Row(x=6.0, y=7.24) -0.9
Row(x=4.0, y=4.26) -1.51
Row(x=12.0, y=10.84) 0.9
Row(x=7.0, y=4.82) -0.6
Row(x=5.0, y=5.68) -1.21
"""

test_z_1 = """
>>> for row in data_1:
...     print(row, round(z_1(row.x), 2))
Row(x=10.0, y=8.04) 0.3
Row(x=8.0, y=6.95) -0.3
Row(x=13.0, y=7.58) 1.21
Row(x=9.0, y=8.81) 0.0
Row(x=11.0, y=8.33) 0.6
Row(x=14.0, y=9.96) 1.51
Row(x=6.0, y=7.24) -0.9
Row(x=4.0, y=4.26) -1.51
Row(x=12.0, y=10.84) 0.9
Row(x=7.0, y=4.82) -0.6
Row(x=5.0, y=5.68) -1.21
"""

test_z_2 = """
>>> for row in data_1:
...     print(row, round(z_2(row.x), 2))
Row(x=10.0, y=8.04) 0.3
Row(x=8.0, y=6.95) -0.3
Row(x=13.0, y=7.58) 1.21
Row(x=9.0, y=8.81) 0.0
Row(x=11.0, y=8.33) 0.6
Row(x=14.0, y=9.96) 1.51
Row(x=6.0, y=7.24) -0.9
Row(x=4.0, y=4.26) -1.51
Row(x=12.0, y=10.84) 0.9
Row(x=7.0, y=4.82) -0.6
Row(x=5.0, y=5.68) -1.21
"""

test_z_3 = """
>>> for row in data_1:
...     print(row, round(z_3(row.x), 2))
Row(x=10.0, y=8.04) 0.3
Row(x=8.0, y=6.95) -0.3
Row(x=13.0, y=7.58) 1.21
Row(x=9.0, y=8.81) 0.0
Row(x=11.0, y=8.33) 0.6
Row(x=14.0, y=9.96) 1.51
Row(x=6.0, y=7.24) -0.9
Row(x=4.0, y=4.26) -1.51
Row(x=12.0, y=10.84) 0.9
Row(x=7.0, y=4.82) -0.6
Row(x=5.0, y=5.68) -1.21
"""

test_z_4 = """
>>> for row in data_1:
...     print(row, round(z_4(row.x), 2))
Row(x=10.0, y=8.04) 0.3
Row(x=8.0, y=6.95) -0.3
Row(x=13.0, y=7.58) 1.21
Row(x=9.0, y=8.81) 0.0
Row(x=11.0, y=8.33) 0.6
Row(x=14.0, y=9.96) 1.51
Row(x=6.0, y=7.24) -0.9
Row(x=4.0, y=4.26) -1.51
Row(x=12.0, y=10.84) 0.9
Row(x=7.0, y=4.82) -0.6
Row(x=5.0, y=5.68) -1.21
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
