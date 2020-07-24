"""Python Cookbook

Chapter 12, recipe 6, Implementing authentication for web services
Server.

Important.

This requires ``demo.cert`` and ``demo.key`` in the local working directory.
"""
import logging
import random
import os
import sys
from typing import Dict, Optional, Any, Callable, Union

from http import HTTPStatus
from flask import Flask, jsonify, request, abort, url_for, Response
import yaml
from Chapter_12.ch12_r06_user import User, asdict
from Chapter_12.card_model import Card, Deck


dealer = Flask("ch12_r07")
dealer.DEBUG = True
dealer.TESTING = True
dealer.logger.setLevel(logging.INFO)

# Following https://www.oasis-open.org
# http://docs.oasis-open.org/odata/odata/v4.0/odata-v4.0-part2-url-conventions.html

spec_yaml = """
openapi: 3.0.3
info:
  title: Python Cookbook Chapter 12, recipe 6.
  version: "1.0"
servers:
- url: https://127.0.0.1:5000/dealer
paths:
  /decks:
    post:
      operationId: make_deck
      security: 
      - http: []
      parameters:
      - name: size
        in: query
        description: number of decks to build and shuffle
        schema:
          type: integer
          default: 1
      responses:
        "200":
          description: Create and shuffle a deck. Returns a unique deck id.
          content: {}
        "400":
          description: Request doesn't accept a JSON response
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
      security: 
      - http: []
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
          description: One hand of cards for each `hand` value in the query string
          content: {}
        "400":
          description: Request doesn't accept a JSON response
          content: {}
        "404":
          description: ID not found.
          content: {}
  /players:
    get:
      operationId: get_all_players
      security: 
      - http: []
      responses:
        "200":
          description: All of the players defined so far
          content: {}
    post:
      operationId: make_player
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Player'
        required: false
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
  /players/{id}:
    get:
      operationId: get_one_player
      security: 
      - http: []
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
  securitySchemes:
    http:
      type: http
      scheme: basic
  schemas:
    Player:
      type: object
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
        password:
          type: string
          minLength: 8
          description: plain password on a request. Hash on a response.
        twitter:
          type: string
          format: uri
        lucky_number:
          type: integer
          minimum: 0
          maximum: 99
      required:
      - email
      - name
      - twitter
      - lucky_number
      - password
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

JSON_Doc = Dict[str, Any]

decks: Optional[Dict[str, Deck]] = None


def get_decks() -> Dict[str, Deck]:
    global decks
    if decks is None:
        random.seed(os.environ.get("DEAL_APP_SEED"))
        decks = {}
    return decks


user_database: Optional[Dict[str, User]] = None


def get_users() -> Dict[str, User]:
    global user_database
    if user_database is None:
        user_database = {}
    return user_database


# Errors come from abort
# HTTPStatus.UNAUTHORIZED, HTTPStatus.BAD_REQUEST, and HTTPStatus.NOT_FOUND, HTTPStatus.FORBIDDEN
# We can create more useful JSON documents
@dealer.errorhandler(HTTPStatus.UNAUTHORIZED)
def unuathorized_error(ex):
    return jsonify(
        error=str(ex)
    ), HTTPStatus.UNAUTHORIZED

@dealer.errorhandler(HTTPStatus.BAD_REQUEST)
def bad_request_error(ex):
    return jsonify(
        error=str(ex)
    ), HTTPStatus.BAD_REQUEST

@dealer.errorhandler(HTTPStatus.FORBIDDEN)
def forbidden_error(ex):
    return jsonify(
        error=str(ex)
    ), HTTPStatus.FORBIDDEN


from functools import wraps
import base64
from flask import g

ViewFunction = Union[Callable[[Any], Response], Callable[[], Response]]


DEFAULT_USER = User(name="", email="", twitter="", lucky_number=-1)



def authorization_required(view_function: ViewFunction) -> ViewFunction:
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        # If no Authorization header, provide a default which fails
        header_value = request.headers.get("Authorization", "BASIC :")
        kind, data = header_value.split()
        # If not BASIC, provide a username:password which will (eventually) fail
        if kind.upper() == "BASIC":
            credentials = base64.b64decode(data)
        else:
            credentials = base64.b64decode("Og==")
        usr_bytes, _, pwd_bytes = credentials.partition(b":")
        username = usr_bytes.decode("ascii")
        password = pwd_bytes.decode("ascii")
        user_database = get_users()
        user = user_database.get(username, DEFAULT_USER)
        if not user.check_password(password):
            abort(
                HTTPStatus.UNAUTHORIZED,
                description="Invalid credentials")
        g.user = user_database[username]
        return view_function(*args, **kwargs)

    return decorated_function


@dealer.before_request
def check_json() -> Optional[Response]:
    if request.path == "/dealer/openapi.json":
        return None
    if "json" in request.headers.get("Accept", "*/*"):
        return None
    if "json" == request.args.get("$format", "html"):
        return None
    abort(
        HTTPStatus.BAD_REQUEST,
        description="Invalid Accept header or $format query"
    )

from flask import make_response
import json


@dealer.route("/dealer/openapi.json")
def openapi3() -> Response:
    response = make_response(json.dumps(specification, indent=2).encode("utf-8"))
    response.headers["Content-Type"] = "application/json"
    return response


def redacted_asdict(user: User) -> Dict[str, Any]:
    """Build the dict of a User, but redact 'password'."""
    document = asdict(user)
    document.pop("password", None)
    return document


from jsonschema import validate  # type: ignore
from jsonschema.exceptions import ValidationError  # type: ignore
import hashlib


@dealer.route("/dealer/players", methods=["POST"])
def make_player() -> Response:
    try:
        document = request.json
    except Exception as ex:
        # Document wasn't even JSON.
        # We can fine-tune the error message here.
        abort(
            HTTPStatus.BAD_REQUEST,
            description=ex
        )
    player_schema = specification["components"]["schemas"]["Player"]
    try:
        validate(document, player_schema)
    except ValidationError as ex:
        abort(HTTPStatus.BAD_REQUEST, description=ex.message)

    user_database = get_users()
    id = hashlib.md5(
        document["twitter"].encode("utf-8")).hexdigest()
    if id in user_database:
        abort(HTTPStatus.FORBIDDEN, description="Duplicate player")

    password = document.pop('password')
    new_user = User(**document)
    new_user.set_password(password)
    user_database[id] = new_user

    response = make_response(
        jsonify(
            player=redacted_asdict(new_user),
            id=id),
        HTTPStatus.CREATED
    )
    response.headers["Location"] = url_for("get_player", id=str(id))
    return response


@dealer.route("/dealer/players", methods=["GET"])
@authorization_required
def get_players() -> Response:
    user_database = get_users()
    response = make_response(
        jsonify(
            players={
                k: redacted_asdict(v)
                for k, v in user_database.items()}
        )
    )
    response.headers["Content-Type"] = "application/json;charset=utf-8"
    return response


@dealer.route("/dealer/players/<id>", methods=["GET"])
@authorization_required
def get_player(id) -> Response:
    user_database = get_users()
    if id not in user_database:
        abort(
            HTTPStatus.NOT_FOUND,
            description=f"{id} not found"
        )

    response = make_response(
        jsonify(
            player=redacted_asdict(user_database[id])
        )
    )
    response.headers["Content-Type"] = "application/json"
    return response


import urllib.parse
import uuid


@dealer.route("/dealer/decks", methods=["POST"])
@authorization_required
def make_deck() -> Response:
    try:
        n_decks = request.get_json()["decks"]
        dealer.logger.info(f"make_deck {request.args}")
    except Exception as ex:
        abort(
            HTTPStatus.BAD_REQUEST,
            description=ex
        )

    decks = get_decks()
    id = str(uuid.uuid1())
    decks[id] = Deck(n=n_decks)
    response_json = jsonify(status="ok", id=id)
    response = make_response(response_json, HTTPStatus.CREATED)
    response.headers["Location"] = url_for("get_one_deck_count", id=str(id))
    response.headers["Content-Type"] = "application/json;charset=utf-8"
    return response


@dealer.route("/dealer/decks/<id>/$count", methods=["GET"])
@authorization_required
def get_one_deck_count(id) -> Response:
    decks = get_decks()
    if id not in decks:
        dealer.logger.debug(id)
        dealer.logger.debug(list(decks.keys()))
        abort(
            HTTPStatus.NOT_FOUND,
            description=f"Unknown /dealer/decks/{id}"
        )
    response = jsonify(id=id, cards=len(decks[id].cards))
    return response


from werkzeug.exceptions import BadRequest


@dealer.route("/dealer/decks/<id>/hands", methods=["GET"])
@authorization_required
def get_hands(id) -> Response:
    decks = get_decks()
    if id not in decks:
        dealer.logger.debug(id)
        abort(HTTPStatus.NOT_FOUND, description=f"ID {id} not found")
    try:
        cards = int(request.args.get("cards", 13))
        top = int(request.args.get("$top", 1))
        skip = int(request.args.get("$skip", 0))
        assert skip * cards + top * cards <= len(
            decks[id].cards
        ), "$skip, $top, and cards larger than the deck"
    except ValueError as ex:
        abort(HTTPStatus.BAD_REQUEST, description=ex)
    subset = decks[id].cards[skip * cards : (skip + top) * cards]
    hands = [subset[h * cards : (h + 1) * cards] for h in range(top)]
    response = jsonify(
        [
            {"hand": i, "cards": [card.serialize() for card in hand]}
            for i, hand in enumerate(hands)
        ]
    )
    return response


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    import ssl

    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ctx.load_cert_chain("demo.cert", "demo.key")
    dealer.run(use_reloader=True, threaded=False, ssl_context=ctx)
