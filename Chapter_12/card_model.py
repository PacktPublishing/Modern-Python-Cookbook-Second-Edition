"""Python Cookbook 2nd ed.

Chapter 12, Data Model used by many seb services recipes
"""
from dataclasses import dataclass, asdict
import json
import random
from typing import Any, Dict, List, Iterator, Type, Union, overload

@dataclass(frozen=True)
class Card:
    """
    >>> c = Card(1, "\\u2660")
    >>> repr(c)
    "Card(rank=1, suit='♠')"
    >>> document = c.serialize()
    >>> document
    {'__class__': 'Card', '__init__': {'rank': 1, 'suit': '♠'}}
    >>> json.dumps(document)
    '{"__class__": "Card", "__init__": {"rank": 1, "suit": "\\\\u2660"}}'
    >>> c2 = Card.deserialize(document)
    >>> c2
    Card(rank=1, suit='♠')
    >>> c == c2
    True
    """
    rank: int
    suit: str

    def serialize(self) -> Dict[str, Any]:
        return {
            "__class__": self.__class__.__name__,
            "__init__": asdict(self)
        }

    @classmethod
    def deserialize(cls: Type, document: Dict[str, Any]) -> 'Card':
        if document["__class__"] != cls.__name__:
            raise TypeError(
                f"Cannot make {cls.__name__} "
                f"from {document['__class__']}"
            )
        return Card(**document["__init__"])


class Deck:
    """
    Create deck or shoe.

    >>> random.seed(2)
    >>> deck = Deck()
    >>> cards = deck.deal(5)
    >>> cards  # doctest: +NORMALIZE_WHITESPACE
    [Card(rank=4, suit='♣'), Card(rank=8, suit='♡'),
     Card(rank=3, suit='♡'), Card(rank=6, suit='♡'),
     Card(rank=2, suit='♠')]
    >>> json_cards = list(card.serialize() for card in cards)
    >>> print(json.dumps(json_cards, indent=2, sort_keys=True))
    [
      {
        "__class__": "Card",
        "__init__": {
          "rank": 4,
          "suit": "\u2663"
        }
      },
      {
        "__class__": "Card",
        "__init__": {
          "rank": 8,
          "suit": "\u2661"
        }
      },
      {
        "__class__": "Card",
        "__init__": {
          "rank": 3,
          "suit": "\u2661"
        }
      },
      {
        "__class__": "Card",
        "__init__": {
          "rank": 6,
          "suit": "\u2661"
        }
      },
      {
        "__class__": "Card",
        "__init__": {
          "rank": 2,
          "suit": "\u2660"
        }
      }
    ]
    """
    SUITS = (
        "\N{black spade suit}",
        "\N{white heart suit}",
        "\N{white diamond suit}",
        "\N{black club suit}",
    )

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

