"""Python Cookbook

Chapter 12, recipe 4, Parsing the URL path
Client.
"""

from pprint import pprint
import urllib.request
import urllib.parse
import urllib.error
import json
from openapi_spec_validator import validate_spec  # type: ignore
from typing import Dict, List, Any, Union, Tuple

# General definition:
# ResponseDoc = Union[Dict[str, Any], List[Any], int, float, str, None]
# This is a bit too general for Mypy's purposes here.

# A type for the OpenAPI Spec
ResponseDoc = Dict[str, Any]


def get_openapi_spec() -> ResponseDoc:
    """Get the OpenAPI specification."""

    openapi_request = urllib.request.Request(
        url="http://127.0.0.1:5000/dealer/openapi.json",
        method="GET",
        headers={"Accept": "application/json",},
    )

    with urllib.request.urlopen(openapi_request) as response:
        assert (
            response.getcode() == 200
        ), f"Error getting OpenAPI Spec: {response.status!r}"
        openapi_spec = json.loads(response.read().decode("utf-8"))
    validate_spec(openapi_spec)
    assert (
        openapi_spec["info"]["title"] == "Python Cookbook Chapter 12, recipe 4."
    ), f"Unepxected Server {openapi_spec['info']['title']}"
    assert (
        openapi_spec["info"]["version"] == "1.0"
    ), f"Unepxected Server Version {openapi_spec['info']['version']}"
    pprint(openapi_spec)

    return openapi_spec

PATH_CACHE = None

def find_path_op(openapi_spec: ResponseDoc, target: str) -> Tuple[str, str]:
    global PATH_CACHE
    if PATH_CACHE is None:
        PATH_CACHE = {
            openapi_spec["paths"][path][operation]["operationId"]: (path, operation)
            for path in openapi_spec["paths"]
                for operation in openapi_spec["paths"][path]
                    if "operationId" in openapi_spec["paths"][path][operation]
        }
    return PATH_CACHE[target]


def create_new_deck(openapi_spec: ResponseDoc, size: int = 6) -> Dict[str, Any]:
    """Post to create a deck."""
    query = {"size": size}
    path, operation = find_path_op(openapi_spec, "make_deck")
    base_url = openapi_spec["servers"][0]["url"]
    query_text = urllib.parse.urlencode(query)
    full_url = f"{base_url}{path}?{query_text}"

    request = urllib.request.Request(
        url=full_url, method="POST", headers={"Accept": "application/json",}
    )

    try:
        with urllib.request.urlopen(request) as response:
            # print(response.status)
            assert response.getcode() == 201, f"Error Creating Deck: {response.status}"
            print(response.headers)
            document = json.loads(response.read().decode("utf-8"))

        assert document["status"] == "ok"
        return document
    except urllib.error.HTTPError as ex:
        print("ERROR: ex")
        print(ex.read())
        raise


def no_spec_create_new_deck(size: int = 6) -> Dict[str, Any]:
    """Post to create a deck."""
    query = {"size": size}
    full_url = urllib.parse.urlunparse(
        urllib.parse.ParseResult(
            scheme="http",
            netloc="127.0.0.1:5000",
            path="/dealer" + "/decks",
            params="",
            query=urllib.parse.urlencode({"size": size}),
            fragment=""
        )
    )

    request = urllib.request.Request(
        url=full_url,
        method="POST",
        headers={"Accept": "application/json",}
    )

    try:
        with urllib.request.urlopen(request) as response:
            # print(response.status)
            assert (
                response.getcode() == 201
            ), f"Error Creating Deck: {response.status}"
            document = json.loads(
                response.read().decode("utf-8"))

        assert document["status"] == "ok"
        return document
    except urllib.error.HTTPError as ex:
        print("ERROR: ex")
        print(ex.read())
        raise


def get_new_deck(openapi_spec: ResponseDoc, id: str) -> Dict[str, Any]:
    """GET to confirm the deck was created; a debugging request."""

    pattern_path, operation = find_path_op(openapi_spec, "get_deck")
    base_url = openapi_spec["servers"][0]["url"]
    instance_path = pattern_path.replace("{id}", id)
    full_url = f"{base_url}{instance_path}"

    request = urllib.request.Request(
        url=(full_url), method="GET", headers={"Accept": "application/json",}
    )

    with urllib.request.urlopen(request) as response:
        assert response.getcode() == 200, f"Error Fetching Deck: {response.status}"
        deck = json.loads(response.read().decode("utf-8"))
    return deck


def no_spec_get_new_deck(id: str) -> Dict[str, Any]:
    """GET to confirm the deck was created; a debugging request."""
    full_url = urllib.parse.urlunparse(
        urllib.parse.ParseResult(
            scheme="http",
            netloc="127.0.0.1:5000",
            path="/dealer" + f"/decks/{id}",
            params="",
            query="",
            fragment=""
        )
    )

    request = urllib.request.Request(
        url=(full_url), method="GET", headers={"Accept": "application/json",}
    )

    with urllib.request.urlopen(request) as response:
        assert response.getcode() == 200, f"Error Fetching Deck: {response.status}"
        deck = json.loads(response.read().decode("utf-8"))
    return deck


def get_hands(
    openapi_spec: ResponseDoc, id: str, cards: int = 13, limit: int = 4
) -> Dict[str, Any]:
    """GET to see some Hands."""

    query = {"$top": limit, "cards": cards}

    pattern_path, operation = find_path_op(openapi_spec, "get_hands")
    base_url = openapi_spec["servers"][0]["url"]
    instance_path = pattern_path.replace("{id}", id)
    query_text = urllib.parse.urlencode(query)
    full_url = f"{base_url}{instance_path}?{query_text}"

    request = urllib.request.Request(
        url=full_url, method="GET", headers={"Accept": "application/json",}
    )

    with urllib.request.urlopen(request) as response:
        assert response.getcode() == 200, f"Error Fetching Hand: {response.status}"
        hands = json.loads(response.read().decode("utf-8"))
    return hands



def no_spec_get_hands(
        id: str,
        cards: int = 13,
        limit: int = 4
) -> Dict[str, Any]:
    """GET to see some Hands."""

    query = {"$top": limit, "cards": cards}

    full_url = urllib.parse.urlunparse(
        urllib.parse.ParseResult(
            scheme="http",
            netloc="127.0.0.1:5000",
            path="/dealer" + f"/decks/{id}/hands",
            params="",
            query=urllib.parse.urlencode(query),
            fragment=""
        )
    )

    request = urllib.request.Request(
        url=full_url,
        method="GET",
        headers={"Accept": "application/json",}
    )

    with urllib.request.urlopen(request) as response:
        assert (
            response.getcode() == 200
        ), f"Error Fetching Hand: {response.status}"
        hands = json.loads(
            response.read().decode("utf-8"))
    return hands

def main_no_spec():
    create_doc = no_spec_create_new_deck(6)
    print(create_doc)
    id = create_doc["id"]
    deck_info = no_spec_get_new_deck(id)
    # print(deck_info)
    hands = no_spec_get_hands(id, cards=6, limit=2)
    for hand in hands:
        print(f"Hand {hand['hand']}")
        pprint(hand['cards'])
        print()

def main():
    spec = get_openapi_spec()
    create_doc = create_new_deck(spec, 6)
    print(create_doc)
    id = create_doc["id"]
    deck_info = get_new_deck(spec, id)
    # print(deck_info)
    hands = get_hands(spec, id, cards=6, limit=2)
    pprint(hands)


if __name__ == "__main__":
    main()
    main_no_spec()
