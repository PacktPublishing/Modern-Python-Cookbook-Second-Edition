"""Python Cookbook 2nd ed.

Chapter 4, recipe 3, Slicing and dicing a list
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
>>> pprint(log_rows)
[['date', 'engine on', 'fuel height'],
 ['', 'engine off', 'fuel height'],
 ['', 'Other notes', ''],
 ['', '', ''],
 ['10/25/13', '08:24:00 AM', '29'],
 ['', '01:15:00 PM', '27'],
 ['', "calm seas -- anchor solomon's island", ''],
 ['10/26/13', '09:12:00 AM', '27'],
 ['', '06:25:00 PM', '22'],
 ['', "choppy -- anchor in jackson's creek", '']]
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

test_recipe = """
>>> from pprint import pprint

Step 1

>>> head, tail = log_rows[:4], log_rows[4:]
>>> head[0]
['date', 'engine on', 'fuel height']
>>> head[-1]
['', '', '']
>>> tail[0]
['10/25/13', '08:24:00 AM', '29']
>>> tail[-1]
['', "choppy -- anchor in jackson's creek", '']
>>> pprint(tail[0::3])
[['10/25/13', '08:24:00 AM', '29'], ['10/26/13', '09:12:00 AM', '27']]
>>> pprint(tail[1::3])
[['', '01:15:00 PM', '27'], ['', '06:25:00 PM', '22']]

 
>>> tail[2::3]  # doctest: +NORMALIZE_WHITESPACE
[['', "calm seas -- anchor solomon's island", ''],
 ['', "choppy -- anchor in jackson's creek", '']]

Step 2

>>> list(zip(tail[0::3], tail[1::3]))  # doctest: +NORMALIZE_WHITESPACE
[(['10/25/13', '08:24:00 AM', '29'], ['', '01:15:00 PM', '27']),
 (['10/26/13', '09:12:00 AM', '27'], ['', '06:25:00 PM', '22'])]

Step 3

>>> list(zip(tail[0::3], tail[1::3]))  # doctest: +NORMALIZE_WHITESPACE
[(['10/25/13', '08:24:00 AM', '29'], ['', '01:15:00 PM', '27']),
 (['10/26/13', '09:12:00 AM', '27'], ['', '06:25:00 PM', '22'])]

Final

>>> paired_rows = list( zip(tail[0::3], tail[1::3]) ) 
>>> [a+b for a, b in paired_rows]  
[['10/25/13', '08:24:00 AM', '29', '', '01:15:00 PM', '27'], ['10/26/13', '09:12:00 AM', '27', '', '06:25:00 PM', '22']]

"""


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
