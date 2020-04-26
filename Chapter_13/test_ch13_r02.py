"""Python Cookbook

Chapter 13, recipe 2, Using YAML for configuration files.
"""
from pathlib import Path
from pytest import *  # type: ignore
import Chapter_13.ch13_r02


config_text = """
query:
  mz:
    - ANZ532
    - AMZ117
    - AMZ080
url:
  scheme: http
  netloc: forecast.weather.gov
  path: shmrn.php
description: >
  Weather forecast for Offshore including the Bahamas
"""


@fixture  # type: ignore
def config_yaml_file(tmpdir):
    filename = tmpdir/"config.yaml"
    filename.write_text(config_text, encoding='utf-8')
    return filename


def test_load_config_simple(config_yaml_file):
    expected = {
        'description': 'Weather forecast for Offshore including the Bahamas\n',
        'query': {'mz': ['ANZ532', 'AMZ117', 'AMZ080']},
        'url': {
            'netloc': 'forecast.weather.gov',
            'path': 'shmrn.php',
            'scheme': 'http'
        }
    }

    config = Chapter_13.ch13_r02.load_config_file(
        Path(config_yaml_file)
    )

    assert expected == config
