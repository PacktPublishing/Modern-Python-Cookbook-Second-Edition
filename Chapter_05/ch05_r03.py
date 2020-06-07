"""Python Cookbook 2nd ed.

Chapter 5, recipe 3, Controlling the order of dict keys
"""

import collections
import csv
from pathlib import Path
from typing import List, Dict, cast, Sequence


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


def get_fuel_use_od(source_path: Path) -> List[Dict[str, str]]:
    with source_path.open() as source_file:
        rdr = csv.DictReader(source_file)
        od = (
            collections.OrderedDict(
                [(column, row[column])
                 for column in cast(Sequence[str], rdr.fieldnames)]
            )
            for row in rdr
        )
        data: List[Dict[str, str]] = list(od)
    return data


test_get_fuel_use_od = """
>>> source_path = Path("data/fuel2.csv")
>>> fuel_use = get_fuel_use_od(source_path)
>>> for row in fuel_use:
...      print(row)
OrderedDict([('date', '10/25/13'), ('engine on', '08:24:00'), ('fuel height on', '29'), ('engine off', '13:15:00'), ('fuel height off', '27')])
OrderedDict([('date', '10/26/13'), ('engine on', '09:12:00'), ('fuel height on', '27'), ('engine off', '18:25:00'), ('fuel height off', '22')])
OrderedDict([('date', '10/28/13'), ('engine on', '13:21:00'), ('fuel height on', '22'), ('engine off', '06:25:00'), ('fuel height off', '14')])
"""

import datetime

parse_date = lambda text: datetime.datetime.strptime(text, "%m/%d/%y").date()
parse_time = lambda text: datetime.datetime.strptime(text, "%H:%M:%S").time()


def summarize(data: List[Dict[str, str]]) -> None:
    for row in data:
        date = parse_date(row["date"])
        start = datetime.datetime.combine(date, parse_time(row["engine on"]))
        end = datetime.datetime.combine(date, parse_time(row["engine off"]))
        print(
            f"{(end-start).seconds/60/60:.1f} hr. {float(row['fuel height on'])} in. to {float(row['fuel height off'])} in."
        )


test_summarize = """
>>> source_path = Path("data/fuel2.csv")
>>> fuel_use = get_fuel_use_od(source_path)
>>> summarize(fuel_use)
4.8 hr. 29.0 in. to 27.0 in.
9.2 hr. 27.0 in. to 22.0 in.
17.1 hr. 22.0 in. to 14.0 in.
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
