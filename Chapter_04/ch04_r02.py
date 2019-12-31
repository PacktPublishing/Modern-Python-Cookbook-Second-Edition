"""Python Cookbook 2nd ed.

Chapter 4, recipe 2, Building lists – literals, appending, and comprehensions
"""
from pathlib import Path

test_raw_data = """
>>> home = Path.cwd()
>>> for path in home.glob('data/*.csv'):
...     print(path.stat().st_size, path.name)
1810 wc1.csv
28 ex2_r12.csv
1790 wc.csv
215 sample.csv
45 craps.csv
28 output.csv
225 fuel.csv
166 waypoints.csv
412 summary_log.csv
156 fuel2.csv
"""

test_gather = """
>>> file_sizes = []
>>> home = Path.cwd()
>>> for path in home.glob('data/*.csv'):
...     file_sizes.append(path.stat().st_size)
>>> print(file_sizes)
[1810, 28, 1790, 215, 45, 28, 225, 166, 412, 156]
>>> print(sum(file_sizes))
4875
"""


test_comprehensions = """
>>> home = Path.cwd()
>>> [path.stat().st_size
...    for path in home.glob('data/*.csv')]
[1810, 28, 1790, 215, 45, 28, 225, 166, 412, 156]
"""

test_generator = """
>>> home = Path.cwd()
>>> list(path.stat().st_size
...    for path in home.glob('data/*.csv'))
[1810, 28, 1790, 215, 45, 28, 225, 166, 412, 156]

>>> sizes = list(path.stat().st_size
...    for path in home.glob('data/*.csv'))
>>> sum(sizes)
4875
>>> max(sizes)
1810
>>> min(sizes)
28
>>> from statistics import mean
>>> round(mean(sizes), 3)
487.5
>>> sizes.index(min(sizes))
1
"""

test_list_extend = """
>>> home = Path.cwd()
>>> ch3 = list(path.stat().st_size
...    for path in home.glob('Chapter_03/*.py'))
>>> ch4 = list(path.stat().st_size
...    for path in home.glob('Chapter_04/*.py'))
>>> len(ch3)
12
>>> len(ch4)
16
>>> final = ch3 + ch4
>>> len(final)
28
>>> sum(final)
59465

>>> final_ex = []
>>> final_ex.extend(ch3)
>>> final_ex.extend(ch4)
>>> len(final_ex)
28
>>> sum(final_ex)
59465
"""

test_insert = """
>>> p = [3, 5, 11, 13]
>>> p.insert(0, 2)
>>> p
[2, 3, 5, 11, 13]
>>> p.insert(3, 7)
>>> p
[2, 3, 5, 7, 11, 13]
"""


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
