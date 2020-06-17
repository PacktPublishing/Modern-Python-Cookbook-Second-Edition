"""Python Cookbook

Chapter 14, recipe 6, Controlling complex sequences of steps.
"""
import argparse
import subprocess
from unittest.mock import Mock, call
from pytest import *  # type: ignore

import Chapter_14.ch14_r06

@fixture  # type: ignore
def mock_subprocess_run():
    return Mock(
        return_value=Mock(
            stdout = "sample output\n"
        )
    )

def test_command(mock_subprocess_run, monkeypatch):
    monkeypatch.setattr(Chapter_14.ch14_r06.subprocess, 'run', mock_subprocess_run)
    options = argparse.Namespace(name="mock_options")

    cmd = Chapter_14.ch14_r06.Command()
    output = cmd.execute(options)

    assert output == "sample output\n"
    mock_subprocess_run.assert_called_once_with(
        ["echo", "Command", repr(options)],
        check=True, stdout=subprocess.PIPE, text=True
    )


def test_simulate(mock_subprocess_run, monkeypatch):
    monkeypatch.setattr(Chapter_14.ch14_r06.subprocess, 'run', mock_subprocess_run)
    options = argparse.Namespace(name="mock_options", samples=42, game_file="game_file.yaml")

    cmd = Chapter_14.ch14_r06.Simulate()
    output = cmd.execute(options)

    assert output == "sample output\n"
    mock_subprocess_run.assert_called_once_with(
        ["python",
         "Chapter_13/ch13_r05.py",
         "--samples", "42",
         "-o", "game_file.yaml"],
        check=True, stdout=subprocess.PIPE, text=True
    )


def test_summarize(mock_subprocess_run, monkeypatch):
    monkeypatch.setattr(Chapter_14.ch14_r06.subprocess, 'run', mock_subprocess_run)
    options = argparse.Namespace(name="mock_options", samples=42, game_files=["game_file.yaml"], summary_file="summary_file.yaml")

    cmd = Chapter_14.ch14_r06.Summarize()
    output = cmd.execute(options)

    assert output == "sample output\n"
    mock_subprocess_run.assert_called_once_with(
        ["python",
         "Chapter_13/ch13_r06.py",
         "-o", "summary_file.yaml",
         "game_file.yaml"
         ],
        check=True, stdout=subprocess.PIPE, text=True
    )


@fixture  # type: ignore
def mock_simulate():
    mock_simulate_class = Mock(
        return_value=Mock(
            name="Simulate instance",
            execute=Mock(
                return_value='simulate output')))
    return mock_simulate_class


@fixture  # type: ignore
def mock_summarize():
    mock_summarize_class = Mock(
        return_value=Mock(
            name="Summarize instance",
            execute=Mock(
                return_value='summarize output')))
    return mock_summarize_class


def test_iterative_sim(mock_simulate, mock_summarize, monkeypatch):
    monkeypatch.setattr(Chapter_14.ch14_r06, 'Simulate', mock_simulate)
    monkeypatch.setattr(Chapter_14.ch14_r06, 'Summarize', mock_summarize)

    options_i = argparse.Namespace(simulations=2, samples=100, summary_file="data/y12.yaml")
    iteration = Chapter_14.ch14_r06.IterativeSimulate()
    iteration.execute(options_i)

    mock_simulate.assert_called_once_with()
    mock_simulate.return_value.execute.assert_has_calls(
        [call(options_i), call(options_i)]
    )
    mock_summarize.assert_called_once_with()
    mock_summarize.return_value.execute.assert_has_calls(
        [call(options_i)]
    )


def test_condition_sum(mock_simulate, mock_summarize, monkeypatch):
    monkeypatch.setattr(Chapter_14.ch14_r06, 'Simulate', mock_simulate)
    monkeypatch.setattr(Chapter_14.ch14_r06, 'Summarize', mock_summarize)

    options_c = argparse.Namespace(simulations=2, samples=100, game_file="data/x.yaml")
    conditional = Chapter_14.ch14_r06.ConditionalSummarize()
    conditional.execute(options_c)

    mock_simulate.assert_called_once_with()
    mock_simulate.return_value.execute.assert_has_calls(
        [call(options_c)]
    )
    mock_summarize.assert_not_called()
