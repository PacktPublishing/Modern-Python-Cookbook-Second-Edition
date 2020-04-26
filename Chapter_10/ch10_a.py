"""Python Cookbook 2nd ed.

Chapter 10, Bonus Material a.

Note: Output from this is used in Chapter 4 examples.
"""

from pathlib import Path
import csv
import datetime
from typing import NamedTuple

# from collections import namedtuple
# Waypoint = namedtuple('Waypoint', ['lat', 'lon', 'date', 'time'])


class Waypoint(NamedTuple):
    """Raw data, values are strings"""

    lat: str
    lon: str
    date: str
    time: str


# Waypoint_Data = namedtuple('Waypoint_Data', ['lat', 'lon', 'timestamp'])
class Waypoint_Data(NamedTuple):
    lat: float
    lon: float
    timestamp: datetime.datetime


import datetime

parse_date = lambda txt: datetime.datetime.strptime(txt, "%Y-%m-%d").date()
parse_time = lambda txt: datetime.datetime.strptime(txt, "%H:%M:%S").time()


def convert_waypoint(waypoint: Waypoint) -> Waypoint_Data:
    return Waypoint_Data(
        lat=float(waypoint.lat),
        lon=float(waypoint.lon),
        timestamp=datetime.datetime.combine(
            parse_date(waypoint.date), parse_time(waypoint.time)
        ),
    )


def wp_0(waypoints_path: Path) -> None:
    with waypoints_path.open() as waypoints_file:
        raw_reader = csv.reader(waypoints_file)
        waypoints_reader = (Waypoint(*row) for row in raw_reader)
        for row in waypoints_reader:
            print(row)


def wp_1(waypoints_path: Path) -> None:
    with waypoints_path.open() as waypoints_file:
        raw_reader = csv.reader(waypoints_file)
        skip_header = filter(lambda row: row[0] != "lat", raw_reader)
        waypoints_reader = (Waypoint(*row) for row in skip_header)
        waypoints_data_reader = (convert_waypoint(wp) for wp in waypoints_reader)

        for row_data in waypoints_data_reader:
            print(row_data.lat, row_data.lon, row_data.timestamp)


def wp_2(waypoints_path: Path) -> None:
    from itertools import starmap

    with waypoints_path.open() as waypoints_file:
        raw_reader = csv.reader(waypoints_file)
        waypoint_raw_reader = starmap(Waypoint, raw_reader)
        for raw_row in waypoint_raw_reader:
            print(raw_row)


__test__ = {
    "wp_0": """
>>> waypoints_path = Path.cwd()/'data'/'waypoints.csv'
>>> wp_0(waypoints_path)
Waypoint(lat='lat', lon='lon', date='date', time='time')
Waypoint(lat='32.8321666666667', lon='-79.9338333333333', date='2012-11-27', time='09:15:00')
Waypoint(lat='31.6714833333333', lon='-80.93325', date='2012-11-28', time='00:00:00')
Waypoint(lat='30.7171666666667', lon='-81.5525', date='2012-11-28', time='11:35:00')
""",
    "wp_1": """
>>> waypoints_path = Path.cwd()/'data'/'waypoints.csv'
>>> wp_1(waypoints_path)
32.8321666666667 -79.9338333333333 2012-11-27 09:15:00
31.6714833333333 -80.93325 2012-11-28 00:00:00
30.7171666666667 -81.5525 2012-11-28 11:35:00
""",
    "wp_2": """
>>> waypoints_path = Path.cwd()/'data'/'waypoints.csv'
>>> wp_2(waypoints_path)
Waypoint(lat='lat', lon='lon', date='date', time='time')
Waypoint(lat='32.8321666666667', lon='-79.9338333333333', date='2012-11-27', time='09:15:00')
Waypoint(lat='31.6714833333333', lon='-80.93325', date='2012-11-28', time='00:00:00')
Waypoint(lat='30.7171666666667', lon='-81.5525', date='2012-11-28', time='11:35:00')
""",
}

if __name__ == "__main__":
    waypoints_path = Path.cwd() / "data" / "waypoints.csv"
    wp_0(waypoints_path)
    wp_1(waypoints_path)
    wp_2(waypoints_path)
