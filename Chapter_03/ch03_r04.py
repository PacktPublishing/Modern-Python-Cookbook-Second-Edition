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


def rtd2(**keywords: float) -> Dict[str, Optional[float]]:
    rate = keywords.get("rate")
    time = keywords.get("time")
    distance = keywords.get("distance")
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


def rtd3(**keywords: float) -> Dict[str, Optional[float]]:
    rate = keywords.pop("rate", None)
    time = keywords.pop("time", None)
    distance = keywords.pop("distance", None)
    if keywords:
        raise TypeError(
            f"Invalid keyword parameter: {', '.join(keywords.keys())}")
    if distance is None and rate is not None and time is not None:
        distance = rate * time
    elif rate is None and distance is not None and time is not None:
        rate = distance / time
    elif time is None and distance is not None and rate is not None:
        time = distance / rate
    else:
        warnings.warn("Nothing to solve for")
    return dict(distance=distance, rate=rate, time=time)

test_rtd3 = """
>>> rtd3(distance=31.2, rate=6) 
{'distance': 31.2, 'rate': 6, 'time': 5.2}

>>> result = rtd2(distance=31.2, rate=6)
>>> ('At {rate}kt, it takes '
... '{time}hrs to cover {distance}nm').format_map(result)
'At 6kt, it takes 5.2hrs to cover 31.2nm'

>>> rtd3(distnace=31.2, rate=6) 
Traceback (most recent call last):
  File "/Users/slott/miniconda3/envs/cookbook/lib/python3.8/doctest.py", line 1328, in __run
    exec(compile(example.source, filename, "single",
  File "<doctest Chapter_03.ch03_r04.__test__.test_rtd3[3]>", line 1, in <module>
  File "/Users/slott/Documents/Writing/Python/Python Cookbook 2e/Modern-Python-Cookbook-Second-Edition/Chapter_03/ch03_r04.py", line 81, in rtd3
    raise ValueError("Invalid keyword parameter: {keywords.keys()}")
TypeError: Invalid keyword parameter: distnace
"""


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
