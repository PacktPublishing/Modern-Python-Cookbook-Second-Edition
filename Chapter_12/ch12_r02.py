"""
openapi: 3.0.3

info:
  title: Python Cookbook Chapter 12, recipe 2.
  description: Parsing the query string in a request
  version: "1.0"

servers:
- url: "http://127.0.0.1:5000/dealer"

paths:
  /hands:
    get:
      parameters:
      - name: cards
        in: query
        style: form
        explode: true
        schema:
          type: integer
      responses:
        "200":
          description: one hand of cards for each `hand` value in the query string
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    hand:
                      type: integer
                    cards:
                      type: array
                      items:
                        $ref: "#/components/schemas/Card"
  /hand:
    get:
      parameters:
      - name: cards
        in: query
        content:
          application/json:
            schema:
              type: string
              default: "5"
      responses:
        "200":
          description: One hand of cards with a size given by the hand value in
            the query string
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "#/components/schemas/Card"

components:
  schemas:
    Card:
      type: object
      properties:
        __class__:
          type: string
          example: "Card"
        __init__:
          type: object
          properties:
            rank:
              type: integer
              example: 1
            suit:
              type: string
              example: "\u2660"
"""
import random
from http import HTTPStatus
import os
from typing import Optional

from flask import Flask, jsonify, request, abort, Response
import yaml

from Chapter_12.card_model import Card, Deck

dealer = Flask("dealer")
dealer.DEBUG = True
dealer.TESTING = True

# Build a Python structure from the YAML source.
specification = yaml.load(__doc__, Loader=yaml.SafeLoader)

deck: Optional[Deck] = None


def get_deck() -> Deck:
    global deck
    if deck is None:
        random.seed(os.environ.get("DEAL_APP_SEED"))
        deck = Deck()
    return deck


@dealer.before_request
def check_json() -> Optional[Response]:
    # Special case for these paths only.
    # It is RECOMMENDED that the root OpenAPI document be named: openapi.json or openapi.yaml.
    if request.path in ("/dealer/openapi.yaml", "/dealer/openapi.json"):
        return None
    if "json" in request.headers.get("Accept", "*/*"):
        return None
    if "json" == request.args.get("$format", "html"):
        return None
    return abort(HTTPStatus.BAD_REQUEST)


from flask import send_file

# @dealer.route('/dealer/openapi.yaml')
def openapi_1() -> Response:
    # Note. No IANA registered standard as of this writing.
    response = send_file("openapi.yaml", mimetype="application/yaml")
    return response


from flask import make_response


@dealer.route("/dealer/openapi.yaml")
def openapi_2() -> Response:
    response = make_response(yaml.dump(specification).encode("utf-8"))
    # Note. No IANA registered standard as of this writing.
    response.headers["Content-Type"] = "application/yaml"
    return response


from flask import make_response
import json


@dealer.route("/dealer/openapi.json")
def openapi_3() -> Response:
    return jsonify(specification)


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


@dealer.route("/dealer/hands")
def multi_hand() -> Response:
    dealer.logger.debug(f"Request: {request.args}")
    try:
        hand_sizes = request.args.getlist("cards", type=int)
    except ValueError as ex:
        abort(HTTPStatus.BAD_REQUEST)
    dealer.logger.info(f"{hand_sizes=}")
    if len(hand_sizes) == 0:
        hand_sizes = [13, 13, 13, 13]
    if not (1 <= sum(hand_sizes) < 53):
        abort(HTTPStatus.BAD_REQUEST)
    deck = get_deck()
    hands = [deck.deal(hand_size) for hand_size in hand_sizes]
    response = jsonify(
        [
            {"hand": i, "cards": [card.serialize() for card in hand]}
            for i, hand in enumerate(hands)
        ]
    )
    return response


if __name__ == "__main__":
    dealer.run(use_reloader=True, threaded=False)

