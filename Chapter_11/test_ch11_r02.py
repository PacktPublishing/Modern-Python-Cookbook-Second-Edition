"""Python Cookbook 2nd ed.

Tests for ch11_r02
"""
import json
from unittest.mock import Mock
import Chapter_11.ch11_r02

from pytest import *  # type: ignore
import yaml

@fixture  # type: ignore
def dealer_client(monkeypatch):
    monkeypatch.setenv("DEAL_APP_SEED", "42")
    app = Chapter_11.ch11_r02.dealer
    return app.test_client()


def test_deal_cards(dealer_client):
    response = dealer_client.get(
        path="/dealer/hand",
        query_string={"cards": 5},
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 200
    assert response.json == [
        {"__class__": "Card", "rank": 10, "suit": "♡"},
        {"__class__": "Card", "rank": 4, "suit": "♡"},
        {"__class__": "Card", "rank": 7, "suit": "♠"},
        {"__class__": "Card", "rank": 11, "suit": "♢"},
        {"__class__": "Card", "rank": 12, "suit": "♡"},
    ]


def test_openapi_yaml(dealer_client):
    response = dealer_client.get(
        path="/dealer/openapi.yaml",
        headers={"Accept": "application/yaml"},
    )
    assert response.status_code == 200
    expected = Chapter_11.ch11_r02.specification
    assert expected == yaml.load(response.data, Loader=yaml.SafeLoader)

def test_openapi_json(dealer_client):
    response = dealer_client.get(
        path="/dealer/openapi.json",
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 200
    expected = Chapter_11.ch11_r02.specification
    assert expected == response.json

