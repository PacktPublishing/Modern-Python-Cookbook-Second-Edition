"""Python Cookbook 2nd ed.

Chapter 3, Recipe 11, Writing reusable scripts with the script-library switch

Note: Output from this is used in Chapter 4 examples.
"""
import csv
from pathlib import Path
from math import radians, sin, cos, sqrt, asin
from functools import partial
from pathlib import Path

MI = 3959
NM = 3440
KM = 6373


def haversine(
    lat_1: float, lon_1: float, lat_2: float, lon_2: float, *, R: float
) -> float:
    """Distance between points.

    R is radius, R=MI computes in miles. Default is nautical miles.

    >>> round(haversine(36.12, -86.67, 33.94, -118.40, R=6372.8), 5)
    2887.25995
    """
    Δ_lat = radians(lat_2) - radians(lat_1)
    Δ_lon = radians(lon_2) - radians(lon_1)
    lat_1 = radians(lat_1)
    lat_2 = radians(lat_2)

    a = sqrt(sin(Δ_lat / 2) ** 2 + cos(lat_1) * cos(lat_2) * sin(Δ_lon / 2) ** 2)
    c = 2 * asin(a)

    return R * c


nm_haversine = partial(haversine, R=NM)


def distances(source_path: Path = Path("data/waypoints.csv")) -> None:
    with source_path.open() as source_file:
        reader = csv.DictReader(source_file)
        start = next(reader)  # Seed pairing with the first row
        for point in reader:
            d = nm_haversine(
                float(start["lat"]),
                float(start["lon"]),
                float(point["lat"]),
                float(point["lon"]),
            )
            print(start, point, d)
            start = point


def test_distance(capsys):
    distances()
    out, err = capsys.readouterr()
    assert out.splitlines() == [
        "{'lat': '32.8321666666667', 'lon': '-79.9338333333333', 'date': "
        "'2012-11-27', 'time': '09:15:00'} {'lat': '31.6714833333333', 'lon': "
        "'-80.93325', 'date': '2012-11-28', 'time': '00:00:00'} 86.20442280809627",
        "{'lat': '31.6714833333333', 'lon': '-80.93325', 'date': '2012-11-28', "
        "'time': '00:00:00'} {'lat': '30.7171666666667', 'lon': '-81.5525', 'date': "
        "'2012-11-28', 'time': '11:35:00'} 65.5310772193093",
    ]


if __name__ == "__main__":
    distances()