"""
In one terminal window,
start the server this to force a particular seed to get a consistent result.
::

    DEAL_APP_SEED=42 PYTHONPATH=. python Chapter_12/ch12_r02.py

In another terminal window, enter commands. These examples use ``curl``,
but ``wget`` can also be used.

Get the OpenAPI spec
::

    % curl http://127.0.0.1:5000/dealer/openapi.yaml --header accept:application/json

Get a hard of cards
::
    
    % curl 'http://127.0.0.1:5000/dealer/hand?cards=5' --header accept:application/json
    [
      {
        "__class__": "Card", 
        "__init__": {
          "rank": 10, 
          "suit": "\u2661"
        }
      }, 
      {
        "__class__": "Card", 
        "__init__": {
          "rank": 4, 
          "suit": "\u2661"
        }
      }, 
      {
        "__class__": "Card", 
        "__init__": {
           "rank": 7, 
           "suit": "\u2660"
        }
      }, 
      {
        "__class__": "Card", 
        "__init__": {
          "rank": 11, 
          "suit": "\u2662"
        }
      }, 
      {
        "__class__": "Card", 
        "__init__": {
          "rank": 12, 
          "suit": "\u2661"
        }
      }
    ]

Get multiple hands
::

    % curl 'http://127.0.0.1:5000/dealer/hands?cards=2&cards=1&cards=1&cards=1' --header accept:application/json

    [
      {
        "cards": [
          {
            "__class__": "Card", 
            "rank": 3, 
            "suit": "\u2663"
          }, 
          {
            "__class__": "Card", 
            "rank": 10, 
            "suit": "\u2660"
          }
        ], 
        "hand": 0
      }, 
      {
        "cards": [
          {
            "__class__": "Card", 
            "__init__": {
              "rank": 9, 
              "suit": "\u2660"
            }
          }
        ], 
        "hand": 1
      }, 
      {
        "cards": [
          {
            "__class__": "Card", 
            "__init__": {
              "rank": 13, 
              "suit": "\u2663"
            }
          }
        ], 
        "hand": 2
      }, 
      {
        "cards": [
          {
            "__class__": "Card", 
            "__init__": {
              "rank": 5, 
              "suit": "\u2663"
            }
          }
        ], 
        "hand": 3
      }
    ]
"""

alternative_specification = {
    "openapi": "3.0.3",
    "info": {
        "description": "Parsing the query string in a request",
        "title": "Python Cookbook Chapter 12, recipe 2.",
        "version": "1.0",
    },
    "servers": [{"url": "http://127.0.0.1:5000/dealer"}],
    "paths": {
        "/hand": {
            "get": {
                "parameters": [
                    {
                        "content": {
                            "application/json": {
                                "schema": {"default": "5", "type": "string"}
                            }
                        },
                        "in": "query",
                        "name": "cards",
                    }
                ],
                "responses": {
                    "200": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "items": {"$ref": "#/components/schemas/Card"},
                                    "type": "array",
                                }
                            }
                        },
                        "description": "One hand of "
                        "cards with "
                        "a size "
                        "given by "
                        "the hand "
                        "value in "
                        "the query "
                        "string",
                    }
                },
            }
        },
        "/hands": {
            "get": {
                "parameters": [
                    {
                        "explode": True,
                        "in": "query",
                        "name": "cards",
                        "schema": {"type": "integer"},
                        "style": "form",
                    }
                ],
                "responses": {
                    "200": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "items": {
                                        "properties": {
                                            "cards": {
                                                "items": {
                                                    "$ref": "#/components/schemas/Card"
                                                },
                                                "type": "array",
                                            },
                                            "hand": {"type": "integer"},
                                        },
                                        "type": "object",
                                    },
                                    "type": "array",
                                }
                            }
                        },
                        "description": "one hand "
                        "of cards "
                        "for each "
                        "`hand` "
                        "value in "
                        "the query "
                        "string",
                    }
                },
            }
        },
    },
    "components": {
        "schemas": {
            "Card": {
                "properties": {
                    "__class__": {"example": "Card", "type": "string"},
                    "__init__": {
                        "properties": {
                            "rank": {"example": 1, "type": "integer"},
                            "suit": {"example": "♠", "type": "string"},
                        },
                        "type": "object",
                    },
                },
                "type": "object",
            }
        }
    }
}

test_specification_matches = """
>>> assert specification ==  alternative_specification
"""


__test__ = {
    n: v
    for n, v in locals().items()
    if n.startswith("test_")
}
