"""Python Cookbook 2nd ed.

Chapter 10, recipe 8, Reading HTML documents

Parse the HTML file and produce the JSON and XML files.
"""
from bs4 import BeautifulSoup  # type: ignore
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple


def null_int(text: str) -> Optional[int]:
    if text:
        return int(text)
    return None

def race_extract_spike(source_path: Path) -> Dict[str, Any]:
    """Initial race extract ignoring data-title complexity."""
    with source_path.open(encoding="utf8") as source_file:
        soup = BeautifulSoup(source_file, "html.parser")

    thead_row = soup.table.thead.tr
    legs: List[Tuple[str, Optional[str]]] = []
    for tag in thead_row.find_all("th"):
        leg_description = tag.string, tag.attrs.get("data-title")
        legs.append(leg_description)

    tbody = soup.table.tbody
    teams: List[Dict[str, Any]] = []
    for row in tbody.find_all("tr"):
        team: Dict[str, Any] = {"name": None, "position": []}
        for col in row.find_all("td"):
            if "ranking-team" in col.attrs.get("class"):
                team["name"] = col.string
            elif "ranking-number" in col.attrs.get("class"):
                team["position"].append(col.string)
            elif "data-title" in col.attrs:
                # Complicated explanation with nested HTML
                # print(col.attrs, col.string)
                pass
            else:
                # Unclear what this is; here's some debugging output
                # print(col.attrs, col.string)
                pass
        teams.append(team)

    document = {
        "legs": legs,
        "teams": teams,
    }
    return document

test_race_extract_spike = """
>>> from pprint import pprint
>>> document = race_extract_spike(Path.cwd() / "data" / "Volvo Ocean Race.html")
>>> pprint(document)
{'legs': [(None, None),
          ('LEG 1', '<strong>ALICANTE - CAPE TOWN</strong>'),
          ('LEG 2', '<strong>CAPE TOWN - ABU DHABI</strong>'),
          ('LEG 3', '<strong>ABU DHABI - SANYA</strong>'),
          ('LEG 4', '<strong>SANYA - AUCKLAND</strong>'),
          ('LEG 5', '<strong>AUCKLAND - ITAJAÍ</strong>'),
          ('LEG 6', '<strong>ITAJAÍ - NEWPORT</strong>'),
          ('LEG 7', '<strong>NEWPORT - LISBON</strong>'),
          ('LEG 8', '<strong>LISBON - LORIENT</strong>'),
          ('LEG 9', '<strong>LORIENT - GOTHENBURG</strong>'),
          ('TOTAL', None)],
 'teams': [{'name': 'Abu Dhabi Ocean Racing',
            'position': ['1', '3', '2', '2', '1', '2', '5', '3', '5', '24']},
           {'name': 'Team Brunel',
            'position': ['3', '1', '5', '5', '4', '3', '1', '5', '2', '29']},
           {'name': 'Dongfeng Race Team',
            'position': ['2', '2', '1', '3', None, '1', '4', '7', '4', None]},
           {'name': 'MAPFRE',
            'position': ['7', '4', '4', '1', '2', '4', '2', '4', '3', None]},
           {'name': 'Team Alvimedica',
            'position': ['5', None, '3', '4', '3', '5', '3', '6', '1', '34']},
           {'name': 'Team SCA',
            'position': ['6', '6', '6', '6', '5', '6', '6', '1', '7', None]},
           {'name': 'Team Vestas Wind',
            'position': ['4',
                         None,
                         None,
                         None,
                         None,
                         None,
                         None,
                         '2',
                         '6',
                         '60']}]}
"""


def clean_leg(text: str) -> str:
    leg_soup = BeautifulSoup(text, "html.parser")
    return leg_soup.text


def get_legs(soup: BeautifulSoup) -> List[str]:
    """Creates legs by appending to a list."""
    legs = []
    thead = soup.table.thead.tr
    for tag in thead.find_all('th'):
        if 'data-title' in tag.attrs:
            leg_description_text = clean_leg(tag.attrs['data-title'])
            legs.append(leg_description_text)
    return legs


