"""Python Cookbook 2nd ed.

Chapter 6, recipe 1
"""
import random
from typing import Tuple


class Dice:
    def __init__(self) -> None:
        # No value provided, only a type hint.
        self.faces: Tuple[int, int]

    def roll(self) -> None:
        self.faces = (random.randint(1, 6), random.randint(1, 6))

    def total(self) -> int:
        return sum(self.faces)

    def hardway(self) -> bool:
        return self.faces[0] == self.faces[1]

    def easyway(self) -> bool:
        return self.faces[0] != self.faces[1]


__test__ = {
    "example1": """
>>> import random
>>> random.seed(1)
>>> d1 = Dice()
>>> d1.roll()
>>> d1.total()
7
>>> d1.faces
(2, 5)

>>> d1.total()
7
""",
    "example2": """
>>> d2 = Dice()
>>> d2.roll()
>>> d2.total()
4
>>> d2.hardway()
False
>>> d2.faces
(1, 3)
""",
}
