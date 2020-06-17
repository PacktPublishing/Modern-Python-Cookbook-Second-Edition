#!python3
"""Python Cookbook

Chapter 13, recipe 5, Designing scripts for composition.
"""
import random
import yaml
import collections
from pathlib import Path
import argparse
import os
import sys
from typing import NamedTuple, List, Iterable, Tuple, Counter, Iterator, Optional

# Roll = namedtuple('Roll', ('faces', 'total'))
class Roll(NamedTuple):
    faces: List[int]
    total: int


def roll(n: int = 2) -> Roll:
    faces = list(random.randint(1, 6) for _ in range(n))
    total = sum(faces)
    return Roll(faces, total)


Game_Summary = List[List[int]]


def craps_game() -> Game_Summary:
    """Summarize the game as a list of dice pairs."""
    come_out = roll()
    if come_out.total in [2, 3, 12]:
        return [come_out.faces]
    elif come_out.total in [7, 11]:
        return [come_out.faces]
    elif come_out.total in [4, 5, 6, 8, 9, 10]:
        sequence = [come_out.faces]
        next = roll()
        while next.total not in [7, come_out.total]:
            sequence.append(next.faces)
            next = roll()
        sequence.append(next.faces)
        return sequence
    else:
        raise Exception(f"Horrifying Logic Bug in {come_out}")


def roll_iter(
        total_games: int,
        seed: Optional[int] = None
    ) -> Iterator[Game_Summary]:
    random.seed(seed)
    for i in range(total_games):
        sequence = craps_game()
        yield sequence


def write_rolls(
        output_path: Path,
        game_iterator: Iterable[Game_Summary]
    ) -> Counter[int]:
    face_count: Counter[int] = collections.Counter()
    with output_path.open("w") as output_file:
        for game_outcome in game_iterator:
            output_file.write(
                yaml.dump(game_outcome, default_flow_style=True, explicit_start=True)
            )
            for roll in game_outcome:
                face_count[sum(roll)] += 1
    return face_count


def summarize(
        configuration: argparse.Namespace,
        counts: Counter[int]
    ) -> None:
    print(configuration, file=sys.stderr)
    print(counts, file=sys.stderr)


def get_options(
        argv: List[str] = sys.argv[1:]
    ) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--samples", type=int)
    parser.add_argument("-o", "--output")
    options = parser.parse_args(argv)

    if options.output is None:
        parser.error("No output file specified")

    options.output_path = Path(options.output)

    if "RANDOMSEED" in os.environ:
        seed_text = os.environ["RANDOMSEED"]
        try:
            options.seed = int(seed_text)
        except ValueError:
            parser.error(f"RANDOMSEED={seed_text!r} isn't a valid seed value")
    else:
        options.seed = None
    return options


def main() -> None:
    options = get_options(sys.argv[1:])
    face_count = write_rolls(
        options.output_path, roll_iter(options.samples, options.seed)
    )
    summarize(options, face_count)


if __name__ == "__main__":
    main()
