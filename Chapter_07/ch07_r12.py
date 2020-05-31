"""Python Cookbook 2nd ed.

Chapter 7, recipe 13, Managing multiple contexts with multiple resources
"""
from Chapter_03.ch03_r08 import haversine, MI, NM, KM

import csv
from dataclasses import dataclass, field, asdict
from pathlib import Path
from types import TracebackType
from typing import Optional, Type, List, Iterable, TextIO, Dict


@dataclass(frozen=True)
class Point:
    lat: float
    lon: float


@dataclass
class Leg:
    start: Point
    end: Point
    distance: float = field(init=False)


class LegMaker:
    def __enter__(self) -> "LegMaker":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[Exception]],
        exc_val: Optional[Exception],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        return None

    def __init__(self, r: float = NM) -> None:
        self.last_point: Optional[Point] = None
        self.last_leg: Optional[Leg] = None
        self.r = r

    def waypoint(self, next_point: Point) -> Optional[Leg]:
        leg: Optional[Leg]
        if self.last_point is None:
            # Special case for the first leg
            leg = None
        else:
            leg = Leg(self.last_point, next_point)
            d = haversine(
                leg.start.lat, leg.start.lon,
                leg.end.lat, leg.end.lon, self.r
            )
            leg.distance = round(d)
        self.last_point = next_point
        return leg

    def end(self) -> None:
        self.last_point = None


test_leg_maker = """
>>> legger = LegMaker()
>>> with legger:
...    route = list(filter(None, [
...        legger.waypoint(Point(38.9784, -76.4922)),
...        legger.waypoint(Point(38.3185, -76.4541)),
...        legger.waypoint(Point(37.5531, -76.3403)),
...        legger.waypoint(Point(36.8443, -76.2922))
...    ]))
>>> round(sum(leg.distance for leg in route), 1)
129
>>> round(sum(leg.distance for leg in route)/6, 1)
21.5
>>> for l in route:
...     print(l)
Leg(start=Point(lat=38.9784, lon=-76.4922), end=Point(lat=38.3185, lon=-76.4541), distance=40)
Leg(start=Point(lat=38.3185, lon=-76.4541), end=Point(lat=37.5531, lon=-76.3403), distance=46)
Leg(start=Point(lat=37.5531, lon=-76.3403), end=Point(lat=36.8443, lon=-76.2922), distance=43)
"""


def flat_dict(leg: Leg) -> Dict[str, float]:
    struct = asdict(leg)
    return dict(
        start_lat=struct["start"]["lat"],
        start_lon=struct["start"]["lon"],
        end_lat=struct["end"]["lat"],
        end_lon=struct["end"]["lon"],
        distance=struct["distance"],
    )

test_flat_dict = """
>>> leg = Leg(Point(38.9784, -76.4922), Point(38.3185, -76.4541))
>>> d = haversine(
...     leg.start.lat, leg.start.lon,
...     leg.end.lat, leg.end.lon,
...     NM
... )
>>> leg.distance = round(d)
>>> flat_dict(leg)
{'start_lat': 38.9784, 'start_lon': -76.4922, 'end_lat': 38.3185, 'end_lon': -76.4541, 'distance': 40}
"""


HEADERS = ["start_lat", "start_lon", "end_lat", "end_lon", "distance"]

def make_route_file(points: Iterable[Point], target: Path) -> None:
    with LegMaker(r=NM) as legger, target.open("w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, HEADERS)
        writer.writeheader()
        for point in points:
            leg = legger.waypoint(point)
            if leg is not None:
                writer.writerow(flat_dict(leg))
    print(f"Finished creating {target}")


test_make_route_file = """
>>> points = [
...     Point(38.9784, -76.4922),
...     Point(38.3185, -76.4541),
...     Point(37.5531, -76.3403),
...     Point(36.8443, -76.2922)
... ]
>>> try:
...     (Path.cwd()/"data"/"ch07_r13.csv").unlink()
... except FileNotFoundError:
...     pass
>>> make_route_file(points, Path.cwd()/"data"/"ch07_r13.csv")  # doctest: +ELLIPSIS
Finished creating .../data/ch07_r13.csv
>>> (Path.cwd()/"data"/"ch07_r13.csv").read_text().splitlines()  # doctest: +NORMALIZE_WHITESPACE
['start_lat,start_lon,end_lat,end_lon,distance', 
 '38.9784,-76.4922,38.3185,-76.4541,40', 
 '38.3185,-76.4541,37.5531,-76.3403,46', 
 '37.5531,-76.3403,36.8443,-76.2922,43']
"""

import bz2


def make_route_bz2(points: Iterable[Point], target: Path) -> None:
    with LegMaker(r=NM) as legger, bz2.open(target, "wt") as archive:
        writer = csv.DictWriter(archive, HEADERS)
        writer.writeheader()
        for point in points:
            leg = legger.waypoint(point)
            if leg is not None:
                writer.writerow(flat_dict(leg))
    print(f"Finished creating {target}")


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}

if __name__ == "__main__":
    points = [
        Point(38.9784, -76.4922),
        Point(38.3185, -76.4541),
        Point(37.5531, -76.3403),
        Point(36.8443, -76.2922),
    ]
    make_route_file(points, Path.cwd() / "data" / "ch07_r13.csv")
    make_route_bz2(points, Path.cwd() / "data" / "ch07_r13.csv.bz2")
