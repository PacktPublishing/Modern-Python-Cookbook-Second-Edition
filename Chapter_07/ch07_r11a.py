"""Python Cookbook 2nd ed.

Chapter 7, recipe 11a, Using contexts and context managers
This (and related recipes) are part of Chapter 7, Recipe 11.

FileFacts(name=PosixPath('anscome_json.py'), modified='2019-11-08T16:24:50.834272', size=993, checksum='ab8cea15584ffbe17eb3763205cae947')
FileFacts(name=PosixPath('hint_game.py'), modified='2016-03-16T14:36:20', size=1152, checksum='43b9119fb44ba26be022ba11928b33ad')

"""
from pathlib import Path

import datetime
from hashlib import md5

# from types import SimpleNamespace as FileFacts
from typing import NamedTuple


class FileFacts(NamedTuple):
    name: Path
    modified: str
    size: int
    checksum: str


def file_facts(path: Path) -> FileFacts:
    return FileFacts(
        name=path,
        modified=datetime.datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
        size=path.stat().st_size,
        checksum=md5(path.read_bytes()).hexdigest(),
    )


if __name__ == "__main__":
    summary_path = Path("data/summary.dat")
    with summary_path.open("w") as summary_file:

        base = Path.cwd()
        for member in base.glob("Chapter_*/*.py"):
            print(file_facts(member), file=summary_file)

    with summary_path.open() as summary_file:
        for line in summary_file:
            print(line.rstrip())
