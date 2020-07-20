"""Python Cookbook

Chapter 14, recipe 3, Combining many applications using the Command design pattern
"""
import argparse
from pathlib import Path
from unittest.mock import Mock, call, sentinel
from pytest import *  # type: ignore

import Chapter_14.ch14_r02


def test_command():
    options = argparse.Namespace()
    cmd = Chapter_14.ch14_r02.Command()
    cmd.execute(options)


@fixture  # type: ignore
def mock_ch13_r05():
    mock_roll_iter = Mock(return_value=sentinel.DATA)
    mock_write_rolls = Mock()
    mock_module = Mock(roll_iter=mock_roll_iter, write_rolls=mock_write_rolls)
    return mock_module


def test_simulate(mock_ch13_r05, monkeypatch, capsys, tmpdir):
    target = tmpdir / "game_file.yaml"
    monkeypatch.setattr(Chapter_14.ch14_r02, 'ch13_r05', mock_ch13_r05)
    options = argparse.Namespace(
        game_file=target,
        games=sentinel.GAMES,
        seed=sentinel.SEED,
    )

    cmd = Chapter_14.ch14_r02.Simulate()
    cmd.execute(options)

    assert mock_ch13_r05.roll_iter.mock_calls == [call(sentinel.GAMES, sentinel.SEED)]
    assert mock_ch13_r05.write_rolls.mock_calls == [call(Path(target), sentinel.DATA)]
    out, err = capsys.readouterr()
    assert out.splitlines() == [
        f"Created {target}"
    ]


@fixture  # type: ignore
def mock_ch13_r06():
    mock_process_all_files = Mock()
    mock_module = Mock(process_all_files=mock_process_all_files)
    return mock_module


def test_summarize(mock_ch13_r06, monkeypatch, capsys, tmpdir):
    target = tmpdir / "summary_file.yaml"
    game_file_1 = tmpdir / "game_file_1.yaml"
    game_file_2 = tmpdir / "game_file_2.yaml"
    monkeypatch.setattr(Chapter_14.ch14_r02, 'ch13_r06', mock_ch13_r06)
    options = argparse.Namespace(
        summary_file=target,
        game_files=[game_file_1, game_file_2]
    )

    cmd = Chapter_14.ch14_r02.Summarize()
    cmd.execute(options)

    assert len(mock_ch13_r06.process_all_files.mock_calls) == 1
    process_args = mock_ch13_r06.process_all_files.mock_calls[0].args
    assert process_args[1] == [game_file_1, game_file_2]


def test_simsum(mock_ch13_r05, mock_ch13_r06, monkeypatch, capsys, tmpdir):
    monkeypatch.setattr(Chapter_14.ch14_r02, 'ch13_r06', mock_ch13_r06)
    monkeypatch.setattr(Chapter_14.ch14_r02, 'ch13_r05', mock_ch13_r05)
    options = argparse.Namespace(
        games=sentinel.GAMES,
        summary_file=tmpdir/"summary.yaml",
        seed=sentinel.SEED
    )

    cmd = Chapter_14.ch14_r02.SimSum()
    cmd.execute(options)

    assert mock_ch13_r05.roll_iter.mock_calls == [call(sentinel.GAMES, sentinel.SEED)]
    assert mock_ch13_r05.write_rolls.mock_calls == [call(cmd.intermediate, sentinel.DATA)]
    out, err = capsys.readouterr()
    assert out.splitlines() == [
        f"Created {str(cmd.intermediate)}"
    ]
    assert len(mock_ch13_r06.process_all_files.mock_calls) == 1
    process_args = mock_ch13_r06.process_all_files.mock_calls[0].args
    assert process_args[1] == [Path(cmd.intermediate)]
