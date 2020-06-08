"""Python Cookbook 2nd ed.

Chapter 11, recipe 9. Testing things that involve randomness.
"""
import random
from typing import List, Iterator, Counter
import collections
import statistics

def resample(population: List[int], N: int) -> Iterator[int]:
    for i in range(N):
        sample = random.choice(population)
        yield sample

def mean_distribution(population: List[int], N: int):
    means: Counter[float] = collections.Counter()
    for _ in range(1000):
        subset = list(resample(population, N))
        measure = round(statistics.mean(subset), 1)
        means[measure] += 1
    return means

test_estimate = """
>>> random.seed(42)
>>> population = [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]
>>> mean_distribution(population, 4).most_common(5)
[(7.8, 51), (7.2, 45), (7.5, 44), (7.1, 41), (7.7, 40)]
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
