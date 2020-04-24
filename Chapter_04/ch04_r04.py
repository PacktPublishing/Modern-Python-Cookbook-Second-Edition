"""Python Cookbook 2nd ed.

Chapter 4, recipe 4, Deleting from a list – deleting, removing, popping, and filtering
"""
import csv
from pathlib import Path
from typing import List, Any


def get_fuel_use(path: Path) -> List[List[Any]]:
    with path.open() as source_file:
        reader = csv.reader(source_file)
        log_rows = list(reader)
    return log_rows


test_load = """
>>> from pprint import pprint
>>> log_rows = get_fuel_use(Path('data/fuel.csv'))
>>> log_rows[0]
['date', 'engine on', 'fuel height']
>>> log_rows[-1]
['', "choppy -- anchor in jackson's creek", '']
"""

# Test Data used below.
log_rows = [
    ["date", "engine on", "fuel height"],
    ["", "engine off", "fuel height"],
    ["", "Other notes", ""],
    ["", "", ""],
    ["10/25/13", "08:24:00 AM", "29"],
    ["", "01:15:00 PM", "27"],
    ["", "calm seas -- anchor solomon's island", ""],
    ["10/26/13", "09:12:00 AM", "27"],
    ["", "06:25:00 PM", "22"],
    ["", "choppy -- anchor in jackson's creek", ""],
]

test_del = """
>>> del log_rows[:4]
>>> log_rows[0]
['10/25/13', '08:24:00 AM', '29']
>>> log_rows[-1]
['', "choppy -- anchor in jackson's creek", '']
"""

test_remove = """
>>> row = ['10/25/13', '08:24:00 AM', '29', '', '01:15:00 PM', '27']
>>> row.remove('')
>>> row
['10/25/13', '08:24:00 AM', '29', '01:15:00 PM', '27']
"""

test_pop = """
>>> row = ['10/25/13', '08:24:00 AM', '29', '', '01:15:00 PM', '27']
>>> target_position = row.index('')
>>> target_position
3
>>> row.pop(target_position)
''
>>> row
['10/25/13', '08:24:00 AM', '29', '01:15:00 PM', '27']
"""

test_slice_assignment = """
>>> row = ['10/25/13', '08:24:00 AM', '29', '', '01:15:00 PM', '27']
>>> target_position = row.index('')
>>> target_position
3
>>> row[3:4] = []
>>> row
['10/25/13', '08:24:00 AM', '29', '01:15:00 PM', '27']
"""


def number_column(row, column=2):
    try:
        float(row[column])
        return True
    except ValueError:
        return False


test_number_filter = """
>>> tail_rows = list(filter(number_column, log_rows))
>>> len(tail_rows)
4
>>> tail_rows[0]
['10/25/13', '08:24:00 AM', '29']
>>> tail_rows[-1]
['', '06:25:00 PM', '22']
"""

test_index_error = """
>>> row = ['', '06:25:00 PM', '22']
>>> del row[3]
Traceback (most recent call last):
  File "/Users/slott/miniconda3/envs/cookbook/lib/python3.8/doctest.py", line 1328, in __run
    compileflags, 1), test.globs)
  File "<doctest examples.txt[80]>", line 1, in <module>
    del row[3]
IndexError: list assignment index out of range
"""

test_remove_fail = """
>>> data_items = [1, 1, 2, 3, 5, 8, 10,
...    13, 21, 34, 36, 55]
>>> for f in data_items:
...    if f%2 == 0: 
...        data_items.remove(f)
>>> data_items
[1, 1, 3, 5, 10, 13, 21, 36, 55]
"""

test_remove_copy = """
>>> data_items = [1, 1, 2, 3, 5, 8, 10,
...    13, 21, 34, 36, 55]
>>> for f in data_items[:]:
...    if f%2 == 0: 
...        data_items.remove(f)
>>> data_items
[1, 1, 3, 5, 13, 21, 55]
"""

test_remove_while = """
>>> data_items = [1, 1, 2, 3, 5, 8, 10,
...    13, 21, 34, 36, 55]
>>> position = 0
>>> while position != len(data_items):
...    f = data_items[position]
...    if f%2 == 0:
...        data_items.remove(f)
...    else:
...        position += 1
>>> data_items
[1, 1, 3, 5, 13, 21, 55]
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
