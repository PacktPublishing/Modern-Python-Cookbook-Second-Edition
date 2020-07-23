"""Python Cookbook 2nd ed.

Chapter 15, recipe 6, Confirming that the data is random – the null hypothesis

Raw data source: ftp://ftp.cmdl.noaa.gov/ccg/co2/trends/co2_mm_mlo.txt

Output from the test() function
::
    (cookbook) Code % PYTHONPATH=. python Chapter_15/ch15_r06.py
    T_obs = 2.75-2.50 = -0.25
    below 18 25.7%, above 52 74.3%
    time 0.002608454000000003
    T_obs = 4.50-2.50 = -2.00
    below 1 1.4%, above 69 98.6%
    time 0.0022212999999999955


Output from the demo() function
::
    1959 mean 315.97
    1960 mean 316.91
    2014 mean 398.61
    1959 v. 1960
    T_obs = 316.91-315.97 = -0.93
    below 306,242 11.3%, above 2,397,914 88.7%
    time 255.784436311


    1959 v. 2014
    T_obs = 398.61-315.97 = -82.64
    below 0 0.0%, above 2,704,156 100.0%
    time 257.159404162


    1959 v. 1960
    T_obs = 316.91-315.97 = 0.93
    below 239,491 88.6%, above 30,924 11.4%
    time 24.733703789999936


    1959 v. 2014
    T_obs = 398.61-315.97 = 82.64
    below 270,415 100.0%, above 0 0.0%
    time 24.85797290900007


The all-combinations take about 3 minutes to report results. Randomized
takes 20 seconds to report similar values.
"""

from pathlib import Path
from statistics import mean
import time
from typing import List, Counter, Callable, Optional

from Chapter_15.ch15_r05 import get_data

import itertools


def all_combos(
        s1: List[float], s2: List[float], limit: Optional[int] = None) -> None:
    """Builds sets and then picks elements from sequences for
    all possible combinations of subset values.
    ::

        universe = sum(pool)
        for combination in itertools.permutations(pool, len(s1))
            m_a = sum(combination)/len(s1)
            m_b = (universe-a)/len(s2)
            delta = m_a - m_b
    """
    start = time.perf_counter()

    T_obs = mean(s1) - mean(s2)
    print(
        f"T_obs = {mean(s2):.2f}-{mean(s1):.2f} "
        f"= {T_obs:.2f}")

    below = above = 0
    pool = s1 + s2
    universe = set(range(len(pool)))
    for a_inxs in itertools.combinations(universe, len(s1)):
        b_inxs = universe - set(a_inxs)
        m_a = mean(pool[i] for i in a_inxs)
        m_b = mean(pool[i] for i in b_inxs)
        if m_a - m_b < T_obs:
            below += 1
        else:
            above += 1
    print(
        f"below {below:,} {below/(below+above):.1%}, "
        f"above {above:,} {above/(below+above):.1%}"
    )

    end = time.perf_counter()
    print("time", end - start)


import random
import collections


def randomized(
        s1: List[float],
        s2: List[float],
        limit: Optional[int] = None) -> None:
    if limit is None or limit <= 0:
        raise ValueError(f"limit of {limit}; must be an integer > 0")
    start = time.perf_counter()

    T_obs = mean(s2) - mean(s1)
    print(
        f"T_obs = {mean(s2):.2f}-{mean(s1):.2f} "
        f"= {T_obs:.2f}")

    counts: Counter[int] = collections.Counter()
    universe = s1 + s2
    for resample in range(limit):
        random.shuffle(universe)
        a = universe[: len(s1)]
        b = universe[len(s2) :]
        delta = int(1000 * (mean(a) - mean(b)))
        counts[delta] += 1

    T = int(1000 * T_obs)
    below = sum(v for k, v in counts.items() if k < T)
    above = sum(v for k, v in counts.items() if k >= T)

    print(
        f"below {below:,} {below/(below+above):.1%}, "
        f"above {above:,} {above/(below+above):.1%}"
    )

    end = time.perf_counter()
    print("time", end - start)


