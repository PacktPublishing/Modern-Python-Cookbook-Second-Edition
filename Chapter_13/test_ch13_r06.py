"""Python Cookbook

Chapter 13, recipe 6, Using logging for control and audit output
"""
import logging
from pathlib import Path
from unittest.mock import Mock, call, sentinel
from pytest import *  # type: ignore
import Chapter_13.ch13_r06

def test_get_option(caplog):
    caplog.set_level(logging.DEBUG, logger="overview_stats.detail")
    opts = Chapter_13.ch13_r06.get_options(["-o", "output.yaml", "file1.dat", "file2.dat"])
    assert opts.file == [Path("file1.dat"), Path("file2.dat")]
    assert opts.output == "output.yaml"
    assert caplog.messages == [
        # MacOS/Linux
        # "options: Namespace(file=[PosixPath('file1.dat'), PosixPath('file2.dat')], output='output.csv')"
        # Generic
        f"options: Namespace(file=[{Path('file1.dat')!r}, {Path('file2.dat')!r}], output='output.yaml')"
    ]


def test_main(caplog, monkeypatch, tmpdir):
    # Given mocked functions
    target = tmpdir / "output.yaml"
    mock_get_options = Mock(
        return_value=Mock(output=target, file=[]))
    mock_process_all_files = Mock()

    monkeypatch.setattr(Chapter_13.ch13_r06, 'get_options', mock_get_options)
    monkeypatch.setattr(Chapter_13.ch13_r06, 'process_all_files', mock_process_all_files)
    caplog.set_level(logging.DEBUG, logger="overview_stats.write")

    # When main()
    Chapter_13.ch13_r06.main(sentinel.ARGV)

    # Then get options, process_all_files, and log entry.
    assert mock_get_options.mock_calls == [
        call(sentinel.ARGV)
    ]
    assert len(mock_process_all_files.mock_calls) == 1
    assert caplog.messages == [
        f"wrote {Path(tmpdir)/'output.yaml'!r}"
    ]


def test_process_all_files(caplog, monkeypatch, tmpdir):
    target = tmpdir / "output.yaml"
    source = tmpdir / "source.yaml"
    source.write_text("# source.yaml", encoding='utf-8')
    mock_gather_stats = Mock(return_value={"count": id(sentinel.STATISTICS)})

    monkeypatch.setattr(Chapter_13.ch13_r06, 'gather_stats', mock_gather_stats)
    caplog.set_level(logging.DEBUG, logger="overview_stats.detail")

    Chapter_13.ch13_r06.process_all_files(target, [Path(source)])

    assert len(mock_gather_stats.mock_calls) == 1
    assert target.read_text(encoding='utf-8') == f"---\ncount: {id(sentinel.STATISTICS)}\n"
    assert caplog.messages == [
        f"read {Path(tmpdir)/'source.yaml'!r}"
    ]


def test_gather_stats(caplog, monkeypatch):
    games = [
        [(1, 1)], [(1, 2)], [(6, 6)], [(4, 3)], [(5, 6)],
        [(2, 2), (5, 2)],
        [(2, 3), (2, 4), (4, 1)],
    ]

    caplog.set_level(logging.DEBUG, logger="overview_stats.detail")
    outcome = Chapter_13.ch13_r06.gather_stats(games)

    assert outcome[("win", 1)] == 2
    assert outcome[("win", 3)] == 1
    assert outcome[("loss", 1)] == 3
    assert outcome[("loss", 2)] == 1
    assert caplog.messages == [
        "game [(1, 1)] -> event ('loss', 1)",
        "game [(1, 2)] -> event ('loss', 1)",
        "game [(6, 6)] -> event ('loss', 1)",
        "game [(4, 3)] -> event ('win', 1)",
        "game [(5, 6)] -> event ('win', 1)",
        "game [(2, 2), (5, 2)] -> event ('loss', 2)",
        "game [(2, 3), (2, 4), (4, 1)] -> event ('win', 3)",
    ]
