"""Python Cookbook 2nd ed.

Chapter 2, recipe 9
"""

from pathlib import Path
import shutil
import os


def version1(source_file_path: Path, target_file_path: Path) -> None:
    shutil.copy(source_file_path, target_file_path)


def version2(source_file_path: Path, target_file_path: Path) -> None:
    try:
        target_file_path.parent.mkdir(exist_ok=True, parents=True)
        shutil.copy(source_file_path, target_file_path)
    except OSError as ex:
        print(ex)


if __name__ == "__main__":
    source_path = Path(
        "~/Documents/Writing/Python/Python Cookbook 2e/Code"
    ).expanduser()
    target_path = Path("~/Dropbox/B05442-2e/Code/").expanduser()
    patterns = "Chapter_*/*.py", "Chapter_*/*.txt", "Chapter_*/*.yaml", "data/*"
    for glob_pattern in patterns:
        for source_file_path in source_path.glob(glob_pattern):
            source_file_detail = source_file_path.relative_to(source_path)
            target_file_path = target_path / source_file_detail
            print(f"Moving {source_file_detail} to {target_file_path}")
            version2(source_file_path, target_file_path)
