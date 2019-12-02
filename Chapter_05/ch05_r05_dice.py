"""Python Cookbook 2nd ed.

Chapter 5, recipe 5, Dice Roller
"""
from cmd import Cmd
from random import randint
from typing import Set, List, Iterable, Optional


class Dice:
    """
    Model a collection of dice, all of a uniform design.

    >>> import random
    >>> random.seed(42)
    >>> d = Dice(3, d=6)
    >>> d.dice
    [6, 1, 1]

    >>> d = Dice(5)
    >>> d.dice
    [6, 3, 2, 2, 2]
    >>> d.freeze(2, 3, 4)
    >>> d.reroll()
    >>> d.dice
    [6, 1, 2, 2, 2]
    >>> d.reroll()
    >>> d.dice
    [6, 6, 2, 2, 2]
    >>> d.count
    3
    """

    def __init__(self, n: int, d: int = 6) -> None:
        self.faces: int = d
        self.dice: List[int] = [0 for _ in range(n)]
        self.frozen: Set[int] = set()
        self.count: int = 1
        self.roll(range(n))

    def roll(self, positions: Iterable[int]) -> None:
        for position in positions:
            self.dice[position] = randint(1, self.faces)

    def freeze(self, *positions: int) -> None:
        bad_values = {p for p in positions if p not in range(len(self.dice))}
        if bad_values:
            raise ValueError(
                f"Invalid positions: {bad_values}, must be 0 to {len(self.dice)}-1"
            )
        self.frozen |= set(positions)

    def unfreeze(self, *positions: int) -> None:
        bad_values = {p for p in positions if p not in self.frozen}
        if bad_values:
            raise ValueError(
                f"Invalid positions: {bad_values}, must be in {self.frozen}"
            )
        self.frozen -= set(positions)

    def reroll(self) -> None:
        unfrozen = set(range(len(self.dice))) - self.frozen
        self.roll(unfrozen)
        self.count += 1


class DiceCLI(Cmd):
    """A handy tool for rolling a number of dice, used in a variety of games."""

    prompt = "] "
    intro = "A dice rolling tool. ? for help."

    def preloop(self):
        self.n_dice = 6
        self.dice = None  # no initial roll.

    def do_dice(self, arg: str) -> Optional[bool]:
        """Sets the number of dice to roll."""
        try:
            self.n_dice = int(arg)
            self.dice = None
            print(f"Rolling {self.n_dice} dice")
        except ValueError:
            print(f"{arg!r} is invalid")
        return False

    def do_EOF(self, arg: str) -> Optional[bool]:
        return True

    def do_quit(self, arg: str) -> Optional[bool]:
        return True

    def emptyline(self):
        """Shows current state of the dice."""
        # There a number of ways to make this easier to understand.
        if self.dice:
            print(f"{self.dice.dice} (roll {self.dice.count})")
            print(f"Saving {self.dice.frozen}")

    def do_roll(self, arg: str) -> Optional[bool]:
        """Roll the dice."""
        if self.dice and self.dice.frozen:
            print(f"Rerolling...")
            self.dice.reroll()
        else:
            print(f"Rolling... ")
            self.dice = Dice(self.n_dice)
        print(f"{self.dice.dice} (roll {self.dice.count})")
        return False

    def do_save(self, arg: str) -> Optional[bool]:
        """Sets positions to save, use spaces between the positions."""
        try:
            positions = list(map(int, arg.split()))
            self.dice.freeze(*positions)
            self.emptyline()
        except ValueError as ex:
            print(f"Invalid positions {arg!r}, ex")
        return False

    def do_unsave(self, arg: str) -> Optional[bool]:
        """Unsaves one or more previously-saved positions."""
        try:
            positions = list(map(int, arg.split()))
            self.dice.unfreeze(*positions)
            self.emptyline()
        except ValueError as ex:
            print(f"Invalid positions {arg!r}, ex")
        return False

    def do_clear(self, arg: str) -> Optional[bool]:
        """Clear the saved positions and the dice, ready for a new roll."""
        self.dice = None
        return False


if __name__ == "__main__":
    game = DiceCLI()
    game.cmdloop()
