"""Python Cookbook 2nd ed.

Chapter 10, recipe 4, Using data classes to simplify working with CSV files

Note: Output from this is used in Chapter 4 examples.
"""
import csv
from dataclasses import dataclass, field
import datetime
from pathlib import Path
from pprint import pprint
from typing import Tuple, Iterator, Dict, Union


@dataclass
class RawRow:
    date: str
    time: str
    lat: str
    lon: str


@dataclass
class Waypoint:
    raw: RawRow
    lat_lon: Tuple[float, float] = field(init=False)
    ts_date: datetime.date = field(init=False)
    ts_time: datetime.time = field(init=False)
    timestamp: datetime.datetime = field(init=False)

    def __post_init__(self):
        self.ts_date = datetime.datetime.strptime(self.raw.date, "%Y-%m-%d").date()
        self.ts_time = datetime.datetime.strptime(self.raw.time, "%H:%M:%S").time()
        self.lat_lon = (float(self.raw.lat), float(self.raw.lon))
        self.timestamp = datetime.datetime.combine(self.ts_date, self.ts_time)


def waypoint_iter(reader: csv.DictReader) -> Iterator[Waypoint]:
    for row in reader:
        raw = RawRow(**row)
        yield Waypoint(raw)


def display(data_path: Path) -> None:
    with data_path.open() as data_file:
        data_reader = csv.DictReader(data_file)
        for waypoint in waypoint_iter(data_reader):
            pprint(waypoint)


test_clean = """
>>> display(Path("data/waypoints.csv"))  # doctest: +NORMALIZE_WHITESPACE
Waypoint(raw=RawRow(date='2012-11-27', time='09:15:00', lat='32.8321666666667', lon='-79.9338333333333'), lat_lon=(32.8321666666667, -79.9338333333333), ts_date=datetime.date(2012, 11, 27), ts_time=datetime.time(9, 15), timestamp=datetime.datetime(2012, 11, 27, 9, 15))
Waypoint(raw=RawRow(date='2012-11-28', time='00:00:00', lat='31.6714833333333', lon='-80.93325'), lat_lon=(31.6714833333333, -80.93325), ts_date=datetime.date(2012, 11, 28), ts_time=datetime.time(0, 0), timestamp=datetime.datetime(2012, 11, 28, 0, 0))
Waypoint(raw=RawRow(date='2012-11-28', time='11:35:00', lat='30.7171666666667', lon='-81.5525'), lat_lon=(30.7171666666667, -81.5525), ts_date=datetime.date(2012, 11, 28), ts_time=datetime.time(11, 35), timestamp=datetime.datetime(2012, 11, 28, 11, 35))
"""


@dataclass
class RawRow_HeaderV2:
    source: Dict[str, str]
    date: str = field(init=False)
    time: str = field(init=False)
    lat: str = field(init=False)
    lon: str = field(init=False)

    def __post_init__(self):
        self.date = self.source["Date of Travel (YYYY-MM-DD)"]
        self.time = self.source["Arrival Time (HH:MM:SS)"]
        self.lat = self.source["Latitude (degrees N)"]
        self.lon = self.source["Logitude (degrees W)"]


Raw = Union[RawRow, RawRow_HeaderV2]

test_raw_row_Headerv2 = """
>>> row = {
...     'Date of Travel (YYYY-MM-DD)': '2012-11-28', 
...     'Arrival Time (HH:MM:SS)': '11:35:00', 
...     'Latitude (degrees N)': '30.7171666666667', 
...     'Logitude (degrees W)': '-81.5525'}
>>> raw = RawRow_HeaderV2(row)
>>> raw
RawRow_HeaderV2(source={'Date of Travel (YYYY-MM-DD)': '2012-11-28', 'Arrival Time (HH:MM:SS)': '11:35:00', 'Latitude (degrees N)': '30.7171666666667', 'Logitude (degrees W)': '-81.5525'}, date='2012-11-28', time='11:35:00', lat='30.7171666666667', lon='-81.5525')
>>> Waypoint(raw)
Waypoint(raw=RawRow_HeaderV2(source={'Date of Travel (YYYY-MM-DD)': '2012-11-28', 'Arrival Time (HH:MM:SS)': '11:35:00', 'Latitude (degrees N)': '30.7171666666667', 'Logitude (degrees W)': '-81.5525'}, date='2012-11-28', time='11:35:00', lat='30.7171666666667', lon='-81.5525'), lat_lon=(30.7171666666667, -81.5525), ts_date=datetime.date(2012, 11, 28), ts_time=datetime.time(11, 35), timestamp=datetime.datetime(2012, 11, 28, 11, 35))
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
