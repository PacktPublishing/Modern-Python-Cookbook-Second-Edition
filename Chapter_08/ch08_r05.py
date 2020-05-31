"""Python Cookbook 2nd ed.

Chapter 8, recipe 5, Using more complex structures – maps of lists
"""

import collections
from dataclasses import dataclass, InitVar, field, fields
from typing import ClassVar
import re
from typing import List, DefaultDict, cast, NamedTuple, Optional, Iterable


@dataclass(frozen=True)
class Event_dc:
    """
    A detail line from a log

    >>> Event_dc("[2016-04-24 11:05:01,462] INFO in module1: Sample Message One")
    Event_dc(timestamp='2016-04-24 11:05:01,462', level='INFO', module='module1', message='Sample Message One')
    """

    line: InitVar[str]
    timestamp: str = field(init=False)
    level: str = field(init=False)
    module: str = field(init=False)
    message: str = field(init=False)

    pattern: ClassVar[re.Pattern] = re.compile(
        r"\[(?P<timestamp>.*?)\]\s+"
        r"(?P<level>\w+)\s+"
        r"in\s+(?P<module>\w+)"
        r":\s+(?P<message>.+)"
    )

    def __init__(self, line: str) -> None:
        if log_line := self.pattern.match(line):
            for field in fields(self):
                object.__setattr__(
                    self, field.name, cast(re.Match, log_line).group(field.name)
                )


class Event(NamedTuple):
    """
    A detail line from a log

    >>> Event.from_line(
    ...     "[2016-04-24 11:05:01,462] INFO in module1: Sample Message One")
    Event(timestamp='2016-04-24 11:05:01,462', level='INFO', module='module1', message='Sample Message One')
    """

    timestamp: str
    level: str
    module: str
    message: str

    @staticmethod
    def from_line(line: str) -> Optional["Event"]:
        pattern = re.compile(
            r"\[(?P<timestamp>.*?)\]\s+"
            r"(?P<level>\w+)\s+"
            r"in\s+(?P<module>\w+)"
            r":\s+(?P<message>.+)"
        )
        if log_line := pattern.match(line):
            return Event(**cast(re.Match, log_line).groupdict())
        return None


Summary = DefaultDict[str, List[Event]]


def summarize(data: Iterable[Event]) -> Summary:
    module_details: Summary = collections.defaultdict(list)
    for event in data:
        module_details[event.module].append(event)
    return module_details


class ModuleEvents(dict):
    def add_event(self, event: Event) -> None:
        if event.module not in self:
            self[event.module] = list()
        self[event.module].append(event)


test_function = """
>>> from pprint import pprint
>>> data = [
...     '[2016-04-24 11:05:01,462] INFO in module1: Sample Message One',
...     '[2016-04-24 11:06:02,624] DEBUG in module2: Debugging',
...     '[2016-04-24 11:07:03,246] WARNING in module1: Something might have gone wrong'
... ]
>>> event_iter = (Event.from_line(txt) for txt in data)
>>> module_details = summarize(event_iter)
>>> pprint(dict(module_details))
{'module1': [Event(timestamp='2016-04-24 11:05:01,462', level='INFO', module='module1', message='Sample Message One'),
             Event(timestamp='2016-04-24 11:07:03,246', level='WARNING', module='module1', message='Something might have gone wrong')],
 'module2': [Event(timestamp='2016-04-24 11:06:02,624', level='DEBUG', module='module2', message='Debugging')]}
>>> sorted(module_details.items())  # doctest: +NORMALIZE_WHITESPACE
[('module1', [Event(timestamp='2016-04-24 11:05:01,462', level='INFO', module='module1', message='Sample Message One'), Event(timestamp='2016-04-24 11:07:03,246', level='WARNING', module='module1', message='Something might have gone wrong')]), ('module2', [Event(timestamp='2016-04-24 11:06:02,624', level='DEBUG', module='module2', message='Debugging')])]
"""

test_class = """
>>> data = [
...     '[2016-04-24 11:05:01,462] INFO in module1: Sample Message One',
...     '[2016-04-24 11:06:02,624] DEBUG in module2: Debugging',
...     '[2016-04-24 11:07:03,246] WARNING in module1: Something might have gone wrong'
... ]
>>> event_iter = (Event.from_line(txt) for txt in data)
>>> module_details = ModuleEvents()
>>> for event in event_iter:
...     module_details.add_event(event)
>>> sorted(module_details.items())  # doctest: +NORMALIZE_WHITESPACE
[('module1', [Event(timestamp='2016-04-24 11:05:01,462', level='INFO', module='module1', message='Sample Message One'), Event(timestamp='2016-04-24 11:07:03,246', level='WARNING', module='module1', message='Something might have gone wrong')]), ('module2', [Event(timestamp='2016-04-24 11:06:02,624', level='DEBUG', module='module2', message='Debugging')])]

"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
