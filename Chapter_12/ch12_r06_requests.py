"""Python Cookbook

Chapter 12, recipe 6, Implementing authentication for web services
Client, using requests.

This requires ``demo.cert`` and ``demo.key`` in the local working directory.

"""
from pprint import pprint
from typing import Dict, List, Any, Union, Tuple

import requests
from openapi_spec_validator import validate_spec  # type: ignore

OpenAPISpec = Dict[str, Any]

ResponseDoc = Dict[str, Any]

def get_openapi_spec() -> OpenAPISpec:
    response = requests.get(
        url="https://127.0.0.1:5000/dealer/openapi.json",
        headers={"Accept": "application/json",},
        verify="demo.cert",  # or use the demo.cert
    )
    assert response.status_code == 200
    openapi_spec = response.json()

    validate_spec(openapi_spec)
    assert (
        openapi_spec["info"]["title"] == "Python Cookbook Chapter 12, recipe 6."
    ), f"Unepxected Server {openapi_spec['info']['title']}"
    assert (
        openapi_spec["info"]["version"] == "1.0"
    ), f"Unepxected Server Version {openapi_spec['info']['version']}"
    pprint(openapi_spec)

    return openapi_spec

Path_Map = Dict[str, Tuple[str, str]]


def make_path_map(openapi_spec: OpenAPISpec) -> Path_Map:
    """Mapping from operationId values to path and operation."""
    operation_ids = {
        openapi_spec["paths"][path][operation]["operationId"]: (path, operation)
        for path in openapi_spec["paths"]
        for operation in openapi_spec["paths"][path]
        if "operationId" in openapi_spec["paths"][path][operation]
    }
    return operation_ids

def create_new_player(
        openapi_spec: OpenAPISpec,
        path_map: Path_Map,
        document: Dict[str, Any]
    ) -> ResponseDoc:
    """Post to create a player."""

    path, operation = path_map["make_player"]
    base_url = openapi_spec["servers"][0]["url"]
    full_url = f"{base_url}{path}"

    response = requests.post(
        url=full_url,
        headers={
            "Accept": "application/json",
        },
        json=document,
        verify="demo.cert"
    )

    assert (
        response.status_code == 201
    ), f"Error {response.status_code}: {response.text}"
    document = response.json()
    assert "id" in document
    return document


def get_one_player(
        openapi_spec: ResponseDoc,
        path_map: Path_Map,
        credentials: Tuple[str, str],
        player_id: str,
    ) -> ResponseDoc:
    """GET to see a specific player."""

    path_template, operation = path_map["get_one_player"]
    base_url = openapi_spec["servers"][0]["url"]
    path_instance = path_template.replace("{id}", player_id)
    full_url = f"{base_url}{path_instance}"

    response = requests.get(
        url=full_url,
        headers={"Accept": "application/json"},
        auth=credentials,
        verify="demo.cert"
    )

    assert response.status_code == 200
    # print(response.headers)
    player_response = response.json()
    return player_response["player"]


def get_all_players(
        openapi_spec: ResponseDoc,
        path_map: Path_Map,
        credentials: Tuple[str, str]
) -> List[ResponseDoc]:
    """GET to see the players."""

    path, operation = path_map["get_all_players"]
    base_url = openapi_spec["servers"][0]["url"]
    full_url = f"{base_url}{path}"

    response = requests.get(
        url=full_url,
        headers={"Accept": "application/json"},
        auth=credentials,
        verify="demo.cert"
    )

    assert response.status_code == 200
    print(response.headers)
    players_response = response.json()
    return players_response


def main():
    spec = get_openapi_spec()
    paths = make_path_map(spec)

    player = {
        "name": "Noriko",
        "email": "nori@example.com",
        "lucky_number": 7,
        "twitter": "https://twitter.com/PacktPub",
        "password": "OpenSesame",
    }

    create_doc = create_new_player(spec, paths, player)
    id = create_doc["id"]

    credentials = (id, "OpenSesame")
    get_one_player(spec, paths, credentials, id)

    players = get_all_players(spec, paths, credentials)
    pprint(players)


if __name__ == "__main__":
    main()
