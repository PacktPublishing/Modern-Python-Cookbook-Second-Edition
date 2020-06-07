"""Python Cookbook 2nd ed.

Chapter 8, recipe 1, Choosing between inheritance and extension – the “is-a” question

"""
from typing import NamedTuple, List
import random

# from collections import namedtuple
# Card = namedtuple('Card', ('rank', 'suit'))


class Card(NamedTuple):
    rank: int
    suit: str


SUITS = "\u2660\u2661\u2662\u2663"
Spades, Hearts, Diamonds, Clubs = tuple(SUITS)

test_Card = """
>>> c_2s = Card(2, Spades)
>>> c_2s
Card(rank=2, suit='♠')
"""


class Deck_W:
    def __init__(self, cards: List[Card]) -> None:
        self.cards = cards
        self.deal_iter = iter(cards)

    def shuffle(self) -> None:
        random.shuffle(self.cards)
        self.deal_iter = iter(self.cards)

    def deal(self) -> Card:
        return next(self.deal_iter)


test_Deck_W = """
>>> domain = list(Card(r+1,s) for r in range(13) for s in SUITS)
>>> d = Deck_W(domain)
>>> random.seed(1)
>>> d.shuffle()
>>> [d.deal() for _ in range(5)]
[Card(rank=13, suit='♡'), Card(rank=3, suit='♡'), Card(rank=10, suit='♡'), Card(rank=6, suit='♢'), Card(rank=1, suit='♢')]
"""


class Deck_X(list):
    def shuffle(self) -> None:
        random.shuffle(self)
        self.deal_iter = iter(self)

    def deal(self) -> Card:
        return next(self.deal_iter)


test_Deck_X = """
>>> domain = Deck_X(Card(r+1,s) for r in range(13) for s in SUITS)
>>> d = Deck_X(domain)
>>> random.seed(1)
>>> d.shuffle()
>>> [d.deal() for _ in range(5)]
[Card(rank=13, suit='♡'), Card(rank=3, suit='♡'), Card(rank=10, suit='♡'), Card(rank=6, suit='♢'), Card(rank=1, suit='♢')]

>>> d2 = Deck_X(Card(r+1,s) for r in range(13) for s in SUITS)
>>> random.seed(1)
>>> d2.shuffle()
>>> [d2.deal() for _ in range(5)]
[Card(rank=13, suit='♡'), Card(rank=3, suit='♡'), Card(rank=10, suit='♡'), Card(rank=6, suit='♢'), Card(rank=1, suit='♢')]
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
