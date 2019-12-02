"""Python Cookbook 2nd ed.

Chapter 5, recipe 2
"""

from datetime import date, datetime
from typing import List


def get_date1() -> date:
    year = int(input("year: "))
    month = int(input("month [1-12]: "))
    day = int(input("day [1-31]: "))
    result = date(year, month, day)
    return result


def get_date2() -> date:
    raw_date_str = input("date [yyyy-mm-dd]: ")
    input_date = datetime.strptime(raw_date_str, "%Y-%m-%d").date()
    return input_date


def get_date_list(get_date=get_date1) -> List[date]:
    d1 = get_date()
    more = input("Another? ").lower()
    results = [d1]
    while more.startswith("y"):
        d2 = get_date()
        results.append(d2)
        more = input("Another? ").lower()
    return results


import unittest
from unittest.mock import Mock, call, patch


class GIVEN_get_date1_WHEN_valid_THEN_date(unittest.TestCase):
    def setUp(self):
        self.mock_input = Mock(side_effect=["2016", "4", "29"])

    def runTest(self):
        with patch("__main__.__builtins__.input", self.mock_input):
            d = get_date1()
        self.assertEqual(d, date(2016, 4, 29))
        self.mock_input.assert_has_calls(
            [call("year: "), call("month [1-12]: "), call("day [1-31]: ")]
        )


class GIVEN_get_date2_WHEN_valid_THEN_date(unittest.TestCase):
    def setUp(self):
        self.mock_input = Mock(side_effect=["2016-4-29"])

    def runTest(self):
        with patch("__main__.__builtins__.input", self.mock_input):
            d = get_date2()
        self.assertEqual(d, date(2016, 4, 29))
        self.mock_input.assert_has_calls([call("date [yyyy-mm-dd]: ")])


class GIVEN_get_date_list_WHEN_valid_THEN_date(unittest.TestCase):
    def setUp(self):
        self.mock_input = Mock(side_effect=["2016-4-29", "y", "2016-5-2", "n"])

    def runTest(self):
        with patch("__main__.__builtins__.input", self.mock_input):
            d = get_date_list(get_date2)
        self.assertEqual(d, [date(2016, 4, 29), date(2016, 5, 2)])
        self.mock_input.assert_has_calls([call("date [yyyy-mm-dd]: ")])


def test_get_date1(monkeypatch):
    mock_input = Mock(side_effect=["2016", "4", "29"])
    monkeypatch.setitem(__builtins__, "input", mock_input)
    d = get_date1()
    assert d == date(2016, 4, 29)
    assert mock_input.mock_calls == [
        call("year: "),
        call("month [1-12]: "),
        call("day [1-31]: "),
    ]


def test_get_date2(monkeypatch):
    mock_input = Mock(side_effect=["2016-4-29"])
    monkeypatch.setitem(__builtins__, "input", mock_input)
    d = get_date2()
    assert d == date(2016, 4, 29)
    assert mock_input.mock_calls == [call("date [yyyy-mm-dd]: ")]


def test_get_date_list(monkeypatch):
    mock_input = Mock(side_effect=["2016-4-29", "y", "2016-5-2", "n"])
    monkeypatch.setitem(__builtins__, "input", mock_input)
    d = get_date_list(get_date2)
    assert d == [date(2016, 4, 29), date(2016, 5, 2)]
    assert mock_input.mock_calls == [
        call("date [yyyy-mm-dd]: "),
        call("Another? "),
        call("date [yyyy-mm-dd]: "),
        call("Another? "),
    ]
