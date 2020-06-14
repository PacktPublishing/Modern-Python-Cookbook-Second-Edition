"""Python Cookbook 2nd ed.

Tests for ch12_r04_server
"""
import json
from unittest.mock import Mock
import Chapter_12.ch12_r04_server
from pytest import *  # type: ignore


@fixture  # type: ignore
def dealer_client(monkeypatch):
    monkeypatch.setenv("DEAL_APP_SEED", "42")
    app = Chapter_12.ch12_r04_server.dealer
    return app.test_client()


def test_openapi_spec(dealer_client):
    spec_response = dealer_client.get("/dealer/openapi.json")
    assert (
        spec_response.get_json()["info"]["title"]
        == "Python Cookbook Chapter 12, recipe 4."
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
                {"__class__": "Card", "__init__": {"rank": 10, "suit": "♡"}},
                {"__class__": "Card", "__init__": {"rank": 1, "suit": "♠"}},
                {"__class__": "Card", "__init__": {"rank": 9, "suit": "♡"}},
                {"__class__": "Card", "__init__": {"rank": 11, "suit": "♢"}},
                {"__class__": "Card", "__init__": {"rank": 5, "suit": "♡"}},
            ],
            "hand": 0,
        }
    ]

def test_deal_bad_make_deck(dealer_client):
    response = dealer_client.post(
        path="/dealer/decks",
        query_string={"decks": "not a number!"},
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 400
    assert response.get_json() is None
    assert b"Bad Request" in response.data


def test_deal_bad_get_hands(dealer_client):
    deck_id = "definitely doesn't exist"
    response = dealer_client.get(
        path=f"/dealer/decks/{deck_id}/hands",
        query_string={"cards": 5},
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 404
    assert response.get_json() is None
    assert b"Not Found" in response.data
    assert b"deck &quot;definitely doesn't exist&quot; not found" in response.data
