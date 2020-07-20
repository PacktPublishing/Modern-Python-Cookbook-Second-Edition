"""Python Cookbook 2nd ed.

Chapter 11, recipe 9. Testing things that involve randomness
pytest Variant.
"""

from types import SimpleNamespace
from unittest.mock import Mock, patch, call, sentinel
from pytest import *  # type: ignore

import Chapter_11.ch11_r09


# Option 1: Mocking the whole random module.

@fixture  # type: ignore
def mock_random():
    expected_resample_data = [
        23, 29, 31, 37, 41, 43, 47, 53]
    random_module = Mock(
        name='mock random',
        choice=Mock(
            name='mock random.choice()',
            side_effect=expected_resample_data))
    return SimpleNamespace(**locals())


def test_resample(mock_random, monkeypatch):
    monkeypatch.setattr(
        Chapter_11.ch11_r09,
        "random",
        mock_random.random_module)

    data = [2, 3, 5, 7, 11, 13, 17, 19]
    resample_data = list(Chapter_11.ch11_r09.resample(data, 8))

    assert resample_data == mock_random.expected_resample_data
    mock_random.random_module.choice.assert_has_calls(8 * [call(data)])

# Option 2: Mocking a specific function

@fixture  # type: ignore
def mock_random_choice():
    expected_resample_data = [
        23, 29, 31, 37, 41, 43, 47, 53]
    mock_choice=Mock(
        name='mock random.choice()',
        side_effect=expected_resample_data)
    return SimpleNamespace(**locals())

def test_resample_choice(mock_random_choice, monkeypatch):
    monkeypatch.setattr(
        Chapter_11.ch11_r09.random,
        "choice",
        mock_random_choice.mock_choice)

    data = [2, 3, 5, 7, 11, 13, 17, 19]
    resample_data = list(Chapter_11.ch11_r09.resample(data, 8))

    assert (
        resample_data
        == mock_random_choice.expected_resample_data
    )
    mock_random_choice.mock_choice.assert_has_calls(8 * [call(data)])

# Using a sentinel

def test_resample_2(monkeypatch):
    mock_choice = Mock(
        name='mock random.choice()',
        side_effect=lambda x: x
    )
    monkeypatch.setattr(
        Chapter_11.ch11_r09.random,
        "choice",
        mock_choice)

    resample_data = list(Chapter_11.ch11_r09.resample(
        sentinel.POPULATION, 8))

    assert resample_data == [sentinel.POPULATION]*8
    mock_choice.assert_has_calls(
        8 * [call(sentinel.POPULATION)])
