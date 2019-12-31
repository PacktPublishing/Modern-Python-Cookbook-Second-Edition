"""Python Cookbook

Chapter 3, recipe 2, Designing functions with optional parameters
"""
import random
from typing import Tuple


def die() -> int:
    return random.randint(1, 6)


def craps() -> Tuple[int, int]:
    return (die(), die())


test_die_craps = """
>>> random.seed(113)
>>> die(), die()
(1, 6)
>>> craps()
(6, 3)
>>> craps()
(1, 4)
"""


def zonk() -> Tuple[int, ...]:
    return tuple(die() for x in range(6))


test_zonk = """
>>> zonk()
(5, 3, 2, 4, 1, 1)
"""


def craps2() -> Tuple[int, ...]:
    return tuple(die() for x in range(2))


def dice2(n: int) -> Tuple[int, ...]:
    return tuple(die() for x in range(n))


test_craps2_dice2 = """
>>> random.seed(113)
>>> craps2()
(1, 6)
>>> dice2(2)
(6, 3)
>>> dice2(6)
(1, 4, 5, 3, 2, 4)
"""


def dice3(n: int = 2) -> Tuple[int, ...]:
    return tuple(die() for x in range(n))


def craps3() -> Tuple[int, ...]:
    return dice3(2)


def zonk3() -> Tuple[int, ...]:
    return dice3(6)


test_dice3_craps3_zonk3 = """
>>> random.seed(113)
>>> craps3()
(1, 6)
>>> zonk3()
(6, 3, 1, 4, 5, 3)
"""


def die4(sides: int = 6) -> int:
    return random.randint(1, 6)


def dice4(n: int = 2, sides: int = 6) -> Tuple[int, ...]:
    return tuple(die4(sides) for x in range(n))


test_dice4 = """
>>> random.seed(113)
>>> dice4()
(1, 6)
>>> dice4(n=6)
(6, 3, 1, 4, 5, 3)
"""
__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
