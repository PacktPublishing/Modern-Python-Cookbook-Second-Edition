"""Python Cookbook 2nd ed.

Chapter 3, Recipe 5
"""
from math import radians, sin, cos, sqrt, asin
from typing import Callable

MI = 3959
NM = 3440
KM = 6373


def haversine(
    lat_1: float, lon_1: float, lat_2: float, lon_2: float, R: float = NM
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

    a = sin(Δ_lat / 2) ** 2 + cos(lat_1) * cos(lat_2) * sin(Δ_lon / 2) ** 2
    c = 2 * asin(sqrt(a))

    return R * c


# Note the lack of parameter type hints -- the *args anonymizes the parameters.
def nm_haversine(*args):
    """
    >>> round(nm_haversine(36.12, -86.67, 33.94, -118.40), 2)
    1558.53
    """
    return haversine(*args, R=NM)


# To avoid confusion about whether or not R is in *args, we're forced to provide explicit parameter types.
def nm_haversine1(lat_1: float, lon_1: float, lat_2: float, lon_2: float) -> float:
    """
    >>> round(nm_haversine(36.12, -86.67, 33.94, -118.40), 2)
    1558.53
    """
    return haversine(lat_1, lon_1, lat_2, lon_2, R=NM)


from functools import partial

nm_haversine2 = partial(haversine, R=NM)

# Lambda's don't permit type hints without some rather complex-looking syntax
NM_Hav = Callable[[float, float, float, float], float]
nm_haversine3: NM_Hav = lambda lat_1, lon_1, lat_2, lon_2: haversine(
    lat_1, lon_1, lat_2, lon_2, R=NM
)

__test__ = {
    "manual": """\
>>> round(nm_haversine1(36.12, -86.67, 33.94, -118.40), 2)
1558.53
""",
    "partial": """\
>>> round(nm_haversine2(36.12, -86.67, 33.94, -118.40), 2)
1558.53
""",
    "lambda": """\
>>> round(nm_haversine3(36.12, -86.67, 33.94, -118.40), 2)
1558.53
""",
}

from pytest import approx  # type: ignore


def test_haversine():
    assert nm_haversine1(36.12, -86.67, 33.94, -118.40) == approx(1558.526)
    assert nm_haversine2(36.12, -86.67, 33.94, -118.40) == approx(1558.526)
    assert nm_haversine3(36.12, -86.67, 33.94, -118.40) == approx(1558.526)
    assert haversine(36.12, -86.67, 33.94, -118.40, R=NM) == approx(1558.526)
