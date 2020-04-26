"""Python Cookbook 2nd ed.

Chapter 8, recipe 8, Deleting from a list of mappings
"""
from typing import (
    Iterable,
    Iterator,
    TypeVar,
    Dict,
    Any,
    TypedDict,
    List,
    Optional,
    cast,
)
from pprint import pprint

# Superficially correct, but very broad
# SongType = Dict[str, Any]

# Better

SongType = TypedDict("SongType", {"title": str, "writer": List[str], "time": str})

raw_data = """title,writer,time
Eruption,['Emerson'],2:43
Stones of Years,"['Emerson', 'Lake']",3:43
Iconoclast,['Emerson'],1:16
Mass,"['Emerson', 'Lake']",3:09
Manticore,['Emerson'],1:49
Battlefield,['Lake'],3:57
Aquatarkus,['Emerson'],3:54
"""

import ast


def build_song(row: Dict[str, str]) -> SongType:
    return SongType(
        title=row["title"], writer=ast.literal_eval(row["writer"]), time=row["time"]
    )


import csv
import io

rdr = csv.DictReader(io.StringIO(raw_data))
source: List[SongType] = list(map(build_song, filter(None, rdr)))

song_list: List[SongType] = [
    {"title": "Eruption", "writer": ["Emerson"], "time": "2:43"},
    {"title": "Stones of Years", "writer": ["Emerson", "Lake"], "time": "3:43"},
    {"title": "Iconoclast", "writer": ["Emerson"], "time": "1:16"},
    {"title": "Mass", "writer": ["Emerson", "Lake"], "time": "3:09"},
    {"title": "Manticore", "writer": ["Emerson"], "time": "1:49"},
    {"title": "Battlefield", "writer": ["Lake"], "time": "3:57"},
    {"title": "Aquatarkus", "writer": ["Emerson"], "time": "3:54"},
]

assert source == song_list, f"{source=} is not the same as {song_list=}"

test_find_lake = """
>>> for item in song_list:
...    if 'Lake' in item['writer']:
...        print("remove", item['title'])
remove Stones of Years
remove Mass
remove Battlefield
"""


def naive_delete(data: List[SongType], writer: str) -> None:
    for index in range(len(data)):
        if "Lake" in data[index]["writer"]:
            del data[index]


test_naive_delete = """
>>> song_list = source.copy()
>>> assert len(song_list) == 7

>>> naive_delete(song_list, 'Lake')
Traceback (most recent call last):
  File "/Applications/PyCharm CE.app/Contents/plugins/python-ce/helpers/pycharm/docrunner.py", line 138, in __run
    exec(compile(example.source, filename, "single",
  File "<doctest ch07_r08.__test__.test_naive_delete[2]>", line 1, in <module>
    naive_delete(song_list, 'Lake')
  File "Chapter_08.ch08_r08.py", line 72, in naive_delete
    if 'Lake' in data[index]['writer']:
IndexError: list index out of range
"""


def index_of_writer(data: List[SongType], writer: str) -> Optional[int]:
    for i in range(len(data)):
        if writer in data[i]["writer"]:
            return i
    return None


def multi_search_delete(data: List[SongType], writer: str) -> None:
    while (position := index_of_writer(data, "Lake")) is not None:
        # The cast is only because mypy 0.761 doesn't completely handle the walrus operator
        del data[cast(int, position)]  # or data.pop(position)


test_multi_search_delete = """
>>> song_list = source.copy()
>>> assert len(song_list) == 7

>>> multi_search_delete(song_list, 'Lake')
>>> pprint(song_list)
[{'time': '2:43', 'title': 'Eruption', 'writer': ['Emerson']},
 {'time': '1:16', 'title': 'Iconoclast', 'writer': ['Emerson']},
 {'time': '1:49', 'title': 'Manticore', 'writer': ['Emerson']},
 {'time': '3:54', 'title': 'Aquatarkus', 'writer': ['Emerson']}]
"""


def incremental_delete(data: List[SongType], writer: str) -> None:
    i = 0
    while i != len(data):
        if "Lake" in data[i]["writer"]:
            del data[i]
        else:
            i += 1


test_incremental_delete = """
>>> song_list = source.copy()
>>> assert len(song_list) == 7

>>> multi_search_delete(song_list, 'Lake')
>>> pprint(song_list)
[{'time': '2:43', 'title': 'Eruption', 'writer': ['Emerson']},
 {'time': '1:16', 'title': 'Iconoclast', 'writer': ['Emerson']},
 {'time': '1:49', 'title': 'Manticore', 'writer': ['Emerson']},
 {'time': '3:54', 'title': 'Aquatarkus', 'writer': ['Emerson']}]
"""


def remover(sub_list: List[SongType], writer: str) -> List[SongType]:
    if len(sub_list) == 0:
        return []
    head, *tail = sub_list
    if writer in head["writer"]:
        return remover(tail, writer)
    else:
        return [head] + remover(tail, writer)


test_recursive_remover = """
>>> song_list = source.copy()
>>> assert len(song_list) == 7

>>> pprint(remover(song_list, 'Lake'))
[{'time': '2:43', 'title': 'Eruption', 'writer': ['Emerson']},
 {'time': '1:16', 'title': 'Iconoclast', 'writer': ['Emerson']},
 {'time': '1:49', 'title': 'Manticore', 'writer': ['Emerson']},
 {'time': '3:54', 'title': 'Aquatarkus', 'writer': ['Emerson']}]
"""


def copy_exclude(data: List[SongType], writer: str) -> List[SongType]:
    return [item for item in data if writer not in item["writer"]]


test_filtered_copy = """
>>> song_list = source.copy()
>>> assert len(song_list) == 7

>>> data = copy_exclude(song_list, 'Lake')
>>> pprint(data)
[{'time': '2:43', 'title': 'Eruption', 'writer': ['Emerson']},
 {'time': '1:16', 'title': 'Iconoclast', 'writer': ['Emerson']},
 {'time': '1:49', 'title': 'Manticore', 'writer': ['Emerson']},
 {'time': '3:54', 'title': 'Aquatarkus', 'writer': ['Emerson']}]
"""


def copy_exclude_2(data: List[SongType], writer: str) -> List[SongType]:
    return list(filter(lambda item: writer not in item["writer"], data))


test_another_filter = """
>>> data = copy_exclude_2(song_list, 'Lake')
>>> pprint(data)
[{'time': '2:43', 'title': 'Eruption', 'writer': ['Emerson']},
 {'time': '1:16', 'title': 'Iconoclast', 'writer': ['Emerson']},
 {'time': '1:49', 'title': 'Manticore', 'writer': ['Emerson']},
 {'time': '3:54', 'title': 'Aquatarkus', 'writer': ['Emerson']}]
"""


# A little advanced. A lead-in to Chapter 8...
def writer_exclude_iter(source: Iterable[SongType], writer: str) -> Iterator[SongType]:
    for item in source:
        if writer in item["writer"]:
            continue
        yield item


test_generator = """
>>> data = list(writer_exclude_iter(song_list, 'Lake'))
>>> pprint(data)
[{'time': '2:43', 'title': 'Eruption', 'writer': ['Emerson']},
 {'time': '1:16', 'title': 'Iconoclast', 'writer': ['Emerson']},
 {'time': '1:49', 'title': 'Manticore', 'writer': ['Emerson']},
 {'time': '3:54', 'title': 'Aquatarkus', 'writer': ['Emerson']}]
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
