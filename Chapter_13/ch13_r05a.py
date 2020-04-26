"""Python Cookbook

Chapter 13, recipe 5, Designing scripts for composition.
class-based design alternative.
"""
import random
import yaml
import collections
from pathlib import Path
import argparse
import os
import sys
from typing import NamedTuple, List, Iterable, Tuple, Counter, Iterator, Optional


class CrapsSimulator:
    def __init__(self, /, seed: int = None) -> None:
        self.rng = random.Random(seed)
        self.faces: List[int]
        self.total: int

    def roll(self, n: int = 2) -> int:
        self.faces = list(self.rng.randint(1, 6) for _ in range(n))
        self.total = sum(self.faces)
        return self.total

    def craps_game(self) -> List[List[int]]:
        self.roll()
        if self.total in [2, 3, 12]:
            return [self.faces]
        elif self.total in [7, 11]:
            return [self.faces]
        elif self.total in [4, 5, 6, 8, 9, 10]:
            point, sequence = self.total, [self.faces]
            self.roll()
            while self.total not in [7, point]:
                sequence.append(self.faces)
                self.roll()
            sequence.append(self.faces)
            return sequence
        else:
            raise Exception("Horrifying Logic Bug")

    def roll_iter(self, total_games: int) -> Iterator[List[List[int]]]:
        for i in range(total_games):
            sequence = self.craps_game()
            yield sequence


test_sim_class = """
>>> sim = CrapsSimulator(seed=42)
>>> list(sim.roll_iter(12))  # doctest: +NORMALIZE_WHITESPACE
[[[6, 1]],
 [[1, 6]],
 [[3, 2], [2, 2], [6, 1]],
 [[6, 6]],
 [[5, 1], [5, 4], [1, 1], [1, 2], [2, 5]],
 [[5, 1], [5, 2]],
 [[6, 6]],
 [[6, 5]],
 [[4, 2], [4, 5], [3, 1], [2, 6], [4, 3]],
 [[3, 2], [2, 3]],
 [[1, 1]],
 [[4, 1], [3, 3], [5, 3], [1, 6]]]
"""


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
