"""Python Cookbook 2nd ed.

Chapter 5, recipe 7, Avoiding mutable default values for function parameters

"""

import collections
from random import randint, seed
from typing import Counter, Optional, Callable, TypeVar, Iterable


def gather_stats_bad(
        n: int,
        samples: int = 1000,
        summary: Counter[int] = collections.Counter()
) -> Counter:
    summary.update(
        sum(randint(1, 6)
            for d in range(n)) for _ in range(samples))
    return summary


test_default_counter = """
>>> seed(1)
>>> s1 = gather_stats_bad(2)
>>> s1
Counter({7: 168, 6: 147, 8: 136, 9: 114, 5: 110, 10: 77, 11: 71, 4: 70, 3: 52, 12: 29, 2: 26})
"""

test_explicit_counter = """
>>> seed(1)
>>> mc = Counter()
>>> gather_stats_bad(2, summary=mc)  # doctest: +ELLIPSIS
Counter...
>>> mc
Counter({7: 168, 6: 147, 8: 136, 9: 114, 5: 110, 10: 77, 11: 71, 4: 70, 3: 52, 12: 29, 2: 26})
"""

test_default_counter_again = """
>>> seed(1)
>>> s3b = gather_stats_bad(2)
>>> s3b
Counter({7: 336, 6: 294, 8: 272, 9: 228, 5: 220, 10: 154, 11: 142, 4: 140, 3: 104, 12: 58, 2: 52})
"""


def create_stats(n: int, samples: int = 1000) -> Counter[int]:
    return update_stats(n, samples, Counter())


def update_stats(n: int, samples: int, summary: Counter[int]) -> Counter[int]:
    summary.update(sum(randint(1, 6) for d in range(n)) for _ in range(samples))
    return summary


def gather_stats_good(
    n: int, samples: int = 1000, summary: Optional[Counter[int]] = None
) -> Counter[int]:
    if summary is None:
        summary = Counter()
    summary.update(sum(randint(1, 6) for d in range(n)) for _ in range(samples))
    return summary


test_good = """
>>> seed(1)
>>> s3a = gather_stats_good(2)
>>> seed(1)
>>> s3b = gather_stats_good(2)
>>> s3a
Counter({7: 168, 6: 147, 8: 136, 9: 114, 5: 110, 10: 77, 11: 71, 4: 70, 3: 52, 12: 29, 2: 26})
>>> s3b
Counter({7: 168, 6: 147, 8: 136, 9: 114, 5: 110, 10: 77, 11: 71, 4: 70, 3: 52, 12: 29, 2: 26})
>>> s3a is s3b
False
"""


T = TypeVar("T")
Summarizer = Callable[[Iterable[T]], Counter[T]]


def gather_stats_flex(
    n: int, samples: int = 1000, summary_func: Summarizer = collections.Counter
) -> Counter[int]:
    summary = summary_func(sum(randint(1, 6) for d in range(n)) for _ in range(samples))
    return summary


test_flex = """
>>> seed(1)
>>> gather_stats_flex(2, 12, summary_func=list)
[7, 4, 5, 8, 10, 3, 5, 8, 6, 10, 9, 7]
>>> seed(1)
>>> gather_stats_flex(2, 12, summary_func=collections.Counter)
Counter({7: 2, 5: 2, 8: 2, 10: 2, 4: 1, 3: 1, 6: 1, 9: 1})
>>> seed(1)
>>> gather_stats_flex(2, 12)
Counter({7: 2, 5: 2, 8: 2, 10: 2, 4: 1, 3: 1, 6: 1, 9: 1})
"""


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
