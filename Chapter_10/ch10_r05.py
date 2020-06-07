"""Python Cookbook 2nd ed.

Chapter 10, recipe 5, Reading complex formats using regular expressions

Note: Output from this is used in Chapter 4 examples.
"""

import re
from pathlib import Path
from pprint import pprint
from typing import Dict, Any, cast, Match, NamedTuple

pattern_text = (
    r"\[   (?P<date>.*?)  \]\s+"
    r"     (?P<level>\w+)   \s+"
    r"in\s+(?P<module>\S+?)"
    r":\s+ (?P<message>.+)"
)
pattern = re.compile(pattern_text, re.X)


class LogLine(NamedTuple):
    date: str
    level: str
    module: str
    message: str


def log_parser(source_line: str) -> LogLine:
    """
    >>> log_parser("[2019-11-07 11:12:13,098765] info in this.module: example message")
    LogLine(date='2019-11-07 11:12:13,098765', level='info', module='this.module', message='example message')
    """
    # match = pattern.match(source_line)
    # if match:
    if match := pattern.match(source_line):
        # Chapter_10/ch10_r03.py:38: error: Item "None" of "Optional[Match[str]]" has no attribute "groupdict"
        # Force non-None consideration by cast(Match, match).groupdict()
        data = cast(Match, match).groupdict()
        return LogLine(**data)
    raise ValueError(f"Unexpected input {source_line=}")


def raw() -> None:
    data_path = Path("data") / "sample.log"
    with data_path.open() as data_file:
        data_reader = map(log_parser, data_file)
        for row in data_reader:
            pprint(row)


import csv


def copy(data_path: Path) -> None:
    target_path = data_path.with_suffix(".csv")
    with target_path.open("w", newline="") as target_file:
        writer = csv.DictWriter(target_file, LogLine._fields)
        writer.writeheader()

        with data_path.open() as data_file:
            reader = map(log_parser, data_file)
            writer.writerows(row._asdict() for row in reader)


test_raw = """
>>> raw()
LogLine(date='2016-06-15 17:57:54,715', level='INFO', module='ch10_r10', message='Sample Message One')
LogLine(date='2016-06-15 17:57:54,715', level='DEBUG', module='ch10_r10', message='Debugging')
LogLine(date='2016-06-15 17:57:54,715', level='WARNING', module='ch10_r10', message='Something might have gone wrong')
"""

test_copy = """
>>> copy(data_path = Path("data") / "sample.log")
>>> import csv
>>> result_path = Path("data") / "sample.csv"
>>> with result_path.open() as result_file:
...     rdr = csv.DictReader(result_file)
...     data = list(rdr)
>>> pprint(data)  # doctest: +NORMALIZE_WHITESPACE
[{'date': '2016-06-15 17:57:54,715',
  'level': 'INFO',
  'message': 'Sample Message One',
  'module': 'ch10_r10'},
 {'date': '2016-06-15 17:57:54,715',
  'level': 'DEBUG',
  'message': 'Debugging',
  'module': 'ch10_r10'},
 {'date': '2016-06-15 17:57:54,715',
  'level': 'WARNING',
  'message': 'Something might have gone wrong',
  'module': 'ch10_r10'}]
"""


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
