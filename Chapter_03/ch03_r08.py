"""Python Cookbook 2nd ed.

Chapter 3, Recipe 8, Picking an order for parameters based on partial functions
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

    a = sqrt(sin(Δ_lat / 2) ** 2 + cos(lat_1) * cos(lat_2) * sin(Δ_lon / 2) ** 2)

    return R * 2 * asin(a)


# Note the lack of parameter type hints -- the *args anonymizes the parameters.
def nm_haversine_1(*args):
    """
    >>> round(nm_haversine_1(36.12, -86.67, 33.94, -118.40), 2)
    1558.53
    """
    return haversine(*args, R=NM)


# To avoid confusion about whether or not R is in *args, we're forced to provide explicit parameter types.
def nm_haversine_2(lat_1: float, lon_1: float, lat_2: float, lon_2: float) -> float:
    """
    >>> round(nm_haversine_2(36.12, -86.67, 33.94, -118.40), 2)
    1558.53
    """
    return haversine(lat_1, lon_1, lat_2, lon_2, R=NM)


from functools import partial

nm_haversine_3 = partial(haversine, R=NM)


test_manual = """
>>> round(nm_haversine_1(36.12, -86.67, 33.94, -118.40), 2)
1558.53
>>> round(nm_haversine_2(36.12, -86.67, 33.94, -118.40), 2)
1558.53
"""
test_partial = """
>>> round(nm_haversine_3(36.12, -86.67, 33.94, -118.40), 2)
1558.53
"""

from pytest import approx  # type: ignore


def test_haversine():
    assert nm_haversine_1(36.12, -86.67, 33.94, -118.40) == approx(1558.526)
    assert nm_haversine_2(36.12, -86.67, 33.94, -118.40) == approx(1558.526)
    assert nm_haversine_3(36.12, -86.67, 33.94, -118.40) == approx(1558.526)
    assert haversine(36.12, -86.67, 33.94, -118.40, R=NM) == approx(1558.526)


def p_haversine(
    R: float, lat_1: float, lon_1: float, lat_2: float, lon_2: float
) -> float:
    Δ_lat = radians(lat_2) - radians(lat_1)
    Δ_lon = radians(lon_2) - radians(lon_1)
    lat_1 = radians(lat_1)
    lat_2 = radians(lat_2)

    a = sqrt(sin(Δ_lat / 2) ** 2 + cos(lat_1) * cos(lat_2) * sin(Δ_lon / 2) ** 2)

    return R * 2 * asin(a)


from functools import partial

nm_haversine_4 = partial(p_haversine, NM)

test_ordered = """
>>> round(nm_haversine_4(36.12, -86.67, 33.94, -118.40), 2)
1558.53
"""

# Lambda's don't permit type hints without some rather complex-looking syntax
NM_Hav = Callable[[float, float, float, float], float]
nm_haversine_5: NM_Hav = lambda lat_1, lon_1, lat_2, lon_2: haversine(
    lat_1, lon_1, lat_2, lon_2, R=NM
)
test_lambda = """
>>> round(nm_haversine_5(36.12, -86.67, 33.94, -118.40), 2)
1558.53
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
