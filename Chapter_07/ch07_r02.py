"""Python Cookbook 2nd ed.

Chapter 7, recipe 2, Essential type hints for class definitions
"""
import random
from typing import Set, List


class Dice:
    RNG = random.Random()

    def __init__(self, n: int, sides: int = 6) -> None:
        self.n_dice = n
        self.sides = sides
        self.faces: List[int]
        self.roll_number = 0

    def __str__(self) -> str:
        return ", ".join(
            f"{i}: {f}"
            for i, f in enumerate(self.faces)
        )

    def total(self) -> int:
        return sum(self.faces)

    def average(self) -> float:
        return sum(self.faces) / self.n_dice

    def first_roll(self) -> List[int]:
        self.roll_number = 0
        self.faces = [self.RNG.randint(1, self.sides) for _ in range(self.n_dice)]
        return self.faces

    def reroll(self, positions: Set[int]) -> List[int]:
        self.roll_number += 1
        for p in positions:
            self.faces[p] = self.RNG.randint(1, self.sides)
        return self.faces


# The following example has type checking disabled.
# To see the effect of using a wrong type, remove the type: ignore comments,
# and run mypy on this module.


def example_mypy_failure() -> None:
    d = Dice(2.5)  # type: ignore
    r1: List[str] = d.first_roll()  # type: ignore
    print(d)


test_dice = """
>>> d1 = Dice(5)
>>> d1.RNG.seed(42)
>>> d1.first_roll()
[6, 1, 1, 6, 3]
>>> d1.reroll({0, 3, 4})
[2, 1, 1, 2, 2]
>>> str(d1)
'0: 2, 1: 1, 2: 1, 3: 2, 4: 2'
"""

test_dice_failure = """
>>> example_mypy_failure()
Traceback (most recent call last):
    ...
TypeError: 'float' object cannot be interpreted as an integer

>>> bad = Dice(2.5)
>>> bad.first_roll()
Traceback (most recent call last):
    ...
TypeError: 'float' object cannot be interpreted as an integer

"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
