"""Python Cookbook 2nd ed.

Chapter 6, recipe 5, Using cmd for creating command-line applications

This is a bit too complex for Chapter 6, but is provided as bonus material.
"""
from cmd import Cmd
import random
from typing import Set, List, Iterable, Optional


class Dice:
    """
    Model a collection of dice, all of a uniform design.
    Some dice are frozen and cannot be re-reolled.

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

    def roll(self, positions_to_roll: Iterable[int]) -> None:
        for position in positions_to_roll:
            self.dice[position] = random.randint(1, self.faces)

    def freeze(self, *positions: int) -> None:
        position_set = set(positions)
        bad_values = position_set - set(range(len(self.dice)))
        if bad_values:
            raise ValueError(f"Invalid positions: {bad_values}")
        self.frozen |= position_set

    def unfreeze(self, *positions: int) -> None:
        position_set = set(positions)
        bad_values = self.frozen - position_set
        if bad_values:
            raise ValueError(
                f"Invalid positions: {bad_values}, must be in {self.frozen}"
            )
        self.frozen -= set(positions)

    def reroll(self) -> None:
        unfrozen = set(range(len(self.dice))) - self.frozen
        self.roll(unfrozen)
        self.count += 1


class Zonk(Cmd):
    """A handy tool for rolling a number of dice, used in a variety of games."""

    use_rawinput = False  # sys.stdout.write() and sys.stdin.readline() are used

    prompt = "] "
    intro = "A dice rolling tool. ? for help."

    def preloop(self):
        self.n_dice = 6
        self.dice = None  # no initial roll.

    def do_dice(self, arg: str) -> bool:
        """Sets the number of dice to roll."""
        try:
            self.n_dice = int(arg)
        except ValueError:
            print(f"{arg!r} is invalid")
            return False
        self.dice = None
        print(f"Rolling {self.n_dice} dice")
        return False

    def do_EOF(self, arg: str) -> bool:
        return True

    def do_quit(self, arg: str) -> bool:
        return True

    def emptyline(self) -> bool:
        """Shows current state of the dice."""
        # There a number of ways to make this easier to understand.
        if self.dice:
            print(f"{self.dice.dice} (roll {self.dice.count})")
            print(f"Saving {self.dice.frozen}")
        return False

    def do_roll(self, arg: str) -> bool:
        """Roll the dice."""
        if self.dice and self.dice.frozen:
            print(f"Rerolling...")
            self.dice.reroll()
        else:
            print(f"Rolling... ")
            self.dice = Dice(self.n_dice)
        print(f"{self.dice.dice} (roll {self.dice.count})")
        return False

    def do_save(self, arg: str) -> bool:
        """Sets positions to save, use spaces between the positions."""
        try:
            positions = list(map(int, arg.split()))
            self.dice.freeze(*positions)
            self.emptyline()
        except ValueError as ex:
            print(f"Invalid positions {arg!r}, {ex}")
        return False

    def do_unsave(self, arg: str) -> bool:
        """Unsaves one or more previously-saved positions."""
        try:
            positions = list(map(int, arg.split()))
            self.dice.unfreeze(*positions)
            self.emptyline()
        except ValueError as ex:
            print(f"Invalid positions {arg!r}, {ex}")
        return False

    def do_clear(self, arg: str) -> Optional[bool]:
        """Clear the saved positions and the dice, ready for a new roll."""
        self.dice = None
        return False


if __name__ == "__main__":
    game = Zonk()
    game.cmdloop()


### Unit test ###

from unittest.mock import Mock, call


def test_command(capsys):
    mock_input = Mock(readline=Mock(side_effect=["roll", "save 0 3", "roll", "quit"]))
    mock_output = Mock()
    random.seed(42)
    r = Zonk(stdin=mock_input, stdout=mock_output)
    r.cmdloop()
    assert mock_output.write.mock_calls == [
        call("A dice rolling tool. ? for help.\n"),
        call("] "),
        call("] "),
        call("] "),
        call("] "),
    ]
    out, err = capsys.readouterr()
    assert out.splitlines() == [
        "Rolling... ",
        "[6, 1, 1, 6, 3, 2] (roll 1)",
        "[6, 1, 1, 6, 3, 2] (roll 1)",
        "Saving {0, 3}",
        "Rerolling...",
        "[6, 2, 2, 6, 6, 1] (roll 2)",
    ]
