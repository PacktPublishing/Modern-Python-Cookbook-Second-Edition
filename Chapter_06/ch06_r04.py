"""Python Cookbook 2nd ed.

Chapter 6, recipe 4, Using argparse to get command-line input
"""

import argparse
import sys
from typing import Tuple, List
from Chapter_03.ch03_r08 import haversine, MI, NM, KM


def point_type(text: str) -> Tuple[float, float]:
    """
    >>> point_type('36.12, -86.67')
    (36.12, -86.67)
    >>> point_type('36.12, 76.abc')
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/cookbook/lib/python3.8/doctest.py", line 1328, in __run
        exec(compile(example.source, filename, "single",
      File "<doctest ch06_r04.point_type[1]>", line 1, in <module>
        point_type('36.12, 76.abc')
      File "Chapter_06.ch06_r04.py", line 22, in point_type
        raise argparse.ArgumentTypeError from ex
    argparse.ArgumentTypeError: could not convert string to float: ' 76.abc'
    """
    try:
        lat_str, lon_str = text.split(",")
        lat = float(lat_str)
        lon = float(lon_str)
        return lat, lon
    except ValueError as ex:
        raise argparse.ArgumentTypeError(ex)


def get_options(argv: List[str]) -> argparse.Namespace:
    """
    >>> opts = get_options(['-u', 'KM', '36.12,-86.67', '33.94,-118.4'])
    >>> opts.units
    'KM'
    >>> opts.p1
    (36.12, -86.67)
    >>> opts.p2
    (33.94, -118.4)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u", "--units",
        action="store", choices=("NM", "MI", "KM"), default="NM")
    parser.add_argument(
        "p1", action="store", type=point_type)
    parser.add_argument(
        "p2", action="store", type=point_type)
    options = parser.parse_args(argv)
    return options


def display(lat1: float, lon1: float, lat2: float, lon2: float, r: str) -> None:
    """
    >>> display(36.12, -86.67, 33.94, -118.4, 'NM')
    From 36.12,-86.67 to 33.94,-118.4 in NM = 1558.53
    """
    r_float = {"NM": NM, "KM": KM, "MI": MI}[r]
    d = haversine(lat1, lon1, lat2, lon2, r_float)
    print(f"From {lat1},{lon1} to {lat2},{lon2} in {r} = {d:.2f}")


def main(argv: List[str] = sys.argv[1:]) -> None:
    options = get_options(argv)
    lat_1, lon_1 = options.p1
    lat_2, lon_2 = options.p2
    display(lat_1, lon_1, lat_2, lon_2, options.units)


if __name__ == "__main__":
    main()
