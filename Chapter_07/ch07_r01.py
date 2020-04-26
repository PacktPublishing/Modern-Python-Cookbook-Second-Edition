"""Python Cookbook 2nd ed.

Chapter 7, recipe 1, Using a class to encapsulate data and processing
"""
from random import randint
from typing import Tuple


class Dice:
    def __init__(self) -> None:
        # No value provided, only a type hint.
        self.faces: Tuple[int, int] = (0, 0)

    def roll(self) -> None:
        self.faces = (randint(1, 6), randint(1, 6))

    def total(self) -> int:
        return sum(self.faces)

    def hardway(self) -> bool:
        return self.faces[0] == self.faces[1]

    def easyway(self) -> bool:
        return self.faces[0] != self.faces[1]


test_example1 = """
>>> import random
>>> random.seed(42)
>>> d1 = Dice()
>>> d1.roll()
>>> d1.total()
7
>>> d1.faces
(6, 1)

>>> d1.total()
7
"""

test_example2 = """
>>> d2 = Dice()
>>> d2.roll()
>>> d2.total()
7
>>> d2.hardway()
False
>>> d2.faces
(1, 6)
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
