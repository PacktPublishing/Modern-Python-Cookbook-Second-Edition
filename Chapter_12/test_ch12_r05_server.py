"""Python Cookbook 2nd ed.

Tests for ch12_r06_server
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
    response1 = dealer_client.post(
        path="/dealer/decks", json={"decks": 6}, headers={"Accept": "application/json"}
    )
    assert response1.status_code == 201
    deck_url = response1.headers["Location"]
    response_document = response1.get_json()
    assert response_document["status"] == "ok"
    deck_id = response_document["id"]

    response2 = dealer_client.get(deck_url, headers={"Accept": "application/json"})
    assert response2.status_code == 200
    response2_doc = response2.get_json()
    assert response2_doc["id"] == deck_id
    assert response2_doc["cards"] == 6 * 52

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


def test_player_sequence(dealer_client):
    expected_player = {
        "email": "player@example.com",
        "name": "Farrier",
        "twitter": "https://twitter.com/F_L_Stevens",
        "lucky_number": 8,
    }
    response1 = dealer_client.post(
        path="/dealer/players",
        json={
            "email": "player@example.com",
            "name": "Farrier",
            "twitter": "https://twitter.com/F_L_Stevens",
            "lucky_number": 8,
        },
        headers={"Accept": "application/json"},
    )
    assert response1.status_code == 201
    response_document = response1.get_json()
    assert response_document["player"] == expected_player
    player_url = response1.headers["Location"]
    player_id = response_document["id"]

    response2 = dealer_client.get(
        path=player_url, headers={"Accept": "application/json"}
    )
    assert response2.status_code == 200
    response_document = response2.get_json()
    assert response_document["player"] == expected_player

    response3 = dealer_client.get(
        path="/dealer/players", headers={"Accept": "application/json"}
    )
    assert response3.status_code == 200
    response_document = response3.get_json()
    assert response_document["players"] == {
        "79dcaabe80c651157e6c67dcef7812b0": expected_player
    }
