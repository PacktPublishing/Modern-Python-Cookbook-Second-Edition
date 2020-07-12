"""Python Cookbook 2nd ed.

Chapter 6, recipe 2, Using input() and getpass() for user input
"""

from datetime import date, datetime
from typing import List, Callable, Any, Protocol


def get_date1() -> date:
    year = None
    while year is None:
        year_text = input("year: ")
        try:
            year = int(year_text)
        except ValueError as ex:
            print(ex)
    month_text = input("month [1-12]: ")
    day_text = input("day [1-31]: ")
    result = date(int(year_text), int(month_text), int(day_text))
    return result


def get_integer(prompt: str) -> int:
    while True:
        value_text = input(prompt)
        try:
            value = int(value_text)
            return value
        except ValueError as ex:
            print(ex)


def get_date2() -> date:
    while True:
        year = get_integer("year: ")
        month = get_integer("month [1-12]: ")
        day = get_integer("day [1-31]: ")
        try:
            result = date(year, month, day)
            return result
        except ValueError as ex:
            problem = f"invalid, {ex}"


def get_date3() -> date:
    while True:
        raw_date_str = input("date [yyyy-mm-dd]: ")
        try:
            input_date = datetime.strptime(
                raw_date_str, "%Y-%m-%d").date()
            return input_date
        except ValueError as ex:
            print(f"invalid date, {ex}")


DateGet = Callable[[], date]


def get_date_list(get_date: DateGet = get_date1) -> List[date]:
    d1 = get_date()
    more = input("Another? ").lower()
    results = [d1]
    while more.startswith("y"):
        d2 = get_date()
        results.append(d2)
        more = input("Another? ").lower()
    return results


class Comparable(Protocol):
    def __lt__(self, other: Any) -> bool:
        ...

    def __le__(self, other: Any) -> bool:
        ...

    def __gt__(self, other: Any) -> bool:
        ...

    def __ge__(self, other: Any) -> bool:
        ...


def range_exception(
    value: Comparable, *, start: Comparable, stop: Comparable
) -> Comparable:
    if start <= value < stop:
        return value
    raise ValueError(f"invalid, not in range {start!r}, {stop!r}: {value!r}")


def get_conv(prompt: str, convert: Callable[[str], Any] = int) -> Any:
    while True:
        value_text = input(prompt)
        try:
            value = convert(value_text)
            return value
        except Exception as ex:
            print(ex)


def get_int_in_range(prompt: str, start: int, stop: int) -> int:
    return get_conv(
        prompt, lambda text: range_exception(int(text), start=start, stop=stop)
    )


def get_date4() -> date:
    while True:
        year = get_int_in_range("year: ", 1900, 2100)
        month = get_int_in_range("month [1-12]: ", 1, 13)
        day_1_date = date(year, month, 1)
        if month == 12:
            next_year, next_month = year + 1, 1
        else:
            next_year, next_month = year, month + 1
        # Alternative: y, m = divmod(y*12+(m-1)+1, 12); m += 1
        day_end_date = date(next_year, next_month, 1)
        stop = (day_end_date - day_1_date).days
        day = get_int_in_range(f"day [1-{stop}]: ", 1, stop + 1)
        try:
            result = date(year, month, day)
            return result
        except ValueError as ex:
            problem = f"invalid, {ex}"


### Unit tests ###

from unittest.mock import Mock, call
from pytest import approx  # type: ignore


def test_get_integer_good(monkeypatch):
    mock_input = Mock(side_effect=["42"])
    monkeypatch.setitem(__builtins__, "input", mock_input)
    v = get_integer("Answer: ")
    assert v == 42
    assert mock_input.mock_calls == [call("Answer: ")]


def test_get_integer_bad(monkeypatch):
    mock_input = Mock(side_effect=["Not a number", "42"])
    monkeypatch.setitem(__builtins__, "input", mock_input)
    v = get_integer("Answer: ")
    assert v == 42
    assert mock_input.mock_calls == [call("Answer: "), call("Answer: ")]


def test_get_conv_simple(monkeypatch):
    mock_input = Mock(side_effect=["bad", "42"])
    monkeypatch.setitem(__builtins__, "input", mock_input)
    v = get_conv("Answer: ", float)
    assert v == approx(42.0)
    assert mock_input.mock_calls == [call("Answer: "), call("Answer: ")]


def test_get_conv_complex(monkeypatch):
    mock_input = Mock(side_effect=["bad", "42", "12"])
    monkeypatch.setitem(__builtins__, "input", mock_input)
    v = get_conv("Answer: ", lambda text: range_exception(int(text), start=1, stop=13))
    assert v == 12
    assert mock_input.mock_calls == [
        call("Answer: "),
        call("Answer: "),
        call("Answer: "),
    ]


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
    mock_input = Mock(side_effect=["2016", "4", "29"])
    monkeypatch.setitem(__builtins__, "input", mock_input)
    d = get_date2()
    assert d == date(2016, 4, 29)
    assert mock_input.mock_calls == [
        call("year: "),
        call("month [1-12]: "),
        call("day [1-31]: "),
    ]


def test_get_date3(monkeypatch):
    mock_input = Mock(side_effect=["2016-4-29"])
    monkeypatch.setitem(__builtins__, "input", mock_input)
    d = get_date3()
    assert d == date(2016, 4, 29)
    assert mock_input.mock_calls == [call("date [yyyy-mm-dd]: ")]


def test_get_date3_error(monkeypatch):
    mock_input = Mock(side_effect=["2016-2-31", "2016-4-29"])
    monkeypatch.setitem(__builtins__, "input", mock_input)
    d = get_date3()
    assert d == date(2016, 4, 29)
    assert mock_input.mock_calls == [call("date [yyyy-mm-dd]: "), call("date [yyyy-mm-dd]: ")]


def test_get_date_list(monkeypatch):
    mock_input = Mock(side_effect=["2016-4-29", "y", "2016-5-2", "n"])
    monkeypatch.setitem(__builtins__, "input", mock_input)
    d = get_date_list(get_date3)
    assert d == [date(2016, 4, 29), date(2016, 5, 2)]
    assert mock_input.mock_calls == [
        call("date [yyyy-mm-dd]: "),
        call("Another? "),
        call("date [yyyy-mm-dd]: "),
        call("Another? "),
    ]


def test_get_date4(monkeypatch):
    mock_input = Mock(side_effect=["2016", "4", "29"])
    monkeypatch.setitem(__builtins__, "input", mock_input)
    d = get_date4()
    assert d == date(2016, 4, 29)
    assert mock_input.mock_calls == [
        call("year: "),
        call("month [1-12]: "),
        call("day [1-30]: "),
    ]
