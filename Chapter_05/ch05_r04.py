"""Python Cookbook 2nd ed.

Chapter 5, recipe 4, Dictionary-Related type hints
"""

import collections
import csv
import datetime
from pathlib import Path
from typing import List, Dict, Iterable, Iterator


def get_fuel_use(source_path: Path) -> List[Dict[str, str]]:
    with source_path.open() as source_file:
        rdr = csv.DictReader(source_file)
        data: List[Dict[str, str]] = list(rdr)
    return data


test_get_fuel_use = """
>>> source_path = Path("data/fuel2.csv")
>>> fuel_use = get_fuel_use(source_path)
>>> for row in fuel_use:
...      print(row)
{'date': '10/25/13', 'engine on': '08:24:00', 'fuel height on': '29', 'engine off': '13:15:00', 'fuel height off': '27'}
{'date': '10/26/13', 'engine on': '09:12:00', 'fuel height on': '27', 'engine off': '18:25:00', 'fuel height off': '22'}
{'date': '10/28/13', 'engine on': '13:21:00', 'fuel height on': '22', 'engine off': '06:25:00', 'fuel height off': '14'}
"""

from mypy_extensions import TypedDict

History = TypedDict(
    "History",
    {
        "date": datetime.date,
        "start_time": datetime.time,
        "start_fuel": float,
        "end_time": datetime.time,
        "end_fuel": float,
    },
)


def make_history(source: Iterable[Dict[str, str]]) -> Iterator[History]:
    for row in source:
        yield dict(
            date=datetime.datetime.strptime(row["date"], "%m/%d/%y").date(),
            start_time=datetime.datetime.strptime(row["engine on"], "%H:%M:%S").time(),
            start_fuel=float(row["fuel height on"]),
            end_time=datetime.datetime.strptime(row["engine off"], "%H:%M:%S").time(),
            end_fuel=float(row["fuel height off"]),
        )


test_get_fuel_history = """
>>> source_path = Path("data/fuel2.csv")
>>> fuel_use = make_history(get_fuel_use(source_path))
>>> for row in fuel_use:
...      print(row)
{'date': datetime.date(2013, 10, 25), 'start_time': datetime.time(8, 24), 'start_fuel': 29.0, 'end_time': datetime.time(13, 15), 'end_fuel': 27.0}
{'date': datetime.date(2013, 10, 26), 'start_time': datetime.time(9, 12), 'start_fuel': 27.0, 'end_time': datetime.time(18, 25), 'end_fuel': 22.0}
{'date': datetime.date(2013, 10, 28), 'start_time': datetime.time(13, 21), 'start_fuel': 22.0, 'end_time': datetime.time(6, 25), 'end_fuel': 14.0}
"""

from typing import NamedTuple

HistoryT = NamedTuple(
    "HistoryT",
    [
        ("date", datetime.date),
        ("start_time", datetime.time),
        ("start_fuel", float),
        ("end_time", datetime.time),
        ("end_fuel", float),
    ],
)


def make_history_t(source: Iterable[Dict[str, str]]) -> Iterator[HistoryT]:
    for row in source:
        yield HistoryT(
            date=datetime.datetime.strptime(row["date"], "%m/%d/%y").date(),
            start_time=datetime.datetime.strptime(row["engine on"], "%H:%M:%S").time(),
            start_fuel=float(row["fuel height on"]),
            end_time=datetime.datetime.strptime(row["engine off"], "%H:%M:%S").time(),
            end_fuel=float(row["fuel height off"]),
        )


test_get_fuel_history_namedtyple = """
>>> source_path = Path("data/fuel2.csv")
>>> fuel_use = make_history_t(get_fuel_use(source_path))
>>> for row in fuel_use:
...      print(row._asdict())
{'date': datetime.date(2013, 10, 25), 'start_time': datetime.time(8, 24), 'start_fuel': 29.0, 'end_time': datetime.time(13, 15), 'end_fuel': 27.0}
{'date': datetime.date(2013, 10, 26), 'start_time': datetime.time(9, 12), 'start_fuel': 27.0, 'end_time': datetime.time(18, 25), 'end_fuel': 22.0}
{'date': datetime.date(2013, 10, 28), 'start_time': datetime.time(13, 21), 'start_fuel': 22.0, 'end_time': datetime.time(6, 25), 'end_fuel': 14.0}
"""

result: History = {"date": 42}  # type: ignore
# Chapter_05/ch04_r04.py:98: error: Keys ('start_time', 'start_fuel', 'end_time', 'end_fuel') missing for TypedDict "History"

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
