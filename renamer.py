"""
Rename a chapter's examples. This does *not* look inside the files for other changes.
Those are fraught with complexities.
"""
from pathlib import Path
import re
from typing import Callable, Iterator


def glob_rename(base: Path, pattern: str, transform: Callable[[str], str]) -> Iterator[Callable[[], None]]:
    """Emits closures that handle the real work."""
    for path in base.glob(pattern):
        target = Path(transform(str(path)))
        print(f"mv {path} {target}")
        yield lambda: path.rename(target)


def search(base: Path, old_name: str) -> None:
    for path in sorted(base.glob("*")):
        if not path.is_file():
            continue
        with path.open() as source:
            for n, line in enumerate(source, start=1):
                if re.search(old_name, line):
                    print(f"{path.name}:{n:3d}:{line.rstrip()}")


def rename(base: Path, old_name: str, new_name: str, dry_run: bool=True) -> None:
    for c in glob_rename(base, f"{old_name}*", lambda n: n.replace(old_name, new_name)):
        if not dry_run:
            c()
    for c in glob_rename(base, f"test_{old_name}*", lambda n: n.replace(old_name, new_name)):
        if not dry_run:
            c()


if __name__ == "__main__":
    # search(Path.cwd() / "Chapter_12", "ch12")
    # rename(Path.cwd() / "Chapter_12", "ch12", "ch13", dry_run=False)
    # rename(Path.cwd() / "Chapter_11", "ch11", "ch12", dry_run=False)
    # rename(Path.cwd() / "Chapter_10", "ch10", "ch11", dry_run=False)
    # rename(Path.cwd() / "Chapter_09", "ch09", "ch10", dry_run=False)
    # rename(Path.cwd() / "Chapter_08", "ch08", "ch09", dry_run=False)
    # rename(Path.cwd() / "Chapter_07", "ch07", "ch08", dry_run=False)
    # rename(Path.cwd() / "Chapter_06", "ch06", "ch07", dry_run=False)
    rename(Path.cwd() / "Chapter_05", "ch05", "ch06", dry_run=False)

    # TODO:
    # 4B -> 5
    # rename(Path.cwd()/"Chapter_04B", "ch04", "ch05", dry_run=True)

