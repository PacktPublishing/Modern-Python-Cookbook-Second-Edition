"""Python Cookbook 2nd ed.

Chapter 10, Bonus Material b.

Note: Output from this is used in Chapter 4 examples.
"""

from pathlib import Path
import csv
import datetime

# from types import SimpleNamespace as Waypoint
from dataclasses import dataclass


@dataclass
class Waypoint:
    lat: float
    lon: float
    timestamp: datetime.datetime


make_date = lambda txt: datetime.datetime.strptime(txt, "%Y-%m-%d").date()
make_time = lambda txt: datetime.datetime.strptime(txt, "%H:%M:%S").time()
make_timestamp = lambda date, time: datetime.datetime.combine(
    make_date(date), make_time(time)
)


def make_row(source):
    return Waypoint(
        lat=float(source["lat"]),
        lon=float(source["lon"]),
        timestamp=make_timestamp(source["date"], source["time"]),
    )


def wp_1(waypoints_path: Path):
    with waypoints_path.open() as waypoints_file:
        raw_reader = csv.DictReader(waypoints_file)
        for row in raw_reader:
            print(row)


def wp_2(waypoints_path: Path):
    with waypoints_path.open() as waypoints_file:
        raw_reader = csv.DictReader(waypoints_file)
        wp_reader = (make_row(row) for row in raw_reader)
        for row in wp_reader:
            print(row)


__test__ = {
    "wp_1": """
>>> waypoints_path = Path.cwd()/'data'/'waypoints.csv'
>>> wp_1(waypoints_path)
{'lat': '32.8321666666667', 'lon': '-79.9338333333333', 'date': '2012-11-27', 'time': '09:15:00'}
{'lat': '31.6714833333333', 'lon': '-80.93325', 'date': '2012-11-28', 'time': '00:00:00'}
{'lat': '30.7171666666667', 'lon': '-81.5525', 'date': '2012-11-28', 'time': '11:35:00'}
""",
    "wp_2": """
>>> waypoints_path = Path.cwd()/'data'/'waypoints.csv'
>>> wp_2(waypoints_path)
Waypoint(lat=32.8321666666667, lon=-79.9338333333333, timestamp=datetime.datetime(2012, 11, 27, 9, 15))
Waypoint(lat=31.6714833333333, lon=-80.93325, timestamp=datetime.datetime(2012, 11, 28, 0, 0))
Waypoint(lat=30.7171666666667, lon=-81.5525, timestamp=datetime.datetime(2012, 11, 28, 11, 35))
""",
}


if __name__ == "__main__":

    waypoints_path = Path.cwd() / "data" / "waypoints.csv"
    wp_1(waypoints_path)
    wp_2(waypoints_path)
