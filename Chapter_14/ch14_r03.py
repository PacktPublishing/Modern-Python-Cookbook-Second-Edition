"""Python Cookbook

Chapter 14, recipe 3, Managing arguments and configuration in composite applications
"""
import argparse
from pathlib import Path
import os
import sys
from typing import List, cast, Type, Optional, Any


class Command:
    @classmethod
    def arguments(
            cls,
            sub_parser: argparse.ArgumentParser
    ) -> None:
        pass

    def __init__(self) -> None:
        pass

    def execute(self, options: argparse.Namespace) -> None:
        pass


import Chapter_13.ch13_r05 as ch13_r05


class Simulate(Command):
    @classmethod
    def arguments(
            cls,
            simulate_parser: argparse.ArgumentParser
    ) -> None:
        simulate_parser.add_argument(
            "-g", "--games", type=int, default=100000)
        simulate_parser.add_argument(
            "-o", "--output", dest="game_file", required=True)
        simulate_parser.add_argument(
            "--seed",
            default=os.environ.get("CH14_R03_SEED", None)
        )
        simulate_parser.set_defaults(command=cls)

    def __init__(self) -> None:
        super().__init__()
        self.seed: Optional[Any] = None

    def execute(self, options: argparse.Namespace) -> None:
        self.game_path = Path(options.game_file)
        if 'seed' in options:
            self.seed = options.seed
        data = ch13_r05.roll_iter(options.games, self.seed)
        ch13_r05.write_rolls(self.game_path, data)


import Chapter_13.ch13_r06 as ch13_r06


class Summarize(Command):
    @classmethod
    def arguments(
            cls,
            summarize_parser: argparse.ArgumentParser
    ) -> None:
        summarize_parser.add_argument(
            "-o", "--output", dest="summary_file", required=True)
        summarize_parser.add_argument(
            "game_files", nargs="*", type=Path)
        summarize_parser.set_defaults(command=cls)

    def execute(self, options: argparse.Namespace) -> None:
        self.summary_path = Path(options.summary_file)
        with self.summary_path.open("w") as result_file:
            ch13_r06.process_all_files(result_file, options.game_files)


class SimSum(Command):

    @classmethod
    def arguments(
            cls,
            simsum_parser: argparse.ArgumentParser
    ) -> None:
        simsum_parser.add_argument(
            "-g", "--games", type=int, default=100000)
        simsum_parser.add_argument(
            "-o", "--output", dest="summary_file")
        simsum_parser.add_argument(
            "--seed",
            default=os.environ.get("CH14_R03_SEED", None)
        )
        simsum_parser.set_defaults(command=cls)

    def __init__(self) -> None:
        super().__init__()
        self.games = 1_000
        self.seed: Optional[int] = None

    def execute(self, options: argparse.Namespace) -> None:
        if 'seed' in options:
            self.seed = options.seed
        if 'games' in options:
            self.games = options.games
        data = ch13_r05.roll_iter(self.games, self.seed)
        game_statistics = ch13_r06.gather_stats(data)
        print(game_statistics)


import argparse


def get_options(argv: List[str] = sys.argv[1:]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="craps")
    subparsers = parser.add_subparsers()

    simulate_parser = subparsers.add_parser("simulate")
    Simulate.arguments(simulate_parser)

    summarize_parser = subparsers.add_parser("summarize")
    Summarize.arguments(summarize_parser)

    simsum_parser = subparsers.add_parser("simsum")
    SimSum.arguments(simsum_parser)

    options = parser.parse_args(argv)
    if "command" not in options:
        parser.error("No command selected")
    return options


def get_options_2(argv: List[str] = sys.argv[1:]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="craps")
    subparsers = parser.add_subparsers()

    sub_commands = [
        ("simulate", Simulate),
        ("summarize", Summarize),
        ("simsum", SimSum),
    ]
    for name, subc in sub_commands:
        cmd_parser = subparsers.add_parser(name)
        subc.arguments(cmd_parser)

    options = parser.parse_args(argv)
    if "command" not in options:
        parser.error("No command selected")
    return options


def get_options_3(argv: List[str] = sys.argv[1:]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="craps")
    subparsers = parser.add_subparsers()

    for subc in Command.__subclasses__():
        cmd_parser = subparsers.add_parser(subc.__name__.lower())
        subc.arguments(cmd_parser)

    options = parser.parse_args(argv)
    if "command" not in options:
        parser.error("No command selected")
    return options


def main() -> None:
    options = get_options_3(sys.argv[1:])
    command = cast(Type[Command], options.command)()
    command.execute(options)


if __name__ == "__main__":
    main()
