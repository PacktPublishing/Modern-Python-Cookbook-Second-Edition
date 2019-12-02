"""Python Cookbook

Chapter 12, recipe 4.
"""

import urllib.request
import urllib.parse
import json
from typing import Dict, Any
from openapi_spec_validator import validate_spec  # type: ignore


def get_openapi_spec() -> Dict[str, Any]:
    """Step 1 -- is the OpenAPI specification valid?
    """
    with urllib.request.urlopen(
        "http://127.0.0.1:5000/dealer/openapi.json"
    ) as spec_request:
        openapi_spec = json.load(spec_request)
        validate_spec(openapi_spec)
    print("openapi.json is valid")
    return openapi_spec


def query_build_1(openapi_spec: Dict[str, Any]) -> None:
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
    """Simpler alternative wth more assumptions"""
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


__test__ = {
    "example": """
Start the server
>>> import subprocess, time, os, pathlib
>>> env = os.environ.copy()
>>> env['PYTHONPATH'] = str(pathlib.Path(__file__).parent.parent)
>>> env['DEAL_APP_SEED'] = '42'
>>> server = subprocess.Popen(["python", "Chapter_12/ch12_r03.py"], env=env)
>>> time.sleep(0.5)

Make the client request
>>> spec = get_openapi_spec()
openapi.json is valid
>>> spec['info']['title']
'Python Cookbook Chapter 12, recipe 3.'

Terminate the server
>>> server.terminate()
>>> time.sleep(0.25)
>>> server.kill()
>>> server.wait()
0
>>> server.returncode
0
"""
}

if __name__ == "__main__":
    spec = get_openapi_spec()
    query_build_1(spec)
    query_build_2(spec)
