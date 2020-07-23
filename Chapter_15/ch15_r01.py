"""Python Cookbook 2nd ed.

Chapter 15, recipe 1, Using the statistics library
"""
from pathlib import Path
from typing import (
    Any,  Callable, cast, Dict, Iterable, Iterator, List,
    TypedDict, Union)


# Idealized definitions. Not actually practical, though.
# Mypy requires use of literal keys, ``p["x"]``, and we'd like to use variables.
# class Point(TypedDict):
#     x: float
#     y: float
#
# class Series(TypedDict, total=False):
#     series: str
#     data: List[Point]
#     # other names, based on the statistical function and variable.

# Generic, and workable.
Point = Dict[str, float]
Series = Dict[str, Union[str, float, List[Point]]]


def get_series(data: List[Series], series_name: str) -> Series:
    series = next(
        s for s in data
        if s['series'] == series_name
    )
    return series


def data_iter(
        series: Series, variable_name: str) -> Iterable[Any]:
    return (
        item[variable_name]
        for item in cast(List[Point], series["data"])
    )

def display_template(data: List[Series]) -> None:
    for series in data:
        for variable_name in 'x', 'y':
            samples = list(
                data_iter(series, variable_name))
            # compute details here.
            series_name = series['series']
            print(
                f"{series_name:>3s} {variable_name}: "
                # display output here.
            )

import statistics
import collections
def display_center(data: List[Series]) -> None:
    for series in data:
        for variable_name in 'x', 'y':
            samples = list(
                data_iter(series, variable_name))
            mean = statistics.mean(samples)
            median = statistics.median(samples)
            mode = collections.Counter(
                samples
            ).most_common(1)
            series_name = series['series']
            print(
                f"{series_name:>3s} {variable_name}: "
                f"mean={round(mean, 2)}, median={median}, "
                f"mode={mode}")

test_display_stats = """
>>> from pprint import pprint
>>> source_path = Path('data/anscombe.json')
>>> data = json.loads(
... source_path.read_text())
>>> display_center(data)
  I x: mean=9.0, median=9.0, mode=[(10.0, 1)]
  I y: mean=7.5, median=7.58, mode=[(8.04, 1)]
 II x: mean=9.0, median=9.0, mode=[(10.0, 1)]
 II y: mean=7.5, median=8.14, mode=[(9.14, 1)]
III x: mean=9.0, median=9.0, mode=[(10.0, 1)]
III y: mean=7.5, median=7.11, mode=[(7.46, 1)]
 IV x: mean=9.0, median=8.0, mode=[(8.0, 10)]
 IV y: mean=7.5, median=7.04, mode=[(6.58, 1)]
"""

def display_extrema(data: List[Series]) -> None:
    for series in data:
        for variable_name in 'x', 'y':
            samples = list(
                data_iter(series, variable_name))
            least = min(samples)
            most = min(samples)
            series_name = series['series']
            print(
                f"{series_name:>3s} {variable_name}: "
                f"min={least}, max={most}")

test_display_extrema = """
>>> from pprint import pprint
>>> source_path = Path('data/anscombe.json')
>>> data = json.loads(
... source_path.read_text())
>>> display_extrema(data)
  I x: min=4.0, max=4.0
  I y: min=4.26, max=4.26
 II x: min=4.0, max=4.0
 II y: min=3.1, max=3.1
III x: min=4.0, max=4.0
III y: min=5.39, max=5.39
 IV x: min=8.0, max=8.0
 IV y: min=5.25, max=5.25
"""

def display_variance(data: List[Series]) -> None:
    for series in data:
        for variable_name in 'x', 'y':
            samples = list(
                data_iter(series, variable_name))
            mean = statistics.mean(samples)
            variance = statistics.variance(samples, mean)
            stdev = statistics.stdev(samples, mean)
            series_name = series['series']
            print(
                f"{series_name:>3s} {variable_name}: "
                f"mean={mean:.2f}, var={variance:.2f}, "
                f"stdev={stdev:.2f}")

test_display_variance = """
>>> from pprint import pprint
>>> source_path = Path('data/anscombe.json')
>>> data = json.loads(
... source_path.read_text())
>>> display_variance(data)
  I x: mean=9.00, var=11.00, stdev=3.32
  I y: mean=7.50, var=4.13, stdev=2.03
 II x: mean=9.00, var=11.00, stdev=3.32
 II y: mean=7.50, var=4.13, stdev=2.03
III x: mean=9.00, var=11.00, stdev=3.32
III y: mean=7.50, var=4.12, stdev=2.03
 IV x: mean=9.00, var=11.00, stdev=3.32
 IV y: mean=7.50, var=4.12, stdev=2.03
"""


