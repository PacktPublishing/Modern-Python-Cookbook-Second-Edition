"""Python Cookbook

Chapter 14, recipe 1, Combining two applications into one
"""
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, call, sentinel
from pytest import *  # type: ignore
import Chapter_14.ch14_r01


def test_summarize_games():
    results = Chapter_14.ch14_r01.summarize_games(10, seed=42)
    expected = {
        ('loss', 1): 2,
        ('loss', 2): 1,
        ('loss', 3): 1,
        ('loss', 5): 2,
        ('win', 1): 3,
        ('win', 2): 1
    }
    assert expected == dict(results)


def test_win_loss():
    raw_stats = {
        ('loss', 1): 2,
        ('loss', 2): 1,
        ('loss', 3): 1,
        ('loss', 5): 2,
        ('win', 1): 3,
        ('win', 2): 1
    }
    results = Chapter_14.ch14_r01.win_loss(raw_stats)
    expected = {'loss': 6, 'win': 4}
    assert expected == dict(results)


@fixture  # type: ignore
def mock_apps():
    raw_stats = {('win', 1): 13}
    mock_summarize_games = Mock(name='summarize_games', return_value=raw_stats)
    mock_win_loss = Mock(name='win_loss', return_value=sentinel.WIN_LOSS)
    mock_time = Mock(name="mock time", perf_counter=Mock(side_effect=[11, 13]))
    return SimpleNamespace(**locals())


def test_simple_composite(mock_apps, monkeypatch, capsys):
    monkeypatch.setattr(Chapter_14.ch14_r01, 'summarize_games', mock_apps.mock_summarize_games)
    monkeypatch.setattr(Chapter_14.ch14_r01, 'win_loss', mock_apps.mock_win_loss)
    monkeypatch.setattr(Chapter_14.ch14_r01, 'time', mock_apps.mock_time)

    Chapter_14.ch14_r01.simple_composite(games=13)

    assert mock_apps.mock_summarize_games.mock_calls == [call(13_000)]
    assert mock_apps.mock_win_loss.mock_calls == [call(mock_apps.raw_stats)]
    out, err = capsys.readouterr()
    assert out.splitlines() == [
        'games 13 rolls 1000',
        f'{sentinel.WIN_LOSS}',
        'serial: 2.00 seconds'
    ]


def test_parallel_composite(mock_apps, monkeypatch, capsys):
    mock_pool = Mock(
        submit=Mock(
            return_value=Mock(
                result=Mock(return_value={('win', 1): 1})))
    )
    mock_pool_context = MagicMock(
        __enter__=Mock(return_value=mock_pool)
    )
    mock_futures = Mock(ProcessPoolExecutor=Mock(return_value=mock_pool_context))
    monkeypatch.setattr(Chapter_14.ch14_r01, 'summarize_games', mock_apps.mock_summarize_games)
    monkeypatch.setattr(Chapter_14.ch14_r01, 'win_loss', mock_apps.mock_win_loss)
    monkeypatch.setattr(Chapter_14.ch14_r01, 'time', mock_apps.mock_time)
    monkeypatch.setattr(Chapter_14.ch14_r01, 'futures', mock_futures)

    Chapter_14.ch14_r01.parallel_composite(games=13, workers=4)

    assert mock_pool.submit.mock_calls == 13*[call(mock_apps.mock_summarize_games, 1_000)]
    assert mock_apps.mock_win_loss.mock_calls == [call(mock_apps.raw_stats)]
    out, err = capsys.readouterr()
    assert out.splitlines() == [
        'games 13 rolls 1000',
        f'{sentinel.WIN_LOSS}',
        'parallel (4): 2.00 seconds'
    ]


def test_get_options():
    options_1 = Chapter_14.ch14_r01.get_options(["-p"])
    assert options_1.parallel
    assert not options_1.serial

    options_1 = Chapter_14.ch14_r01.get_options(["-s"])
    assert options_1.serial
    assert not options_1.parallel
