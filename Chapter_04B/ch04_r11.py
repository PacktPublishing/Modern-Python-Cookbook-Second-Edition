"""Python Cookbook 2nd ed.

Chapter 5, recipe 2, Removing from dictionaries – the pop() method and the del statement

This bumps into an open issue: https://github.com/python/mypy/issues/7316
"""
import collections
import re
from typing import DefaultDict, Tuple, List, Dict, Iterable, Iterator, cast

# The 20-char request id's are base64.b85encode(uuid.uuid1().bytes)

log = """
[2019/11/12:08:09:10,123] INFO #PJQXB^eRwnEGG?2%32U path="/openapi.yaml" method=GET
[2019/11/12:08:09:10,234] INFO 9DiC!B^nXxnEGG?2%32U path="/items?limit=x" method=GET
[2019/11/12:08:09:10,235] INFO 9DiC!B^nXxnEGG?2%32U error="invalid query"
[2019/11/12:08:09:10,345] INFO #PJQXB^eRwnEGG?2%32U status="200" bytes="11234"
[2019/11/12:08:09:10,456] INFO 9DiC!B^nXxnEGG?2%32U status="404" bytes="987"
[2019/11/12:08:09:10,567] INFO >UL>PB_R>&nEGG?2%32U path="/category/42" method=GET
"""

log_parser_t = re.compile(r"\[(.*?)\] (\w+) (\S+) (.*)")

LogRec = Tuple[str, ...]


def request_iter_t(source: Iterable[str]) -> Iterator[List[LogRec]]:
    requests: DefaultDict[str, List[LogRec]] = collections.defaultdict(list)
    for line in source:
        if (match := log_parser_t.match(line)) is not None:
            match = cast(re.Match, match)  # https://github.com/python/mypy/issues/7316
            id = match.group(3)
            requests[id].append(tuple(match.groups()))
            if match.group(4).startswith("status"):
                yield requests[id]
                del requests[id]
    if requests:
        print("Dangling", requests)


test_request_iter_t = """
>>> for r in request_iter_t(log.splitlines()):
...     print(r)
[('2019/11/12:08:09:10,123', 'INFO', '#PJQXB^eRwnEGG?2%32U', 'path="/openapi.yaml" method=GET'), ('2019/11/12:08:09:10,345', 'INFO', '#PJQXB^eRwnEGG?2%32U', 'status="200" bytes="11234"')]
[('2019/11/12:08:09:10,234', 'INFO', '9DiC!B^nXxnEGG?2%32U', 'path="/items?limit=x" method=GET'), ('2019/11/12:08:09:10,235', 'INFO', '9DiC!B^nXxnEGG?2%32U', 'error="invalid query"'), ('2019/11/12:08:09:10,456', 'INFO', '9DiC!B^nXxnEGG?2%32U', 'status="404" bytes="987"')]
Dangling defaultdict(<class 'list'>, {'>UL>PB_R>&nEGG?2%32U': [('2019/11/12:08:09:10,567', 'INFO', '>UL>PB_R>&nEGG?2%32U', 'path="/category/42" method=GET')]})

"""

log_parser_d = re.compile(
    r"\[(?P<time>.*?)\] " r"(?P<sev>\w+) " r"(?P<id>\S+) " r"(?P<msg>.*)"
)

LogRecD = Dict[str, str]


def request_iter_d(source: Iterable[str]) -> Iterator[List[LogRecD]]:
    requests: DefaultDict[str, List[LogRecD]] = collections.defaultdict(list)
    for line in source:
        if (match := log_parser_d.match(line)) is not None:
            match = cast(re.Match, match)  # https://github.com/python/mypy/issues/7316
            record = match.groupdict()
            id = record.pop("id")
            requests[id].append(record)
            if record["msg"].startswith("status"):
                yield requests[id]
                del requests[id]
    if requests:
        print("Dangling", requests)


test_request_iter_d = """
>>> for r in request_iter_d(log.splitlines()):
...     print(r)
[{'time': '2019/11/12:08:09:10,123', 'sev': 'INFO', 'msg': 'path="/openapi.yaml" method=GET'}, {'time': '2019/11/12:08:09:10,345', 'sev': 'INFO', 'msg': 'status="200" bytes="11234"'}]
[{'time': '2019/11/12:08:09:10,234', 'sev': 'INFO', 'msg': 'path="/items?limit=x" method=GET'}, {'time': '2019/11/12:08:09:10,235', 'sev': 'INFO', 'msg': 'error="invalid query"'}, {'time': '2019/11/12:08:09:10,456', 'sev': 'INFO', 'msg': 'status="404" bytes="987"'}]
Dangling defaultdict(<class 'list'>, {'>UL>PB_R>&nEGG?2%32U': [{'time': '2019/11/12:08:09:10,567', 'sev': 'INFO', 'msg': 'path="/category/42" method=GET'}]})

"""


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
