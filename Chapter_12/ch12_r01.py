"""Python Cookbook 2nd ed.

Chapter 12, recipe 1.
"""
import json
import random
from typing import (
    List,
    Dict,
    Iterator,
    Any,
    Callable,
    Union,
    Optional,
    Tuple,
    Iterable,
    cast,
    overload,
    TYPE_CHECKING,
    Text,
    Protocol,
)


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
        return {"__class__": "Card", "rank": self.rank, "suit": self.suit}


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
            Card(r, s) for r in range(1, 14) for s in self.SUITS for _ in range(n)
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


# Copy-Pasta from wsgiref/types.pyi
class StartResponse(Protocol):
    def __call__(
        self,
        status: str,
        headers: List[Tuple[str, str]],
        exc_info: Optional[Tuple] = ...,
    ) -> Callable[[bytes], Any]:
        ...


WSGIEnvironment = Dict[Text, Any]
WSGIApplication = Callable[[WSGIEnvironment, StartResponse], Iterable[bytes]]

from http import HTTPStatus

deck: Optional[Deck] = None


def deal_cards(
    environ: Dict[str, Any], start_response: StartResponse
) -> Iterable[bytes]:
    global deck
    if deck is None:
        random.seed(environ.get("DEAL_APP_SEED"))
        deck = Deck()
    hand_size = int(environ.get("HAND_SIZE", 5))
    cards = deck.deal(hand_size)
    status = f"{HTTPStatus.OK.value} {HTTPStatus.OK.phrase}"
    headers = [("Content-Type", "application/json;charset=utf-8")]
    start_response(status, headers)
    json_cards = list(card.to_json() for card in cards)
    return [json.dumps(json_cards, indent=2).encode("utf-8")]


class DealCards:
    def __init__(self, hand_size: int = 5, seed: Optional[int] = None) -> None:
        self.hand_size = hand_size
        random.seed(seed)
        self.deck = Deck()
        self.offset = 0

    def __call__(
        self, environ: Dict[str, Any], start_response: StartResponse
    ) -> Iterable[bytes]:
        if self.offset + self.hand_size >= len(self.deck):
            self.deck = Deck()
            self.offset = 0
        cards = self.deck[self.offset : self.offset + self.hand_size]
        self.offset += self.hand_size
        status = f"{HTTPStatus.OK.value} {HTTPStatus.OK.phrase}"
        headers = [("Content-Type", "application/json;charset=utf-8")]
        start_response(status, headers)
        json_cards = list(card.to_json() for card in cards)
        return [json.dumps(json_cards, indent=2).encode("utf-8")]


from urllib.parse import parse_qs


class JSON_Filter:
    def __init__(self, json_app: WSGIApplication) -> None:
        self.json_app = json_app

    def __call__(
        self, environ: Dict[str, Any], start_response: StartResponse
    ) -> Iterable[bytes]:
        if "HTTP_ACCEPT" in environ:
            if "json" in environ["HTTP_ACCEPT"]:
                environ["$format"] = "json"
                return self.json_app(environ, start_response)
        decoded_query = parse_qs(environ["QUERY_STRING"])
        if "$format" in decoded_query:
            if decoded_query["$format"][0].lower() == "json":
                environ["$format"] = "json"
                return self.json_app(environ, start_response)
        status = f"{HTTPStatus.BAD_REQUEST.value} {HTTPStatus.BAD_REQUEST.phrase}"
        headers = [("Content-Type", "text/plain;charset=utf-8")]
        start_response(status, headers)
        return [
            "Request doesn't include ?$format=json or Accept:application/json header".encode(
                "utf-8"
            )
        ]


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    # dealer = DealCards()
    json_wrapper = JSON_Filter(deal_cards)

    httpd = make_server("", 8080, json_wrapper)  # type: ignore
    httpd.serve_forever()
