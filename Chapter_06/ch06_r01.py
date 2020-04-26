"""Python Cookbook 2nd ed.

Chapter 6, recipe 2, Using features of the print() function
"""
from pathlib import Path
import csv
from typing import Dict, List


def get_fuel_use(source_path: Path) -> List[Dict[str, str]]:
    with source_path.open() as source_file:
        rdr = csv.DictReader(source_file)
        return list(rdr)


test_get_fuel_use = """
>>> source_path = Path("data/fuel2.csv") 
>>> fuel_use = get_fuel_use(source_path) 
>>> for row in fuel_use: 
...     print(row)
{'date': '10/25/13', 'engine on': '08:24:00', 'fuel height on': '29', 'engine off': '13:15:00', 'fuel height off': '27'}
{'date': '10/26/13', 'engine on': '09:12:00', 'fuel height on': '27', 'engine off': '18:25:00', 'fuel height off': '22'}
{'date': '10/28/13', 'engine on': '13:21:00', 'fuel height on': '22', 'engine off': '06:25:00', 'fuel height off': '14'}
"""

test_print_1 = """
>>> fuel_use = get_fuel_use(Path("data/fuel2.csv")) 
>>> for leg in fuel_use:
...    start = float(leg["fuel height on"])
...    finish = float(leg["fuel height off"])
...    print("On", leg["date"],
...    "from", leg["engine on"],
...    "to", leg["engine off"],
...    "change", start-finish, "in.")
On 10/25/13 from 08:24:00 to 13:15:00 change 2.0 in.
On 10/26/13 from 09:12:00 to 18:25:00 change 5.0 in.
On 10/28/13 from 13:21:00 to 06:25:00 change 8.0 in.
"""


test_print_2 = """
>>> fuel_use = get_fuel_use(Path("data/fuel2.csv")) 
>>> print("date", "start", "end", "depth", sep=" | ")
date | start | end | depth
>>> for leg in fuel_use:
...    start = float(leg["fuel height on"])
...    finish = float(leg["fuel height off"])
...    print(leg["date"], leg["engine on"],
...    leg["engine off"], start-finish, sep=" | ")
10/25/13 | 08:24:00 | 13:15:00 | 2.0
10/26/13 | 09:12:00 | 18:25:00 | 5.0
10/28/13 | 13:21:00 | 06:25:00 | 8.0
"""

test_print_3 = """
>>> fuel_use = get_fuel_use(Path("data/fuel2.csv")) 
>>> for leg in fuel_use:
...    start = float(leg["fuel height on"])
...    finish = float(leg["fuel height off"])
...    print("date", leg["date"], sep="=", end=", ")
...    print("on", leg["engine on"], sep="=", end=", ")
...    print("off", leg["engine off"], sep="=", end=", ")
...    print("change", start-finish, sep="=")
date=10/25/13, on=08:24:00, off=13:15:00, change=2.0
date=10/26/13, on=09:12:00, off=18:25:00, change=5.0
date=10/28/13, on=13:21:00, off=06:25:00, change=8.0
"""


import sys


def print_like(*args, sep=None, end=None, file=sys.stdout):
    if sep is None:
        sep = " "
    if end is None:
        end = "\n"
    arg_iter = iter(args)
    value = next(arg_iter)
    file.write(str(value))
    for value in arg_iter:
        file.write(sep)
        file.write(str(value))
        file.write(end)
    file.flush()


test_print_like = """
>>> print_like("number", 1, sep="=", end=", ")
>>> print_like("string", "value", sep="=") 
"""


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
