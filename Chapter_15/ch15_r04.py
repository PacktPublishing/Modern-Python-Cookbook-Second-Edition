"""Python Cookbook 2nd ed.

Chapter 15, recipe 4, Computing regression parameters
"""

import statistics
from typing import Iterable, TypedDict, List, NamedTuple
from Chapter_15.ch15_r03 import correlation, Point


class Regression(NamedTuple):
    alpha: float
    beta: float

def regression(series: List[Point]) -> Regression:

    m_x = statistics.mean(p["x"] for p in series)
    m_y = statistics.mean(p["y"] for p in series)
    s_x = statistics.stdev(p["x"] for p in series)
    s_y = statistics.stdev(p["y"] for p in series)
    r_xy = correlation(series)

    b = r_xy * s_y / s_x
    a = m_y - b * m_x
    return Regression(a, b)


from math import sqrt


def regr2(series: Iterable[Point]) -> Regression:
    sumx = sumy = sumxy = sumx2 = sumy2 = n = 0.0
    for point in series:
        x, y = point["x"], point["y"]
        n += 1
        sumx += x
        sumy += y
        sumxy += x * y
        sumx2 += x ** 2
        sumy2 += y ** 2
    m_x = sumx / n
    m_y = sumy / n
    s_x = sqrt((n * sumx2 - sumx ** 2) / (n * (n - 1)))
    s_y = sqrt((n * sumy2 - sumy ** 2) / (n * (n - 1)))
    r_xy = (n * sumxy - sumx * sumy) / (
        sqrt(n * sumx2 - sumx ** 2) * sqrt(n * sumy2 - sumy ** 2)
    )
    b = r_xy * s_y / s_x
    a = m_y - b * m_x
    return Regression(a, b)


from pathlib import Path
import json

source_path = Path("data") / "anscombe.json"

test_regression = """
>>> data = json.loads(source_path.read_text())
>>> for series in data:
...    a, b = regression(series['data'])
...    print(
...        f"{series['series']:>3s} "
...        f"y={round(a, 2)}+{round(b,3)}*x"
...    )
  I y=3.0+0.5*x
 II y=3.0+0.5*x
III y=3.0+0.5*x
 IV y=3.0+0.5*x

"""

test_regr2 = """
>>> data = json.loads(source_path.read_text())
>>> for series in data:
...    a, b = regr2(series['data'])
...    print(f"{series['series']:>3s} y={round(a, 2)}+{round(b,3)}*x")
  I y=3.0+0.5*x
 II y=3.0+0.5*x
III y=3.0+0.5*x
 IV y=3.0+0.5*x

"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
