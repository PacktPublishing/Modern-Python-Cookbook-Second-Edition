"""Python Cookbook

Chapter 13, recipe 3, Using Python for configuration files
"""

from pathlib import Path
from typing import Dict, Any, cast


def load_config_file(config_path: Path) -> Dict[str, Any]:
    """Loads a configuration mapping object with contents
    of a given file.

    :param config_path: Path to be read.
    :returns: mapping with configuration parameter values
    """
    code = compile(
        config_path.read_text(),
        config_path.name,
        "exec")
    locals: Dict[str, Any] = {}
    exec(code, {"__builtins__": __builtins__}, locals)
    return locals


from pathlib import Path
import platform
import os
import sys

def load_config_file_xtra(config_path: Path) -> Dict[str, Any]:
    """Loads a configuration mapping object with contents
    of a given file. The execution context includes a selected
    portion of the standard library, include the :class:`pathlib.Path` class.

    :param config_path: Path to be read.
    :returns: mapping with configuration parameter values
    """
    def not_allowed(*arg, **kw) -> None:
        raise RuntimeError("Operation not allowed")

    code = compile(
        config_path.read_text(),
        config_path.name,
        "exec")
    safe_builtins = cast(Dict[str, Any], __builtins__).copy()
    for name in ("eval", "exec", "compile", "__import__"):
        safe_builtins[name] = not_allowed
    globals = {
        "__builtins__": safe_builtins,
        "Path": Path,
        "platform": platform,
        "environ": os.environ.copy(),
    }
    locals: Dict[str, Any] = {}
    exec(code, globals, locals)
    return locals


__test__ = {
    n: v for n, v in locals().items() if n.startswith("test_")
}
