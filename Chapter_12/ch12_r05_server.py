"""Python Cookbook

Chapter 12, recipe 5, Parsing a JSON request
Server.
"""
import random
import logging
import os
import sys
from typing import Dict, Any, Optional
from http import HTTPStatus
from flask import Flask, jsonify, request, abort, url_for, Response
import yaml
from Chapter_12.card_model import Card, Deck

dealer = Flask("ch12_r05")
dealer.DEBUG = True
dealer.TESTING = True

# Following https://www.oasis-open.org
# http://docs.oasis-open.org/odata/odata/v4.0/odata-v4.0-part2-url-conventions.html
spec_yaml = """
openapi: 3.0.3
info:
  title: Python Cookbook Chapter 12, recipe 5.
  description: Parsing a JSON request
  version: "1.0"
servers:
- url: http://127.0.0.1:5000/dealer
paths:
  /decks:
    post:
      operationId: make_deck
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/decks'
      responses:
        "201":
          description: Create and shuffle a deck. Returns a unique deck id.
          headers: 
            Location: 
              schema: 
                type: string
                format: uri
              description: URL for new deck
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
          description: Request doesn't accept a JSON response or request invalid
          content: {}
          
  /decks/{id}/$count:
    get:
      operationId: get_deck_size
      parameters:
      - $ref: "#/components/parameters/deck_id"
      responses:
        "200":
          description: Summary of the deck size
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: string
                  cards:
                    type: integer
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
          
  /players:
    post:
      operationId: make_player
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Player'
      responses:
        "201":
          description: Player created
          content:
            application/json:
              schema:
                type: object
                properties:
                  player:
                    $ref: "#/components/schemas/Player"
                  id:
                    type:
                        string
        "403":
          description: Player is invalid or a duplicate
          content: {}
          
    get:
      operationId: get_all_players
      responses:
        "200":
          description: One hand of cards for each `hand` ID in the query string
          content:
            application/json:
              schema:
                type: object
                properties:
                  players:
                    type: array
                    items: 
                      $ref: "#/components/schemas/Player"

  /players/{id}:
    get:
      operationId: get_one_player
      parameters:
      - $ref: "#/components/parameters/player_id"
      responses:
        "200":
          description: The details of a specific player
          content:
            application/json:
              schema:
                type: object
                properties:
                  player:
                    $ref: '#/components/schemas/Player'
                example:
                  player:
                    email: example@example.com
                    name: example
                    twitter: https://twitter.com/PacktPub
                    lucky_number: 13
        "404":
          description: Player ID not found
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
    decks:
      description: Number of decks to build and deal
      type: integer
      minimum: 1
      maximum: 20
    Player:
      type: object
      properties:
        email:
          type: string
          format: email
        name:
          type: string
        twitter:
          type: string
          format: uri
        lucky_number:
          type: integer
  parameters:
    deck_id:
      name: id
      in: path
      required: true
      description: Deck identification
      schema:
        type: string
    player_id:
      name: id
      in: path
      required: true
      description: Player identification
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


JSON_Doc = Dict[str, Any]
players: Optional[Dict[str, JSON_Doc]] = None


def get_players() -> Dict[str, JSON_Doc]:
    global players
    if players is None:
        # Database connection might go here.
        players = {}
    return players


@dealer.before_request
def check_json() -> Optional[Response]:
    if request.path == "/dealer/openapi.json":
        return None
    if "json" in request.headers.get("Accept", "*/*"):
        return None
    if "json" == request.args.get("$format", "html"):
        return None
    return abort(HTTPStatus.BAD_REQUEST)


from flask import make_response
import json


@dealer.route("/dealer/openapi.json")
def openapi3() -> Response:
    response = make_response(json.dumps(specification, indent=2).encode("utf-8"))
    response.headers["Content-Type"] = "application/json"
    return response

# This can be used to show what a bad OpenAPI specification looks like.
# @dealer.route("/dealer/openapi.json")
# def openapi3x() -> Response:
#     response = make_response(json.dumps({"um": "nope"}, indent=2).encode("utf-8"))
#     response.headers["Content-Type"] = "application/json"
#     return response


from jsonschema import validate  # type: ignore
from jsonschema.exceptions import ValidationError  # type: ignore
import hashlib


@dealer.route("/dealer/players", methods=["POST"])
def make_player() -> Response:
    try:
        document = request.get_json()
    except Exception as ex:
        # Document wasn't proper JSON.
        # We can fine-tune an error message here.
        abort(HTTPStatus.BAD_REQUEST)
    player_schema = (
        specification["components"]["schemas"]["Player"]
    )
    try:
        validate(document, player_schema)
    except ValidationError as ex:
        abort(HTTPStatus.BAD_REQUEST, description=ex.message)

    players = get_players()
    id = hashlib.md5(document["twitter"].encode("utf-8")).hexdigest()
    if id in players:
        abort(HTTPStatus.BAD_REQUEST, description="Duplicate player")

    players[id] = document
    response = make_response(jsonify(player=document, id=id), HTTPStatus.CREATED)
    response.headers["Location"] = url_for("get_one_player", id=str(id))
    response.headers["Content-Type"] = "application/json;charset=utf-8"
    return response


@dealer.route("/dealer/players", methods=["GET"])
def get_all_players() -> Response:
    players = get_players()
    response = make_response(jsonify(players=players))
    response.headers["Content-Type"] = "application/json;charset=utf-8"
    return response


@dealer.route("/dealer/players/<id>", methods=["GET"])
def get_one_player(id: str) -> Response:
    players = get_players()
    if id not in players:
        abort(HTTPStatus.NOT_FOUND, description=f"Player {id} not found")

    response = make_response(jsonify(player=players[id]))
    response.headers["Content-Type"] = "application/json;charset=utf-8"
    return response


import urllib.parse
import uuid


@dealer.route("/dealer/decks", methods=["POST"])
def make_deck() -> Response:
    try:
        n_decks = request.get_json()["decks"]
        dealer.logger.info(f"make_deck {request.args}")
    except Exception as ex:
        abort(HTTPStatus.BAD_REQUEST)

    decks = get_decks()
    id = str(uuid.uuid1())
    decks[id] = Deck(n=n_decks)

    response_json = jsonify(status="ok", id=id)
    response = make_response(
        response_json, HTTPStatus.CREATED)
    response.headers["Location"] = url_for(
        "get_one_deck_count", id=str(id))
    response.headers["Content-Type"] = "application/json;charset=utf-8"
    return response


@dealer.route("/deaker/decks/<id>/$count", methods=["GET"])
def get_one_deck_count(id: str) -> Response:
    decks = get_decks()
    if id not in decks:
        dealer.logger.debug(id)
        dealer.logger.debug(list(decks.keys()))
        abort(HTTPStatus.NOT_FOUND)
    response = jsonify(id=id, cards=len(decks[id]))
    return response


@dealer.route("/dealer/decks/<id>/hands", methods=["GET"])
def get_hands(id: str) -> Response:
    decks = get_decks()
    if id not in decks:
        dealer.logger.debug(id)
        abort(HTTPStatus.NOT_FOUND, description="Deck {id} not found")
    try:
        cards = int(request.args.get("cards", 13))
        top = int(request.args.get("$top", 1))
        skip = int(request.args.get("$skip", 0))
        assert skip * cards + top * cards <= len(
            decks[id].cards
        ), "$skip, $top, and cards larger than the deck"
    except ValueError as ex:
        abort(HTTPStatus.BAD_REQUEST)
    subset = decks[id].cards[skip * cards : (skip + top) * cards]
    hands = [subset[h * cards : (h + 1) * cards] for h in range(top)]
    response = jsonify(
        [
            {"hand": i, "cards": [card.serialize() for card in hand]}
            for i, hand in enumerate(hands)
        ]
    )
    response.headers["Content-Type"] = "application/json;charset=utf-8"
    return response


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    dealer.run(use_reloader=True, threaded=False)
