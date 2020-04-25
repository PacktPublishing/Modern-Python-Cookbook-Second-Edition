"""Python Cookbook

Chapter 13, recipe 5. Designing scripts for composition
"""
import yaml
from pytest import *  # type: ignore
import Chapter_13.ch13_r05
import random

def test_roll_iter():
    actual = list(Chapter_13.ch13_r05.roll_iter(12, seed=42))
    expected = [
        [[6, 1]],
        [[1, 6]],
        [[3, 2], [2, 2], [6, 1]],
        [[6, 6]],
        [[5, 1], [5, 4], [1, 1], [1, 2], [2, 5]],
        [[5, 1], [5, 2]],
        [[6, 6]],
        [[6, 5]],
        [[4, 2], [4, 5], [3, 1], [2, 6], [4, 3]],
        [[3, 2], [2, 3]],
        [[1, 1]],
        [[4, 1], [3, 3], [5, 3], [1, 6]]
    ]
    assert expected == actual

def test_craps_game(tmpdir, monkeypatch):
    (tmpdir / "data").mkdir()
    tmp_output_path = tmpdir / "data" / "ch13_r05_test.yaml"
    monkeypatch.setenv("RANDOMSEED", "2")
    options = Chapter_13.ch13_r05.get_options(
        ["--samples", "10", "--output", str(tmp_output_path)]
    )
    face_count = Chapter_13.ch13_r05.write_rolls(
        options.output_path,
        Chapter_13.ch13_r05.roll_iter(options.samples, options.seed),
    )
    assert face_count == {
        8: 8,
        7: 6,
        10: 5,
        4: 3,
        6: 3,
        9: 3,
        2: 2,
        3: 1,
        5: 1,
        11: 1,
        12: 1,
    }
    results = list(
        yaml.load_all(
            tmp_output_path.read_text(encoding="utf-8"), Loader=yaml.SafeLoader
        )
    )
    assert results == [
        [[1, 1]],
        [[1, 3], [2, 6], [6, 3], [3, 5], [2, 5]],
        [[1, 5], [6, 2], [4, 6], [4, 6], [5, 3], [5, 4], [5, 3], [1, 1], [3, 4]],
        [[3, 4]],
        [[4, 5], [2, 5]],
        [[2, 2], [2, 1], [2, 3], [2, 2]],
        [[5, 5], [3, 5], [6, 5], [2, 4], [4, 6]],
        [[5, 3], [5, 3]],
        [[3, 4]],
        [[2, 4], [6, 6], [4, 6], [5, 2]],
    ]
