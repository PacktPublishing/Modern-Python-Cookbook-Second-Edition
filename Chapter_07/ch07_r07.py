"""Python Cookbook 2nd ed.

Chapter 7, recipe 7, Optimizing small objects with __slots__
"""
import random
from typing import Optional

# Card = collections.namedtuple('Card', ('rank', 'suit'))

from typing import NamedTuple, List, Union


class Card(NamedTuple):
    rank: int
    suit: str


class Hand:
    """
    >>> h = Hand(1)
    >>> h.deal(Card(1,'\N{white heart suit}'))
    >>> h.deal(Card(10, '\N{black club suit}'))
    >>> h
    Hand(bet=1, hand=[Card(rank=1, suit='♡'), Card(rank=10, suit='♣')])
    >>> h.total = 11
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/cookbook/lib/python3.8/doctest.py", line 1328, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.Hand[4]>", line 1, in <module>
        h.total = 11 #doctest: +IGNORE_EXCEPTION_DETAIL
    AttributeError: 'Hand' object has no attribute 'total'
    """

    __slots__ = ("cards", "bet")

    def __init__(self, bet: int, hand: Union["Hand", List[Card], None] = None) -> None:
        self.cards: List[Card] = (
            [] if hand is None else hand.cards if isinstance(hand, Hand) else hand
        )
        self.bet: int = bet

    def deal(self, card: Card) -> None:
        self.cards.append(card)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(" f"bet={self.bet}, hand={self.cards})"


if __name__ == "__main__":

    SUITS = (
        "\N{black spade suit}",
        "\N{white heart suit}",
        "\N{white diamond suit}",
        "\N{black club suit}",
    )
    deck = [Card(r, s) for r in range(1, 14) for s in SUITS]
    random.seed(2)
    random.shuffle(deck)
    dealer = iter(deck)

    h = Hand(2)
    h.deal(next(dealer))
    h.deal(next(dealer))
    print(h)
