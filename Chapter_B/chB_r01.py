"""Python Cookbook 2nd ed.

Chapter B, Bonus, recipe 1, Using the statistics library
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

def data_iter(
        series: Series, variable_name: str) -> Iterable[Any]:
    return (
        item[variable_name]
        for item in cast(List[Point], series["data"])
    )


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
