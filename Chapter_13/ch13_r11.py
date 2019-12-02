"""Python Cookbook

Chapter 13, recipe 11
"""

import subprocess
from typing import Counter, List, Any, Iterable, Iterator


def command_iter(files: int) -> Iterable[List[str]]:
    for n in range(files):
        filename = f"data/game_{n}.yaml"
        command = [
            "python3",
            "Chapter_13/ch13_r05.py",
            "--samples",
            "10",
            "--output",
            filename,
        ]
        yield command


def command_output_iter(commands: Iterable[List[str]]) -> Iterator[str]:
    for command in commands:
        process = subprocess.run(command, stdout=subprocess.PIPE, check=True, text=True)
        output_text = process.stdout
        output_lines = (l.strip() for l in output_text.splitlines())
        yield from output_lines


import collections


def process_batches(output_lines_iter: Iterable[str]) -> Iterable[Counter[Any]]:
    for line in output_lines_iter:
        if line.startswith("Counter"):
            batch_counter = eval(line)
            yield batch_counter


if __name__ == "__main__":
    command_sequence = command_iter(2)
    output_lines_iter = command_output_iter(command_sequence)
    total_counter: Counter[Any] = collections.Counter()
    for batch_counter in process_batches(output_lines_iter):
        print(batch_counter)
        total_counter.update(batch_counter)
    print("Total")
    print(total_counter)
