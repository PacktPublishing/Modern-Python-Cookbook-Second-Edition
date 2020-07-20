"""
openapi: 3.0.3
info:
  title: Python Cookbook Chapter 12, recipe 1.
  description: Using the Flask framework for RESTful APIs
  version: "1.0"
servers:
- url: "http://127.0.0.1:5000/dealer"
paths:
  /hand:
    get:
      parameters:
      - name: cards
        in: query
        required: false
        style: form
        schema:
          type: string
        explode: false
      responses:
        "200":
          description: One hand of cards with a size given by the hand value in the query string
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    __class__:
                        type: string
                    __init__:
                        type: object
                        properties:
                            rank:
                                type: integer
                            suit:
                                type: string
components: {}
"""
import random
import os
from typing import Optional
from flask import Flask, jsonify, request, abort, Response
from http import HTTPStatus

from Chapter_12.card_model import Card, Deck

dealer = Flask("dealer")

deck: Optional[Deck] = None


def get_deck() -> Deck:
    global deck
    if deck is None:
        random.seed(os.environ.get("DEAL_APP_SEED"))
        deck = Deck()
    return deck


@dealer.before_request
def check_json() -> Optional[Response]:
    if "json" in request.headers.get("Accept", "*/*"):
        return None
    if "json" == request.args.get("$format", "html"):
        return None
    print(f"Missing $format=json in {request.args}")
    return abort(HTTPStatus.BAD_REQUEST)


@dealer.route("/dealer/hand")
def deal() -> Response:
    try:
        hand_size = int(request.args.get("cards", 5))
        assert 1 <= hand_size < 53
    except Exception as ex:
        abort(HTTPStatus.BAD_REQUEST)
    deck = get_deck()
    cards = deck.deal(hand_size)
    response = jsonify([card.serialize() for card in cards])
    return response


if __name__ == "__main__":
    dealer.run(use_reloader=True, threaded=False)

"""
https://editor.swagger.io/

Start with this to force a particular seed to get a consistent result.
::

    DEAL_APP_SEED=42 PYTHONPATH=. python Chapter_12.ch12_r01.py

Note the --header for the accept is required, as are the quotes to stop zsh from looking at the ?
::

    curl 'http://127.0.0.1:5000/dealer/hand?cards=5' --header accept:application/json                         

Response::

    [{"__class__":"Card","rank":10,"suit":"\u2661"},{"__class__":"Card","rank":4,"suit":"\u2661"},{"__class__":"Card","rank":7,"suit":"\u2660"},{"__class__":"Card","rank":11,"suit":"\u2662"},{"__class__":"Card","rank":12,"suit":"\u2661"}]
"""
