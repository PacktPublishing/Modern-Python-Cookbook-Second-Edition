"""Python Cookbook 2nd ed.

Chapter 5, recipe 1, Creating dictionaries – inserting and updating
"""
import collections
import re
from typing import Dict, Iterable, Tuple, cast, Iterator, List, Sequence

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

LogRec = Sequence[str]

def parsed_lines(lines: Iterable[str]) -> Iterator[LogRec]:
    for line in lines:
        if (match := log_parser_t.match(line)) is not None:
            match = cast(re.Match, match)  # https://github.com/python/mypy/issues/7316
            yield match.groups()

test_set_item = """
>>> from pprint import pprint
>>> log_lines = list(parsed_lines(log.splitlines()))
>>> pprint(log_lines)  # doctest: +NORMALIZE_WHITESPACE
[('2019/11/12:08:09:10,123', 'INFO', '#PJQXB^eRwnEGG?2%32U', 'path="/openapi.yaml" method=GET'), 
 ('2019/11/12:08:09:10,234', 'INFO', '9DiC!B^nXxnEGG?2%32U', 'path="/items?limit=x" method=GET'), 
 ('2019/11/12:08:09:10,235', 'INFO', '9DiC!B^nXxnEGG?2%32U', 'error="invalid query"'), 
 ('2019/11/12:08:09:10,345', 'INFO', '#PJQXB^eRwnEGG?2%32U', 'status="200" bytes="11234"'), 
 ('2019/11/12:08:09:10,456', 'INFO', '9DiC!B^nXxnEGG?2%32U', 'status="404" bytes="987"'), 
 ('2019/11/12:08:09:10,567', 'INFO', '>UL>PB_R>&nEGG?2%32U', 'path="/category/42" method=GET')]

>>> histogram = {}
>>> for line in log_lines:
...     path_method = line[3]  # group(4) of the match
...     if path_method.startswith("path"):
...         if path_method not in histogram:
...             histogram[path_method] = 0
...         histogram[path_method] += 1
>>> for k in histogram:
...     print(f"{k} {histogram[k]}")
path="/openapi.yaml" method=GET 1
path="/items?limit=x" method=GET 1
path="/category/42" method=GET 1
"""

param_parser = re.compile(r'(\w+)=(".*?"|\w+)')

test_comprehension = """
>>> from pprint import pprint
>>> log_lines = list(parsed_lines(log.splitlines()))
>>> pprint(log_lines)  # doctest: +NORMALIZE_WHITESPACE
[('2019/11/12:08:09:10,123', 'INFO', '#PJQXB^eRwnEGG?2%32U', 'path="/openapi.yaml" method=GET'), 
 ('2019/11/12:08:09:10,234', 'INFO', '9DiC!B^nXxnEGG?2%32U', 'path="/items?limit=x" method=GET'), 
 ('2019/11/12:08:09:10,235', 'INFO', '9DiC!B^nXxnEGG?2%32U', 'error="invalid query"'), 
 ('2019/11/12:08:09:10,345', 'INFO', '#PJQXB^eRwnEGG?2%32U', 'status="200" bytes="11234"'), 
 ('2019/11/12:08:09:10,456', 'INFO', '9DiC!B^nXxnEGG?2%32U', 'status="404" bytes="987"'), 
 ('2019/11/12:08:09:10,567', 'INFO', '>UL>PB_R>&nEGG?2%32U', 'path="/category/42" method=GET')]

>>> for line in log_lines:
...     name_value_pairs = param_parser.findall(line[3])
...     params = {match[0]: match[1] for match in name_value_pairs}
...     print(params)
{'path': '"/openapi.yaml"', 'method': 'GET'}
{'path': '"/items?limit=x"', 'method': 'GET'}
{'error': '"invalid query"'}
{'status': '"200"', 'bytes': '"11234"'}
{'status': '"404"', 'bytes': '"987"'}
{'path': '"/category/42"', 'method': 'GET'}

"""

