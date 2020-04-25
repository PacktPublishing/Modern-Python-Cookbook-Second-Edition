"""Python Cookbook

Chapter 11, recipe 3, Making REST requests with urllib.
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


test_example = """
Start the server
>>> import subprocess, time, os, pathlib
>>> env = os.environ.copy()
>>> env['PYTHONPATH'] = str(pathlib.Path(__file__).parent.parent)
>>> env['DEAL_APP_SEED'] = '42'
>>> server = subprocess.Popen(["python", "Chapter_11/ch11_r02.py"], env=env)

Pause to let the server start
>>> time.sleep(1.0)

Make the client request
>>> spec = get_openapi_spec()
openapi.json is valid
>>> spec['info']['title']
'Python Cookbook Chapter 11, recipe 2.'

>>> query_build_1()  # doctest: +ELLIPSIS
200
Content-Type: application/json
Content-Length: 235
Server: Werkzeug/1.0.1 Python/3.8.0
Date: ...
<BLANKLINE>
<BLANKLINE>
[{'__class__': 'Card', 'rank': 10, 'suit': '♡'}, {'__class__': 'Card', 'rank': 4, 'suit': '♡'}, {'__class__': 'Card', 'rank': 7, 'suit': '♠'}, {'__class__': 'Card', 'rank': 11, 'suit': '♢'}, {'__class__': 'Card', 'rank': 12, 'suit': '♡'}]

>>> query_build_2(spec)  # doctest: +ELLIPSIS
200
Content-Type: application/json
Content-Length: 318
Server: Werkzeug/1.0.1 Python/3.8.0
Date: ...
<BLANKLINE>
<BLANKLINE>
[{'cards': [{'__class__': 'Card', 'rank': 3, 'suit': '♣'}, {'__class__': 'Card', 'rank': 10, 'suit': '♠'}], 'hand': 0}, {'cards': [{'__class__': 'Card', 'rank': 9, 'suit': '♠'}], 'hand': 1}, {'cards': [{'__class__': 'Card', 'rank': 13, 'suit': '♣'}], 'hand': 2}, {'cards': [{'__class__': 'Card', 'rank': 5, 'suit': '♣'}], 'hand': 3}]

Terminate the server
>>> server.terminate()
>>> time.sleep(0.25)
>>> server.kill()
>>> server.wait()
0
>>> server.returncode
0
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}

if __name__ == "__main__":
    spec = get_openapi_spec()
    query_build_1()
    query_build_2(spec)
