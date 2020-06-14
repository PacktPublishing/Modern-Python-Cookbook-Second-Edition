"""Python Cookbook 2nd ed.

Tests for ch12_r06_server
"""
import base64
import json
from unittest.mock import Mock
import Chapter_12.ch12_r06_server
import Chapter_12.ch12_r06_user
from pytest import *  # type: ignore


@fixture  # type: ignore
def fixed_salt(monkeypatch):
    mocked_os = Mock(urandom=Mock(return_value=bytes(range(30))))
    monkeypatch.setattr(Chapter_12.ch12_r06_user, "os", mocked_os)


@fixture  # type: ignore
def dealer_client(monkeypatch, fixed_salt):
    monkeypatch.setenv("DEAL_APP_SEED", "42")
    app = Chapter_12.ch12_r06_server.dealer
    return app.test_client()


def test_openapi_spec(dealer_client):
    spec_response = dealer_client.get("/dealer/openapi.json")
    print(spec_response)
    assert spec_response.status_code == 200
    assert (
        spec_response.get_json()["info"]["title"]
        == "Python Cookbook Chapter 12, recipe 6."
    )


def test_deal_cards_sequence(dealer_client):
    expected_player = {
        "email": "packt@example.com",
        "name": "Packt",
        "twitter": "https://twitter.com/PacktPub",
        "lucky_number": 8,
    }
    response1 = dealer_client.post(
        path="/dealer/players",
        json={
            "email": "packt@example.com",
            "name": "Packt",
            "twitter": "https://twitter.com/PacktPub",
            "lucky_number": 8,
            "password": "OpenSesame",
        },
        headers={"Accept": "application/json"},
    )
    print(response1.data)
    assert response1.status_code == 201
    response_document = response1.get_json()
    assert response_document["player"] == expected_player
    player_url = response1.headers["Location"]
    player_id = response_document["id"]

    credentials = base64.b64encode(f"{player_id}:OpenSesame".encode("utf-8"))

    response2 = dealer_client.post(
        path="/dealer/decks",
        json={"decks": 6},
        headers={
            "Accept": "application/json",
            "Authorization": f"BASIC {credentials.decode('ascii')}",
        },
    )
    assert response2.status_code == 201
    deck_url = response2.headers["Location"]
    response_document = response2.get_json()
    assert response_document["status"] == "ok"
    deck_id = response_document["id"]

    response3 = dealer_client.get(
        deck_url,
        headers={
            "Accept": "application/json",
            "Authorization": f"BASIC {credentials.decode('ascii')}",
        },
    )
    assert response3.status_code == 200
    response3_doc = response3.get_json()
    assert response3_doc["id"] == deck_id
    assert response3_doc["cards"] == 6 * 52

    response4 = dealer_client.get(
        path=f"/dealer/decks/{deck_id}/hands",
        query_string={"cards": 5},
        headers={
            "Accept": "application/json",
            "Authorization": f"BASIC {credentials.decode('ascii')}",
        },
    )
    assert response4.status_code == 200
    assert response4.json == [
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
            "password": "OpenSesame",
        },
        headers={"Accept": "application/json"},
    )
    print(response1.data)
    assert response1.status_code == 201
    response_document = response1.get_json()
    assert response_document["player"] == expected_player
    player_url = response1.headers["Location"]
    player_id = response_document["id"]

    credentials = base64.b64encode(f"{player_id}:OpenSesame".encode("utf-8"))
    response2 = dealer_client.get(
        path=player_url,
        headers={
            "Accept": "application/json",
            "Authorization": f"BASIC {credentials.decode('ascii')}",
        },
    )
    assert response2.status_code == 200
    response_document = response2.get_json()
    assert response_document["player"] == expected_player

    response3 = dealer_client.get(
        path="/dealer/players",
        headers={
            "Accept": "application/json",
            "Authorization": f"BASIC {credentials.decode('ascii')}",
        },
    )
    assert response3.status_code == 200
    response_document = response3.get_json()
    # There may be more than one, depending on the order
    # the tests were run.
    assert (
        response_document["players"]["79dcaabe80c651157e6c67dcef7812b0"]
        == expected_player
    )


def test_bad_credentials(dealer_client):
    expected_player = {
        "email": "test_bad_credentials@example.com",
        "name": "test_bad_credentials",
        "twitter": "https://twitter.com/test_bad_credentials",
        "lucky_number": 8,
    }

    response1 = dealer_client.post(
        path="/dealer/players",
        json={
            "email": "test_bad_credentials@example.com",
            "name": "test_bad_credentials",
            "twitter": "https://twitter.com/test_bad_credentials",
            "lucky_number": 8,
            "password": "OpenSesame",
        },
        headers={"Accept": "application/json"},
    )
    print(response1.data)
    assert response1.status_code == 201
    response_document = response1.get_json()
    player_url = response1.headers["Location"]
    player_id = response_document["id"]

    credentials = base64.b64encode(f"{player_id}:Not-OpenSesame".encode("utf-8"))
    response2 = dealer_client.get(
        path=player_url,
        headers={
            "Accept": "application/json",
            "Authorization": f"BASIC {credentials.decode('ascii')}",
        },
    )
    assert response2.status_code == 401
    response_document = response2.get_json()
    assert response_document == {'error': '401 Unauthorized: Invalid credentials'}
