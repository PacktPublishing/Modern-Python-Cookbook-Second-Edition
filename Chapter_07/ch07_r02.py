"""Python Cookbook 2nd ed.

Chapter 7, recipe 2
"""
import logging
from typing import TYPE_CHECKING, Protocol

SUITS = "\u2660\u2661\u2662\u2663"
Spades, Hearts, Diamonds, Clubs = SUITS


class Card:
    """Superclass for cards"""

    __slots__ = ("rank", "suit")

    def __init__(self, rank: int, suit: str) -> None:
        super().__init__()
        self.rank = rank
        self.suit = suit

    def __repr__(self) -> str:
        return f"{self.rank:2d} {self.suit}"


class AceCard(Card):
    def __repr__(self) -> str:
        return f" A {self.suit}"


class FaceCard(Card):
    def __repr__(self) -> str:
        names = {11: "J", 12: "Q", 13: "K"}
        return f" {names[self.rank]} {self.suit}"


def make_card(rank: int, suit: str) -> Card:
    """Type hint agrees with class hierarchy."""
    if rank == 1:
        return AceCard(rank, suit)
    if 2 <= rank < 11:
        return Card(rank, suit)
    if 11 <= rank:
        return FaceCard(rank, suit)
    raise ValueError(f"Invalid rank {rank}")


class PointedCard(Protocol):
    """Define properties required so we can mixin properly."""

    rank: int


class CribbagePoints(PointedCard):
    # Inform mypy this mixin has a valid reference to rank
    # See https://mypy.readthedocs.io/en/latest/more_types.html#mixin-classes

    # Older technique is to force the definition only when running mypy.
    # if TYPE_CHECKING:
    #     rank: int

    def points(self: PointedCard) -> int:
        return self.rank


class CribbageFacePoints(PointedCard):
    def points(self: PointedCard) -> int:
        return 10


class CribbageCard(Card, CribbagePoints):
    pass


class CribbageAce(AceCard, CribbagePoints):
    pass


class CribbageFace(FaceCard, CribbageFacePoints):
    pass


def make_cribbage_card(rank: int, suit: str) -> Card:
    """Even with the mixins, these classes are subclasses of ``Card``."""
    if rank == 1:
        return CribbageAce(rank, suit)
    if 2 <= rank < 11:
        return CribbageCard(rank, suit)
    if 11 <= rank:
        return CribbageFace(rank, suit)
    raise ValueError(f"Invalid rank {rank}")


class Logged(PointedCard):
    """Add a logger. Must be first in the superclass list."""

    def __init__(self, *args, **kw):
        self.logger = logging.getLogger(self.__class__.__name__)
        super().__init__(*args, **kw)

    def points(self):
        p = super().points()
        self.logger.debug("points {0}", p)
        return p


class LoggedCribbageAce(AceCard, Logged, CribbagePoints):
    pass


class LoggedCribbageCard(Card, Logged, CribbagePoints):
    pass


class LoggedCribbageFace(FaceCard, Logged, CribbageFacePoints):
    pass


def make_logged_card(rank: int, suit: str) -> Card:
    """Even with the mixins, these classes are subclasses of ``Card``."""
    if rank == 1:
        return LoggedCribbageAce(rank, suit)
    if 2 <= rank < 11:
        return LoggedCribbageCard(rank, suit)
    if 11 <= rank:
        return LoggedCribbageFace(rank, suit)
    raise ValueError(f"Invalid rank {rank}")


__test__ = {
    "make_cribbage_card": """
>>> import random
>>> random.seed(1)
>>> deck = [make_cribbage_card(rank+1, suit) for rank in range(13) for suit in SUITS]
>>> random.shuffle(deck)
>>> len(deck)
52
>>> deck[:5]
[ K ♡,  3 ♡, 10 ♡,  6 ♢,  A ♢]
>>> sum(c.points() for c in deck[:5])
30

>>> c = deck[5]
>>> c
10 ♢
>>> c.__class__.__name__
'CribbageCard'
>>> c.__class__.mro()  # doctest: +NORMALIZE_WHITESPACE
[<class 'Chapter_07.ch07_r02.CribbageCard'>, <class 'Chapter_07.ch07_r02.Card'>, <class 'Chapter_07.ch07_r02.CribbagePoints'>, <class 'Chapter_07.ch07_r02.PointedCard'>, <class 'typing.Protocol'>, <class 'typing.Generic'>, <class 'object'>]

""",
    "make_logged_card": """
>>> import random
>>> random.seed(1)
>>> deck = [make_logged_card(rank+1, suit) for rank in range(13) for suit in SUITS]
>>> random.shuffle(deck)
>>> len(deck)
52
>>> deck[:5]
[ K ♡,  3 ♡, 10 ♡,  6 ♢,  A ♢]
>>> sum(c.points() for c in deck[:5])
30

>>> c = deck[5]
>>> c.logger.name
'LoggedCribbageCard'
>>> c.__class__.mro()  # doctest: +NORMALIZE_WHITESPACE
[<class 'Chapter_07.ch07_r02.LoggedCribbageCard'>,
 <class 'Chapter_07.ch07_r02.Card'>,
 <class 'Chapter_07.ch07_r02.Logged'>,
 <class 'Chapter_07.ch07_r02.CribbagePoints'>,
 <class 'Chapter_07.ch07_r02.PointedCard'>,
 <class 'typing.Protocol'>,
 <class 'typing.Generic'>,
 <class 'object'>]

""",
}
