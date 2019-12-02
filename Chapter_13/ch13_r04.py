"""Python Cookbook

Chapter 13, recipe 4
"""
from pathlib import Path
import platform
from typing import TextIO, Dict, Any


def load_config_file(
    config_file: TextIO, classname: str = "Configuration"
) -> Dict[str, Any]:
    code = compile(config_file.read(), config_file.name, "exec")
    globals = {"__builtins__": __builtins__, "Path": Path, "platform": platform}
    locals: Dict[str, Any] = {}
    exec(code, globals, locals)
    return locals[classname]


import importlib


def load_config_module(name: str) -> Dict[str, Any]:
    module_name, _, class_name = name.rpartition(".")
    settings_module = importlib.import_module(module_name)
    return vars(settings_module)[class_name]


class ConfigMetaclass(type):
    def __repr__(self) -> str:
        name = (
            super().__name__
            + "("
            + ", ".join(b.__name__ for b in super().__bases__)
            + ")"
        )
        base_values = {
            n: v
            for base in reversed(super().__mro__)
            for n, v in vars(base).items()
            if not n.startswith("_")
        }
        values_text = [f"    {name} = {value!r}" for name, value in base_values.items()]
        return "\n".join(["class {name}:"] + values_text)


class Configuration(metaclass=ConfigMetaclass):
    unchanged = "default"
    override = "default"
    feature_override = "default"
    feature = "default"


class Customized(Configuration):
    override = "customized"
    feature_override = "customized"


class Feature_On(Configuration):
    feature = "enabled"
    feature_override = "enabled"


class Config_Feature(Feature_On, Customized):
    local = "local"


__test__ = {
    "load_config_file": """
>>> settings_path = Path('Chapter_13/settings.py')
>>> with settings_path.open() as settings_file:
...     configuration = load_config_file(settings_file, 'Chesapeake')
>>> configuration.__doc__.strip()
'Weather for Cheaspeake Bay'
>>> configuration.query
{'mz': ['ANZ532']}
>>> configuration.url['netloc']
'forecast.weather.gov'
""",
    "load_config": """
>>> configuration = load_config_module('Chapter_13.settings.Chesapeake')
>>> configuration.__doc__.strip()
'Weather for Cheaspeake Bay'
>>> print(configuration)  # doctest: +ELLIPSIS
<class 'Chapter_13.settings.Chesapeake'>
>>> from pprint import pprint
>>> pprint(vars(configuration))
mappingproxy({'__doc__': '\\n    Weather for Cheaspeake Bay\\n    ',
              '__module__': 'Chapter_13.settings',
              'query': {'mz': ['ANZ532']}})
""",
}