def faster_randomized(
        s1: List[float],
        s2: List[float],
        limit: Optional[int] = 270_415) -> None:
    if limit is None or limit <= 0:
        raise ValueError(f"limit of {limit}; must be an integer > 0")
    start = time.perf_counter()

    T_obs = mean(s2) - mean(s1)
    print(
        f"T_obs = {mean(s2):.2f}-{mean(s1):.2f} "
        f"= {T_obs:.2f}")

    counts: Counter[int] = collections.Counter()
    universe = s1 + s2
    a_size = len(s1)
    b_size = len(s2)
    s_u = sum(universe)
    for resample in range(limit):
        random.shuffle(universe)
        a = universe[: len(s1)]
        s_a = sum(a)
        m_a = s_a/a_size
        m_b = (s_u-s_a)/b_size
        delta = int(1000*(m_a-m_b))
        counts[delta] += 1

    T = int(1000 * T_obs)
    below = sum(v for k, v in counts.items() if k < T)
    above = sum(v for k, v in counts.items() if k >= T)

    print(
        f"below {below:,} {below/(below+above):.1%}, "
        f"above {above:,} {above/(below+above):.1%}"
    )

    end = time.perf_counter()
    print("time", end - start)


def test():
    s1 = (1, 2, 3, 4)  # mean = 2.5, stdev = 1.29
    s2 = (2, 2, 3, 4)  # mean = 2.75
    all_combos(s1, s2)

    s3 = (3, 4, 5, 6)  # mean = 4.5
    all_combos(s1, s3)


test_small_diff = """
>>> s1 = (1, 2, 3, 4)  # mean = 2.5, stdev = 1.29
>>> s2 = (2, 2, 3, 4)  # mean = 2.75
>>> all_combos(s1, s2)  # doctest: +ELLIPSIS
T_obs = 2.75-2.50 = -0.25
below 18 25.7%, above 52 74.3%
time ...
"""

test_big_diff = """
>>> s1 = (1, 2, 3, 4)  # mean = 2.5, stdev = 1.29
>>> s3 = (3, 4, 5, 6)  # mean = 4.5
>>> all_combos(s1, s3)  # doctest: +ELLIPSIS
T_obs = 4.50-2.50 = -2.00
below 1 1.4%, above 69 98.6%
time ...
"""

test_randomized = """
>>> random.seed(42)
>>> s4 = list(range(1,10,2))
>>> s5 = list(range(6,15,2))
>>> randomized(s4, s5, 100)  # doctest: +ELLIPSIS
T_obs = 10.00-5.00 = 5.00
below 97 97.0%, above 3 3.0%
time ...
"""

test_fast_randomized = """
>>> random.seed(42)
>>> random.seed(42)
>>> s4 = list(range(1,10,2))
>>> s5 = list(range(6,15,2))
>>> faster_randomized(s4, s5, 100)  # doctest: +ELLIPSIS
T_obs = 10.00-5.00 = 5.00
below 97 97.0%, above 3 3.0%
time ...
"""

Resampler = Callable[[List[float], List[float], Optional[int]], None]

def demo(source_path: Path, resampler: Resampler) -> None:
    with source_path.open() as source_file:
        all_data = list(get_data(source_file))
    y1959 = [r.interpolated for r in all_data if r.year == 1959]
    y1960 = [r.interpolated for r in all_data if r.year == 1960]
    y2014 = [r.interpolated for r in all_data if r.year == 2014]

    m_1959 = mean(y1959)
    m_1960 = mean(y1960)
    m_2014 = mean(y2014)
    print(f"1959 mean {m_1959:.2f}")
    print(f"1960 mean {m_1960:.2f}")
    print(f"2014 mean {m_2014:.2f}")

    print("\n\n1959 v. 1960")
    resampler(y1959, y1960, 270_415)

    print("\n\n1959 v. 2014")
    resampler(y1959, y2014, 270_415)

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}


if __name__ == "__main__":
    # test()
    source_path = Path("data") / "co2_mm_mlo.txt"
    # demo(source_path, all_combos)
    # demo(source_path, randomized)
    demo(source_path, faster_randomized)
