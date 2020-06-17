"""Python Cookbook

Chapter 14, recipe 5, Wrapping a program and checking the output
"""
import collections
from pathlib import Path
from unittest.mock import Mock, call, sentinel
from pytest import *  # type: ignore

import Chapter_14.ch14_r05


def test_command_iter(tmpdir):
    results = list(
        Chapter_14.ch14_r05.command_iter(tmpdir, files=2)
    )
    expected = [
        [
            'python',
            'Chapter_13/ch13_r05.py',
            '--samples',
            '10',
            '--output',
            tmpdir/ 'game_0.yaml'],
        [
            'python',
            'Chapter_13/ch13_r05.py',
            '--samples',
            '10',
            '--output',
            tmpdir / 'game_1.yaml']
        ]
    assert expected == results

@fixture  # type: ignore
def mock_subprocess_run():
    return Mock(
        side_effect=
            lambda command, stdout, check, text:
                stdout.write("line 0\nline 1\n")
    )

def test_command_output_iter(mock_subprocess_run, monkeypatch, tmpdir):
    monkeypatch.setattr(Chapter_14.ch14_r05.subprocess, 'run', mock_subprocess_run)
    results = list(
        Chapter_14.ch14_r05.command_output_iter(Path(tmpdir), [sentinel.CMD_1, sentinel.CMD_2])
    )
    expected = [
        "line 0", "line 1", "line 0", "line 1"
    ]
    assert expected == results
    assert len(mock_subprocess_run.mock_calls) == 2
    assert mock_subprocess_run.mock_calls[0].args == (sentinel.CMD_1,)
    assert mock_subprocess_run.mock_calls[0].kwargs['check']
    assert mock_subprocess_run.mock_calls[0].kwargs['text']
    assert mock_subprocess_run.mock_calls[1].args == (sentinel.CMD_2,)
    assert mock_subprocess_run.mock_calls[1].kwargs['check']
    assert mock_subprocess_run.mock_calls[1].kwargs['text']


def test_collect_batches():
    expected = [
        collections.Counter([("win", 1), ("win", 2), ("win", 2)]),
        collections.Counter([("loss", 3), ("loss", 4), ("loss", 4)])
    ]
    source = [
        "text",
        str(expected[0]),
        "text",
        str(expected[1]),
        "text",
    ]
    results = list(
        Chapter_14.ch14_r05.collect_batches(source)
    )
    assert expected == results


@fixture  # type: ignore
def mock_command_iter():
    return Mock(return_value=[sentinel.CMD_1, sentinel.CMD_2])


@fixture  # type: ignore
def mock_command_output_iter():
    return Mock(return_value=[sentinel.OUT_1, sentinel.OUT_2])


@fixture  # type: ignore
def mock_collect_batches_iter():
    return Mock(return_value=[[str(sentinel.BATCH_1)], [str(sentinel.BATCH_2)]])


@fixture  # type: ignore
def mock_path(tmpdir):
    return Mock(
        side_effect=lambda p: Path(tmpdir/p)
    )

def test_main(
        mock_command_iter,
        mock_command_output_iter,
        mock_collect_batches_iter,
        mock_path,
        monkeypatch,
        capsys,
        tmpdir):
    monkeypatch.setattr(Chapter_14.ch14_r05, 'command_iter', mock_command_iter)
    monkeypatch.setattr(Chapter_14.ch14_r05, 'command_output_iter', mock_command_output_iter)
    monkeypatch.setattr(Chapter_14.ch14_r05, 'collect_batches', mock_collect_batches_iter)
    monkeypatch.setattr(Chapter_14.ch14_r05, 'Path', mock_path)

    Chapter_14.ch14_r05.summarize(
        directory=Path(tmpdir/"data"),
        games=2,
        temporary=Path(tmpdir/"tmp")
    )

    out, err = capsys.readouterr()
    assert out.splitlines() == [
        "['sentinel.BATCH_1']",
        "['sentinel.BATCH_2']",
        'Total',
        "Counter({'sentinel.BATCH_1': 1, 'sentinel.BATCH_2': 1})"
    ]

    mock_command_iter.assert_has_calls(
        [call(mock_path("data"), 2)]
    )
    mock_command_output_iter.assert_has_calls(
        [call(Path(tmpdir/"tmp"), [sentinel.CMD_1, sentinel.CMD_2])]
    )
    mock_collect_batches_iter.assert_has_calls(
        [call([sentinel.OUT_1, sentinel.OUT_2])]
    )

