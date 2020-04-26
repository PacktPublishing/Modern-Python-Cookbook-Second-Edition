"""Python Cookbook

Chapter 13, recipe 1, Finding configuration files.
"""
from pathlib import Path
import collections
from typing import TextIO, Dict, Any, ChainMap


def load_config_file(config_path: Path) -> Dict[str, Any]:
    """Loads a configuration mapping object with contents
    of a given file.

    :param config_path: Path to be read.
    :returns: mapping with configuration parameter values
    """
    # Details omitted.


def get_config() -> ChainMap[str, Any]:
    system_path = Path("/etc") / "profile"
    local_paths = [
        Path.home() / ".bash_profile",
        Path.home() / ".bash_login",
        Path.home() / ".profile",
    ]

    configuration_items = [
        dict(
            some_setting="Default Value",
            another_setting="Another Default",
            some_option="Built-In Choice",
        )
    ]

    if system_path.exists():
        configuration_items.append(
            load_config_file(system_path))

    for config_path in local_paths:
        if config_path.exists():
            configuration_items.append(
                load_config_file(config_path))
            break

    configuration = collections.ChainMap(
        *reversed(configuration_items))
    return configuration
