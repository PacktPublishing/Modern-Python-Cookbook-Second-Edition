"""Python Cookbook 2nd ed.

Chapter 3, recipe 1, Function parameters and type hints
"""
from typing import Tuple, Union
from math import isclose

# https://www.easyrgb.com/en/math.php

def rgb2hsl(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    r = rgb[0]/255
    g = rgb[1]/255
    b = rgb[2]/255

    min_color = min(r, g, b)
    max_color = max(r, g, b)
    delta_color = max_color - min_color

    lightness = (min_color + max_color) / 2
    if isclose(delta_color, 0.0):
        # The lightness is the shade of gray, no hue.
        hue = 0.0
        saturation = 0.0
    else:
        if lightness < 0.5:
            saturation = delta_color / (max_color + min_color)
        else:
            saturation = delta_color / (2.0 - max_color - min_color)

        mid_color = delta_color / 2
        r_factor = (((max_color - r) / 6) + mid_color) / delta_color
        g_factor = (((max_color - g) / 6) + mid_color) / delta_color
        b_factor = (((max_color - b) / 6) + mid_color) / delta_color

        if r == max_color:
            hue =       b_factor - g_factor
        elif g == max_color:
            hue = 1/3 + r_factor - b_factor
        elif b == max_color:
            hue = 2/3 + g_factor - r_factor

        if hue < 0:
            hue += 1
        if hue > 1:
            hue -= 1

    return hue, saturation, lightness

def hex2rgb(hx_int: Union[int, str]) -> Tuple[int, int, int]:
    if isinstance(hx_int, str):
        if hx_int[0] == "#":
            hx_int = int(hx_int[1:], 16)
        else:
            hx_int = int(hx_int, 16)
    # reveal_type(hx_int)
    r, g, b = (hx_int >> 16)&0xff, (hx_int >> 8)&0xff, hx_int&0xff
    return r, g, b


# Examples from https://www.easyrgb.com/en/convert.php#inputFORM
# Brick Red: #C62D42 == HSL    0-1.0 =  0.97712  0.62963  0.47647   351.76°
# Sea Green: #93DFB8 == HSL    0-1.0 =  0.41447  0.54286  0.72549   149.21°
# Wisteria: #C9A0DC == HSL    0-1.0 =  0.78056  0.46153  0.74510   281.00°

test_first_version = """
>>> def hex2rgb(hx_int):
...    if isinstance(hx_int, str):
...        if hx_int[0] == "#":
...            hx_int = int(hx_int[1:], 16)
...        else:
...            hx_int = int(hx_int, 16)
...    r, g, b = (hx_int >> 16)&0xff, (hx_int >> 8)&0xff, hx_int&0xff
...    return r, g, b
>>> hex2rgb("#C62D42")
(198, 45, 66)
"""

test_Brick_Red = """
>>> hex2rgb("#C62D42")
(198, 45, 66)
>>> h, s, l = rgb2hsl(hex2rgb("#C62D42"))
>>> f"{h:0.5f}  {s:0.5f}  {l:0.5f}"
'0.97712  0.62963  0.47647'
"""

test_Sea_Green = """
>>> hex2rgb("93DFB8")
(147, 223, 184)
>>> h, s, l = rgb2hsl(hex2rgb("93DFB8"))
>>> f"{h:0.5f}  {s:0.5f}  {l:0.5f}"
'0.41447  0.54286  0.72549'
"""

test_Wisteria = """
>>> hex2rgb(0xC9A0DC)
(201, 160, 220)
>>> h, s, l = rgb2hsl(hex2rgb(0xC9A0DC))
>>> f"{h:0.5f}  {s:0.5f}  {l:0.5f}"
'0.78056  0.46154  0.74510'
"""


from typing import NamedTuple
class RGB(NamedTuple):
    red: int
    green: int
    blue: int

def hex_to_rgb2(hx_int: Union[int, str]) -> RGB:
    """
    >>> hex_to_rgb2("#C62D42")
    RGB(red=198, green=45, blue=66)
    >>> hex_to_rgb2("C62D42")
    RGB(red=198, green=45, blue=66)
    >>> hex_to_rgb2(0xC62D42)
    RGB(red=198, green=45, blue=66)
    """
    if isinstance(hx_int, str):
        if hx_int[0] == "#":
            hx_int = int(hx_int[1:], 16)
        else:
            hx_int = int(hx_int, 16)
    # reveal_type(hx_int)
    return RGB(
        (hx_int >> 16)&0xff,
        (hx_int >> 8)&0xff,
        (hx_int&0xff)
    )

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
