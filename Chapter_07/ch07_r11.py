"""Python Cookbook 2nd ed.

Chapter 7, recipe 11, Using contexts and context managers
"""

from Chapter_03.ch03_r08 import haversine, MI, NM, KM
from typing import Type, NamedTuple, Optional, Callable, List
from types import TracebackType


class Point(NamedTuple):
    lat: float
    lon: float


class Distance:
    def __init__(self, r: float) -> None:
        self.r = r

    def __enter__(self) -> Callable[[Point, Point], float]:
        return self.distance

    def __exit__(
        self,
        exc_type: Optional[Type[Exception]],
        exc_val: Optional[Exception],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        return None

    def distance(self, p1: Point, p2: Point) -> float:
        return haversine(p1.lat, p1.lon, p2.lat, p2.lon, self.r)


test_distance = """
>>> p1 = Point(38.9784, -76.4922)
>>> p2 = Point(36.8443, -76.2922)
>>> with Distance(r=NM) as nm_dist:
...     print(f"{nm_dist(p1, p2)=:.2f}")
nm_dist(p1, p2)=128.48

>>> nm_distance = Distance(r=NM)
>>> with nm_distance as nm_calc:
...     print(f"{nm_calc(p1, p2)=:.2f}")
nm_calc(p1, p2)=128.48
"""


class Distance_2:
    def __init__(self, r: float) -> None:
        self.r = r

    def __enter__(self) -> Callable[[Point, Point], float]:
        return self.distance

    def __exit__(
        self,
        exc_type: Optional[Type[Exception]],
        exc_val: Optional[Exception],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        if exc_type == TypeError:
            raise ValueError(f"Invalid r={self.r}")
        return None

    def distance(self, p1: Point, p2: Point) -> float:
        return haversine(p1.lat, p1.lon, p2.lat, p2.lon, self.r)


test_bad = """
>>> p1 = Point(38.9784, -76.4922)
>>> p2 = Point(36.8443, -76.2922)
>>> with Distance(None) as nm_dist:
...     print(f"{nm_dist(p1, p2)=:.2f}")
Traceback (most recent call last):
  File "/Users/slott/miniconda3/envs/cookbook/lib/python3.8/doctest.py", line 1328, in __run
    exec(compile(example.source, filename, "single",
  File "<doctest Chapter_07.ch07_r12.__test__.test_bad[2]>", line 2, in <module>
  File "/Users/slott/Documents/Writing/Python/Python Cookbook 2e/Modern-Python-Cookbook-Second-Edition/Chapter_07.ch07_r12.py", line 32, in distance
    return haversine(p1.lat, p1.lon, p2.lat, p2.lon, self.r)
  File "/Users/slott/Documents/Writing/Python/Python Cookbook 2e/Modern-Python-Cookbook-Second-Edition/Chapter_03/ch03_r08.py", line 30, in haversine
    return R * 2 * asin(a)
TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'

"""

test_bad_2 = """
>>> p1 = Point(38.9784, -76.4922)
>>> p2 = Point(36.8443, -76.2922)
>>> with Distance_2(None) as nm_dist:
...     print(f"{nm_dist(p1, p2)=:.2f}")
Traceback (most recent call last):
    ...
ValueError: Invalid r=None
"""


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
