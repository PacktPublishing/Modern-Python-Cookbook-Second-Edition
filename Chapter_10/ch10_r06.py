"""Python Cookbook 2nd ed.

Chapter 10, recipe 6.

Raw data source: ftp://ftp.cmdl.noaa.gov/ccg/co2/trends/co2_mm_mlo.txt

Output::
    (cookbook) Code % PYTHONPATH=. python Chapter_10/ch10_r06.py
    T_obs = m_1-m_2 = 2.50-2.75 = -0.25
    below 18 25.7%, above 52 74.3%
    time 0.003134122000000003
    T_obs = m_1-m_2 = 2.50-4.50 = -2.00
    below 1 1.4%, above 69 98.6%
    time 0.0019881789999999927
    1959 mean 315.97
    1960 mean 316.91
    2014 mean 398.61
    1959 v. 1960
    T_obs = m_1-m_2 = 315.97-316.91 = -0.93
    below 306,242 11.3%, above 2,397,914 88.7%
    time 203.51845443


    1959 v. 2014
    T_obs = m_1-m_2 = 315.97-398.61 = -82.64
    below 0 0.0%, above 2,704,156 100.0%
    time 195.715965735
    1959 v. 1960
    T_obs = m_2-m_1 = 316.91-315.97 = 0.93
    below 239,539 88.6%, above 30,876 11.4%
    time 22.33877652800004


    1959 v. 2014
    T_obs = m_2-m_1 = 398.61-315.97 = 82.64
    below 270,415 100.0%, above 0 0.0%
    time 22.02112613899999

The all-combinations take about 3 minutes to report results. Randomized
takes 20 seconds to report similar values.
"""

from pathlib import Path
from statistics import mean
import time
from typing import List, Counter

from Chapter_10.ch10_r05 import get_data

import itertools


def all_combos(s1: List[float], s2: List[float]) -> None:
    """Builds sets and then picks elements from sequences for
    all possible combinations of subset values.

    A less naive version of this works on simple sums.
    ::

        universe = sum(pool)
        for combination in itertools.permutations(pool, len(s1))
            m_a = sum(combination)/len(s1)
            m_b = (universe-a)/len(s2)
            delta = m_a - m_b
    """
    start = time.perf_counter()

    T_obs = mean(s1) - mean(s2)
    print(f"T_obs = m_1-m_2 = {mean(s1):.2f}-{mean(s2):.2f} = {T_obs:.2f}")

    below = above = 0
    pool = s1 + s2
    universe = set(range(len(pool)))
    for a_inxs in itertools.combinations(universe, len(s1)):
        b_inxs = universe - set(a_inxs)
        # a = list(pool[i] for i in a_inxs)
        # b = list(pool[i] for i in b_inxs)
        m_a = mean(pool[i] for i in a_inxs)
        m_b = mean(pool[i] for i in b_inxs)
        # print( a_inxs, a, m_a )
        # print( b_inxs, b, m_b )
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


def randomized(s1: List[float], s2: List[float], limit: int = 270415) -> None:
    start = time.perf_counter()

    T_obs = mean(s2) - mean(s1)
    print(f"T_obs = m_2-m_1 = {mean(s2):.2f}-{mean(s1):.2f} = {T_obs:.2f}")

    counts: Counter[int] = collections.Counter()
    universe = s1 + s2
    for resample in range(limit):
        random.shuffle(universe)
        a = universe[: len(s2)]
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


def test():
    s1 = (1, 2, 3, 4)  # mean = 2.5, stdev = 1.29
    s2 = (2, 2, 3, 4)  # mean = 2.75
    all_combos(s1, s2)

    s3 = (3, 4, 5, 6)  # mean = 4.5
    all_combos(s1, s3)


__test__ = {
    "small diff": """
>>> s1 = (1, 2, 3, 4)  # mean = 2.5, stdev = 1.29
>>> s2 = (2, 2, 3, 4)  # mean = 2.75
>>> all_combos(s1, s2)  # doctest: +ELLIPSIS
T_obs = m_1-m_2 = 2.50-2.75 = -0.25
below 18 25.7%, above 52 74.3%
time ...

""",
    "big diff": """
>>> s1 = (1, 2, 3, 4)  # mean = 2.5, stdev = 1.29
>>> s3 = (3, 4, 5, 6)  # mean = 4.5
>>> all_combos(s1, s3)  # doctest: +ELLIPSIS
T_obs = m_1-m_2 = 2.50-4.50 = -2.00
below 1 1.4%, above 69 98.6%
time ...

""",
}


def demo(source_path: Path) -> None:
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

    print("1959 v. 1960")
    all_combos(y1959, y1960)

    print("\n\n1959 v. 2014")
    all_combos(y1959, y2014)

    print("1959 v. 1960")
    randomized(y1959, y1960)

    print("\n\n1959 v. 2014")
    randomized(y1959, y2014)


if __name__ == "__main__":
    test()
    source_path = Path("data") / "co2_mm_mlo.txt"
    # demo(source_path)
