"""Python Cookbook 2nd ed.

Tests for ch12_r06_requests
"""
import base64
import json
from unittest.mock import Mock
import urllib.request
from pytest import *  # type: ignore
import Chapter_12.ch12_r06_requests
from Chapter_12.ch12_r06_server import specification


@fixture  # type: ignore
def mock_requests(monkeypatch):
    player = {
        "email": "example@example.com",
        "name": "example",
        "twitter": "https://twitter.com/PacktPub",
        "lucky_number": 13,
    }

    def get_response_maker(url, *args, **kwargs):
        """Given a Request, build a mock response."""
        if url.endswith("/openapi.json"):
            return Mock(
                status_code=200,
                json=Mock(
                    return_value=specification
                ),
                headers={},
            )
        elif url.endswith("/players/mock_id"):
            assert "auth" in kwargs
            return Mock(
                status_code=200,
                json=Mock(
                    return_value={"player": player}
                ),
            )
        elif url.endswith("/players"):
            assert "auth" in kwargs
            return Mock(
                status_code=200,
                json=Mock(
                    return_value={"players": [player]}
                ),
            )
        else:
            assert False, f"Unsupported request: {vars(url)}, {args=}, {kwargs=}"

    def post_response_maker(url, *args, **kwargs):
        if url.endswith("/players"):
            document = kwargs['json']
            assert "password" in document, "Missing password"
            return Mock(
                status_code=201,
                json=Mock(return_value={"status": "ok", "id": "mock_id"}),
                headers={"Link": "/players/mock_id"},
            )
        else:
            assert False, f"Unsupported request: {vars(url)}, {args=}, {kwargs=}"

    mock_requests_module = Mock(
        get=Mock(side_effect=get_response_maker),
        post=Mock(side_effect=post_response_maker),
    )
    monkeypatch.setattr(
        Chapter_12.ch12_r06_requests, "requests", mock_requests_module
    )


def test_get_openapi_spec(mock_requests):
    spec = Chapter_12.ch12_r06_requests.get_openapi_spec()
    assert spec["info"]["title"] == "Python Cookbook Chapter 12, recipe 6."
    paths = Chapter_12.ch12_r06_requests.make_path_map(spec)
    assert "make_player" in paths
    assert "get_all_players" in paths
    assert "get_one_player" in paths


def test_create_new_player(mock_requests):
    player = {
        "email": "example@example.com",
        "name": "example",
        "twitter": "https://twitter.com/PacktPub",
        "lucky_number": 13,
        "password": "Hunter2",
    }
    paths = Chapter_12.ch12_r06_requests.make_path_map(specification)
    response = Chapter_12.ch12_r06_requests.create_new_player(
        specification, paths, player)
    assert response == {"status": "ok", "id": "mock_id"}


def test_get_one_player(mock_requests):
    paths = Chapter_12.ch12_r06_requests.make_path_map(specification)
    credentials = ("mock_id", "OpenSesame")
    response = Chapter_12.ch12_r06_requests.get_one_player(
        specification, paths, credentials, "mock_id"
    )
    assert response == {
        "email": "example@example.com",
        "name": "example",
        "twitter": "https://twitter.com/PacktPub",
        "lucky_number": 13,
    }


def test_get_all_players(mock_requests):
    paths = Chapter_12.ch12_r06_requests.make_path_map(specification)
    credentials = ("mock_id", "OpenSesame")
    response = Chapter_12.ch12_r06_requests.get_all_players(
        specification, paths, credentials
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
