"""Python Cookbook 2nd ed.

Chapter 10, recipe 6, Reading JSON and YAML documents

Note: Output from this is used in Chapter 4 examples.
"""

import json
from pathlib import Path


def race_summary(source_path: Path) -> None:
    document = json.loads(source_path.read_text())

    for n, leg in enumerate(document["legs"]):
        print(leg)
        for team_finishes in document["teams"]:
            print(team_finishes["name"], team_finishes["position"][n])


test_summary = """
>>> race_summary(source_path=Path("data") / "race_result.json")  # doctest: +ELLIPSIS
ALICANTE - CAPE TOWN
Abu Dhabi Ocean Racing 1
Team Brunel 3
Dongfeng Race Team 2
MAPFRE 7
Team Alvimedica 5
Team SCA 6
Team Vestas Wind 4
...
LORIENT - GOTHENBURG
Abu Dhabi Ocean Racing 5
Team Brunel 2
Dongfeng Race Team 4
MAPFRE 3
Team Alvimedica 1
Team SCA 7
Team Vestas Wind 6

"""

from typing import Any, Union, Dict
import datetime


def default_date(object: Any) -> Union[Any, Dict[str, Any]]:
    if isinstance(object, datetime.datetime):
        return {"$date": object.isoformat()}
    return object


test_default_date = """
>>> example_date = datetime.datetime(2014, 6, 7, 8, 9, 10)
>>> document = {'date': example_date}
>>> print(
...     json.dumps(document, default=default_date, indent=2))
{
  "date": {
    "$date": "2014-06-07T08:09:10"
  }
}
"""


def as_date(object: Dict[str, Any]) -> Union[Any, Dict[str, Any]]:
    if {"$date"} == set(object.keys()):
        # return datetime.datetime.strptime(object["$date"], "%Y-%m-%dT%H:%M:%S")
        return datetime.datetime.fromisoformat(object["$date"])
    return object


test_as_date = """
>>> source = '''{"date": {"$date": "2014-06-07T08:09:10"}}'''
>>> json.loads(source, object_hook=as_date)
{'date': datetime.datetime(2014, 6, 7, 8, 9, 10)}
"""


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
