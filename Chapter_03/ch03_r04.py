"""Python Cookbook 2nd ed.

Chapter 3, recipe 4, Using super flexible keyword parameters
"""

from typing import Optional, Dict
import warnings


def rtd(
    distance: Optional[float] = None,
    rate: Optional[float] = None,
    time: Optional[float] = None,
) -> Dict[str, Optional[float]]:
    if distance is None and rate is not None and time is not None:
        distance = rate * time
    elif rate is None and distance is not None and time is not None:
        rate = distance / time
    elif time is None and distance is not None and rate is not None:
        time = distance / rate
    else:
        warnings.warn("Nothing to solve for")
    return dict(distance=distance, rate=rate, time=time)


test_rtd = """
>>> rtd(distance=31.2, rate=6) 
{'distance': 31.2, 'rate': 6, 'time': 5.2}

>>> result = rtd(distance=31.2, rate=6)
>>> ('At {rate}kt, it takes '
... '{time}hrs to cover {distance}nm').format_map(result)
'At 6kt, it takes 5.2hrs to cover 31.2nm'
"""


def rtd2(**keywords):
    rate = keywords.get('rate', None)
    time = keywords.get('time', None)
    distance = keywords.get('distance', None)
    if distance is None and rate is not None and time is not None:
        distance = rate * time
    elif rate is None and distance is not None and time is not None:
        rate = distance / time
    elif time is None and distance is not None and rate is not None:
        time = distance / rate
    else:
        warnings.warn("Nothing to solve for")
    return dict(distance=distance, rate=rate, time=time)

test_rtd2 = """
>>> rtd2(distance=31.2, rate=6) 
{'distance': 31.2, 'rate': 6, 'time': 5.2}

>>> result = rtd2(distance=31.2, rate=6)
>>> ('At {rate}kt, it takes '
... '{time}hrs to cover {distance}nm').format_map(result)
'At 6kt, it takes 5.2hrs to cover 31.2nm'

>>> rtd2(distnace=31.2, rate=6) 
{'distance': None, 'rate': 6, 'time': None}

>>> warnings.simplefilter("error")
>>> rtd2(distnace=31.2, rate=6) 
Traceback (most recent call last):
  File "/Applications/PyCharm CE.app/Contents/helpers/pycharm/docrunner.py", line 139, in __run
    exec(compile(example.source, filename, "single",
  File "<doctest ch03_r04.__test__.test_rtd2[5]>", line 1, in <module>
    rtd2(distnace=31.2, rate=6)
  File "Chapter_03/ch03_r04.py", line 48, in rtd2
    warnings.warn("Nothing to solve for")
UserWarning: Nothing to solve for"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
