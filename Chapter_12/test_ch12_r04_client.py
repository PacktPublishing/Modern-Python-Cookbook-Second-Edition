"""Python Cookbook 2nd ed.

Tests for ch12_r04_client
"""
import json
from unittest.mock import Mock
import urllib.request
from pytest import *  # type: ignore
import Chapter_12.ch12_r04_client
from Chapter_12.ch12_r04_server import specification


@fixture  # type: ignore
def mock_urllib(monkeypatch):
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
        elif request.selector.endswith("/decks?size=1") and request.method == "POST":
            return mock_context(
                Mock(
                    status="201 Created",
                    read=Mock(return_value=b'{"status": "ok", "id": "mock_id"}'),
                    headers={"Link": "/decks/mock_id"},
                    getcode=Mock(return_value=201),
                )
            )
        elif request.selector.endswith("/decks/mock_id") and request.method == "GET":
            return mock_context(
                Mock(
                    status="200 OK",
                    read=Mock(
                        return_value=b'[{"__class__": "Card", "rank": 1, "suit": "\\u2660"}]'
                    ),
                    getcode=Mock(return_value=200),
                )
            )
        elif (
            request.selector.endswith("/decks/mock_id/hands?%24top=2&cards=1")
            and request.method == "GET"
        ):
            return mock_context(
                Mock(
                    status="200 OK",
                    read=Mock(
                        return_value=b'[{"cards": {"__class__": "Card", "rank": 1, "suit": "\\u2660"}, "hand": 0}]'
                    ),
                    getcode=Mock(return_value=200),
                )
            )
        else:
            assert False, f"Unsupported request: {vars(request)}, {args=}, {kwargs=}"

    mock_urllib_request = Mock(
        wraps=urllib.request, urlopen=Mock(side_effect=response_maker)
    )
    monkeypatch.setattr(
        Chapter_12.ch12_r04_client.urllib, "request", mock_urllib_request
    )


def test_get_openapi_spec(mock_urllib):
    spec = Chapter_12.ch12_r04_client.get_openapi_spec()
    assert spec["info"]["title"] == "Python Cookbook Chapter 12, recipe 4."


def test_create_new_deck(mock_urllib):
    response = Chapter_12.ch12_r04_client.create_new_deck(specification, 1)
    assert response == {"status": "ok", "id": "mock_id"}


def test_get_new_deck(mock_urllib):
    response = Chapter_12.ch12_r04_client.get_new_deck(specification, "mock_id")
    assert response == [{"__class__": "Card", "rank": 1, "suit": "\u2660"}]


def test_get_hands(mock_urllib):
    response = Chapter_12.ch12_r04_client.get_hands(
        specification, "mock_id", cards=1, limit=2
    )
    assert response == [
        {"cards": {"__class__": "Card", "rank": 1, "suit": "\u2660"}, "hand": 0}
    ]



def test_no_spec_create_new_deck(mock_urllib):
    response = Chapter_12.ch12_r04_client.no_spec_create_new_deck(1)
    assert response == {"status": "ok", "id": "mock_id"}


def test_no_spec_get_new_deck(mock_urllib):
    response = Chapter_12.ch12_r04_client.no_spec_get_new_deck("mock_id")
    assert response == [{"__class__": "Card", "rank": 1, "suit": "\u2660"}]


def test_no_spec_get_hands(mock_urllib):
    response = Chapter_12.ch12_r04_client.no_spec_get_hands(
        "mock_id", cards=1, limit=2
    )
    assert response == [
        {"cards": {"__class__": "Card", "rank": 1, "suit": "\u2660"}, "hand": 0}
    ]
