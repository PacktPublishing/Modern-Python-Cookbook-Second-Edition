"""Python Cookbook 2nd ed.

Chapter 9, recipe 4, Picking a subset – three ways to filter.
"""
import datetime
from pprint import pprint
import re
from typing import Iterable, Iterator, Optional
from Chapter_09.ch09_r01 import DatedLog


def draft_module_iter(source: Iterable[DatedLog]) -> Iterator[DatedLog]:
    for row in source:
        if row.module == "module2":
            yield row


def pass_module(row: DatedLog) -> bool:
    return row.module == "module2"


test_pass_module = """
>>> data = [
... DatedLog(date=datetime.datetime(2016, 4, 24, 11, 5, 1, 462000), level='INFO', module='module1', message='Sample Message One'),
... DatedLog(date=datetime.datetime(2016, 4, 24, 11, 6, 2, 624000), level='DEBUG', module='module2', message='Debugging'),
... DatedLog(date=datetime.datetime(2016, 4, 24, 11, 7, 3, 246000), level='WARNING', module='module1', message='Something might have gone wrong')
... ]
>>> pass_module(data[0])
False
>>> pass_module(data[1])
True
"""


def module_iter(source: Iterable[DatedLog]) -> Iterator[DatedLog]:
    for item in source:
        if pass_module(item):
            yield item


test_module_iter_function = """
>>> data = [
... DatedLog(date=datetime.datetime(2016, 4, 24, 11, 5, 1, 462000), level='INFO', module='module1', message='Sample Message One'),
... DatedLog(date=datetime.datetime(2016, 4, 24, 11, 6, 2, 624000), level='DEBUG', module='module2', message='Debugging'),
... DatedLog(date=datetime.datetime(2016, 4, 24, 11, 7, 3, 246000), level='WARNING', module='module1', message='Something might have gone wrong')
... ]
>>> for row in module_iter(data):
...     pprint(row)
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 6, 2, 624000), level='DEBUG', module='module2', message='Debugging')
"""

test_pass_module_generator_expression = """
>>> data = [
... DatedLog(date=datetime.datetime(2016, 4, 24, 11, 5, 1, 462000), level='INFO', module='module1', message='Sample Message One'),
... DatedLog(date=datetime.datetime(2016, 4, 24, 11, 6, 2, 624000), level='DEBUG', module='module2', message='Debugging'),
... DatedLog(date=datetime.datetime(2016, 4, 24, 11, 7, 3, 246000), level='WARNING', module='module1', message='Something might have gone wrong')
... ]
>>> for row in (item for item in data if pass_module(item)):
...     pprint(row)
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 6, 2, 624000), level='DEBUG', module='module2', message='Debugging')


>>> def module_iter(source: Iterable[DatedLog]) -> Iterator[DatedLog]:
...     return (item for item in source if pass_module(item))
>>> for row in module_iter(data):
...     pprint(row)
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 6, 2, 624000), level='DEBUG', module='module2', message='Debugging')

"""

test_pass_module_filter_function = """
>>> data = [
... DatedLog(date=datetime.datetime(2016, 4, 24, 11, 5, 1, 462000), level='INFO', module='module1', message='Sample Message One'),
... DatedLog(date=datetime.datetime(2016, 4, 24, 11, 6, 2, 624000), level='DEBUG', module='module2', message='Debugging'),
... DatedLog(date=datetime.datetime(2016, 4, 24, 11, 7, 3, 246000), level='WARNING', module='module1', message='Something might have gone wrong')
... ]
>>> for row in filter(pass_module, data):
...     pprint(row)
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 6, 2, 624000), level='DEBUG', module='module2', message='Debugging')

"""

pattern = re.compile(r"module\d+")


def reject_modules(row: DatedLog) -> bool:
    return bool(pattern.match(row.module))


test_reject_modules_filter_function = """
>>> data = [
... DatedLog(date=datetime.datetime(2016, 4, 24, 11, 5, 1, 462000), level='INFO', module='module1', message='Sample Message One'),
... DatedLog(date=datetime.datetime(2016, 4, 24, 11, 6, 2, 624000), level='DEBUG', module='module2', message='Debugging'),
... DatedLog(date=datetime.datetime(2016, 4, 24, 11, 7, 3, 246000), level='WARNING', module='module1', message='Something might have gone wrong'),
... DatedLog(date=datetime.datetime(2016, 4, 24, 11, 8, 5, 468000), level='WARNING', module='other', message='Unexpected')
... ]
>>> def reject_modules_iter(source: Iterable[DatedLog]) -> Iterator[DatedLog]:
...     for item in source:
...         if reject_modules(item):
...             continue
...         yield item
>>> for row in reject_modules_iter(data):
...     pprint(row)
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 8, 5, 468000), level='WARNING', module='other', message='Unexpected')


>>> for row in filter(lambda r: not reject_modules(r), data):
...     pprint(row)
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 8, 5, 468000), level='WARNING', module='other', message='Unexpected')
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
