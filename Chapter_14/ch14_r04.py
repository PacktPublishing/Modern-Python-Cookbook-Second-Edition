"""Python Cookbook

Chapter 14, recipe 4, Wrapping and combining CLI applications

This uses an explicit `python` command
so Chapter_13/ch13_r05.py does not have to be marked executable.
"""
import argparse
from pathlib import Path
import subprocess
import sys
from typing import List, Optional


def get_options(
        argv: Optional[List[str]] = None
) -> argparse.Namespace:
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("games", type=int)
    options = parser.parse_args(argv)
    return options


def make_files(directory: Path, files: int = 100) -> None:
    """Create sample data files."""
    for n in range(files):
        filename = directory / f"game_{n}.yaml"
        command = [
            "python",  # Can be removed if the app is executable
            "Chapter_13/ch13_r05.py",
            "--samples",
            "10",
            "--output",
            str(filename),
        ]
        subprocess.run(command, check=True)


def make_files_clean(directory: Path, files: int = 100) -> None:
    """Create sample data files, with cleanup after a failure."""
    try:
        make_files(directory, files)
    except subprocess.CalledProcessError as ex:
        # Remove any files.
        for partial in directory.glob("game_*.yaml"):
            partial.unlink()
        raise


def main() -> None:
    options = get_options()
    make_files_clean(options.directory, options.games)


if __name__ == "__main__":
    main()
