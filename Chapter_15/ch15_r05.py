"""Python Cookbook 2nd ed.

Chapter 15, recipe 5, Computing an autocorrelation

Raw data source: ftp://ftp.cmdl.noaa.gov/ccg/co2/trends/co2_mm_mlo.txt

Note: Output from this is used in Chapter 4 examples.
"""

from pathlib import Path
import csv
import json
from typing import Iterable, Iterator, Dict, TextIO


def non_comment_iter(source: Iterable[str]) -> Iterator[str]:
    for line in source:
        if line[0] == "#":
            continue
        yield line


def raw_data_iter(
        source: Iterable[str]) -> Iterator[Dict[str, str]]:
    header = [
        "year",
        "month",
        "decimal_date",
        "average",
        "interpolated",
        "trend",
        "days",
    ]
    rdr = csv.DictReader(
        source, header, delimiter=" ", skipinitialspace=True)
    return rdr


from typing import NamedTuple


class Sample(NamedTuple):
    year: int
    month: int
    decimal_date: float
    average: float
    interpolated: float
    trend: float
    days: int


def cleanse(row: Dict[str, str]) -> Sample:
    return Sample(
        year=int(row["year"]),
        month=int(row["month"]),
        decimal_date=float(row["decimal_date"]),
        average=float(row["average"]),
        interpolated=float(row["interpolated"]),
        trend=float(row["trend"]),
        days=int(row["days"]),
    )


def get_data(source_file: TextIO) -> Iterator[Sample]:
    non_comment_data = non_comment_iter(source_file)
    raw_data = raw_data_iter(non_comment_data)
    cleansed_data = (cleanse(row) for row in raw_data)
    return cleansed_data

test_get_data = """
>>> source_path = Path("data") / "co2_mm_mlo.txt"
>>> with source_path.open() as source_file:
...     all_data = list(get_data(source_file))
>>> all_data[:3]  # doctest: +NORMALIZE_WHITESPACE
[Sample(year=1958, month=3, decimal_date=1958.208, average=315.71, interpolated=315.71, trend=314.62, days=-1), 
 Sample(year=1958, month=4, decimal_date=1958.292, average=317.45, interpolated=317.45, trend=315.29, days=-1), 
 Sample(year=1958, month=5, decimal_date=1958.375, average=317.5, interpolated=317.5, trend=314.71, days=-1)]

"""
__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}


from Chapter_15.ch15_r03 import correlation, Point
from Chapter_15.ch15_r04 import regression
from statistics import mean, median

if __name__ == "__main__":
    source_path = Path("data") / "co2_mm_mlo.txt"
    with source_path.open() as source_file:

        co2_ppm = list(
            row.interpolated
            for row in get_data(source_file))
        print(f"Read {len(co2_ppm)} Samples")

    for tau in range(1, 20):
        data = [
            Point({"x": x, "y": y})
            for x, y in zip(co2_ppm[:-tau], co2_ppm[tau:])
        ]
        r_tau_0 = correlation(data[:60])
        r_tau_60 = correlation(data[60:120])
        print(f"r_{{xx}}(τ={tau:2d}) = {r_tau_0:6.3f}")

    monthly_mean = [
        Point(
            {"x": x, "y": mean(co2_ppm[x : x + 12])}
        )
        for x in range(0, len(co2_ppm), 12)
    ]

    # print(monthly_mean)
    alpha, beta = regression(monthly_mean)
    print(f"y = {alpha:.1f}+x*{beta:.4f}")
    r = correlation(monthly_mean)
    print(f"r^2 = {r**2:.3f}")

    for d in monthly_mean:
        print(f"{d} x={d['x']}, y={alpha+d['x']*beta}")
