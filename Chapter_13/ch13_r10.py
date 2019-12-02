"""Python Cookbook

Chapter 13, recipe 10
"""
import subprocess
from pathlib import Path


def make_files(files: int = 100) -> None:
    try:
        for n in range(files):
            filename = f"data/game_{n}.yaml"
            command = [
                "python3",
                "ch13_r05.py",
                "--samples",
                "10",
                "--output",
                filename,
            ]
            subprocess.run(command, check=True)
    except subprocess.CalledProcessError as ex:
        # Remove any files.
        for partial in Path("data").glob("game_*.yaml"):
            partial.unlink()
        raise