def get_legs_comprehension(soup: BeautifulSoup) -> List[str]:
    """Creates leg"""
    thead = soup.table.thead.tr
    legs = [
        clean_leg(tag.attrs['data-title'])
          for tag in thead.find_all('th')
            if 'data-title' in tag.attrs
    ]
    return legs


def race_extract(source_path: Path) -> Dict[str, Any]:
    with source_path.open(encoding="utf8") as source_file:
        soup = BeautifulSoup(source_file, "html.parser")

    legs: List[str] = []
    thead = soup.table.thead.tr
    for tag in thead.find_all("th"):
        if "data-title" in tag.attrs:
            leg_description_text = clean_leg(tag.attrs["data-title"])
            legs.append(leg_description_text)
        else:
            # Hard to parse -- here's some debugging output
            # print(tag.attrs, tag.string)
            pass

    teams: List[Dict[str, Any]] = []
    tbody = soup.table.tbody
    for row in tbody.find_all("tr"):
        team: Dict[str, Any] = {"name": None, "position": []}
        for col in row.find_all("td"):
            if "ranking-team" in col.attrs.get("class"):
                team["name"] = col.string
            elif "ranking-number" in col.attrs.get("class"):
                team["position"].append(null_int(col.string))
            else:
                # Hard to parse -- here's some debugging output
                # print(col.attrs, col.string)
                pass
        # Totals may be included.
        team["position"] = team["position"][: len(legs)]
        teams.append(team)

    document = {
        "legs": legs,
        "teams": teams,
    }
    return document


test_get_legs = """
>>> source_path = Path.cwd() / "data" / "Volvo Ocean Race.html"
>>> with source_path.open(encoding="utf8") as source_file:
...     soup = BeautifulSoup(source_file, "html.parser")
>>> get_legs(soup)
['ALICANTE - CAPE TOWN', 'CAPE TOWN - ABU DHABI', 'ABU DHABI - SANYA', 'SANYA - AUCKLAND', 'AUCKLAND - ITAJAÍ', 'ITAJAÍ - NEWPORT', 'NEWPORT - LISBON', 'LISBON - LORIENT', 'LORIENT - GOTHENBURG']
>>> get_legs_comprehension(soup)
['ALICANTE - CAPE TOWN', 'CAPE TOWN - ABU DHABI', 'ABU DHABI - SANYA', 'SANYA - AUCKLAND', 'AUCKLAND - ITAJAÍ', 'ITAJAÍ - NEWPORT', 'NEWPORT - LISBON', 'LISBON - LORIENT', 'LORIENT - GOTHENBURG']

"""

def show_json(document: Dict[str, Any]) -> None:
    import json

    print(json.dumps(document, indent=2))


def show_xml(document: Dict[str, Any]) -> None:
    from xml.etree import ElementTree as XML

    xml_document = XML.Element("results")
    legs_xml = XML.SubElement(xml_document, "legs")
    for n, leg in enumerate(document["legs"], start=1):
        leg_xml = XML.SubElement(legs_xml, "leg", n=str(n))
        leg_xml.text = leg

    teams_xml = XML.SubElement(xml_document, "teams")
    for team in document["teams"]:
        team_xml = XML.SubElement(teams_xml, "team")
        name_xml = XML.SubElement(team_xml, "name")
        name_xml.text = team["name"]
        position_xml = XML.SubElement(team_xml, "position")
        for n, position in enumerate(team["position"], start=1):
            leg_xml = XML.SubElement(position_xml, "leg", n=str(n))
            leg_xml.text = str(position)

    pi = XML.ProcessingInstruction("xml", 'version="1.0"')
    XML.dump(pi)
    XML.dump(xml_document)


