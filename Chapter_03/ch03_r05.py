"""Python Cookbook 2nd ed.

Chapter 3, recipe 5, Forcing keyword-only arguments with the * separator
"""


def Twc(T: float, V: float) -> float:
    return 13.12 + 0.6215 * T - 11.37 * V ** 0.16 + 0.3965 * T * V ** 0.16


import csv
from typing import TextIO


def wind_chill(
    *,
    start_T: int,
    stop_T: int,
    step_T: int,
    start_V: int,
    stop_V: int,
    step_V: int,
    target: TextIO
) -> None:
    """Wind Chill Table."""
    writer = csv.writer(target)
    heading = [""] + [str(t) for t in range(start_T, stop_T, step_T)]
    writer.writerow(heading)
    for V in range(start_V, stop_V, step_V):
        row = [float(V)] + [Twc(T, V) for T in range(start_T, stop_T, step_T)]
        writer.writerow(row)


test_wc_good = """
>>> from pathlib import Path

>>> p = Path('data/wc1.csv')
>>> with p.open('w', newline='') as output_file:
...     wind_chill(start_T=0, stop_T=-45, step_T=-5, 
...     start_V=0, stop_V=20, step_V=2, 
...     target=output_file) 
"""

test_wc_fail = """
>>> from pathlib import Path

>>> p = Path('data/wc1.csv')
>>> with p.open('w', newline='') as target:
...     wind_chill(0, -45, -5, 0, 20, 2, target)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: wind_chill() takes 0 positional arguments but 7 were given
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
