"""Python Cookbook 2nd ed.

Chapter 10, recipe 7, Reading XML documents

Note: Output from this is used in Chapter 4 examples.
"""

import xml.etree.ElementTree as XML
from pathlib import Path
from typing import cast


def race_summary(source_path: Path) -> None:
    source_text = source_path.read_text(encoding="UTF-8")
    document = XML.fromstring(source_text)

    legs = cast(XML.Element, document.find("legs"))
    teams = cast(XML.Element, document.find("teams"))

    for leg in legs.findall("leg"):
        print(cast(str, leg.text).strip())
        n = leg.attrib["n"]

        for team in teams.findall("team"):
            position_leg = cast(XML.Element, team.find(f"position/leg[@n='{n}']"))
            name = cast(XML.Element, team.find("name"))
            print(cast(str, name.text).strip(), cast(str, position_leg.text).strip())


test_summary = """
>>> race_summary(source_path=Path("data") / "race_result.xml")  # doctest: +ELLIPSIS
ALICANTE - CAPE TOWN
Abu Dhabi Ocean Racing 1
Team Brunel 3
Dongfeng Race Team 2
MAPFRE 7
Team Alvimedica 5
Team SCA 6
Team Vestas Wind 4
...
LORIENT - GOTHENBURG
Abu Dhabi Ocean Racing 5
Team Brunel 2
Dongfeng Race Team 4
MAPFRE 3
Team Alvimedica 1
Team SCA 7
Team Vestas Wind 6

"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
