"""Python Cookbook

Chapter 12, recipe 5, Parsing a JSON request
Client.
"""

from dataclasses import dataclass
from pprint import pprint
import urllib.request
import urllib.parse
import json
from openapi_spec_validator import validate_spec  # type: ignore
from typing import Dict, List, Any, Union, Tuple

# General definition:
# ResponseDoc = Union[Dict[str, Any], List[Any], int, float, str, None]
# This is a bit too general for Mypy's purposes here.

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
        ), f"Error getting OpenAPI Spec: {response.getcode()!r}"
        openapi_spec = json.loads(response.read().decode("utf-8"))
    validate_spec(openapi_spec)
    assert (
        openapi_spec["info"]["title"] == "Python Cookbook Chapter 12, recipe 5."
    ), f"Unepxected Server {openapi_spec['info']['title']}"
    assert (
        openapi_spec["info"]["version"] == "1.0"
    ), f"Unepxected Server Version {openapi_spec['info']['version']}"
    pprint(openapi_spec)

    return openapi_spec


Path_Map = Dict[str, Tuple[str, str]]


def make_path_map(openapi_spec: ResponseDoc) -> Path_Map:
    operation_ids = {
        openapi_spec["paths"][path][operation]["operationId"]: (path, operation)
        for path in openapi_spec["paths"]
        for operation in openapi_spec["paths"][path]
        if (
            "operationId" in openapi_spec["paths"][path][operation]
        )
    }
    return operation_ids


@dataclass
class Player:
    player_name: str
    email_address: str
    other_field: int
    handle: str


def create_new_player(
        openapi_spec: ResponseDoc,
        path_map: Path_Map,
        input_form: Player) -> ResponseDoc:
    """Post to create a player."""

    path, operation = path_map["make_player"]
    base_url = openapi_spec["servers"][0]["url"]
    full_url = f"{base_url}{path}"

    document = {
        "name": input_form.player_name,
        "email": input_form.email_address,
        "lucky_number": input_form.other_field,
        "twitter": input_form.handle,
    }

    request = urllib.request.Request(
        url=full_url,
        method="POST",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json;charset=utf-8",
        },
        data=json.dumps(document).encode("utf-8"),
    )

    try:
        with urllib.request.urlopen(request) as response:
            # print(response.getcode())
            assert (
                response.getcode() == 201
            ), f"Error {response.getcode()}: {response.text}"
            print(response.headers)
            document = json.loads(response.read().decode("utf-8"))

        print(document)
        return document
    except urllib.error.HTTPError as ex:
        print(ex.getcode())
        print(ex.headers)
        print(ex.read())
        raise


def get_all_players(openapi_spec: ResponseDoc, path_map: Path_Map) -> List[ResponseDoc]:
    """GET to see the players."""

    path, operation = path_map["get_all_players"]
    base_url = openapi_spec["servers"][0]["url"]
    full_url = f"{base_url}{path}"

    request = urllib.request.Request(
        url=full_url, method="GET", headers={"Accept": "application/json",}
    )

    with urllib.request.urlopen(request) as response:
        assert response.getcode() == 200
        # print(response.headers)
        players = json.loads(response.read().decode("utf-8"))
    return players


def get_one_player(
    openapi_spec: ResponseDoc, path_map: Path_Map, player_id: str
) -> ResponseDoc:
    """GET to see a specific player."""

    path_template, operation = path_map["get_one_player"]
    base_url = openapi_spec["servers"][0]["url"]
    path_instance = path_template.replace("{id}", player_id)
    full_url = f"{base_url}{path_instance}"

    request = urllib.request.Request(
        url=full_url, method="GET", headers={"Accept": "application/json",}
    )

    from urllib.error import HTTPError

    try:
        with urllib.request.urlopen(request) as response:
            print(response.getcode())
            print(response.headers)
            player_response = json.loads(response.read().decode("utf-8"))
        return player_response["player"]
    except HTTPError as ex:
        print(ex.getcode())
        print(ex.read())
        raise


def main():
    spec = get_openapi_spec()
    paths = make_path_map(spec)
    input_form = Player(
        player_name="Noriko",
        email_address="nori@example.com",
        other_field=7,
        handle="https://twitter.com/PacktPub",
    )
    create_doc = create_new_player(spec, paths, input_form)
    id = create_doc["id"]
    get_one_player(spec, paths, id)
    players = get_all_players(spec, paths)
    print(players)


if __name__ == "__main__":
    main()
