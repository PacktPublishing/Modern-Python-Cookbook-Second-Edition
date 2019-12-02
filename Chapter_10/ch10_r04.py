"""Python Cookbook 2nd ed.

Chapter 10, recipe 4.
"""

import statistics
from typing import Iterable, Dict, Tuple
from Chapter_10.ch10_r03 import correlation


def regression(data: Iterable[Dict[str, float]]) -> Tuple[float, float]:

    m_x = statistics.mean(i["x"] for i in data)
    m_y = statistics.mean(i["y"] for i in data)
    s_x = statistics.stdev(i["x"] for i in data)
    s_y = statistics.stdev(i["y"] for i in data)
    r_xy = correlation(data)

    b = r_xy * s_y / s_x
    a = m_y - b * m_x
    return a, b


from math import sqrt


def regr2(data: Iterable[Dict[str, float]]) -> Tuple[float, float]:
    sumx = sumy = sumxy = sumx2 = sumy2 = n = 0.0
    for item in data:
        x, y = item["x"], item["y"]
        n += 1
        sumx += x
        sumy += y
        sumxy += x * y
        sumx2 += x ** 2
        sumy2 += y ** 2
    m_x = sumx / n
    m_y = sumy / n
    s_x = sqrt((n * sumx2 - sumx ** 2) / (n * (n - 1)))
    s_y = sqrt((n * sumy2 - sumy ** 2) / (n * (n - 1)))
    r_xy = (n * sumxy - sumx * sumy) / (
        sqrt(n * sumx2 - sumx ** 2) * sqrt(n * sumy2 - sumy ** 2)
    )
    b = r_xy * s_y / s_x
    a = m_y - b * m_x
    return a, b


from pathlib import Path
import json

# from collections import OrderedDict

source_path = Path("data") / "anscombe.json"

__test__ = {
    "regression": """
# old: object_pairs_hook=OrderedDict)
>>> data = json.loads(source_path.read_text())
>>> for series in data:
...    a, b = regression(series['data'])
...    print(series['series'], 'y=', round(a, 2), '+', round(b,3), '*x')
I y= 3.0 + 0.5 *x
II y= 3.0 + 0.5 *x
III y= 3.0 + 0.5 *x
IV y= 3.0 + 0.5 *x
""",
    "regr2": """
>>> data = json.loads(source_path.read_text())
>>> for series in data:
...    a, b = regr2(series['data'])
...    print(series['series'], 'y=', round(a, 2), '+', round(b,3), '*x')
I y= 3.0 + 0.5 *x
II y= 3.0 + 0.5 *x
III y= 3.0 + 0.5 *x
IV y= 3.0 + 0.5 *x
""",
}
