"""Python Cookbook

Chapter 13, recipe 3, Using Python for configuration files
"""
from pathlib import Path
from textwrap import dedent
from pytest import *  # type: ignore
import Chapter_13.ch13_r03


@fixture  # type: ignore
def settings_py_file(tmpdir):
    filename = tmpdir/"settings.py"
    content = dedent('''
    """Weather forecast for Offshore including the Bahamas
    """
    query = {'mz': ['ANZ532', 'AMZ117', 'AMZ080']}
    url = {
      'scheme': 'http',
      'netloc': 'forecast.weather.gov',
      'path': '/shmrn.php'
    }
    ''')
    filename.write_text(content, encoding='utf-8')
    return filename

def test_load_config_file(settings_py_file):
    settings = Chapter_13.ch13_r03.load_config_file(Path(settings_py_file))
    expected = {
        '__doc__': 'Weather forecast for Offshore including the Bahamas\n',
        'query': {'mz': ['ANZ532', 'AMZ117', 'AMZ080']},
        'url': {
            'netloc': 'forecast.weather.gov',
            'path': '/shmrn.php',
            'scheme': 'http'}}
    assert expected == settings


@fixture  # type: ignore
def settings_extra_py_file(tmpdir):
    filename = tmpdir/"settings.py"
    content = dedent('''
    """Config with related paths"""
    if environ.get("APP_ENV", "production"):
        base = Path('/var/app/')
    else:
        base = Path.cwd("var")
    log = base/'log'
    out = base/'out'
    ''')
    filename.write_text(content, encoding='utf-8')
    return filename

def test_load_config_file_path(settings_extra_py_file):
    settings = Chapter_13.ch13_r03.load_config_file_xtra(Path(settings_extra_py_file))
    expected = {
        '__doc__': 'Config with related paths',
        'base': Path('/var/app'),
        'log': Path('/var/app/log'),
        'out': Path('/var/app/out')}
    assert expected == settings



@fixture  # type: ignore
def settings_invalid_py_file(tmpdir):
    filename = tmpdir/"settings.py"
    content = dedent('''
    """Config with related paths"""
    import os
    exec("os.system('shutdown')")
    ''')
    filename.write_text(content, encoding='utf-8')
    return filename

def test_load_config_file_invalid(settings_invalid_py_file):
    with raises(RuntimeError) as exc_info:
        settings = Chapter_13.ch13_r03.load_config_file_xtra(Path(settings_invalid_py_file))
    assert exc_info.type == RuntimeError
    assert exc_info.value.args == ("Operation not allowed",)

