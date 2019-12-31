"""Python Cookbook 2nd ed.

Chapter 3, recipe 3, Designing type hints for optional parameters
"""
import random


def dice(n, sides=6):
    return tuple(random.randint(1, sides) for _ in range(n))


test_dice = """
>>> random.seed(113)
>>> dice(2)
(1, 6)
"""

from typing import Tuple


def dice_t(n: int, sides: int = 6) -> Tuple[int, ...]:
    return tuple(random.randint(1, sides) for _ in range(n))


Dice = Tuple[int, ...]


def craps() -> Dice:
    return dice_t(2)


def zonk(n: int = 6) -> Dice:
    return dice_t(n)


def mage_hitpoints(n) -> int:
    return sum(dice_t(n, 4))


test_craps = """
>>> random.seed(113)
>>> craps()
(1, 6)
"""

test_zonk = """
>>> random.seed(113)
>>> zonk()
(1, 6, 6, 3, 1, 4)
"""

test_mage = """
>>> random.seed(113)
>>> mage_hitpoints(8)
19
"""

from typing import Optional, Tuple


def polydice(n: Optional[int] = None, sides: int = 6) -> Tuple[int, ...]:
    if n is None:
        n = 2 if sides == 6 else 1
    return tuple(random.randint(1, sides) for _ in range(n))


test_polydice = """
>>> random.seed(113)
>>> polydice()
(1, 6)
>>> polydice(6)
(6, 3, 1, 4, 5, 3)
>>> polydice(sides=8)
(4,)
>>> polydice(n=8, sides=4)
(4, 1, 1, 3, 2, 3, 4, 3)
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