import statistics
def set_mean(data: List[Series]) -> None:
    for series in data:
        for variable_name in "x", "y":
            result = f"mean_{variable_name}"
            samples = data_iter(series, variable_name)
            series[result] = statistics.mean(samples)


test_set_mean = """
>>> from pprint import pprint
>>> source_path = Path('data/anscombe.json')
>>> data = json.loads(
... source_path.read_text())
>>> set_mean(data)
>>> pprint(data)
[{'data': [{'x': 10.0, 'y': 8.04},
           {'x': 8.0, 'y': 6.95},
           {'x': 13.0, 'y': 7.58},
           {'x': 9.0, 'y': 8.81},
           {'x': 11.0, 'y': 8.33},
           {'x': 14.0, 'y': 9.96},
           {'x': 6.0, 'y': 7.24},
           {'x': 4.0, 'y': 4.26},
           {'x': 12.0, 'y': 10.84},
           {'x': 7.0, 'y': 4.82},
           {'x': 5.0, 'y': 5.68}],
  'mean_x': 9.0,
  'mean_y': 7.500909090909091,
  'series': 'I'},
 {'data': [{'x': 10.0, 'y': 9.14},
           {'x': 8.0, 'y': 8.14},
           {'x': 13.0, 'y': 8.74},
           {'x': 9.0, 'y': 8.77},
           {'x': 11.0, 'y': 9.26},
           {'x': 14.0, 'y': 8.1},
           {'x': 6.0, 'y': 6.13},
           {'x': 4.0, 'y': 3.1},
           {'x': 12.0, 'y': 9.13},
           {'x': 7.0, 'y': 7.26},
           {'x': 5.0, 'y': 4.74}],
  'mean_x': 9.0,
  'mean_y': 7.500909090909091,
  'series': 'II'},
 {'data': [{'x': 10.0, 'y': 7.46},
           {'x': 8.0, 'y': 6.77},
           {'x': 13.0, 'y': 12.74},
           {'x': 9.0, 'y': 7.11},
           {'x': 11.0, 'y': 7.81},
           {'x': 14.0, 'y': 8.84},
           {'x': 6.0, 'y': 6.08},
           {'x': 4.0, 'y': 5.39},
           {'x': 12.0, 'y': 8.15},
           {'x': 7.0, 'y': 6.42},
           {'x': 5.0, 'y': 5.73}],
  'mean_x': 9.0,
  'mean_y': 7.5,
  'series': 'III'},
 {'data': [{'x': 8.0, 'y': 6.58},
           {'x': 8.0, 'y': 5.76},
           {'x': 8.0, 'y': 7.71},
           {'x': 8.0, 'y': 8.84},
           {'x': 8.0, 'y': 8.47},
           {'x': 8.0, 'y': 7.04},
           {'x': 8.0, 'y': 5.25},
           {'x': 19.0, 'y': 12.5},
           {'x': 8.0, 'y': 5.56},
           {'x': 8.0, 'y': 7.91},
           {'x': 8.0, 'y': 6.89}],
  'mean_x': 9.0,
  'mean_y': 7.500909090909091,
  'series': 'IV'}]

"""


Summary_Func = Callable[[Iterable[float]], float]


def set_summary(
        data: List[Series], summary: Summary_Func) -> None:
    for series in data:
        for variable_name in "x", "y":
            summary_name = f"{summary.__name__}_{variable_name}"
            samples = data_iter(series, variable_name)
            series[summary_name] = summary(samples)


from pathlib import Path
import json

def summarize(source_path: Path):
    data: List[Series] = json.loads(
        source_path.read_text(),
    )

    import statistics

    for function in (
        statistics.mean,
        statistics.median,
        min,
        max,
        statistics.variance,
        statistics.stdev,
    ):
        # reveal_type(function)  # shows builtins.function
        set_summary(data, cast(Summary_Func, function))

    print(json.dumps(data, indent=2))


