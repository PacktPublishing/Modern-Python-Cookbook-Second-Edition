"""Python Cookbook 2nd ed.

Chapter 11, recipe 8. Testing things that involve dates or times
Pytest Variant.
"""
import datetime
import json
from pathlib import Path

from unittest.mock import Mock, patch
from pytest import *  # type: ignore

import Chapter_11.ch11_r08


@fixture  # type: ignore
def mock_datetime():
    return Mock(
        wraps="datetime",
        datetime=Mock(
            utcnow=Mock(
                return_value=datetime.datetime(
                    2017, 9, 10, 11, 12, 13))
        ),
    )


def test_save_data(mock_datetime, tmpdir, monkeypatch):
    monkeypatch.setattr(
        Chapter_11.ch11_r08, "datetime", mock_datetime)

    data = {"primes": [2, 3, 5, 7, 11, 13, 17, 19]}
    Chapter_11.ch11_r08.save_data(Path(tmpdir), data)

    expected_path = (
            Path(tmpdir) / "extract_20170910111213.json")
    with expected_path.open() as result_file:
        result_data = json.load(result_file)
        assert data == result_data

    mock_datetime.datetime.utcnow.assert_called_once_with()

@fixture  # type: ignore
def mock_datetime_now():
    return Mock(
        name='mock datetime',
        datetime=Mock(
            name='mock datetime.datetime',
            utcnow=Mock(
                return_value=datetime.datetime(
                    2017, 7, 4, 1, 2, 3)
            ),
            now=Mock(
                return_value=datetime.datetime(
                    2017, 7, 4, 4, 2, 3)
            )
        )
    )

def test_save_data_now(mock_datetime_now, tmpdir, monkeypatch):
    monkeypatch.setattr(
        Chapter_11.ch11_r08, "datetime", mock_datetime_now)

    data = {"primes": [2, 3, 5, 7, 11, 13, 17, 19]}
    Chapter_11.ch11_r08.save_data(Path(tmpdir), data)

    expected_path = (
            Path(tmpdir) / "extract_20170704010203.json")
    with expected_path.open() as result_file:
        result_data = json.load(result_file)
        assert data == result_data

    mock_datetime_now.datetime.utcnow.assert_called_once_with()
    assert mock_datetime_now.datetime.now.mock_calls == []
