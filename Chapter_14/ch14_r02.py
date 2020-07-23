"""Python Cookbook

Chapter 14, recipe 2, Combining many applications using the Command design pattern
"""
import argparse
from pathlib import Path
import sys
from typing import Type, Optional, Any


class Command:
    def __init__(self) -> None:
        pass

    def execute(self, options: argparse.Namespace) -> None:
        pass


import Chapter_13.ch13_r05 as ch13_r05


class Simulate(Command):
    def __init__(self) -> None:
        super().__init__()
        self.seed: Optional[Any] = None
        self.game_path: Path

    def execute(self, options: argparse.Namespace) -> None:
        self.game_path = Path(options.game_file)
        if 'seed' in options:
            self.seed = options.seed
        data = ch13_r05.roll_iter(options.games, self.seed)
        ch13_r05.write_rolls(self.game_path, data)
        print(f"Created {str(self.game_path)}")


import Chapter_13.ch13_r06 as ch13_r06


class Summarize(Command):
    def execute(self, options: argparse.Namespace) -> None:
        self.summary_path = Path(options.summary_file)
        with self.summary_path.open("w") as result_file:
            game_paths = [Path(f) for f in options.game_files]
            ch13_r06.process_all_files(result_file, game_paths)


class Sequence(Command):
    def __init__(self, *commands: Type[Command]) -> None:
        super().__init__()
        self.commands = [command() for command in commands]

    def execute(self, options: argparse.Namespace) -> None:
        for command in self.commands:
            command.execute(options)


class SimSum(Sequence):
    def __init__(self) -> None:
        super().__init__(Simulate, Summarize)

    def execute(self, options: argparse.Namespace) -> None:
        self.intermediate = (
            Path("data") / "ch14_r02_temporary.yaml"
        )
        new_namespace = Namespace(
            game_file=str(self.intermediate),
            game_files=[str(self.intermediate)],
            **vars(options)
        )
        super().execute(new_namespace)


from argparse import Namespace


def main() -> None:
    options_1 = Namespace(games=100, game_file="x.yaml")
    command1 = Simulate()
    command1.execute(options_1)

    options_2 = Namespace(summary_file="y.yaml", game_files=["x.yaml"])
    command2 = Summarize()
    command2.execute(options_2)

def main_2() -> None:
    # Without thinking about how the two commands interaction
    options = Namespace(
        games=100,
        game_file="x.yaml",
        summary_file="y.yaml",
        game_files=["x.yaml"]
    )
    both_command = Sequence(Simulate, Summarize)
    both_command.execute(options)

def main_3() -> None:
    # Better design reflecting the file shared between commands.
    better_options = Namespace(
        games=100,
        summary_file="y.yaml")
    sim_sum_command = SimSum()
    sim_sum_command.execute(better_options)


if __name__ == "__main__":
    main()
