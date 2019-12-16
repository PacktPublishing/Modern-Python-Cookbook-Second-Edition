"""Python Cookbook 2nd ed.

Chapter 10, recipe 5.

Raw data source: ftp://ftp.cmdl.noaa.gov/ccg/co2/trends/co2_mm_mlo.txt

Note: Output from this is used in Chapter 4 examples.
"""

from pathlib import Path
import csv
import json
from typing import Iterable, Iterator, Dict, TextIO


def non_comment_iter(source: TextIO) -> Iterator[str]:
    for line in source:
        if line[0] == "#":
            continue
        yield line


def raw_data_iter(source: Iterable[str]) -> Iterator[Dict[str, str]]:
    header = [
        "year",
        "month",
        "decimal_date",
        "average",
        "interpolated",
        "trend",
        "days",
    ]
    rdr = csv.DictReader(source, header, delimiter=" ", skipinitialspace=True)
    return rdr


# from types import SimpleNamespace as Sample
from typing import NamedTuple


class Sample(NamedTuple):
    year: int
    month: int
    decimal_date: float
    average: float
    interpolated: float
    trend: float
    days: int


def cleanse(row: Dict[str, str]):
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

    # print(list(raw_data)[:10])

    cleansed_data = (cleanse(row) for row in raw_data)

    # print(list(cleansed_data)[:10])
    return cleansed_data


from Chapter_10.ch10_r03 import correlation
from Chapter_10.ch10_r04 import regression
from statistics import mean, median

if __name__ == "__main__":
    source_path = Path("data") / "co2_mm_mlo.txt"
    with source_path.open() as source_file:

        co2_ppm = list(row.interpolated for row in get_data(source_file))
        print(len(co2_ppm))
        # print(co2_ppm)

        for tau in range(1, 20):
            # print(co2_ppm[:-tau], co2_ppm[tau:])
            data = [{"x": x, "y": y} for x, y in zip(co2_ppm[:-tau], co2_ppm[tau:])]
            r_tau_0 = correlation(data[:60])
            r_tau_60 = correlation(data[60:120])
            print(f"r_{{xx}}(τ={tau:2d}) = {r_tau_0:6.3f}")

        monthly_mean = [
            {"x": x, "y": mean(co2_ppm[x : x + 12])} for x in range(0, len(co2_ppm), 12)
        ]

        # print(monthly_mean)
        alpha, beta = regression(monthly_mean)
        print(f"y = {alpha}+x*{beta}")
        r = correlation(monthly_mean)
        print(f"r^2 = {r**2}")

        for d in monthly_mean:
            print(f"{d} x={d['x']}, y={alpha+d['x']*beta}")
