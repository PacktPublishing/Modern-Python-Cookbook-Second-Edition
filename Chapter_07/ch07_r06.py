"""Python Cookbook 2nd ed.

Chapter 7, recipe 6, Using frozen dataclasses for immutable objects
"""


from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Card:
    rank: int
    suit: str


test_card = """
>>> eight_hearts = Card(rank=8, suit='\N{White Heart Suit}')
>>> eight_hearts
Card(rank=8, suit='♡')
>>> eight_hearts.rank
8
>>> eight_hearts.suit
'♡'


>>> eight_hearts.suit = '\N{Black Spade Suit}'
Traceback (most recent call last):
  File "/Users/slott/miniconda3/envs/cookbook/lib/python3.8/doctest.py", line 1328, in __run
    compileflags, 1), test.globs)
  File "<doctest examples.txt[30]>", line 1, in <module>
    eight_hearts.suit = '\N{Black Spade Suit}'
dataclasses.FrozenInstanceError: cannot assign to field 'suit'
"""


@dataclass(frozen=True, order=True)
class CardPoints:
    rank: int
    suit: str

    def points(self) -> int:
        if 1 <= self.rank < 10:
            return self.rank
        else:
            return 10


test_card_points = """
>>> hj = CardPoints(rank=11, suit='\N{White Heart Suit}')
>>> h5 = CardPoints(rank=5, suit='\N{White Heart Suit}')
>>> print(f"Hand: {hj=}, {h5=}")
Hand: hj=CardPoints(rank=11, suit='♡'), h5=CardPoints(rank=5, suit='♡')
>>> print(f"Total: {hj.points() + h5.points()=}")
Total: hj.points() + h5.points()=15
"""

from dataclasses import field
from typing import List


@dataclass(frozen=True, order=True)
class Hand:
    cards: List[CardPoints] = field(default_factory=list)


test_hand = """
>>> cards = [
... CardPoints(rank=3, suit='♢'), 
... CardPoints(rank=6, suit='♠'), 
... CardPoints(rank=7, suit='♢'), 
... CardPoints(rank=1, suit='♠'), 
... CardPoints(rank=6, suit='♢'), 
... CardPoints(rank=10, suit='♡')]
>>> 
>>> h = Hand(cards)
>>> crib = Hand()
>>> d3 = CardPoints(rank=3, suit='♢')
>>> h.cards.remove(d3)
>>> crib.cards.append(d3)
>>> s1 = CardPoints(rank=1, suit='♠')
>>> h.cards.remove(s1)
>>> crib.cards.append(s1)
>>> crib
Hand(cards=[CardPoints(rank=3, suit='♢'), CardPoints(rank=1, suit='♠')])
>>> crib.another_attribute = "dealer"
Traceback (most recent call last):
  ...
dataclasses.FrozenInstanceError: cannot assign to field 'another_attribute'
>>> crib.cards = 355/113
Traceback (most recent call last):
  ...
dataclasses.FrozenInstanceError: cannot assign to field 'cards'

"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
