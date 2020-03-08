"""Python Cookbook 2nd ed.

Chapter 9, recipe c.

Note: Output from this is used in Chapter 4 examples.
"""
import logging
from logging import Formatter
from pathlib import Path
from typing import Dict, Any, Iterator, TextIO, Counter


def create_log() -> None:
    PROD_LOG_FORMAT = "[{asctime}] {levelname} in {module}: {message}"
    sample_log_path = Path("data") / "ch09_r10.log"
    with sample_log_path.open("w") as sample_log_file:
        logging.basicConfig(stream=sample_log_file, level=logging.DEBUG)
        logger = logging.getLogger("")
        for handler in logger.handlers:
            handler.setFormatter(Formatter(PROD_LOG_FORMAT, style="{"))

        logger.info("Sample Message One")
        logger.debug("Debugging")
        logger.warning("Something might have gone wrong")
        logging.shutdown()
    print(f"Wrote {sample_log_path}")


import re
from pathlib import Path
import csv

log_pattern = re.compile(
    r"\[(?P<timestamp>.*?)\]"
    r"\s(?P<levelname>\w+)"
    r"\sin\s(?P<module>[\w\._]+):"
    r"\s(?P<message>.*)"
)


def extract_row_iter(source_log_file: TextIO) -> Iterator[Dict[str, Any]]:
    for line in source_log_file:
        match = log_pattern.match(line)
        if match is None:
            continue
        yield match.groupdict()


def parse_log() -> None:
    summary_path = Path("data") / "summary_log.csv"
    with summary_path.open("w") as summary_file:

        writer = csv.DictWriter(
            summary_file, ["timestamp", "levelname", "module", "message"]
        )
        writer.writeheader()

        source_log_dir = Path("data")
        for source_log_path in source_log_dir.glob("*.log"):
            with source_log_path.open() as source_log_file:
                writer.writerows(extract_row_iter(source_log_file))

            print("Converted", source_log_path, "to", summary_path)


def counting_extract_row_iter(
    counts: Counter, source_log_file: TextIO
) -> Iterator[Dict[str, Any]]:
    for line in source_log_file:
        match = log_pattern.match(line)
        if match is None:
            counts["non-match"] += 1
            continue
        counts["valid"] += 1
        yield match.groupdict()


import collections


def parse_log2() -> None:
    summary_path = Path("data") / "summary_log.csv"
    with summary_path.open("w") as summary_file:

        writer = csv.DictWriter(
            summary_file, ["timestamp", "levelname", "module", "message"]
        )
        writer.writeheader()

        source_log_dir = Path("data")
        for source_log_path in source_log_dir.glob("*.log"):
            counts: Counter[str] = collections.Counter()
            with source_log_path.open() as source_log_file:
                writer.writerows(counting_extract_row_iter(counts, source_log_file))

            print("Converted", source_log_path, "to", summary_path)
            print(counts)


__test__ = {
    "example1": """
The log was written separately; we can't create logs with pytest -- it captures them for us.

>>> parse_log2()
Converted data/write.log to data/summary_log.csv
Counter({'non-match': 21})
Converted data/extra_detail.log to data/summary_log.csv
Counter({'non-match': 1})
Converted data/sample.log to data/summary_log.csv
Counter({'valid': 3})
Converted data/ch09_r10.log to data/summary_log.csv
Counter({'valid': 3})
""",
}


if __name__ == "__main__":
    create_log()
    parse_log2()
