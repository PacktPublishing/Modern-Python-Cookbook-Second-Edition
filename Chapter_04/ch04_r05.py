"""Python Cookbook 2nd ed.

Chapter 4, recipe 5, Writing list-related type hints
"""

from typing import List, Tuple, Union

scheme = [
    ("Brick_Red", (198, 45, 66)),
    ("color1", (198.00, 100.50, 45.00)),
    ("color2", (198.00, 45.00, 142.50)),
]

RGB_I = Tuple[int, int, int]
RGB_F = Tuple[float, float, float]
ColorRGB = Tuple[str, Union[RGB_I, RGB_F]]
ColorRGBList = List[ColorRGB]

BadIdea = List[Tuple[str, Union[Tuple[int, int, int], Tuple[float, float, float]]]]


def hexify(r: float, g: float, b: float) -> str:
    """
    >>> hexify(198, 45, 66)
    '#C62D42'
    >>> r, g, b = 198, 45, 66
    >>> f"#{int(r):02X}{int(g):02X}{int(b):02X}"
    '#C62D42'
    """
    return f"#{int(r)<<16 | int(g)<<8 | int(b):06X}"


ColorCode = Tuple[str, str]
ColorCodeList = List[ColorCode]


def source_to_hex(src: ColorRGBList) -> ColorCodeList:
    return [(n, hexify(*color)) for n, color in src]


test_list = """
>>> scheme
[('Brick_Red', (198, 45, 66)), ('color1', (198.0, 100.5, 45.0)), ('color2', (198.0, 45.0, 142.5))]
>>> source_to_hex(scheme)
[('Brick_Red', '#C62D42'), ('color1', '#C6642D'), ('color2', '#C62D8E')]
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
