"""Python Cookbook 2nd ed.

Chapter 3, recipe 7, Writing hints for more complex types
"""

from typing import Optional, Union, Dict
from decimal import Decimal


def temperature(
        *,
        f_temp: Optional[float] = None,
        c_temp: Optional[float] = None
    ) -> Dict[str, float]:
    """Convert between Fahrenheit temperature and
    Celsius temperature.

    :key f_temp: Temperature in °F.
    :key c_temp: Temperature in °C.
    :returns: dictionary with two keys:
        :f_temp: Temperature in °F.
        :c_temp: Temperature in °C.
    """

    if f_temp is not None:
        c_temp = 5 * (f_temp - 32) / 9
    elif c_temp is not None:
        f_temp = 32 + 9 * c_temp / 5
    else:
        raise TypeError("One of f_temp or c_temp must be provided")
    result: Dict[str, float] = {"c_temp": c_temp, "f_temp": f_temp}
    return result


def temperature_bad(
    *, f_temp: Optional[float] = None, c_temp: Optional[float] = None
) -> float:
    if f_temp is not None:
        c_temp = 5 * (f_temp - 32) / 9
    elif f_temp is not None:
        f_temp = 32 + 9 * c_temp / 5
    else:
        raise TypeError("One of f_temp or c_temp must be provided")
    result = {"c_temp": c_temp, "f_temp": f_temp}
    return result  # type: ignore


# Without the type: ignore, we'll get mypy errors.
# Chapter_03/ch03_r07.py:45: error: Incompatible return value type (got "Dict[str, float]", expected "float")

from pytest import approx  # type: ignore


def test_temperature():
    assert temperature(f_temp=72) == {"c_temp": approx(22.22222), "f_temp": 72}
    assert temperature(c_temp=22.2) == {"c_temp": 22.2, "f_temp": approx(71.96)}


from mypy_extensions import TypedDict

TempDict = TypedDict("TempDict", {"c_temp": float, "f_temp": float,})


def temperature_d(
    *, f_temp: Optional[float] = None, c_temp: Optional[float] = None
) -> TempDict:
    """Convert between Fahrenheit temperature and
    Celsius temperature.

    :key f_temp: Temperature in °F.
    :key c_temp: Temperature in °C.
    :returns: dictionary with two keys:
        :f_temp: Temperature in °F.
        :c_temp: Temperature in °C.
    """

    if f_temp is not None:
        c_temp = 5 * (f_temp - 32) / 9
    elif c_temp is not None:
        f_temp = 32 + 9 * c_temp / 5
    else:
        raise TypeError("One of f_temp or c_temp must be provided")
    result: TempDict = {"c_temp": c_temp, "f_temp": f_temp}
    return result
