"""Python Cookbook 2nd ed.

Chapter 6, recipe 6, Using the OS environment settings
"""
import argparse
import os
import sys
from typing import List

from Chapter_03.ch03_r08 import haversine, MI, NM, KM
from Chapter_06.ch06_r04 import point_type, display


def get_options(argv: List[str] = sys.argv[1:]) -> argparse.Namespace:
    """
    >>> os.environ['UNITS'] = 'NM'
    >>> get_options(['36.12,-86.67'])
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/cookbook/lib/python3.8/doctest.py", line 1328, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.get_options[1]>", line 1, in <module>
        get_options(['ch06_r06.py', '36.12,-86.67'])
      File "/Users/slott/Documents/Writing/Python/Python Cookbook 2e/Code/ch06_r06.py", line 49, in get_options
        sys.exit("Neither HOME_PORT nor p2 argument provided.")
    SystemExit: Neither HOME_PORT nor p2 argument provided.

    >>> os.environ['UNITS'] = 'NM'
    >>> os.environ['HOME_PORT'] = '36.842952,-76.300171'
    >>> get_options(['36.12,-86.67'])
    Namespace(p1=(36.12, -86.67), p2=(36.842952, -76.300171), units='NM')

    >>> os.environ['UNITS'] = 'XX'
    >>> os.environ['HOME_PORT'] = '36.842952,-76.300171'
    >>> get_options(['36.12,-86.67'])
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/cookbook/lib/python3.8/doctest.py", line 1328, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.get_options[5]>", line 1, in <module>
        get_options(['ch06_r06.py', '36.12,-86.67'])
      File "/Users/slott/Documents/Writing/Python/Python Cookbook 2e/Code/ch06_r06.py", line 27, in get_options
        sys.exit("Invalid value for UNITS, not KM, NM, or MI")
    SystemExit: Invalid UNITS, 'XX' not KM, NM, or MI
    """
    default_units = os.environ.get("UNITS", "KM")
    if default_units not in ("KM", "NM", "MI"):
        sys.exit(f"Invalid UNITS, {default_units!r} not KM, NM, or MI")
    default_home_port = os.environ.get("HOME_PORT")
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-u", "--units",
        action="store", choices=("NM", "MI", "KM"), default=default_units
    )
    parser.add_argument("p1", action="store", type=point_type)
    parser.add_argument(
        "p2", nargs="?", action="store", type=point_type, default=default_home_port
    )
    options = parser.parse_args(argv)

    if options.p2 is None:
        sys.exit("Neither HOME_PORT nor p2 argument provided.")

    return options


def main(argv: List[str] = sys.argv[1:]) -> None:
    options = get_options()
    lat_1, lon_1 = options.p1
    lat_2, lon_2 = options.p2
    display(lat_1, lon_1, lat_2, lon_2, options.units)


if __name__ == "__main__":
    main()
