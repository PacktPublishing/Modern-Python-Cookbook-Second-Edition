"""Python Cookbook 2nd ed.

Chapter 11, recipe 9. pytest Variant.
"""

from types import SimpleNamespace
from unittest.mock import Mock, patch, call
from pytest import *  # type: ignore
import Chapter_11.ch11_r09


@fixture  # type: ignore
def mock_random():
    expected_resample_data = [23, 29, 31, 37, 41, 43, 47, 53]
    random_module = Mock(choice=Mock(side_effect=expected_resample_data))
    return SimpleNamespace(**locals())


def test_resample(monkeypatch, mock_random):
    monkeypatch.setattr(Chapter_11.ch11_r09, "random", mock_random.random_module)
    data = [2, 3, 5, 7, 11, 13, 17, 19]

    resample_data = list(Chapter_11.ch11_r09.resample(data, 8))
    assert resample_data == mock_random.expected_resample_data
    mock_random.random_module.choice.assert_has_calls(8 * [call(data)])
