"""Python Cookbook 2nd ed.

Chapter 8, recipe 7, Improving performance with an an ordered collection
"""
import bisect
from typing import Iterable, Iterator
from Chapter_08.ch08_r06 import *


class Hand:
    def __init__(self, card_iter: Iterable[Card]) -> None:
        self.cards = list(card_iter)
        self.cards.sort()

    def add(self, aCard: Card) -> None:
        bisect.insort(self.cards, aCard)

    def index(self, aCard: Card) -> int:
        i = bisect.bisect_left(self.cards, aCard)
        if i != len(self.cards) and self.cards[i] == aCard:
            return i
        raise ValueError

    def __contains__(self, aCard: Card) -> bool:
        try:
            self.index(aCard)
            return True
        except ValueError:
            return False

    def __iter__(self) -> Iterator[Card]:
        return iter(self.cards)

    def __le__(self, other: Any) -> bool:
        for card in self:
            if card not in other:
                return False
        return True


test_hand = """
>>> import random
>>> random.seed(4)
>>> deck = make_deck()
>>> random.shuffle(deck)
>>> h = Hand(deck[:12])
>>> [str(c) for c in h.cards]
[' 9 ♣', '10 ♣', ' J ♠', ' J ♢', ' J ♢', ' Q ♠', ' Q ♣', ' K ♠', ' K ♠', ' K ♣', ' A ♡', ' A ♣']

>>> pinochle = Hand([make_card(11,'♢'), make_card(12,'♠')])
>>> pinochle <= h
True
>>> sum(c.points() for c in h)
56
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}

import random


def pick_seed():
    pinochle = Hand([make_card(11, "♢"), make_card(12, "♠")])
    for seed in range(4096):
        random.seed(seed)
        deck = make_deck()
        random.shuffle(deck)
        h = Hand(deck[:12])
        if pinochle <= h:
            print(seed, h.cards)
            return
    print("No Pinochle in range(4096)")


if __name__ == "__main__":
    pick_seed()
