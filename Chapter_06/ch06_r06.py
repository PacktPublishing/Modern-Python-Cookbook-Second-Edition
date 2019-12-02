"""Python Cookbook 2nd ed.

Chapter 6, recipe 6
"""
import math


class StatsList(list):
    """
    >>> subset1 = StatsList([10, 8, 13, 9, 11])
    >>> data = StatsList([14, 6, 4, 12, 7, 5])
    >>> data.extend(subset1)
    >>> data
    [14, 6, 4, 12, 7, 5, 10, 8, 13, 9, 11]
    >>> round(data.mean(), 1)
    9.0
    >>> round(data.variance(), 1)
    11.0
    """

    def sum(self) -> float:
        return sum(v for v in self)

    def size(self) -> float:
        return sum(1 for v in self)

    def sum2(self) -> float:
        return sum(v ** 2 for v in self)

    def mean(self) -> float:
        return self.sum() / self.size()

    def variance(self) -> float:
        return (self.sum2() - self.sum() ** 2 / self.size()) / (self.size() - 1)

    def stddev(self) -> float:
        return math.sqrt(self.variance())
