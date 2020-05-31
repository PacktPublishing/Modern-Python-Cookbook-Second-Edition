"""Python Cookbook 2nd ed.

Chapter 8, recipe 6, Creating a class that has orderable objects
"""

# https://github.com/python/mypy/issues/4610

from functools import total_ordering
from typing import Any


@total_ordering
class Ord:

    def __eq__(self, other: Any) -> bool:
        return False

    def __lt__(self, other: "Ord") -> bool:
        return False


Ord() <= Ord()  # type: ignore

# Chapter_08/ch08_r06_bug.py:22: error: Unsupported left operand type for <= ("Ord")
