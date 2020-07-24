"""Python Cookbook

Chapter 12, recipe 6, Implementing authentication for web services
Client, using urllib.

This requires ``demo.cert`` and ``demo.key`` in the local working directory.

"""

import base64
import json
from pprint import pprint
from typing import Dict, List, Any, Union, Tuple
import urllib.request
import urllib.parse
import ssl

from openapi_spec_validator import validate_spec  # type: ignore

# General definition:
# ResponseDoc = Union[Dict[str, Any], List[Any], int, float, str, None]
# This is a bit too general for Mypy's purposes here.

ResponseDoc = Dict[str, Any]



def get_openapi_spec(opener: urllib.request.OpenerDirector) -> ResponseDoc:
    """Get the OpenAPI specification."""

    openapi_request = urllib.request.Request(
        url="https://127.0.0.1:5000/dealer/openapi.json",
        method="GET",
        headers={"Accept": "application/json",},
    )

    with opener.open(openapi_request) as response:
        assert (
            response.getcode() == 200
        ), f"Error getting OpenAPI Spec: {response.getcode()!r}"
        openapi_spec = json.loads(response.read().decode("utf-8"))
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


def make_path_map(openapi_spec: ResponseDoc) -> Path_Map:
    """Mapping from operationId values to path and operation."""
    operation_ids = {
        openapi_spec["paths"][path][operation]["operationId"]: (path, operation)
        for path in openapi_spec["paths"]
        for operation in openapi_spec["paths"][path]
        if "operationId" in openapi_spec["paths"][path][operation]
    }
    return operation_ids


def create_new_player(
        opener: urllib.request.OpenerDirector,
        openapi_spec: ResponseDoc,
        path_map: Path_Map,
        document: Dict[str, Any]
    ) -> ResponseDoc:
    """Post to create a player."""

    path, operation = path_map["make_player"]
    base_url = openapi_spec["servers"][0]["url"]
    full_url = f"{base_url}{path}"

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
        with opener.open(request) as response:
            # print(response.getcode())
            assert (
                response.getcode() == 201
            ), f"Error {response.getcode()}: {response.text}"
            print(response.headers)
            document = json.loads(response.read().decode("utf-8"))

        print(document)
        assert "id" in document
        return document
    except urllib.error.HTTPError as ex:
        print(ex.getcode())
        print(ex.headers)
        print(ex.read())
        raise


def get_all_players(
        opener: urllib.request.OpenerDirector,
        openapi_spec: ResponseDoc,
        path_map: Path_Map,
        credentials: Tuple[str, str]
) -> List[ResponseDoc]:
    """GET to see the players."""

    path, operation = path_map["get_all_players"]
    base_url = openapi_spec["servers"][0]["url"]
    full_url = f"{base_url}{path}"

    b64credentials = base64.b64encode(
        f"{credentials[0]}:{credentials[1]}".encode("utf-8")
    )
    request = urllib.request.Request(
        url=full_url,
        method="GET",
        headers={
            "Accept": "application/json",
            "Authorization": f"BASIC {b64credentials.decode('ascii')}",
        },
    )

    with opener.open(request) as response:
        assert response.getcode() == 200
        # print(response.headers)
        players = json.loads(response.read().decode("utf-8"))
    return players


def get_one_player(
        opener: urllib.request.OpenerDirector,
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

    b64credentials = base64.b64encode(
        f"{credentials[0]}:{credentials[1]}".encode("utf-8")
    )
    request = urllib.request.Request(
        url=full_url,
        method="GET",
        headers={
            "Accept": "application/json",
            "Authorization": f"BASIC {b64credentials.decode('ascii')}",
        },
    )

    from urllib.error import HTTPError

    try:
        with opener.open(request) as response:
            print(response.getcode())
            print(response.headers)
            player_response = json.loads(response.read().decode("utf-8"))
        return player_response["player"]
    except HTTPError as ex:
        print(ex.getcode())
        print(ex.read())
        raise


def main():
    # SSL client setup.
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    opener = urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=context)
    )

    spec = get_openapi_spec(opener)
    paths = make_path_map(spec)

    player = {
        "name": "Noriko",
        "email": "nori@example.com",
        "lucky_number": 7,
        "twitter": "https://twitter.com/PacktPub",
        "password": "OpenSesame",
    }

    create_doc = create_new_player(opener, spec, paths, player)
    id = create_doc["id"]
    credentials = (id, "OpenSesame")
    get_one_player(opener, spec, paths, credentials, id)
    players = get_all_players(opener, spec, paths, credentials)
    print(players)


if __name__ == "__main__":
    main()
