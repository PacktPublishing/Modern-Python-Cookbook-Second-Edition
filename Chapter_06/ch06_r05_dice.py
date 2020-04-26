"""Python Cookbook 2nd ed.

Chapter 6, recipe 5, Using cmd for creating command-line applications
"""
import cmd
import random
from typing import Set, List, Iterable, Optional


class DiceCLI(cmd.Cmd):
    """A handy tool for rolling a number of dice, used in a variety of games."""

    use_rawinput = False  # sys.stdout.write() and sys.stdin.readline() are used

    prompt = "] "
    intro = "A dice rolling tool. ? for help."

    def preloop(self):
        self.n_dice = 6
        self.dice = None  # no initial roll.
        self.reroll_count = 0

    def do_dice(self, arg: str) -> bool:
        """Sets the number of dice to roll."""
        try:
            self.n_dice = int(arg)
            self.dice = None
            print(f"Rolling {self.n_dice} dice")
        except ValueError:
            print(f"{arg!r} is invalid")
        return False

    def do_EOF(self, arg: str) -> bool:
        return True

    def do_quit(self, arg: str) -> bool:
        return True

    def emptyline(self) -> bool:
        """Shows current state of the dice."""
        if self.dice:
            print(f"{self.dice}", end=" ")
        if self.reroll_count:
            print(f"(reroll {self.reroll_count})")
        else:
            print()
        return False

    def do_roll(self, arg: str) -> bool:
        """Roll the dice. Use the dice command to set the number of dice."""
        self.dice = [random.randint(1, 6) for _ in range(self.n_dice)]
        print(f"{self.dice}")
        return False

    def do_reroll(self, arg: str) -> bool:
        """Reroll selected dice. Provide the 0-based positions."""
        try:
            positions = map(int, arg.split())
        except ValueError as ex:
            print(ex)
            return False
        for p in positions:
            self.dice[p] = random.randint(1, 6)
        self.reroll_count += 1
        print(f"{self.dice} (reroll {self.reroll_count})")
        return False


if __name__ == "__main__":
    game = DiceCLI()
    game.cmdloop()


### Unit test ###

from unittest.mock import Mock, call


def test_command(capsys):
    mock_input = Mock(
        readline=Mock(side_effect=["roll", "reroll 1 2 4 5", "roll", "quit"])
    )
    mock_output = Mock()
    random.seed(42)
    r = DiceCLI(stdin=mock_input, stdout=mock_output)
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
        "[6, 1, 1, 6, 3, 2]",
        "[6, 2, 2, 6, 6, 1] (reroll 1)",
        "[6, 6, 5, 1, 5, 4]",
    ]
