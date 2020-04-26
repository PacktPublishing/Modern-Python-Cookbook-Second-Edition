"""Python Cookbook 2nd ed.

Chapter 12, Data Model used by many server recipes
"""
import json
import random
from typing import List, Iterator, Union, overload

class Card:
    """
    >>> c = Card(1, "\\u2660")
    >>> repr(c)
    "Card(rank=1, suit='♠')"
    >>> c.to_json()
    {'__class__': 'Card', 'rank': 1, 'suit': '♠'}
    """

    __slots__ = ("rank", "suit")

    def __init__(self, rank: int, suit: str) -> None:
        self.rank = int(rank)
        self.suit = suit

    def __repr__(self):
        return f"Card(rank={self.rank!r}, suit={self.suit!r})"

    def to_json(self):
        return {
            "__class__": "Card",
            "rank": self.rank,
            "suit": self.suit
        }


class Deck:
    SUITS = (
        "\N{black spade suit}",
        "\N{white heart suit}",
        "\N{white diamond suit}",
        "\N{black club suit}",
    )
    """
    Create deck or shoe.

    >>> random.seed(2)
    >>> deck = Deck()
    >>> cards = deck.deal(5)
    >>> cards  # doctest: +NORMALIZE_WHITESPACE
    [Card(rank=4, suit='♣'), Card(rank=8, suit='♡'),
     Card(rank=3, suit='♡'), Card(rank=6, suit='♡'),
     Card(rank=2, suit='♠')]
    >>> json_cards = list(card.to_json() for card in deck.deal(5))
    >>> print(json.dumps(json_cards, indent=2, sort_keys=True))
    [
      {
        "__class__": "Card",
        "rank": 2,
        "suit": "\u2662"
      },
      {
        "__class__": "Card",
        "rank": 13,
        "suit": "\u2663"
      },
      {
        "__class__": "Card",
        "rank": 7,
        "suit": "\u2662"
      },
      {
        "__class__": "Card",
        "rank": 6,
        "suit": "\u2662"
      },
      {
        "__class__": "Card",
        "rank": 7,
        "suit": "\u2660"
      }
    ]
    """

    def __init__(self, n: int = 1) -> None:
        self.n = n
        self.create_deck(self.n)

    def create_deck(self, n: int = 1) -> None:
        self.cards = [
            Card(r, s)
            for r in range(1, 14)
            for s in self.SUITS for _ in range(n)
        ]
        random.shuffle(self.cards)
        self.offset = 0

    def deal(self, hand_size: int = 5) -> List[Card]:
        if self.offset + hand_size > len(self.cards):
            self.create_deck(self.n)
        hand = self.cards[self.offset : self.offset + hand_size]
        self.offset += hand_size
        return hand

    def __len__(self) -> int:
        return len(self.cards)

    @overload
    def __getitem__(self, position: int) -> Card:
        ...

    @overload
    def __getitem__(self, position: slice) -> List[Card]:
        ...

    def __getitem__(self, position: Union[int, slice]) -> Union[Card, List[Card]]:
        return self.cards[position]

    def __iter__(self) -> Iterator[Card]:
        return iter(self.cards)

