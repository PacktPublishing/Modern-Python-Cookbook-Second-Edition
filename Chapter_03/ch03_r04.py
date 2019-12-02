"""Python Cookbook 2nd ed.

Chapter 3, recipe 4
"""
from typing import *

# from fractions import Fraction
from decimal import Decimal

Number = Union[int, float, complex, Decimal]


def temperature(
    *, f_temp: Optional[Number] = None, c_temp: Optional[Number] = None
) -> Mapping[str, Number]:

    if f_temp is not None:
        c_temp = 5 * (f_temp - 32) / 9
    elif c_temp is not None:
        f_temp = 32 + 9 * c_temp / 5
    else:
        raise Exception("Logic Design Problem")
    result: Dict[str, Number] = {"c_temp": c_temp, "f_temp": f_temp}
    return result


def temperature_bad(
    *, f_temp: Optional[Number] = None, c_temp: Optional[Number] = None
) -> Number:

    if f_temp is not None:
        c_temp = 5 * (f_temp - 32) / 9
    elif f_temp is not None:
        f_temp = 32 + 9 * c_temp / 5
    else:
        raise Exception("Logic Design Problem")
    result = {"c_temp": c_temp, "f_temp": f_temp}  # type: Dict[str, Number]
    return result  # type: ignore


# Chapter_03/ch03_r04.py:40: error: Incompatible return value type (got "Dict[str, Union[int, float, complex, Decimal]]", expected "Union[int, float, complex, Decimal]")

from pytest import approx  # type: ignore


def test_temperature():
    assert temperature(f_temp=72) == {"c_temp": approx(22.22222), "f_temp": 72}
    assert temperature(c_temp=22.2) == {"c_temp": 22.2, "f_temp": approx(71.96)}