test_summarize = """
>>> summarize(source_path = Path('data/anscombe.json'))
[
  {
    "series": "I",
    "data": [
      {
        "x": 10.0,
        "y": 8.04
      },
      {
        "x": 8.0,
        "y": 6.95
      },
      {
        "x": 13.0,
        "y": 7.58
      },
      {
        "x": 9.0,
        "y": 8.81
      },
      {
        "x": 11.0,
        "y": 8.33
      },
      {
        "x": 14.0,
        "y": 9.96
      },
      {
        "x": 6.0,
        "y": 7.24
      },
      {
        "x": 4.0,
        "y": 4.26
      },
      {
        "x": 12.0,
        "y": 10.84
      },
      {
        "x": 7.0,
        "y": 4.82
      },
      {
        "x": 5.0,
        "y": 5.68
      }
    ],
    "mean_x": 9.0,
    "mean_y": 7.500909090909091,
    "median_x": 9.0,
    "median_y": 7.58,
    "min_x": 4.0,
    "min_y": 4.26,
    "max_x": 14.0,
    "max_y": 10.84,
    "variance_x": 11.0,
    "variance_y": 4.127269090909091,
    "stdev_x": 3.3166247903554,
    "stdev_y": 2.031568135925815
  },
  {
    "series": "II",
    "data": [
      {
        "x": 10.0,
        "y": 9.14
      },
      {
        "x": 8.0,
        "y": 8.14
      },
      {
        "x": 13.0,
        "y": 8.74
      },
      {
        "x": 9.0,
        "y": 8.77
      },
      {
        "x": 11.0,
        "y": 9.26
      },
      {
        "x": 14.0,
        "y": 8.1
      },
      {
        "x": 6.0,
        "y": 6.13
      },
      {
        "x": 4.0,
        "y": 3.1
      },
      {
        "x": 12.0,
        "y": 9.13
      },
      {
        "x": 7.0,
        "y": 7.26
      },
      {
        "x": 5.0,
        "y": 4.74
      }
    ],
    "mean_x": 9.0,
    "mean_y": 7.500909090909091,
    "median_x": 9.0,
    "median_y": 8.14,
    "min_x": 4.0,
    "min_y": 3.1,
    "max_x": 14.0,
    "max_y": 9.26,
    "variance_x": 11.0,
    "variance_y": 4.127629090909091,
    "stdev_x": 3.3166247903554,
    "stdev_y": 2.0316567355016177
  },
  {
    "series": "III",
    "data": [
      {
        "x": 10.0,
        "y": 7.46
      },
      {
        "x": 8.0,
        "y": 6.77
      },
      {
        "x": 13.0,
        "y": 12.74
      },
      {
        "x": 9.0,
        "y": 7.11
      },
      {
        "x": 11.0,
        "y": 7.81
      },
      {
        "x": 14.0,
        "y": 8.84
      },
      {
        "x": 6.0,
        "y": 6.08
      },
      {
        "x": 4.0,
        "y": 5.39
      },
      {
        "x": 12.0,
        "y": 8.15
      },
      {
        "x": 7.0,
        "y": 6.42
      },
      {
        "x": 5.0,
        "y": 5.73
      }
    ],
    "mean_x": 9.0,
    "mean_y": 7.5,
    "median_x": 9.0,
    "median_y": 7.11,
    "min_x": 4.0,
    "min_y": 5.39,
    "max_x": 14.0,
    "max_y": 12.74,
    "variance_x": 11.0,
    "variance_y": 4.12262,
    "stdev_x": 3.3166247903554,
    "stdev_y": 2.030423601123667
  },
  {
    "series": "IV",
    "data": [
      {
        "x": 8.0,
        "y": 6.58
      },
      {
        "x": 8.0,
        "y": 5.76
      },
      {
        "x": 8.0,
        "y": 7.71
      },
      {
        "x": 8.0,
        "y": 8.84
      },
      {
        "x": 8.0,
        "y": 8.47
      },
      {
        "x": 8.0,
        "y": 7.04
      },
      {
        "x": 8.0,
        "y": 5.25
      },
      {
        "x": 19.0,
        "y": 12.5
      },
      {
        "x": 8.0,
        "y": 5.56
      },
      {
        "x": 8.0,
        "y": 7.91
      },
      {
        "x": 8.0,
        "y": 6.89
      }
    ],
    "mean_x": 9.0,
    "mean_y": 7.500909090909091,
    "median_x": 8.0,
    "median_y": 7.04,
    "min_x": 8.0,
    "min_y": 5.25,
    "max_x": 19.0,
    "max_y": 12.5,
    "variance_x": 11.0,
    "variance_y": 4.123249090909091,
    "stdev_x": 3.3166247903554,
    "stdev_y": 2.0305785113876023
  }
]
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}

if __name__ == "__main__":
    summarize(source_path=Path("data/anscombe.json"))
