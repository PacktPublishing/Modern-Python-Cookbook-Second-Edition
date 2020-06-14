"""Python Cookbook 2nd ed.

Tests for ch12_r01
"""
import json
from unittest.mock import Mock
import Chapter_12.ch12_r01
from pytest import *  # type: ignore


@fixture  # type: ignore
def dealer_client(monkeypatch):
    monkeypatch.setenv("DEAL_APP_SEED", "42")
    app = Chapter_12.ch12_r01.dealer
    return app.test_client()


def test_deal_cards(dealer_client):
    response = dealer_client.get(
        path="/dealer/hand",
        query_string={"cards": 5},
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 200
    assert response.json == [
        {"__class__": "Card", "__init__": {"rank": 10, "suit": "♡"}},
        {"__class__": "Card", "__init__": {"rank": 4, "suit": "♡"}},
        {"__class__": "Card", "__init__": {"rank": 7, "suit": "♠"}},
        {"__class__": "Card", "__init__": {"rank": 11, "suit": "♢"}},
        {"__class__": "Card", "__init__": {"rank": 12, "suit": "♡"}},
    ]
