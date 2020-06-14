"""Python Cookbook 2nd ed.

Chapter 12, WSGI implementation.
"""
from typing import  (
    Dict,
    Any,
    Callable,
    Optional,
    Tuple,
    Iterable,
    cast,
    TYPE_CHECKING,
    Text,
    Protocol,
    )

from Chapter_12.card_model import *

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
    json_cards = list(card.serialize() for card in cards)
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
        json_cards = list(card.serialize() for card in cards)
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
