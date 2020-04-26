"""Python Cookbook 2nd ed.

Tests for ch12_r06_client
"""
import base64
import json
from unittest.mock import Mock
import urllib.request
from pytest import *  # type: ignore
import Chapter_12.ch12_r06_client
from Chapter_12.ch12_r06_server import specification


@fixture  # type: ignore
def mock_urllib(monkeypatch):
    player = {
        "email": "example@example.com",
        "name": "example",
        "twitter": "https://twitter.com/PacktPub",
        "lucky_number": 13,
    }

    def mock_context(response):
        """Wrap a response to behave like a context"""
        return Mock(
            __enter__=Mock(return_value=response), __exit__=Mock(return_value=None)
        )

    def response_maker(request, *args, **kwargs):
        """Given a Request, build a mock response."""
        if request.selector.endswith("/openapi.json") and request.method == "GET":
            return mock_context(
                Mock(
                    status="200 OK",
                    read=Mock(return_value=json.dumps(specification).encode("utf-8")),
                    headers={},
                    getcode=Mock(return_value=200),
                )
            )
        elif request.selector.endswith("/players") and request.method == "POST":
            document = json.loads(request.data)
            assert "password" in document, "Missing password"
            return mock_context(
                Mock(
                    status="201 Created",
                    read=Mock(return_value=b'{"status": "ok", "id": "mock_id"}'),
                    headers={"Link": "/players/mock_id"},
                    getcode=Mock(return_value=201),
                )
            )
        elif request.selector.endswith("/players/mock_id") and request.method == "GET":
            assert "Authorization" in request.headers
            return mock_context(
                Mock(
                    status="200 OK",
                    read=Mock(
                        return_value=json.dumps({"player": player}).encode("utf-8")
                    ),
                    getcode=Mock(return_value=200),
                )
            )
        elif request.selector.endswith("/players") and request.method == "GET":
            assert "Authorization" in request.headers
            return mock_context(
                Mock(
                    status="200 OK",
                    read=Mock(
                        return_value=json.dumps({"players": [player]}).encode("utf-8")
                    ),
                    getcode=Mock(return_value=200),
                )
            )
        else:
            assert False, f"Unsupported request: {vars(request)}, {args=}, {kwargs=}"

    mock_opener = Mock(name="opener", open=Mock(side_effect=response_maker))
    mock_urllib_request = Mock(
        wraps=urllib.request,
        urlopen=Mock(side_effect=response_maker),
        build_opener=Mock(return_value=mock_opener),
    )
    monkeypatch.setattr(
        Chapter_12.ch12_r06_client.urllib, "request", mock_urllib_request
    )
    return mock_opener


def test_get_openapi_spec(mock_urllib):
    spec = Chapter_12.ch12_r06_client.get_openapi_spec(mock_urllib)
    assert spec["info"]["title"] == "Python Cookbook Chapter 12, recipe 6."
    paths = Chapter_12.ch12_r06_client.make_path_map(spec)
    assert "make_player" in paths
    assert "get_all_players" in paths
    assert "get_one_player" in paths


def test_create_new_player(mock_urllib):
    player = {
        "email": "example@example.com",
        "name": "example",
        "twitter": "https://twitter.com/PacktPub",
        "lucky_number": 13,
        "password": "Hunter2",
    }
    paths = Chapter_12.ch12_r06_client.make_path_map(specification)
    response = Chapter_12.ch12_r06_client.create_new_player(
        mock_urllib, specification, paths, player)
    assert response == {"status": "ok", "id": "mock_id"}


def test_get_one_player(mock_urllib):
    paths = Chapter_12.ch12_r06_client.make_path_map(specification)
    credentials = ("mock_id", "OpenSesame")
    response = Chapter_12.ch12_r06_client.get_one_player(
        mock_urllib, specification, paths, credentials, "mock_id"
    )
    assert response == {
        "email": "example@example.com",
        "name": "example",
        "twitter": "https://twitter.com/PacktPub",
        "lucky_number": 13,
    }


def test_get_all_players(mock_urllib):
    paths = Chapter_12.ch12_r06_client.make_path_map(specification)
    credentials = ("mock_id", "OpenSesame")
    response = Chapter_12.ch12_r06_client.get_all_players(
        mock_urllib, specification, paths, credentials
    )
    assert response == {
        "players": [
            {
                "email": "example@example.com",
                "name": "example",
                "twitter": "https://twitter.com/PacktPub",
                "lucky_number": 13,
            }
        ]
    }
