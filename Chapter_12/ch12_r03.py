"""Python Cookbook

Chapter 12, recipe 3, Making REST requests with urllib.
"""

import urllib.request
import urllib.parse
import json
from typing import Dict, Any
from openapi_spec_validator import validate_spec  # type: ignore


def get_openapi_spec() -> Dict[str, Any]:
    """Is the OpenAPI specification valid?
    """
    with urllib.request.urlopen(
        "http://127.0.0.1:5000/dealer/openapi.json"
    ) as spec_request:
        openapi_spec = json.load(spec_request)
        validate_spec(openapi_spec)
    print("openapi.json is valid")
    return openapi_spec


def query_build_1() -> None:
    """Build and execute a query in pieces."""
    query = {"hand": 5}
    full_url = urllib.parse.ParseResult(
        scheme="http",
        netloc="127.0.0.1:5000",
        path="/dealer" + "/hand",
        params="",
        query=urllib.parse.urlencode(query),
        fragment="",
    )

    request2 = urllib.request.Request(
        url=urllib.parse.urlunparse(full_url),
        method="GET",
        headers={"Accept": "application/json",},
    )

    with urllib.request.urlopen(request2) as response:
        print(response.getcode())
        print(response.headers)
        print(json.loads(response.read().decode("utf-8")))


def query_build_2(openapi_spec: Dict[str, Any]) -> None:
    """Simpler alternative from OpenAPI Spec"""
    query = [("cards", 2), ("cards", 1), ("cards", 1), ("cards", 1)]
    query_text = urllib.parse.urlencode(query)
    request3 = urllib.request.Request(
        url=f"{openapi_spec['servers'][0]['url']}/hands?{query_text}",
        method="GET",
        headers={"Accept": "application/json",},
    )
    with urllib.request.urlopen(request3) as response:
        print(response.getcode())
        print(response.headers)
        print(json.loads(response.read().decode("utf-8")))


if __name__ == "__main__":
    print("Be sure the servar was started before running this.")
    print("For example, DEAL_APP_SEED=42 PYTHONPATH=. python Chapter_12/ch12_r02.py")
    spec = get_openapi_spec()
    query_build_1()
    query_build_2(spec)
