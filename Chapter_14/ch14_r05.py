"""Python Cookbook

Chapter 14, recipe 5, Wrapping a program and checking the output

This uses an explicit `python` command
so Chapter_13/ch13_r05.py does not have to be marked executable.
"""
import argparse
from pathlib import Path
import subprocess
import sys
from typing import Counter, List, Any, Iterable, Iterator


def get_options(argv: List[str] = sys.argv[1:]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("games", type=int)
    options = parser.parse_args(argv)
    return options


def command_iter(directory: Path, files: int) -> Iterable[List[str]]:
    for n in range(files):
        filename = directory / f"game_{n}.yaml"
        command = [
            "python",
            "Chapter_13/ch13_r05.py",
            "--samples",
            "10",
            "--output",
            str(filename),
        ]
        yield command


def command_output_iter(temporary: Path, commands: Iterable[List[str]]) -> Iterator[str]:
    for command in commands:
        temp_path = temporary/"stdout"
        with temp_path.open('w') as temp_file:
            process = subprocess.run(
                command,
                stdout=temp_file,
                check=True,
                text=True)
        output_text = temp_path.read_text()
        output_lines = (l.strip() for l in output_text.splitlines())
        yield from output_lines


import collections


def collect_batches(output_lines_iter: Iterable[str]) -> Iterable[Counter[Any]]:
    for line in output_lines_iter:
        if line.startswith("Counter"):
            batch_counter = eval(line)
            yield batch_counter


def summarize(
        directory: Path,
        games: int,
        temporary: Path
) -> None:
    total_counter: Counter[Any] = collections.Counter()

    command_sequence = command_iter(directory, games)
    output_lines_iter = command_output_iter(
        temporary, command_sequence)
    batch_summaries = collect_batches(output_lines_iter)
    for batch_counter in batch_summaries:
        print(batch_counter)
        total_counter.update(batch_counter)
    print("Total")
    print(total_counter)


import csv


def summarize_2(
        directory: Path,
        games: int,
        temporary: Path
) -> None:

    def counter_iter(
            directory: Path,
            games: int,
            temporary: Path
    ) -> Iterator[Counter]:
        total_counter: Counter[Any] = collections.Counter()
        command_sequence = command_iter(directory, games)
        output_lines_iter = command_output_iter(
            temporary, command_sequence)
        batch_summaries = collect_batches(output_lines_iter)
        for batch_counter in batch_summaries:
            yield batch_counter
            total_counter.update(batch_counter)
        yield total_counter

    wtr = csv.writer(sys.stdout)
    for counter in counter_iter(directory, games, temporary):
        array = [counter[i] for i in range(20)]
        wtr.writerow(array)

def main() -> None:
    options = get_options()
    summarize_2(
        directory=options.directory,
        games=options.games,
        temporary=Path("/tmp")
    )

if __name__ == "__main__":
    main()
