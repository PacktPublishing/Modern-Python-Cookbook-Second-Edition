"""Python Cookbook 2nd ed.

Tests for ch12_r05_server
"""
import json
from unittest.mock import Mock
import Chapter_12.ch12_r05_server
from pytest import *  # type: ignore


@fixture  # type: ignore
def dealer_client(monkeypatch):
    monkeypatch.setenv("DEAL_APP_SEED", "42")
    app = Chapter_12.ch12_r05_server.dealer
    return app.test_client()


def test_openapi_spec(dealer_client):
    spec_response = dealer_client.get("/dealer/openapi.json")
    assert (
        spec_response.get_json()["info"]["title"]
        == "Python Cookbook Chapter 12, recipe 5."
    )


def test_deal_cards_sequence(dealer_client):
    # Typical
    # response1 = dealer_client.post("/dealer/decks", json={'decks': 6}, headers={'Accept': "application/json"})
    # In this specific case
    response1 = dealer_client.post(
        path="/dealer/decks",
        query_string={"decks": 6},
        headers={"Accept": "application/json"},
    )
    assert response1.status_code == 201
    response_document = response1.get_json()
    assert response_document["status"] == "ok"
    deck_url = response1.headers["Location"]
    deck_id = response_document["id"]

    response2 = dealer_client.get(deck_url, headers={"Accept": "application/json"})
    assert response2.status_code == 200
    assert len(response2.get_json()) == 6 * 52

    response3 = dealer_client.get(
        path=f"/dealer/decks/{deck_id}/hands",
        query_string={"cards": 5},
        headers={"Accept": "application/json"},
    )
    assert response3.status_code == 200
    assert response3.json == [
        {
            "cards": [
                {"__class__": "Card", "rank": 10, "suit": "♡"},
                {"__class__": "Card", "rank": 1, "suit": "♠"},
                {"__class__": "Card", "rank": 9, "suit": "♡"},
                {"__class__": "Card", "rank": 11, "suit": "♢"},
                {"__class__": "Card", "rank": 5, "suit": "♡"},
            ],
            "hand": 0,
        }
    ]
