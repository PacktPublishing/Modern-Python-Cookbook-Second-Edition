"""Python Cookbook

Chapter 14, recipe 4, Wrapping and combining CLI applications
"""
from pathlib import Path
from subprocess import CalledProcessError
from unittest.mock import Mock, call
from pytest import *  # type: ignore
import Chapter_14.ch14_r04


@fixture  # type: ignore
def mock_subprocess_run_good():
    def make_file(command, check):
        Path(command[5]).write_text("mock output")
    run_function = Mock(
        side_effect=make_file
    )
    return run_function


@fixture  # type: ignore
def mock_subprocess_run_fail():
    def make_file(command, check):
        Path(command[5]).write_text("mock output")
    run_function = Mock(
        side_effect=[
            make_file,
            CalledProcessError(13, ['mock', 'command'])
        ]
    )
    return run_function


def test_make_files_clean_good(
        mock_subprocess_run_good,
        monkeypatch,
        tmpdir):
    monkeypatch.setattr(
        Chapter_14.ch14_r04.subprocess,
        'run',
        mock_subprocess_run_good)

    directory = Path(tmpdir)
    Chapter_14.ch14_r04.make_files_clean(directory, files=3)

    expected = [
        call(
            [
                "python",
                "Chapter_13/ch13_r05.py",
                "--samples",
                "10",
                "--output",
                str(tmpdir/"game_0.yaml"),
            ],
            check=True,
        ),
        call(
            [
                "python",
                "Chapter_13/ch13_r05.py",
                "--samples",
                "10",
                "--output",
                str(tmpdir/"game_1.yaml"),
            ],
            check=True,
        ),
        call(
            [
                "python",
                "Chapter_13/ch13_r05.py",
                "--samples",
                "10",
                "--output",
                str(tmpdir/"game_2.yaml"),
            ],
            check=True,
        ),
    ]
    assert expected == mock_subprocess_run_good.mock_calls
    assert len(list(directory.glob("game_*.yaml"))) == 3


def test_make_files_clean_fail(
        mock_subprocess_run_fail,
        monkeypatch,
        tmpdir):
    monkeypatch.setattr(
        Chapter_14.ch14_r04.subprocess,
        'run',
        mock_subprocess_run_fail)

    directory = Path(tmpdir)
    with raises(CalledProcessError):
        Chapter_14.ch14_r04.make_files_clean(directory, files=3)

    expected = [
        call(
            [
                "python",
                "Chapter_13/ch13_r05.py",
                "--samples",
                "10",
                "--output",
                str(tmpdir/"game_0.yaml"),
            ],
            check=True,
        ),
        call(
            [
                "python",
                "Chapter_13/ch13_r05.py",
                "--samples",
                "10",
                "--output",
                str(tmpdir/"game_1.yaml"),
            ],
            check=True,
        )
    ]
    assert expected == mock_subprocess_run_fail.mock_calls
    assert len(list(directory.glob("game_*.yaml"))) == 0

