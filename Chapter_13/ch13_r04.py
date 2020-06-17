"""Python Cookbook

Chapter 13, recipe 4, Using class-as-namespace for configuration values.
"""
from pathlib import Path
import platform
from typing import Dict, Any, Type

ConfigClass = Type[object]

def load_config_file(
        config_path: Path, classname: str = "Configuration"
    ) -> ConfigClass:
    code = compile(
        config_path.read_text(),
        config_path.name,
        "exec")
    globals = {
        "__builtins__": __builtins__,
        "Path": Path,
        "platform": platform}
    locals: Dict[str, ConfigClass] = {}
    exec(code, globals, locals)
    result: ConfigClass = locals[classname]
    return result

def main_1():
    config: Dict[str, Any] = load_config_file("settings.py", "Chesapeake")
    print(config.query)
    print(config.url)


import importlib


def load_config_module(name: str) -> ConfigClass:
    module_name, _, class_name = name.rpartition(".")
    settings_module = importlib.import_module(module_name)
    result: ConfigClass = vars(settings_module)[class_name]
    return result

class ConfigMetaclass(type):
    """Displays a subclass with superclass values injected"""
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
        values_text = [f"class {name}:"] + [
            f"    {name} = {value!r}"
            for name, value in base_values.items()
        ]
        return "\n".join(values_text)


class Configuration(metaclass=ConfigMetaclass):
    unchanged = "default"
    override = "default"
    feature_x_override = "default"
    feature_x = "disabled"


class Customized(Configuration):
    override = "customized"
    feature_x_override = "x-customized"


class Feature_X_On(Configuration):
    feature_x = "enabled"


class Config_Feature_X(Feature_X_On, Customized):
    local = "local"


test_config_customized = """
>>> config1 = Customized
>>> config1.unchanged
'default'
>>> config1.override
'customized'
>>> config1.feature_x
'disabled'
>>> config1.feature_x_override
'x-customized'

>>> print(Customized)
class Customized(Configuration):
    unchanged = 'default'
    override = 'customized'
    feature_x_override = 'x-customized'
    feature_x = 'disabled'
"""

test_config_feature_x = """
>>> config2 = Config_Feature_X
>>> config2.unchanged
'default'
>>> config2.override
'customized'
>>> config2.feature_x
'enabled'
>>> config2.feature_x_override
'x-customized'
>>> config2.local 
'local'
"""

test_display = """
>>> print(Config_Feature_X)
class Config_Feature_X(Feature_X_On, Customized):
    unchanged = 'default'
    override = 'customized'
    feature_x_override = 'x-customized'
    feature_x = 'enabled'
    local = 'local'
"""

__test__ = {
    n: v for n, v in locals().items() if n.startswith("test_")
}
