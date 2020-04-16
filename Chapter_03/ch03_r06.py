"""Python Cookbook 2nd ed.

Chapter 3, recipe 6, Defining position-only parameters with the / separator

"""


def F(c: float, /) -> float:
    return 32 + c * (9 / 5)


def C(f: float, /, truncate: bool=False) -> float:
    c = 5 * (f - 32) / 9
    if truncate:
        return round(c, 0)
    return c


test_f = """
>>> F(0)
32.0
>>> F(25)
77.0
"""

test_c = """
>>> C(32)
0.0
>>> C(77)
25.0
>>> round(C(72), 3)
22.222
>>> C(72)  # doctest: +ELLIPSIS
22.22222222222222...
>>> C(72, truncate=True)
22.0
>>> C(72, True)
22.0
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
