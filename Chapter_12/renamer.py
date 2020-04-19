from pathlib import Path
from typing import Callable

def rename(pattern: str, transform: Callable[[str], str]):
    for path in Path.cwd().glob(pattern):
        target = Path(transform(str(path)))
        print(f"mv {path} {target}")
        path.rename(target)

if __name__ == "__main__":
    rename("ch13*", lambda n: n.replace("ch13", "ch12"))
    rename("test_ch13*", lambda n: n.replace("ch13", "ch12"))
