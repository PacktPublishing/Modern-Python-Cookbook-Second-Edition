"""Python Cookbook 2nd ed.

Chapter 9, recipe 2, Applying transformations to a collection
"""
import datetime
from Chapter_09.ch09_r01 import RawLog, DatedLog
from typing import Iterable, Iterator

from pprint import pprint


def parse_date(item: RawLog) -> DatedLog:
    date = datetime.datetime.strptime(item.date, "%Y-%m-%d %H:%M:%S,%f")
    return DatedLog(date, item.level, item.module, item.message)


test_parse_date = """
>>> item = RawLog("2016-04-24 11:05:01,462", "INFO", "module1", "Sample Message One")
>>> parse_date(item)
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 5, 1, 462000), level='INFO', module='module1', message='Sample Message One')
"""


def parse_date_iter(source: Iterable[RawLog]) -> Iterator[DatedLog]:
    for item in source:
        yield parse_date(item)


test_parse_date_generator_function = """
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
"""

test_parse_date_generator_expression = """
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
>>> for item in (parse_date(item) for item in data):
...     pprint(item)
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 5, 1, 462000), level='INFO', module='module1', message='Sample Message One')
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 6, 2, 624000), level='DEBUG', module='module2', message='Debugging')
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 7, 3, 246000), level='WARNING', module='module1', message='Something might have gone wrong')


>>> def parse_date_iter(source: Iterable[RawLog]) -> Iterator[DatedLog]:
...     return (parse_date(item) for item in source)
>>> for item in parse_date_iter(data):
...     pprint(item)
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 5, 1, 462000), level='INFO', module='module1', message='Sample Message One')
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 6, 2, 624000), level='DEBUG', module='module2', message='Debugging')
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 7, 3, 246000), level='WARNING', module='module1', message='Something might have gone wrong')
"""


test_parse_date_map_function = """
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
>>> for item in map(parse_date, data):
...     pprint(item)
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 5, 1, 462000), level='INFO', module='module1', message='Sample Message One')
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 6, 2, 624000), level='DEBUG', module='module2', message='Debugging')
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 7, 3, 246000), level='WARNING', module='module1', message='Something might have gone wrong')
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