test_setdefault = """
>>> from pprint import pprint
>>> log_lines = list(parsed_lines(log.splitlines()))
>>> pprint(log_lines)  # doctest: +NORMALIZE_WHITESPACE
[('2019/11/12:08:09:10,123', 'INFO', '#PJQXB^eRwnEGG?2%32U', 'path="/openapi.yaml" method=GET'), 
 ('2019/11/12:08:09:10,234', 'INFO', '9DiC!B^nXxnEGG?2%32U', 'path="/items?limit=x" method=GET'), 
 ('2019/11/12:08:09:10,235', 'INFO', '9DiC!B^nXxnEGG?2%32U', 'error="invalid query"'), 
 ('2019/11/12:08:09:10,345', 'INFO', '#PJQXB^eRwnEGG?2%32U', 'status="200" bytes="11234"'), 
 ('2019/11/12:08:09:10,456', 'INFO', '9DiC!B^nXxnEGG?2%32U', 'status="404" bytes="987"'), 
 ('2019/11/12:08:09:10,567', 'INFO', '>UL>PB_R>&nEGG?2%32U', 'path="/category/42" method=GET')]

>>> histogram = {}
>>> for line in log_lines:
...     path_method = line[3]  # group(4) of the match
...     if path_method.startswith("path"):
...         histogram.setdefault(path_method, 0) 
...         histogram[path_method] += 1
0
0
0
>>> for k in histogram:
...     print(f"{k} {histogram[k]}")
path="/openapi.yaml" method=GET 1
path="/items?limit=x" method=GET 1
path="/category/42" method=GET 1
"""


test_defaultdict = """
>>> from pprint import pprint
>>> log_lines = list(parsed_lines(log.splitlines()))
>>> pprint(log_lines)  # doctest: +NORMALIZE_WHITESPACE
[('2019/11/12:08:09:10,123', 'INFO', '#PJQXB^eRwnEGG?2%32U', 'path="/openapi.yaml" method=GET'), 
 ('2019/11/12:08:09:10,234', 'INFO', '9DiC!B^nXxnEGG?2%32U', 'path="/items?limit=x" method=GET'), 
 ('2019/11/12:08:09:10,235', 'INFO', '9DiC!B^nXxnEGG?2%32U', 'error="invalid query"'), 
 ('2019/11/12:08:09:10,345', 'INFO', '#PJQXB^eRwnEGG?2%32U', 'status="200" bytes="11234"'), 
 ('2019/11/12:08:09:10,456', 'INFO', '9DiC!B^nXxnEGG?2%32U', 'status="404" bytes="987"'), 
 ('2019/11/12:08:09:10,567', 'INFO', '>UL>PB_R>&nEGG?2%32U', 'path="/category/42" method=GET')]

>>> from collections import defaultdict
>>> histogram = defaultdict(int)
>>> for line in log_lines:
...     path_method = line[3]  # group(4) of the match
...     if path_method.startswith("path"):
...         histogram[path_method] += 1

>>> for k in histogram:
...     print(f"{k} {histogram[k]}")
path="/openapi.yaml" method=GET 1
path="/items?limit=x" method=GET 1
path="/category/42" method=GET 1
"""

test_counter = """
>>> from pprint import pprint
>>> log_lines = list(parsed_lines(log.splitlines()))
>>> pprint(log_lines)  # doctest: +NORMALIZE_WHITESPACE
[('2019/11/12:08:09:10,123', 'INFO', '#PJQXB^eRwnEGG?2%32U', 'path="/openapi.yaml" method=GET'), 
 ('2019/11/12:08:09:10,234', 'INFO', '9DiC!B^nXxnEGG?2%32U', 'path="/items?limit=x" method=GET'), 
 ('2019/11/12:08:09:10,235', 'INFO', '9DiC!B^nXxnEGG?2%32U', 'error="invalid query"'), 
 ('2019/11/12:08:09:10,345', 'INFO', '#PJQXB^eRwnEGG?2%32U', 'status="200" bytes="11234"'), 
 ('2019/11/12:08:09:10,456', 'INFO', '9DiC!B^nXxnEGG?2%32U', 'status="404" bytes="987"'), 
 ('2019/11/12:08:09:10,567', 'INFO', '>UL>PB_R>&nEGG?2%32U', 'path="/category/42" method=GET')]

>>> from collections import Counter
>>> histogram = Counter(line[3] 
...     for line in log_lines
...     if line[3].startswith("path")
... )

>>> for k in histogram:
...     print(f"{k} {histogram[k]}")
path="/openapi.yaml" method=GET 1
path="/items?limit=x" method=GET 1
path="/category/42" method=GET 1
"""



__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
