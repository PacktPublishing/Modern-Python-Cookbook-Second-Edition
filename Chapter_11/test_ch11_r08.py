"""Python Cookbook 2nd ed.

Chapter 11, recipe 8. Pytest Variant.
"""
import Chapter_11.ch11_r08

from unittest.mock import Mock, patch
from pytest import *  # type: ignore
import datetime
from pathlib import Path
import json


@fixture  # type: ignore
def mock_datetime():
    return Mock(
        wraps="datetime",
        datetime=Mock(
            utcnow=Mock(return_value=datetime.datetime(2017, 9, 10, 11, 12, 13))
        ),
    )


def test_save_data(monkeypatch, tmpdir, mock_datetime):
    data = {"primes": [2, 3, 5, 7, 11, 13, 17, 19]}
    monkeypatch.setattr(Chapter_11.ch11_r08, "datetime", mock_datetime)

    Chapter_11.ch11_r08.save_data(Path(tmpdir), data)

    expected_path = Path(tmpdir) / "extract_20170910111213.json"
    with expected_path.open() as result_file:
        result_data = json.load(result_file)
        assert data == result_data

    mock_datetime.datetime.utcnow.assert_called_once_with()
