"""Python Cookbook

Chapter 12, recipe 3, Using class-as-namespace for configuration values
"""
from pathlib import Path
from textwrap import dedent
from pytest import *  # type: ignore
import Chapter_12.ch12_r04


def test_load_config_file():
    settings_path = Path('Chapter_12/settings.py')
    configuration = Chapter_12.ch12_r04.load_config_file(
        settings_path, 'Chesapeake')
    assert configuration.__doc__.strip() == 'Weather for Chesapeake Bay'
    assert configuration.query == {'mz': ['ANZ532']}
    assert configuration.url['netloc'] == 'forecast.weather.gov'


def test_load_config_module():
    configuration = Chapter_12.ch12_r04.load_config_module('Chapter_12.settings.Chesapeake')
    assert configuration.__doc__.strip() == 'Weather for Chesapeake Bay'
    assert str(configuration) == "<class 'Chapter_12.settings.Chesapeake'>"
    assert dict(vars(configuration)) == {
        '__doc__': '\n    Weather for Chesapeake Bay\n    ',
        '__module__': 'Chapter_12.settings',
        'query': {'mz': ['ANZ532']}
    }
