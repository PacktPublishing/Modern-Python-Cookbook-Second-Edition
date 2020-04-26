"""Python Cookbook

Chapter 13, recipe 2, Using YAML for configuration files.
"""
from pathlib import Path
from typing import Dict, Any
import yaml


def load_config_file(config_path: Path) -> Dict[str, Any]:
    """Loads a configuration mapping object with contents
    of a given file.

    :param config_path: Path to be read.
    :returns: mapping with configuration parameter values
    """
    with config_path.open() as config_file:
        document = yaml.load(
            config_file, Loader=yaml.SafeLoader)
    return document


# Further Examples.
# Uses of UnsafeLoader

class Card:
    def __init__(self, rank: int, suit: str) -> None:
        self.rank = rank
        self.suit = suit

    def __repr__(self) -> str:
        return f"{self.rank} {self.suit}"


card_text = """
!!python/object/apply:Chapter_13.ch13_r02.Card
kwds:
    rank: 7
    suit: ♣︎
"""


test_load_card = """
>>> yaml.load(card_text, Loader=yaml.UnsafeLoader)
7 ♣︎
"""

import collections

od_text = """
!!python/object/apply:collections.OrderedDict
args:
    -   !!omap
        -   key1: string value
        -   numerator: 355
        -   denominator: 113
"""

test_load_OrderedDict = """
>>> yaml.load(od_text, Loader=yaml.UnsafeLoader)
OrderedDict([('key1', 'string value'), ('numerator', 355), ('denominator', 113)])

"""

__test__ = {
    n: v for n, v in locals().items() if n.startswith("test_")
}
