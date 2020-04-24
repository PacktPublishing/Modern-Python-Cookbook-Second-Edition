"""Python Cookbook 2nd ed.

Chapter 4, recipe 7, Using set methods and operators
"""

import ast
from pathlib import Path
from pprint import pprint
from typing import Any, List, Tuple, Iterator, Set, cast

class ImportVisitor(ast.NodeVisitor):
    def __init__(self, module: str) -> None:
        self.module = module
        self.imports: Set[str] = set()
    def visit_Import(self, node: ast.Import) -> Any:
        if isinstance(node.names, list):
            # print(f"  import {[n.name for n in node.names]}")
            self.imports.union(set(n.name for n in node.names))
        else:
            # print(f"  import {node.names.name}")
            self.imports.add(cast(ast.alias, node.names).name)
    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        if isinstance(node.names, list):
            # print(f"  from {node.module} import {[n.name for n in node.names]}")
            pass
        else:
            # print(f"  from {node.module} import {node.names.name}")
            pass
        if node.module:
            self.imports.add(node.module)

def get_imports(base: Path = Path.cwd()) -> Iterator[Tuple[str, List[str]]]:
    for module in base.glob("**/*.py"):
        if any(parent.name.startswith('.') for parent in module.parents):
            continue
        tree = ast.parse(module.read_text(), module.name, type_comments=True)
        # print(module.stem)
        iv = ImportVisitor(f"{module.parent.name}.{module.stem}")
        iv.visit(tree)
        yield (iv.module, sorted(iv.imports))

if __name__ == "__main__":
    import_details = list(get_imports(Path("Chapter_12")))
    modules = set(module for module, imports in import_details)
    examples = set(module for module in modules if '.ch12_' in module)
    print(examples)
    other = modules - examples
    print(other)

    example_details = [(m, i) for m, i in import_details if m in examples]
    pprint(sorted(example_details))

    other_detials = [(m, i) for m, i in import_details if m in other]
    pprint(sorted(other_detials))

    reused = set()
    for module, imports in import_details:
        if module in examples:
            for depends_on in imports:
                if depends_on in modules:
                    print(f"module {module} depends on {depends_on}")
                    reused.add(depends_on)
    print(reused)

test_add_example = """
>>> import_details = [
... ('Chapter_12.ch12_r01', ['typing', 'pathlib']),
... ('Chapter_12.ch12_r02', ['typing', 'pathlib']),
... ('Chapter_12.ch12_r03', ['typing', 'pathlib']),
... ('Chapter_12.ch12_r04', ['typing', 'pathlib']),
... ('Chapter_12.ch12_r05', ['typing', 'pathlib']),
... ('Chapter_12.ch12_r06', ['typing', 'textwrap', 'pathlib']),
... ('Chapter_12.ch12_r07',
...  ['typing', 'Chapter_12.ch12_r06', 'Chapter_12.ch12_r05', 'concurrent']),
... ('Chapter_12.ch12_r08', ['typing', 'argparse', 'pathlib']),
... ('Chapter_12.ch12_r09', ['typing', 'pathlib']),
... ('Chapter_12.ch12_r10', ['typing', 'pathlib']),
... ('Chapter_12.ch12_r11', ['typing', 'pathlib']),
... ('Chapter_12.ch12_r12', ['typing', 'argparse'])
... ]
>>> all_imports = set()
>>> for item, import_list in import_details:
...    for name in import_list:
...       all_imports.add(name)
>>> print(all_imports)  # doctest: +SKIP
>>> sorted(all_imports)
['Chapter_12.ch12_r05', 'Chapter_12.ch12_r06', 'argparse', 'concurrent', 'pathlib', 'textwrap', 'typing']
"""

test_set_comprehension = """
>>> import_details = [
... ('Chapter_12.ch12_r01', ['typing', 'pathlib']),
... ('Chapter_12.ch12_r02', ['typing', 'pathlib']),
... ('Chapter_12.ch12_r03', ['typing', 'pathlib']),
... ('Chapter_12.ch12_r04', ['typing', 'pathlib']),
... ('Chapter_12.ch12_r05', ['typing', 'pathlib']),
... ('Chapter_12.ch12_r06', ['typing', 'textwrap', 'pathlib']),
... ('Chapter_12.ch12_r07',
...  ['typing', 'Chapter_12.ch12_r06', 'Chapter_12.ch12_r05', 'concurrent']),
... ('Chapter_12.ch12_r08', ['typing', 'argparse', 'pathlib']),
... ('Chapter_12.ch12_r09', ['typing', 'pathlib']),
... ('Chapter_12.ch12_r10', ['typing', 'pathlib']),
... ('Chapter_12.ch12_r11', ['typing', 'pathlib']),
... ('Chapter_12.ch12_r12', ['typing', 'argparse'])
... ]
>>> all_imports = {name
...     for item, import_list in import_details
...         for name in import_list 
... }
>>> sorted(all_imports)
['Chapter_12.ch12_r05', 'Chapter_12.ch12_r06', 'argparse', 'concurrent', 'pathlib', 'textwrap', 'typing']

>>> all_imports = set(name
...     for item, import_list in import_details
...         for name in import_list 
... )
>>> all_imports  # doctest: +SKIP
{'Chapter_12.ch12_r05', 'Chapter_12.ch12_r06', 'argparse', 'concurrent', 'pathlib', 'textwrap', 'typing'}
>>> sorted(all_imports)
['Chapter_12.ch12_r05', 'Chapter_12.ch12_r06', 'argparse', 'concurrent', 'pathlib', 'textwrap', 'typing']

"""


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
