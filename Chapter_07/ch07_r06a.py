"""Python Cookbook 2nd ed.

Chapter 7, recipe 6a.
"""
from typing import Any, Protocol
from Chapter_07.ch07_r02 import AceCard, Card, FaceCard, SUITS, PointedCard

Spades, Hearts, Diamonds, Clubs = SUITS


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

    def __eq__(self: CardLike, other: Any) -> bool:
        return (self.rank, self.suit) == (other.rank, other.suit)

    def __ne__(self: CardLike, other: Any) -> bool:
        return (self.rank, self.suit) != (other.rank, other.suit)


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


def make_card(rank, suit):
    if rank in (9, 10):
        return PinochleNumber(rank, suit)
    elif rank in (11, 12, 13):
        return PinochleFace(rank, suit)
    else:
        return PinochleAce(rank, suit)


def make_deck():
    return [make_card(r, s) for _ in range(2) for r in range(9, 15) for s in SUITS]


__test__ = {
    "card": """
>>> c1 = make_card(9, '♡')
>>> c2 = make_card(10, '♡')
>>> c1 < c2
True
>>> c1 == c1
True
>>> c1 == c2
False
>>> c1 > c2
False
""",
    "deck": """
>>> deck = make_deck()
>>> len(deck)
48
>>> deck[:8]
[ 9 ♠,  9 ♡,  9 ♢,  9 ♣, 10 ♠, 10 ♡, 10 ♢, 10 ♣]
>>> deck[24:32]
[ 9 ♠,  9 ♡,  9 ♢,  9 ♣, 10 ♠, 10 ♡, 10 ♢, 10 ♣]


>>> import random
>>> random.seed(4)
>>> random.shuffle(deck)
>>> sorted(deck[:12])
[ 9 ♣, 10 ♣,  J ♠,  J ♢,  J ♢,  Q ♠,  Q ♣,  K ♠,  K ♠,  K ♣,  A ♡,  A ♣]
""",
    "card-int": """
>>> c1 = make_card(9, '♡')
>>> c1 == 9
Traceback (most recent call last):
  File "/Users/slott/miniconda3/envs/cookbook/lib/python3.8/doctest.py", line 1328, in __run
    compileflags, 1), test.globs)
  File "<doctest Chapter_07.ch07_r06a.__test__.card-int[1]>", line 1, in <module>
  File "/Users/slott/Documents/Writing/Python/Python Cookbook 2e/Code/Chapter_07/ch07_r06a.py", line 20, in __eq__
    return (self.rank, self.suit) == (other.rank, other.suit)
AttributeError: 'int' object has no attribute 'rank'

""",
}
