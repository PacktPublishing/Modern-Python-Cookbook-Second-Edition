"""Python Cookbook 2nd ed.

Chapter 8, recipe 6, Creating a class that has orderable objects
"""
from typing import Any, Protocol, Union, List
from Chapter_08.ch08_r02 import AceCard, Card, FaceCard, SUITS, PointedCard

Spades, Hearts, Diamonds, Clubs = tuple(SUITS)


class CardLike(Protocol):
    rank: int
    suit: str


class SortedCard(CardLike):
    def __lt__(self: CardLike, other: Any) -> bool:
        return (self.rank, self.suit) < (other.rank, other.suit)

    def __le__(self: CardLike, other: Any) -> bool:
        return (self.rank, self.suit) <= (other.rank, other.suit)

    def __gt__(self: CardLike, other: Any) -> bool:
        return (self.rank, self.suit) > (other.rank, other.suit)

    def __ge__(self: CardLike, other: Any) -> bool:
        return (self.rank, self.suit) >= (other.rank, other.suit)


class PinochlePoints(PointedCard):
    def points(self: PointedCard) -> int:
        _points = {9: 0, 10: 10, 11: 2, 12: 3, 13: 4, 14: 11}
        return _points[self.rank]


class PinochleAce(AceCard, SortedCard, PinochlePoints):
    pass


class PinochleFace(FaceCard, SortedCard, PinochlePoints):
    pass


class PinochleNumber(Card, SortedCard, PinochlePoints):
    pass


PinochleCard = Union[PinochleAce, PinochleFace, PinochleNumber]


def make_card(rank: int, suit: str) -> PinochleCard:
    if rank in (9, 10):
        return PinochleNumber(rank, suit)
    elif rank in (11, 12, 13):
        return PinochleFace(rank, suit)
    else:
        return PinochleAce(rank, suit)


def make_deck() -> List[PinochleCard]:
    return [make_card(r, s) for _ in range(2) for r in range(9, 15) for s in SUITS]


test_card = """
>>> c1 = make_card(9, '♡')
>>> c2 = make_card(10, '♡')
>>> c3 = make_card(9, '♡')
>>> c1 < c2
True
>>> c1 == c1
True
>>> c1 == c2
False
>>> c1 == c3
True
>>> c1 > c2
False
"""

test_deck = """
>>> deck = make_deck()
>>> len(deck)
48
>>> [str(c) for c in deck[:8]]
[' 9 ♠', ' 9 ♡', ' 9 ♢', ' 9 ♣', '10 ♠', '10 ♡', '10 ♢', '10 ♣']
>>> [str(c) for c in deck[24:32]]
[' 9 ♠', ' 9 ♡', ' 9 ♢', ' 9 ♣', '10 ♠', '10 ♡', '10 ♢', '10 ♣']


>>> import random
>>> random.seed(4)
>>> random.shuffle(deck)
>>> [str(c) for c in sorted(deck[:12])]
[' 9 ♣', '10 ♣', ' J ♠', ' J ♢', ' J ♢', ' Q ♠', ' Q ♣', ' K ♠', ' K ♠', ' K ♣', ' A ♡', ' A ♣']
"""


def has_rank(c: PinochleCard, rank: int) -> bool:
    """
    Makes an equality comparison visible to MyPy.
    Why does this return a meaningful value? Because of the equality comparison in the base class.

    >>> c1 = make_card(9, '♡')
    >>> has_rank(c1, 9)
    False
    """
    return c == rank


test_card_int = """
>>> c1 = make_card(9, '♡')
>>> c1
PinochleNumber(rank=9, suit='♡')
>>> c1 <= 10  #doctest: +IGNORE_EXCEPTION_DETAIL 
Traceback (most recent call last):
  File "/Applications/PyCharm CE.app/Contents/plugins/python-ce/helpers/pycharm/docrunner.py", line 138, in __run
    exec(compile(example.source, filename, "single",
  File "<doctest ch07_r06b.__test__.test_card_int[2]>", line 1, in <module>
    c1 <= 10
  File "/Users/slott/Documents/Writing/Python/Python Cookbook 2e/Modern-Python-Cookbook-Second-Edition/Chapter_08.ch08_r06a.py", line 21, in __le__
    return (self.rank, self.suit) <= (other.rank, other.suit)
AttributeError: 'int' object has no attribute 'rank'
>>> c1 == 9
False
"""


class SortedIntCard(CardLike):
    def __lt__(self: CardLike, other: Any) -> bool:
        if isinstance(other, int):
            return self.rank < other
        return (self.rank, self.suit) < (other.rank, other.suit)

    def __le__(self: CardLike, other: Any) -> bool:
        if isinstance(other, int):
            return self.rank <= other
        return (self.rank, self.suit) <= (other.rank, other.suit)

    def __gt__(self: CardLike, other: Any) -> bool:
        if isinstance(other, int):
            return self.rank > other
        return (self.rank, self.suit) > (other.rank, other.suit)

    def __ge__(self: CardLike, other: Any) -> bool:
        if isinstance(other, int):
            return self.rank >= other
        return (self.rank, self.suit) >= (other.rank, other.suit)


class PinochleIntAce(AceCard, SortedIntCard, PinochlePoints):
    pass


class PinochleIntFace(FaceCard, SortedIntCard, PinochlePoints):
    pass


class PinochleIntNumber(Card, SortedIntCard, PinochlePoints):
    pass


PinochleIntCard = Union[PinochleIntAce, PinochleIntFace, PinochleIntNumber]


def make_int_card(rank: int, suit: str) -> PinochleIntCard:
    if rank in (9, 10):
        return PinochleIntNumber(rank, suit)
    elif rank in (11, 12, 13):
        return PinochleIntFace(rank, suit)
    else:
        return PinochleIntAce(rank, suit)


test_intcard_int = """
>>> c1 = make_int_card(9, '♡')
>>> c1
PinochleIntNumber(rank=9, suit='♡')
>>> c1 <= 10
True

The following doesn't work because we've inherited an equality test from the base class.
We need to re-engineer the base Card class.

>>> c1 == 9
False
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
