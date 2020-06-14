"""Python Cookbook

Chapter 12, recipe 4, Parsing the URL path
Server.
"""
import os
import random
import logging
import sys
import yaml
from typing import Optional, Dict

from http import HTTPStatus
from flask import (
    Flask, jsonify, request, abort, url_for, Response
    )
from Chapter_12.card_model import Card, Deck

dealer = Flask("ch12_r04")
dealer.DEBUG = True
dealer.TESTING = True

# Following https://www.oasis-open.org
# http://docs.oasis-open.org/odata/odata/v4.0/odata-v4.0-part2-url-conventions.html
spec_yaml = """
openapi: 3.0.3
info:
  title: Python Cookbook Chapter 12, recipe 4.
  description: Parsing the URL path
  version: "1.0"
servers:
- url: http://127.0.0.1:5000/dealer
paths:
  /decks:
    post:
      operationId: make_deck
      parameters:
      - name: size
        in: query  # This is atypical for a post request.
        description: number of decks to build and shuffle
        schema:
          type: integer
          default: 1
      responses:
        "201":
          description: Create and shuffle a deck. Returns a unique deck id.
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    description: deck_id used for later queries
                    type: string
                  status:
                    description: response status
                    type: string
                    enum: ["ok", "problem"]
        "400":
          description: Request doesn't accept a JSON response or size invalid
          content: {}
  /decks/{id}:
    get:
      operationId: get_deck
      parameters:
      - $ref: "#/components/parameters/deck_id"
      responses:
        "200":
          description: the requested deck
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "#/components/schemas/Card"
        "400":
          description: Request doesn't accept a JSON response
          content: {}
        "404":
          description: ID not found.
          content: {}
  /decks/{id}/hands:
    get:
      operationId: get_hands
      parameters:
      - $ref: "#/components/parameters/deck_id"
      - name: cards
        in: query
        description: number of cards in each hand
        schema:
          type: integer
          default: 13
      - name: $top
        in: query
        description: number of hands to deal
        schema:
          type: integer
          default: 1
      - name: $skip
        in: query
        description: number of hands to skip before starting to deal
        schema:
          type: integer
          default: 0
      responses:
        "200":
          description: One hand of cards for each `hand` ID in the query string
          content:
            application/json:
              schema:
                type: object
                properties:
                  hand:
                    type: integer
                  cards:
                    type: array
                    items: 
                      $ref: "#/components/schemas/Card"
        "400":
          description: Request doesn't accept a JSON response
          content: {}
        "404":
          description: ID not found.
          content: {}
          
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
  parameters:
    deck_id:
      name: id
      in: path
      required: true
      description: Deck identification
      schema:
        type: string
"""
specification = yaml.load(spec_yaml, Loader=yaml.SafeLoader)


decks: Optional[Dict[str, Deck]] = None


def get_decks() -> Dict[str, Deck]:
    global decks
    if decks is None:
        random.seed(os.environ.get("DEAL_APP_SEED"))
        # Database connection might go here.
        decks = {}
    return decks


@dealer.before_request
def check_json() -> Optional[Response]:
    exceptions = {"/dealer/openapi.yaml", "/dealer/openapi.json"}
    if request.path in exceptions:
        return None
    if "json" in request.headers.get("Accept", "*/*"):
        return None
    if "json" == request.args.get("$format", "html"):
        return None
    return abort(HTTPStatus.BAD_REQUEST)


from flask import make_response
import json


@dealer.route("/dealer/openapi.json")
def openapi3_json() -> Response:
    response = make_response(
        json.dumps(specification, indent=2).encode("utf-8"))
    response.headers["Content-Type"] = "application/json"
    return response


@dealer.route("/dealer/openapi.yaml")
def openapi3_yaml() -> Response:
    response = make_response(yaml.dump(specification, indent=2).encode("utf-8"))
    response.headers["Content-Type"] = "application/yaml"
    return response


import urllib.parse
import uuid


@dealer.route("/dealer/decks", methods=["POST"])
def make_deck() -> Response:
    try:
        # More Typical to use request.get_json() in POST
        dealer.logger.info(f"make_deck {request.args}")
        n_decks = int(request.args.get("decks", 1))
        assert 1 <= n_decks
    except Exception as ex:
        abort(HTTPStatus.BAD_REQUEST)

    decks = get_decks()
    id = str(uuid.uuid1())
    decks[id] = Deck(n=n_decks)

    response_json = jsonify(status="ok", id=id)
    response = make_response(
        response_json, HTTPStatus.CREATED)
    response.headers["Location"] = url_for(
        "get_deck", id=id)
    return response


@dealer.route("/dealer/decks/<id>", methods=["GET"])
def get_deck(id: str) -> Response:
    decks = get_decks()
    if id not in decks:
        dealer.logger.error(id)
        dealer.logger.debug(list(decks.keys()))
        abort(HTTPStatus.BAD_REQUEST)
    response = jsonify([c.serialize() for c in decks[id].cards])
    return response


@dealer.route("/dealer/decks/<id>/hands", methods=["GET"])
def get_hands(id: str) -> Response:
    decks = get_decks()
    if id not in decks:
        dealer.logger.error(id)
        abort(
            HTTPStatus.NOT_FOUND,
            description=f"deck {id!r} not found")
    try:
        cards = int(request.args.get("cards", 13))
        top = int(request.args.get("$top", 1))
        skip = int(request.args.get("$skip", 0))
        assert (
            skip * cards + top * cards <= len(decks[id].cards)
        ), "$skip, $top, and cards larger than the deck"
    except (ValueError, AssertionError) as ex:
        dealer.logger.error(ex)
        abort(HTTPStatus.BAD_REQUEST)
    subset = decks[id].cards[
         skip * cards : skip * cards + top * cards]
    hands = [
        subset[h * cards : (h + 1) * cards]
        for h in range(top)]

    response = jsonify(
        [
            {
                "hand": i,
                "cards": [card.serialize() for card in hand]
            } for i, hand in enumerate(hands)
        ]
    )
    return response


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    dealer.run(use_reloader=True, threaded=False)
