"""Python Cookbook 2nd ed.

Chapter 7, recipe 4, Using typing.NamedTuple for immutable objects
"""


from typing import NamedTuple


class Card(NamedTuple):
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
>>> eight_hearts[0]
8

>>> eight_hearts.suit = '\N{Black Spade Suit}'
Traceback (most recent call last):
  File "/Users/slott/miniconda3/envs/cookbook/lib/python3.8/doctest.py", line 1328, in __run
    compileflags, 1), test.globs)
  File "<doctest examples.txt[30]>", line 1, in <module>
    eight_hearts.suit = '\N{Black Spade Suit}'
AttributeError: can't set attribute
"""


class CardPoints(NamedTuple):
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

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
