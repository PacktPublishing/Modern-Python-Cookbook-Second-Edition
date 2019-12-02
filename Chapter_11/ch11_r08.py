"""Python Cookbook 2nd ed.

Chapter 11, recipe 8. Dates.
"""
from typing import Any

import datetime
import json
from pathlib import Path


def save_data(base: Path, some_payload: Any) -> None:
    now_date = datetime.datetime.utcnow()
    now_text = now_date.strftime("extract_%Y%m%d%H%M%S")
    file_path = (base / now_text).with_suffix(".json")
    with file_path.open("w") as target_file:
        json.dump(some_payload, target_file, indent=2)
