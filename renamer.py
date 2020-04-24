"""
Rename a chapter's examples. This does *not* look inside the files for other changes.
Those are fraught with complexities.
"""
from pathlib import Path
from typing import Callable

def glob_rename(base: Path, pattern: str, transform: Callable[[str], str]):
    for path in base.glob(pattern):
        target = Path(transform(str(path)))
        print(f"mv {path} {target}")
        path.rename(target)

def rename(base: Path, old_name: str, new_name: str) -> None:
    glob_rename(base, f"{old_name}*", lambda n: n.replace(old_name, new_name))
    glob_rename(base, f"test_{old_name}*", lambda n: n.replace(old_name, new_name))

if __name__ == "__main__":
    rename(Path.cwd()/"Chapter_04B", "ch04", "ch05")
    # rename(Path.cwd()/"Chapter_12", "ch12", "ch13")

