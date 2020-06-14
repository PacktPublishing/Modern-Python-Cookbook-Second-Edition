"""Python Cookbook 2nd ed.

Tests for ch12_wsgi
"""
import json
from unittest.mock import Mock
import Chapter_12.ch12_wsgi


def test_deal_cards():
    """Without the werkzeug.test.Client: must check the mock start response."""
    mock_start = Mock()
    environ = {"HAND_SIZE": 6, "DEAL_APP_SEED": 42}
    response = b"".join(
        Chapter_12.ch12_wsgi.deal_cards(environ, start_response=mock_start)
    )
    assert json.loads(response) == [
        {"__class__": "Card", "__init__": {"rank": 3, "suit": "♡"}},
        {"__class__": "Card", "__init__": {"rank": 6, "suit": "♣"}},
        {"__class__": "Card", "__init__": {"rank": 7, "suit": "♡"}},
        {"__class__": "Card", "__init__": {"rank": 1, "suit": "♣"}},
        {"__class__": "Card", "__init__": {"rank": 6, "suit": "♡"}},
        {"__class__": "Card", "__init__": {"rank": 10, "suit": "♢"}},
    ]
    mock_start.assert_called_once_with(
        "200 OK", [("Content-Type", "application/json;charset=utf-8")]
    )


def test_DeaLCards():
    """Without the werkzeug.test.Client: must check the mock start response."""
    dealer = Chapter_12.ch12_wsgi.DealCards(hand_size=6, seed=42)
    mock_start = Mock()
    environ = {}
    response = b"".join(dealer(environ, start_response=mock_start))
    assert json.loads(response) == [
        {"__class__": "Card", "__init__": {"rank": 3, "suit": "♡"}},
        {"__class__": "Card", "__init__": {"rank": 6, "suit": "♣"}},
        {"__class__": "Card", "__init__": {"rank": 7, "suit": "♡"}},
        {"__class__": "Card", "__init__": {"rank": 1, "suit": "♣"}},
        {"__class__": "Card", "__init__": {"rank": 6, "suit": "♡"}},
        {"__class__": "Card", "__init__": {"rank": 10, "suit": "♢"}},
    ]
    mock_start.assert_called_once_with(
        "200 OK", [("Content-Type", "application/json;charset=utf-8")]
    )


from werkzeug.test import Client


def test_json_filter_good_1():
    dealer = Chapter_12.ch12_wsgi.DealCards(hand_size=6, seed=42)
    json_wrapper = Chapter_12.ch12_wsgi.JSON_Filter(dealer)
    client = Client(json_wrapper)
    response, status, headers = client.get(headers={"Accept": "application/json"})
    assert status == "200 OK"
    assert dict(headers) == {"Content-Type": "application/json;charset=utf-8"}
    response = b"".join(response)
    assert json.loads(response) == [
        {"__class__": "Card", "__init__": {"rank": 3, "suit": "♡"}},
        {"__class__": "Card", "__init__": {"rank": 6, "suit": "♣"}},
        {"__class__": "Card", "__init__": {"rank": 7, "suit": "♡"}},
        {"__class__": "Card", "__init__": {"rank": 1, "suit": "♣"}},
        {"__class__": "Card", "__init__": {"rank": 6, "suit": "♡"}},
        {"__class__": "Card", "__init__": {"rank": 10, "suit": "♢"}},
    ]


def test_json_filter_reject():
    dealer = Chapter_12.ch12_wsgi.DealCards(hand_size=6, seed=42)
    json_wrapper = Chapter_12.ch12_wsgi.JSON_Filter(dealer)
    client = Client(json_wrapper)
    response, status, headers = client.get(headers={"Accept": "*/*"})
    assert status == "400 Bad Request"
    assert dict(headers) == {"Content-Type": "text/plain;charset=utf-8"}
    response = b"".join(response)
    assert (
        response
        == b"Request doesn't include ?$format=json or Accept:application/json header"
    )


def test_json_filter_good_2():
    dealer = Chapter_12.ch12_wsgi.DealCards(hand_size=6, seed=42)
    json_wrapper = Chapter_12.ch12_wsgi.JSON_Filter(dealer)
    client = Client(json_wrapper)
    response, status, headers = client.get(query_string={"$format": "json"})
    print(response)
    assert status == "200 OK"
    assert dict(headers) == {"Content-Type": "application/json;charset=utf-8"}
    assert json.loads(b"".join(response)) == [
        {"__class__": "Card", "__init__": {"rank": 3, "suit": "♡"}},
        {"__class__": "Card", "__init__": {"rank": 6, "suit": "♣"}},
        {"__class__": "Card", "__init__": {"rank": 7, "suit": "♡"}},
        {"__class__": "Card", "__init__": {"rank": 1, "suit": "♣"}},
        {"__class__": "Card", "__init__": {"rank": 6, "suit": "♡"}},
        {"__class__": "Card", "__init__": {"rank": 10, "suit": "♢"}},
    ]
