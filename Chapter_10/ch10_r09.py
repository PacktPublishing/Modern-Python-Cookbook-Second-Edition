"""Python Cookbook 2nd ed.

Chapter 10, recipe 9, Refactoring a csv DictReader to a dataclass reader
"""

import csv
import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, ClassVar, Dict, Tuple


def show_waypoints_raw(data_path: Path) -> None:
    with data_path.open() as data_file:
        data_reader = csv.DictReader(data_file)
        for row in data_reader:
            ts_date = datetime.datetime.strptime(row["date"], "%Y-%m-%d").date()
            ts_time = datetime.datetime.strptime(row["time"], "%H:%M:%S").time()
            timestamp = datetime.datetime.combine(ts_date, ts_time)
            lat_lon = (float(row["lat"]), float(row["lon"]))
            print(f"{timestamp:%m-%d %H:%M}, " f"{lat_lon[0]:.3f} {lat_lon[1]:.3f}")


test_legacy = """
>>> show_waypoints_raw(Path("data/waypoints.csv"))
11-27 09:15, 32.832 -79.934
11-28 00:00, 31.671 -80.933
11-28 11:35, 30.717 -81.552
"""


@dataclass
class Waypoint_1:
    arrival_date: str
    arrival_time: str
    lat: str
    lon: str
    _timestamp: Optional[datetime.datetime] = field(init=False, default=None)

    @staticmethod
    def from_source(row: Dict[str, str]) -> "Waypoint_1":
        name_map = {
            "date": "arrival_date",
            "time": "arrival_time",
            "lat": "lat",
            "lon": "lon",
        }
        return Waypoint_1(**{name_map[header]: value for header, value in row.items()})

    @property
    def arrival(self):
        if self._timestamp is None:
            ts_date = datetime.datetime.strptime(self.arrival_date, "%Y-%m-%d").date()
            ts_time = datetime.datetime.strptime(self.arrival_time, "%H:%M:%S").time()
            self._timestamp = datetime.datetime.combine(ts_date, ts_time)
        return self._timestamp

    @property
    def lat_lon(self):
        return float(self.lat), float(self.lon)


def show_waypoints_1(data_path: Path) -> None:
    with data_path.open() as data_file:
        data_reader = csv.DictReader(data_file)
        waypoint_iter = (Waypoint_1.from_source(row) for row in data_reader)
        for row in waypoint_iter:
            print(
                f"{row.arrival:%m-%d %H:%M}, "
                f"{row.lat_lon[0]:.3f} "
                f"{row.lat_lon[1]:.3f}"
            )


test_v2 = """
>>> Waypoint_1.from_source({"date": "2019-09-10", "time": "11:12:13", "lat": "1", "lon": "2"})
Waypoint_1(arrival_date='2019-09-10', arrival_time='11:12:13', lat='1', lon='2', _timestamp=None)
>>> show_waypoints_1(Path("data/waypoints.csv"))
11-27 09:15, 32.832 -79.934
11-28 00:00, 31.671 -80.933
11-28 11:35, 30.717 -81.552
"""


@dataclass
class Waypoint_2:
    arrival: datetime.datetime
    lat_lon: Tuple[float, float]

    @staticmethod
    def from_source(row: Dict[str, str]) -> Optional["Waypoint_2"]:
        try:
            ts_date = datetime.datetime.strptime(row["date"], "%Y-%m-%d").date()
            ts_time = datetime.datetime.strptime(row["time"], "%H:%M:%S").time()
            arrival = datetime.datetime.combine(ts_date, ts_time)
            return Waypoint_2(
                arrival=arrival, lat_lon=(float(row["lat"]), float(row["lon"]))
            )
        except (ValueError, KeyError):
            return None


def show_waypoints_2(data_path: Path) -> None:
    with data_path.open() as data_file:
        data_reader = csv.DictReader(data_file)
        waypoint_iter = (Waypoint_2.from_source(row) for row in data_reader)
        for row in filter(None, waypoint_iter):
            print(
                f"{row.arrival:%m-%d %H:%M}, "
                f"{row.lat_lon[0]:.3f} "
                f"{row.lat_lon[1]:.3f}"
            )


test_v2 = """
>>> Waypoint_2.from_source({"date": "2019-09-10", "time": "11:12:13", "lat": "1", "lon": "2"})
Waypoint_2(arrival=datetime.datetime(2019, 9, 10, 11, 12, 13), lat_lon=(1.0, 2.0))
>>> Waypoint_2.from_source({"date": "", "time": "", "lat": "", "lon": ""})
>>> show_waypoints_2(Path("data/waypoints.csv"))
11-27 09:15, 32.832 -79.934
11-28 00:00, 31.671 -80.933
11-28 11:35, 30.717 -81.552
"""


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
