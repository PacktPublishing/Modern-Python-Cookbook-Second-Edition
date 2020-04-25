"""Python Cookbook

Chapter 13, recipe 1.
"""
from pathlib import Path
from pytest import *  # type: ignore
from unittest.mock import Mock, patch, mock_open, MagicMock, call
import Chapter_13.ch13_r01


@fixture  # type: ignore
def mock_path(monkeypatch, tmpdir):
    mocked_class = Mock(
        wraps=Path,
        return_value=Path(tmpdir / "etc"),
        home=Mock(return_value=Path(tmpdir / "home")),
    )
    monkeypatch.setattr(Chapter_13.ch13_r01, "Path", mocked_class)

    (tmpdir / "etc").mkdir()
    (tmpdir / "etc" / "profile").write_text(
        "exists", encoding="utf-8")
    (tmpdir / "home").mkdir()
    (tmpdir / "home" / ".profile").write_text(
        "exists", encoding="utf-8")
    return mocked_class


@fixture  # type: ignore
def mock_load_config(monkeypatch):
    mocked_load_config_file = Mock(return_value={})
    monkeypatch.setattr(
        Chapter_13.ch13_r01,
        "load_config_file",
        mocked_load_config_file
    )
    return mocked_load_config_file


def test_get_config(mock_load_config, mock_path):
    config = Chapter_13.ch13_r01.get_config()

    assert mock_path.mock_calls == [
        call("/etc"),
        call.home(),
        call.home(),
        call.home(),
    ]
    assert mock_load_config.mock_calls == [
        call(mock_path.return_value / "profile"),
        call(mock_path.home.return_value / ".profile"),
    ]
