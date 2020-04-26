"""Python Cookbook 2nd ed.

Chapter 7, recipe 5, Using dataclasses for mutable objects
"""

from dataclasses import dataclass
from typing import List, ClassVar, Tuple
from Chapter_07.ch07_r04 import CardPoints
import random


@dataclass(init=False)
class Deck:
    suits: ClassVar[Tuple[str, ...]] = (
        "\N{Black Club Suit}",
        "\N{White Diamond Suit}",
        "\N{White Heart Suit}",
        "\N{Black Spade Suit}",
    )
    cards: List[CardPoints]

    def __init__(self) -> None:
        self.cards = [
            CardPoints(rank=r, suit=s) for r in range(1, 14) for s in self.suits
        ]
        random.shuffle(self.cards)


@dataclass
class CribbageHand:
    cards: List[CardPoints]

    def to_crib(self, card1, card2):
        self.cards.remove(card1)
        self.cards.remove(card2)


test_Dataclass = """
>>> random.seed(42)
>>> d = Deck()
>>> cards = d.cards[:6]
>>> cards
[CardPoints(rank=3, suit='♢'), CardPoints(rank=6, suit='♠'), CardPoints(rank=7, suit='♢'), CardPoints(rank=1, suit='♠'), CardPoints(rank=6, suit='♢'), CardPoints(rank=10, suit='♡')]

>>> cards = [
... CardPoints(rank=3, suit='♢'), 
... CardPoints(rank=6, suit='♠'), 
... CardPoints(rank=7, suit='♢'), 
... CardPoints(rank=1, suit='♠'), 
... CardPoints(rank=6, suit='♢'), 
... CardPoints(rank=10, suit='♡')]
>>> ch1 = CribbageHand(cards)
>>> ch1
CribbageHand(cards=[CardPoints(rank=3, suit='♢'), CardPoints(rank=6, suit='♠'), CardPoints(rank=7, suit='♢'), CardPoints(rank=1, suit='♠'), CardPoints(rank=6, suit='♢'), CardPoints(rank=10, suit='♡')])
>>> [c.points() for c in ch1.cards]
[3, 6, 7, 1, 6, 10]
>>> ch1.to_crib(CardPoints(rank=3, suit='♢'), CardPoints(rank=1, suit='♠'))
>>> ch1
CribbageHand(cards=[CardPoints(rank=6, suit='♠'), CardPoints(rank=7, suit='♢'), CardPoints(rank=6, suit='♢'), CardPoints(rank=10, suit='♡')])
>>> [c.points() for c in ch1.cards]
[6, 7, 6, 10]
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
