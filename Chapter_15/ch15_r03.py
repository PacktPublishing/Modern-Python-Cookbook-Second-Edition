"""Python Cookbook 2nd ed.

Chapter 15, recipe 3, Computing the coefficient of correlation
"""

from math import sqrt
from typing import Iterable, TypedDict, List

class Point(TypedDict):
    x: float
    y: float

class Series(TypedDict):
    series: str
    data: List[Point]

def get_series(data: List[Series], series_name: str) -> Series:
    series = next(
        s for s in data
           if s["series"] == series_name
        )
    return series

def correlation(series: List[Point]) -> float:
    sumxy = sum(p["x"] * p["y"] for p in series)
    sumx = sum(p["x"] for p in series)
    sumy = sum(p["y"] for p in series)
    sumx2 = sum(p["x"] ** 2 for p in series)
    sumy2 = sum(p["y"] ** 2 for p in series)
    n = sum(1 for p in series)

    r = (n * sumxy - sumx * sumy) / (
        sqrt(n * sumx2 - sumx ** 2) * sqrt(n * sumy2 - sumy ** 2)
    )
    return r


def corr2(series: List[Point]) -> float:
    sumx = sumy = sumxy = sumx2 = sumy2 = n = 0.0
    for point in series:
        x, y = point["x"], point["y"]
        n += 1
        sumx += x
        sumy += y
        sumxy += x * y
        sumx2 += x ** 2
        sumy2 += y ** 2

    r = (n * sumxy - sumx * sumy) / (
        sqrt(n * sumx2 - sumx ** 2) * sqrt(n * sumy2 - sumy ** 2)
    )
    return r


from pathlib import Path
import json

source_path = Path("data") / "anscombe.json"
test_correlation = """
>>> data = json.loads(source_path.read_text())
>>> for series in data:
...    r = correlation(series['data'])
...    print(series['series'], 'r=', round(r, 2))
I r= 0.82
II r= 0.82
III r= 0.82
IV r= 0.82

"""

test_corr2 = """
>>> data = json.loads(source_path.read_text())
>>> for series in data:
...    r = corr2(series['data'])
...    print(f"{series['series']:>3s}, r={r:.2f}")
  I, r=0.82
 II, r=0.82
III, r=0.82
 IV, r=0.82

"""

def main():
    data: List[Series] = json.loads(
        source_path.read_text(),
    )
    for series in data:
        r = correlation(series["data"])
        print(
            f"{series['series']:>3s}, r={r:.3f}"
        )

test_main = """
>>> main()
  I, r=0.816
 II, r=0.816
III, r=0.816
 IV, r=0.817
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}

if __name__ == "__main__":
    main()
