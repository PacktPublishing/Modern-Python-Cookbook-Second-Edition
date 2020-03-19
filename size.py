"""
Size of the book's code base.

Include all non-blank lines in .py files.

Also include all non-blank lines of the examples.txt files.
"""
from pathlib import Path
from typing import Iterator, NamedTuple

class SampleCode(NamedTuple):
    path: Path
    lines: int

def module_iter(base: Path = Path.cwd()) -> Iterator:
    for p in base.glob("Chapter_*/*.py"):
        lines = list(filter(None, p.read_text().splitlines()))
        yield SampleCode(p, len(lines))

def example_iter(base: Path = Path.cwd()) -> Iterator:
    for p in base.glob("Chapter_*/examples.txt"):
        lines = list(filter(None, p.read_text().splitlines()))
        yield SampleCode(p, len(lines))

if __name__ == "__main__":
    book = list(module_iter()) + list(example_iter())
    sample_files = sum(1 for s in book)
    lines_of_code = sum(s.lines for s in book)
    print(f"{lines_of_code:,d} lines of code")
    print(f"{sample_files:,d} files")
