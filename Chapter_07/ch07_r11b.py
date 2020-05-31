"""Python Cookbook 2nd ed.

Chapter 7, recipe 11b, Using contexts and context managers
"""
import random
import secrets
from typing import Iterable, List, Set, Tuple, Optional, Type
from types import TracebackType

class Dice:
    def __init__(self, n: int, /, d: int = 6) -> None:
        self.n_dice = n
        self.faces = d
        self.history: List[Tuple[int, ...]] = list()

    def roller(self) -> 'Roller':
        return Roller(self, 3)

    @property
    def roll(self) -> Tuple[int, ...]:
        if self.history:
            return self.history[-1]
        raise ValueError("Dice were never rolled")

class Roller:
    def __init__(self, dice: Dice, tries: int) -> None:
        self.dice = dice
        self.tries = tries
        self._roll: List[int] = [0 for _ in range(self.dice.n_dice)]
        self.frozen: Set[int] = set()
        self.history: List[Tuple[int, ...]] = list()

    def __enter__(self) -> 'Roller':
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[Exception]],
        exc_val: Optional[Exception],
        exc_tb: Optional[TracebackType]
    ) -> Optional[bool]:
        self.dice.history.extend(self.history)
        return None

    def roll(self) -> Tuple[int, ...]:
        if len(self.history) != self.tries:
            for i in range(self.dice.n_dice):
                if i not in self.frozen:
                    self._roll[i] = random.randint(1, self.dice.faces)
            self.history.append(tuple(self._roll))
        return self.history[-1]

    def freeze(self, *positions: int) -> None:
        self.frozen = set(positions)


if __name__ == "__main__":
    random.seed(42)
    hand = Dice(5, d=6)
    with hand.roller() as roller:
        r1 = roller.roll()
        print(r1)
        roller.freeze(0, 3)
        r2 = roller.roll()
        print(r2)
        roller.freeze(1, 2, 4)
        r3 = roller.roll()
        print(r3)
    print(hand.roll)
    print(hand.history)

test_dice_roller = """
>>> random.seed(42)
>>> hand = Dice(5, d=6)
>>> with hand.roller() as roller:
...     r1 = roller.roll()
...     print(r1)
...     roller.freeze(0, 3)
...     r2 = roller.roll()
...     print(r2)
...     roller.freeze(1, 2, 4)
...     r3 = roller.roll()
...     print(r3)
(6, 1, 1, 6, 3)
(6, 2, 2, 6, 2)
(6, 2, 2, 1, 2)
>>> print(hand.roll)
(6, 2, 2, 1, 2)
>>> print(hand.history)
[(6, 1, 1, 6, 3), (6, 2, 2, 6, 2), (6, 2, 2, 1, 2)]
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
