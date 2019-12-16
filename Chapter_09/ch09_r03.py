"""Python Cookbook 2nd ed.

Chapter 9, recipe 3.

Note: Output from this is used in Chapter 4 examples.
"""

import re
from pathlib import Path
from pprint import pprint
from typing import Dict, Any, cast, Match

pattern_text = (
    r"\[(?P<date>\d+-\d+-\d+ \d+:\d+:\d+,\d+)\]"
    r"\s+(?P<level>\w+)"
    r"\s+in\s+(?P<module>[\w_\.]+):"
    r"\s+(?P<message>.*)"
)
pattern = re.compile(pattern_text)


def log_parser(source_line: str) -> Dict[str, Any]:
    """
    >>> log_parser("[2019-11-07 11:12:13,098765] info in this.module: example message")
    {'date': '2019-11-07 11:12:13,098765', 'level': 'info', 'module': 'this.module', 'message': 'example message'}
    """
    # match = pattern.match(source_line)
    # if match:
    if match := pattern.match(source_line):
        # Chapter_09/ch09_r03.py:27: error: Item "None" of "Optional[Match[str]]" has no attribute "groupdict"
        # return match.groupdict()
        return cast(Match, match).groupdict()
    raise ValueError(f"Unexpected input {source_line=}")


def raw() -> None:
    data_path = Path("data") / "sample.log"
    with data_path.open() as data_file:
        data_reader = map(log_parser, data_file)
        for row in data_reader:
            pprint(row)


def copy() -> None:
    import csv

    data_path = Path("data") / "sample.log"
    target_path = data_path.with_suffix(".csv")
    with target_path.open("w", newline="") as target_file:
        writer = csv.DictWriter(target_file, ["date", "level", "module", "message"])
        writer.writeheader()

        with data_path.open() as data_file:
            reader = map(log_parser, data_file)
            writer.writerows(reader)


__test__ = {
    "raw": """
>>> raw()
{'date': '2016-06-15 17:57:54,715',
 'level': 'INFO',
 'message': 'Sample Message One',
 'module': 'ch09_r10'}
{'date': '2016-06-15 17:57:54,715',
 'level': 'DEBUG',
 'message': 'Debugging',
 'module': 'ch09_r10'}
{'date': '2016-06-15 17:57:54,715',
 'level': 'WARNING',
 'message': 'Something might have gone wrong',
 'module': 'ch09_r10'}

""",
}

if __name__ == "__main__":
    copy()
