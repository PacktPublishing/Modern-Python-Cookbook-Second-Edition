"""Python Cookbook 2nd ed.

Chapter 9, recipe 1, Writing generator functions with the yield statement
"""
import datetime
from pprint import pprint
import re
from typing import Tuple, Iterable, Iterator, NamedTuple, Match, cast


class RawLog(NamedTuple):
    date: str
    level: str
    module: str
    message: str


def parse_line_iter(source: Iterable[str]) -> Iterator[RawLog]:
    pattern = re.compile(
        r"\[   (?P<date>.*?)  \]\s+"
        r"     (?P<level>\w+)   \s+"
        r"in\s+(?P<module>.+?)"
        r":\s+ (?P<message>.+)",
        re.X
    )
    for line in source:
        if match := pattern.match(line):
            yield RawLog(*cast(Match, match).groups())


test_parse_line_iter = """
>>> log_lines = [
...     '[2016-04-24 11:05:01,462] INFO in module1: Sample Message One',
...     '[2016-04-24 11:06:02,624] DEBUG in module2: Debugging',
...     '[2016-04-24 11:07:03,246] WARNING in module1: Something might have gone wrong'
... ]
>>> for item in parse_line_iter(log_lines):
...     pprint(item)
RawLog(date='2016-04-24 11:05:01,462', level='INFO', module='module1', message='Sample Message One')
RawLog(date='2016-04-24 11:06:02,624', level='DEBUG', module='module2', message='Debugging')
RawLog(date='2016-04-24 11:07:03,246', level='WARNING', module='module1', message='Something might have gone wrong')
"""


class DatedLog(NamedTuple):
    date: datetime.datetime
    level: str
    module: str
    message: str


def parse_date_iter(source: Iterable[RawLog]) -> Iterator[DatedLog]:
    for item in source:
        date = datetime.datetime.strptime(item.date, "%Y-%m-%d %H:%M:%S,%f")
        yield DatedLog(date, item.level, item.module, item.message)


def parse_date(item: RawLog) -> DatedLog:
    date = datetime.datetime.strptime(item.date, "%Y-%m-%d %H:%M:%S,%f")
    return DatedLog(date, item.level, item.module, item.message)


test_parse_date_iter = """
>>> data = [
...     RawLog("2016-04-24 11:05:01,462", "INFO", "module1", "Sample Message One"),
...     RawLog("2016-04-24 11:06:02,624", "DEBUG", "module2", "Debugging"),
...     RawLog(
...         "2016-04-24 11:07:03,246",
...         "WARNING",
...         "module1",
...         "Something might have gone wrong",
...     ),
... ]
>>> for item in parse_date_iter(data):
...     pprint(item)
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 5, 1, 462000), level='INFO', module='module1', message='Sample Message One')
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 6, 2, 624000), level='DEBUG', module='module2', message='Debugging')
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 7, 3, 246000), level='WARNING', module='module1', message='Something might have gone wrong')

>>> details = list(parse_date_iter(data))
>>> len(details)
3

>>> parse_date_iter(data) # doctest: +ELLIPSIS
<generator object parse_date_iter at 0x...>

>>> iter(parse_date_iter(data)) # doctest: +ELLIPSIS
<generator object parse_date_iter at 0x...>

"""

test_combined = """
>>> log_lines = [
...     '[2016-04-24 11:05:01,462] INFO in module1: Sample Message One',
...     '[2016-04-24 11:06:02,624] DEBUG in module2: Debugging',
...     '[2016-04-24 11:07:03,246] WARNING in module1: Something might have gone wrong'
... ]
>>> for item in parse_date_iter(parse_line_iter(log_lines)):
...     pprint(item)
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 5, 1, 462000), level='INFO', module='module1', message='Sample Message One')
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 6, 2, 624000), level='DEBUG', module='module2', message='Debugging')
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 7, 3, 246000), level='WARNING', module='module1', message='Something might have gone wrong')
"""


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
