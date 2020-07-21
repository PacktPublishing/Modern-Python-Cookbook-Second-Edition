"""Python Cookbook 2nd ed.

Chapter 10, recipe 3, Reading delimited files with the csv module

Note: Output from this is used in Chapter 4 examples.
"""

import csv
import datetime
from pathlib import Path
from pprint import pprint
from typing import Iterable, Iterator, Dict, Any, TypedDict, Tuple, cast


def raw(data_path: Path) -> None:
    with data_path.open() as data_file:
        data_reader = csv.DictReader(data_file)
        for row in data_reader:
            pprint(row)


Raw = Dict[str, Any]
Waypoint = Dict[str, Any]


def clean_row(source_row: Raw) -> Waypoint:
    ts_date = datetime.datetime.strptime(source_row["date"], "%Y-%m-%d").date()
    ts_time = datetime.datetime.strptime(source_row["time"], "%H:%M:%S").time()
    return dict(
        date=source_row["date"],
        time=source_row["time"],
        lat=source_row["lat"],
        lon=source_row["lon"],
        lat_lon=(float(source_row["lat"]), float(source_row["lon"])),
        ts_date=ts_date,
        ts_time=ts_time,
        timestamp=datetime.datetime.combine(ts_date, ts_time),
    )


def cleanse(reader: csv.DictReader) -> Iterator[Waypoint]:
    for row in reader:
        yield clean_row(cast(Raw, row))


def display_clean(data_path: Path) -> None:
    with data_path.open() as data_file:
        data_reader = csv.DictReader(data_file)
        clean_data_reader = cleanse(data_reader)
        for row in clean_data_reader:
            pprint(row)


test_raw = """
>>> raw(Path("data/waypoints.csv"))
{'date': '2012-11-27',
 'lat': '32.8321666666667',
 'lon': '-79.9338333333333',
 'time': '09:15:00'}
{'date': '2012-11-28',
 'lat': '31.6714833333333',
 'lon': '-80.93325',
 'time': '00:00:00'}
{'date': '2012-11-28',
 'lat': '30.7171666666667',
 'lon': '-81.5525',
 'time': '11:35:00'}
"""

test_clean = """
>>> display_clean(Path("data/waypoints.csv"))
{'date': '2012-11-27',
 'lat': '32.8321666666667',
 'lat_lon': (32.8321666666667, -79.9338333333333),
 'lon': '-79.9338333333333',
 'time': '09:15:00',
 'timestamp': datetime.datetime(2012, 11, 27, 9, 15),
 'ts_date': datetime.date(2012, 11, 27),
 'ts_time': datetime.time(9, 15)}
{'date': '2012-11-28',
 'lat': '31.6714833333333',
 'lat_lon': (31.6714833333333, -80.93325),
 'lon': '-80.93325',
 'time': '00:00:00',
 'timestamp': datetime.datetime(2012, 11, 28, 0, 0),
 'ts_date': datetime.date(2012, 11, 28),
 'ts_time': datetime.time(0, 0)}
{'date': '2012-11-28',
 'lat': '30.7171666666667',
 'lat_lon': (30.7171666666667, -81.5525),
 'lon': '-81.5525',
 'time': '11:35:00',
 'timestamp': datetime.datetime(2012, 11, 28, 11, 35),
 'ts_date': datetime.date(2012, 11, 28),
 'ts_time': datetime.time(11, 35)}
"""


# Alternative Definitions


class Raw_TD(TypedDict):
    date: str
    time: str
    lat: str
    lon: str


class Waypoint_TD(Raw_TD):
    lat_lon: Tuple[float, float]
    ts_date: datetime.date
    ts_time: datetime.time
    timestamp: datetime.datetime


def clean_row_td(source_row: Raw_TD) -> Waypoint_TD:
    ts_date = datetime.datetime.strptime(source_row["date"], "%Y-%m-%d").date()
    ts_time = datetime.datetime.strptime(source_row["time"], "%H:%M:%S").time()
    return Waypoint_TD(
        date=source_row["date"],
        time=source_row["time"],
        lat=source_row["lat"],
        lon=source_row["lon"],
        lat_lon=(float(source_row["lat"]), float(source_row["lon"])),
        ts_date=ts_date,
        ts_time=ts_time,
        timestamp=datetime.datetime.combine(ts_date, ts_time),
    )


def cleanse_td(reader: csv.DictReader) -> Iterator[Waypoint_TD]:
    for row in reader:
        yield clean_row_td(cast(Raw_TD, row))


def display_clean_td(data_path: Path) -> None:
    with data_path.open() as data_file:
        data_reader = csv.DictReader(data_file)
        clean_data_reader = cleanse_td(data_reader)
        for row in clean_data_reader:
            pprint(row)
            assert row['date'] == row['ts_date'].strftime("%Y-%m-%d")


test_clean_td = """
>>> display_clean_td(Path("data/waypoints.csv"))
{'date': '2012-11-27',
 'lat': '32.8321666666667',
 'lat_lon': (32.8321666666667, -79.9338333333333),
 'lon': '-79.9338333333333',
 'time': '09:15:00',
 'timestamp': datetime.datetime(2012, 11, 27, 9, 15),
 'ts_date': datetime.date(2012, 11, 27),
 'ts_time': datetime.time(9, 15)}
{'date': '2012-11-28',
 'lat': '31.6714833333333',
 'lat_lon': (31.6714833333333, -80.93325),
 'lon': '-80.93325',
 'time': '00:00:00',
 'timestamp': datetime.datetime(2012, 11, 28, 0, 0),
 'ts_date': datetime.date(2012, 11, 28),
 'ts_time': datetime.time(0, 0)}
{'date': '2012-11-28',
 'lat': '30.7171666666667',
 'lat_lon': (30.7171666666667, -81.5525),
 'lon': '-81.5525',
 'time': '11:35:00',
 'timestamp': datetime.datetime(2012, 11, 28, 11, 35),
 'ts_date': datetime.date(2012, 11, 28),
 'ts_time': datetime.time(11, 35)}
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
