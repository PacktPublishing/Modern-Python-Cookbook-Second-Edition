"""Python Cookbook 2nd ed.

Chapter 4, recipe 9, Set-related type hints
"""

import collections
from enum import Enum
import random
from typing import List, Tuple, Set


class Die(str, Enum):
    d_1 = "\u2680"
    d_2 = "\u2681"
    d_3 = "\u2682"
    d_4 = "\u2683"
    d_5 = "\u2684"
    d_6 = "\u2685"


def zonk(n: int = 6) -> Tuple[Die, ...]:
    faces = list(Die)
    return tuple(random.choice(faces) for _ in range(n))


test_zonk = """
>>> random.seed(42)
>>> zonk()
(<Die.d_6: '⚅'>, <Die.d_1: '⚀'>, <Die.d_1: '⚀'>, <Die.d_6: '⚅'>, <Die.d_3: '⚂'>, <Die.d_2: '⚁'>)

"""


def eval_zonk_6(hand: Tuple[Die, ...]) -> str:
    assert len(hand) == 6, "Only works for 6-dice zonk."
    faces = list(Die)
    small_straights = [
        set(faces[:-1]), set(faces[1:])
    ]
    unique: Set[Die] = set(hand)
    # print(f"{unique=}")
    if len(unique) == 6:
        return "large straight"
    elif len(unique) == 5 and unique in small_straights:
        return "small straight"
    elif len(unique) == 2:
        return "three of a kind"
    elif len(unique) == 1:
        return "six of a kind!"
    elif len(unique) in {3, 4}:
        # len(unique) == 4: wwwxyz (good) or wwxxyz (non-scoring)
        # len(unique) == 3: xxxxyz, xxxyyz (good) or xxyyzz (non-scoring)
        frequencies: Set[int] = set(collections.Counter(hand).values())
        # print(f"{frequencies=}")
        if 3 in frequencies or 4 in frequencies:
            return "three of a kind"
        elif Die.d_1 in unique:
            return "ace"
    return "Zonk!"


test_eval_zonk_6 = """
>>> eval_zonk_6([Die.d_1, Die.d_1, Die.d_1, Die.d_1, Die.d_1, Die.d_1])
'six of a kind!'
>>> eval_zonk_6([Die.d_1, Die.d_2, Die.d_1, Die.d_1, Die.d_1, Die.d_1])
'three of a kind'
>>> eval_zonk_6([Die.d_1, Die.d_2, Die.d_3, Die.d_2, Die.d_2, Die.d_2])
'three of a kind'
>>> eval_zonk_6([Die.d_1, Die.d_2, Die.d_1, Die.d_2, Die.d_1, Die.d_2])
'three of a kind'
>>> eval_zonk_6([Die.d_1, Die.d_2, Die.d_3, Die.d_4, Die.d_5, Die.d_2])
'small straight'
>>> eval_zonk_6([Die.d_1, Die.d_2, Die.d_3, Die.d_4, Die.d_5, Die.d_6])
'large straight'
>>> eval_zonk_6([Die.d_1, Die.d_2, Die.d_3, Die.d_2, Die.d_3, Die.d_4])
'ace'
>>> eval_zonk_6([Die.d_2, Die.d_2, Die.d_3, Die.d_3, Die.d_4, Die.d_4])
'Zonk!'
>>> eval_zonk_6([Die.d_1, Die.d_2, Die.d_3, Die.d_3, Die.d_5, Die.d_6])
'Zonk!'

"""

test_integration = """
>>> random.seed(42)
>>> roll = zonk()
>>> roll
(<Die.d_6: '⚅'>, <Die.d_1: '⚀'>, <Die.d_1: '⚀'>, <Die.d_6: '⚅'>, <Die.d_3: '⚂'>, <Die.d_2: '⚁'>)
>>> eval_zonk_6(roll)
'ace'
>>> roll = zonk()
>>> roll
(<Die.d_2: '⚁'>, <Die.d_2: '⚁'>, <Die.d_6: '⚅'>, <Die.d_1: '⚀'>, <Die.d_6: '⚅'>, <Die.d_6: '⚅'>)
>>> eval_zonk_6(roll)
'three of a kind'
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