test_show_json = """
>>> document = race_extract(Path.cwd() / "data" / "Volvo Ocean Race.html")
>>> show_json(document)
{
  "legs": [
    "ALICANTE - CAPE TOWN",
    "CAPE TOWN - ABU DHABI",
    "ABU DHABI - SANYA",
    "SANYA - AUCKLAND",
    "AUCKLAND - ITAJA\\u00cd",
    "ITAJA\\u00cd - NEWPORT",
    "NEWPORT - LISBON",
    "LISBON - LORIENT",
    "LORIENT - GOTHENBURG"
  ],
  "teams": [
    {
      "name": "Abu Dhabi Ocean Racing",
      "position": [
        1,
        3,
        2,
        2,
        1,
        2,
        5,
        3,
        5
      ]
    },
    {
      "name": "Team Brunel",
      "position": [
        3,
        1,
        5,
        5,
        4,
        3,
        1,
        5,
        2
      ]
    },
    {
      "name": "Dongfeng Race Team",
      "position": [
        2,
        2,
        1,
        3,
        null,
        1,
        4,
        7,
        4
      ]
    },
    {
      "name": "MAPFRE",
      "position": [
        7,
        4,
        4,
        1,
        2,
        4,
        2,
        4,
        3
      ]
    },
    {
      "name": "Team Alvimedica",
      "position": [
        5,
        null,
        3,
        4,
        3,
        5,
        3,
        6,
        1
      ]
    },
    {
      "name": "Team SCA",
      "position": [
        6,
        6,
        6,
        6,
        5,
        6,
        6,
        1,
        7
      ]
    },
    {
      "name": "Team Vestas Wind",
      "position": [
        4,
        null,
        null,
        null,
        null,
        null,
        null,
        2,
        6
      ]
    }
  ]
}
"""

test_show_xml = """
>>> document = race_extract(Path.cwd() / "data" / "Volvo Ocean Race.html")
>>> show_xml(document)
<?xml version="1.0"?>
<results><legs><leg n="1">ALICANTE - CAPE TOWN</leg><leg n="2">CAPE TOWN - ABU DHABI</leg><leg n="3">ABU DHABI - SANYA</leg><leg n="4">SANYA - AUCKLAND</leg><leg n="5">AUCKLAND - ITAJAÍ</leg><leg n="6">ITAJAÍ - NEWPORT</leg><leg n="7">NEWPORT - LISBON</leg><leg n="8">LISBON - LORIENT</leg><leg n="9">LORIENT - GOTHENBURG</leg></legs><teams><team><name>Abu Dhabi Ocean Racing</name><position><leg n="1">1</leg><leg n="2">3</leg><leg n="3">2</leg><leg n="4">2</leg><leg n="5">1</leg><leg n="6">2</leg><leg n="7">5</leg><leg n="8">3</leg><leg n="9">5</leg></position></team><team><name>Team Brunel</name><position><leg n="1">3</leg><leg n="2">1</leg><leg n="3">5</leg><leg n="4">5</leg><leg n="5">4</leg><leg n="6">3</leg><leg n="7">1</leg><leg n="8">5</leg><leg n="9">2</leg></position></team><team><name>Dongfeng Race Team</name><position><leg n="1">2</leg><leg n="2">2</leg><leg n="3">1</leg><leg n="4">3</leg><leg n="5">None</leg><leg n="6">1</leg><leg n="7">4</leg><leg n="8">7</leg><leg n="9">4</leg></position></team><team><name>MAPFRE</name><position><leg n="1">7</leg><leg n="2">4</leg><leg n="3">4</leg><leg n="4">1</leg><leg n="5">2</leg><leg n="6">4</leg><leg n="7">2</leg><leg n="8">4</leg><leg n="9">3</leg></position></team><team><name>Team Alvimedica</name><position><leg n="1">5</leg><leg n="2">None</leg><leg n="3">3</leg><leg n="4">4</leg><leg n="5">3</leg><leg n="6">5</leg><leg n="7">3</leg><leg n="8">6</leg><leg n="9">1</leg></position></team><team><name>Team SCA</name><position><leg n="1">6</leg><leg n="2">6</leg><leg n="3">6</leg><leg n="4">6</leg><leg n="5">5</leg><leg n="6">6</leg><leg n="7">6</leg><leg n="8">1</leg><leg n="9">7</leg></position></team><team><name>Team Vestas Wind</name><position><leg n="1">4</leg><leg n="2">None</leg><leg n="3">None</leg><leg n="4">None</leg><leg n="5">None</leg><leg n="6">None</leg><leg n="7">None</leg><leg n="8">2</leg><leg n="9">6</leg></position></team></teams></results>
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
