"""Python Cookbook 2nd ed.

Chapter 8, recipe 3, Leveraging Python's duck typing
"""
import random
from typing import Tuple, Optional, List, Iterator, Type


class Dice1:
    def __init__(self, seed=None) -> None:
        self._rng = random.Random(seed)
        self.roll()

    def roll(self) -> Tuple[int, ...]:
        self.dice = (self._rng.randint(1, 6), self._rng.randint(1, 6))
        return self.dice


class Die:
    def __init__(self, rng: random.Random) -> None:
        self._rng = rng

    def roll(self) -> int:
        return self._rng.randint(1, 6)


class Dice2:
    def __init__(self, seed: Optional[int] = None) -> None:
        self._rng = random.Random(seed)
        self._dice = [Die(self._rng) for _ in range(2)]
        self.roll()

    def roll(self) -> Tuple[int, ...]:
        self.dice = tuple(d.roll() for d in self._dice)
        return self.dice


def roller(
    dice_class: Type[Dice2], seed: int = None, *, samples: int = 10
) -> Iterator[Tuple[int, ...]]:
    dice = dice_class(seed)
    for _ in range(samples):
        yield dice.roll()


test_roller = """
>>> from Chapter_08.ch08_r03 import roller, Dice1, Dice2
>>> list(roller(Dice1, 1, samples=5))
[(1, 3), (1, 4), (4, 4), (6, 4), (2, 1)]
>>> list(roller(Dice2, 1, samples=5))
[(1, 3), (1, 4), (4, 4), (6, 4), (2, 1)]
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
