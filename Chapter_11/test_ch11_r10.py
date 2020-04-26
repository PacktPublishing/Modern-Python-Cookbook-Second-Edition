"""Python Cookbook 2nd ed.

Chapter 11, recipe 10. Mocking external resources

This exercises Chapter_10.ch10_r02 features as part of Chapter 11.
"""
from unittest.mock import Mock, sentinel
from pytest import *  # type: ignore

from pathlib import Path
import Chapter_10.ch10_r02

# Scenario: Everything works, sometimes called the “Happy Path.”

# Scenario: The save_data() function raises an exception, leaving a file corrupted.

# Scenario: The output_old_path.unlink() function raises an exception other than a FileNotFoundError exception.

# Scenario: The output_path.rename() function raise an exception other than a FileNotFoundError exception.

# Scenario: The output_new_path.rename() function raises an exception other than an IOError exception.

@fixture  # type: ignore
def original_file(tmpdir):
    precious_file = tmpdir/"important_data.csv"
    precious_file.write_text(
        hex(id(sentinel.ORIGINAL_DATA)), encoding="utf-8")
    return precious_file

def save_data_good(path, content):
    path.write_text(
        hex(id(sentinel.GOOD_DATA)), encoding="utf-8")

def test_safe_write_happy(original_file, monkeypatch):
    mock_save_data = Mock(side_effect=save_data_good)
    monkeypatch.setattr(
        Chapter_10.ch10_r02, 'save_data', mock_save_data)

    data = [
        Chapter_10.ch10_r02.Quotient(355, 113)
    ]
    Chapter_10.ch10_r02.safe_write(
        Path(original_file), data)

    actual = original_file.read_text(encoding="utf-8")
    assert actual == hex(id(sentinel.GOOD_DATA))


def save_data_failure(path, content):
    path.write_text(
        hex(id(sentinel.CORRUPT_DATA)), encoding="utf-8")
    raise RuntimeError("mock exception")



def test_safe_write_scenario_2(original_file, monkeypatch):
    mock_save_data = Mock(side_effect=save_data_failure)
    monkeypatch.setattr(
        Chapter_10.ch10_r02, 'save_data', mock_save_data)

    data = [
        Chapter_10.ch10_r02.Quotient(355, 113)
    ]
    with raises(RuntimeError) as ex:
        Chapter_10.ch10_r02.safe_write(
            Path(original_file), data)

    actual = original_file.read_text(encoding="utf-8")
    assert actual == hex(id(sentinel.ORIGINAL_DATA))

scenario_3 = {"original": None, "old": RuntimeError("3"), "new": None}
scenario_4 = {"original": RuntimeError("4"), "old": None, "new": None}
scenario_5 = {"original": None, "old": None, "new": RuntimeError("5")}

@fixture(params=[scenario_3, scenario_4, scenario_5])  # type: ignore
def mock_pathlib_path(request):
    """
    There are two paths created in this order: the new, and the old.
    The original is created from Path.
    The new and old are created from the original Path.with_suffix()
    """
    new_path = Mock(rename=Mock(side_effect=request.param["new"]))
    old_path = Mock(unlink=Mock(side_effect=request.param["old"]))
    original_path = Mock(
        with_suffix=Mock(side_effect=[new_path, old_path]),
        rename=Mock(side_effect=request.param["original"])
    )
    return original_path


def test_safe_write_scenarios(
        original_file, mock_pathlib_path, monkeypatch):
    mock_save_data = Mock(side_effect=save_data_good)
    monkeypatch.setattr(
        Chapter_10.ch10_r02, 'save_data', mock_save_data)

    data = [
        Chapter_10.ch10_r02.Quotient(355, 113)
    ]
    with raises(RuntimeError) as exc_info:
        Chapter_10.ch10_r02.safe_write(mock_pathlib_path, data)
    assert exc_info.type == RuntimeError
    assert exc_info.value.args in {("3",), ("4",), ("5",)}

    actual = original_file.read_text(encoding="utf-8")
    assert actual == hex(id(sentinel.ORIGINAL_DATA))
    assert mock_save_data.called_once()
    assert mock_pathlib_path.glob_rename.called_once()
