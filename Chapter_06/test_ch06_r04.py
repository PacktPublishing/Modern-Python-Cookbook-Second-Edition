"""Python Cookbook 2nd ed.

Chapter 6, recipe 4, Using argparse to get command-line input

The test cases need to be kept separate from the main processing
of the ch06_r04 module.
"""

from pytest import *  # type: ignore
from Chapter_06 import ch06_r04


def test_main_good(capsys):
    ch06_r04.main(["-u", "KM", "36.12,-86.67", "33.94,-118.40"])
    out, err = capsys.readouterr()
    assert out.splitlines() == ["From 36.12,-86.67 to 33.94,-118.4 in KM = 2887.35"]


def test_main_bad(capsys):
    with raises(SystemExit):
        ch06_r04.main(["-u", "KM", "36.12,-86.67", "33.94,-118asd"])
    out, err = capsys.readouterr()
    assert out == ""
    assert err.splitlines() == [
        "usage: pytest [-h] [-u {NM,MI,KM}] p1 p2",
        "pytest: error: argument p2: could not convert string to float: '-118asd'",
    ]
