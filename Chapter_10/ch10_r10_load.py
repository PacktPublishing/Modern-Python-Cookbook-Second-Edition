"""Python Cookbook 2nd ed.

Chapter 10, recipe 10. Mocking external resources like databases or the cloud
Database Load Module.
"""

from pathlib import Path
import re
import os
from typing import TextIO, Iterator, Dict, Any, Match, cast

log_pattern = re.compile(
    r"\[(?P<timestamp>.*?)\]"
    r"\s(?P<levelname>\w+)"
    r"\sin\s(?P<module>[\w\._]+):"
    r"\s(?P<message>.*)"
)


def extract_row_iter(source_log_file: TextIO) -> Iterator[Dict[str, str]]:
    for line in source_log_file:
        if (match := log_pattern.match(line)) is not None:
            yield cast(Match, match).groupdict()


import datetime

LOG_FORMAT = "%Y-%m-%d %H:%M:%S,%f"


def cleanse(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    >>> cleanse({'timestamp':'2016-06-15 17:57:54,715'})
    {'timestamp': '2016-06-15T17:57:54.715000'}
    """
    date = datetime.datetime.strptime(row["timestamp"], LOG_FORMAT)
    row["timestamp"] = date.isoformat()
    return row


def log_data_iter(source_path: Path) -> Iterator[Dict[str, Any]]:
    with source_path.open() as source_file:
        raw_iter = extract_row_iter(source_file)
        clean_iter = (cleanse(r) for r in raw_iter)
        yield from clean_iter


def demo_log_reader():
    from pprint import pprint
    from pathlib import Path

    source_path = Path("data") / "data_load.log"
    for row in log_data_iter(source_path):
        pprint(row)


import base64
import urllib.request
import json


class ElasticClient:
    service = "https://api.orchestrate.io"

    def __init__(self, api_key: str, password: str="") -> None:
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization":
                ElasticClient.basic_header(api_key, password),
        }

    @staticmethod
    def basic_header(username: str, password: str="") -> str:
        """
        >>> ElasticClient.basic_header('Aladdin', 'OpenSesame')
        'Basic QWxhZGRpbjpPcGVuU2VzYW1l'
        """
        combined_bytes = f"{username}:{password}".encode("utf-8")
        encoded_bytes = base64.b64encode(combined_bytes)
        return "Basic " + encoded_bytes.decode("ascii")

    def load_eventlog(self, data_document: Dict[str, Any]) -> Dict[str, str]:
        request = urllib.request.Request(
            url=self.service + "/v0/eventlog",
            headers=self.headers,
            method="POST",
            data=json.dumps(data_document).encode("utf-8"),
        )

        with urllib.request.urlopen(request) as response:
            assert response.status == 201, f"Insertion Error: {response.status}"
            response_headers = dict(response.getheaders())
            return response_headers["Location"]

    def query_eventlog(self) -> Dict[str, Any]:
        request = urllib.request.Request(
            url=self.service + "/v0/eventlog", headers=self.headers, method="GET",
        )

        with urllib.request.urlopen(request) as response:
            assert response.status == 200, f"Query Error: {response.status}"
            body = response.read().decode("utf-8")
            data = json.loads(body)
        return data



from pprint import pprint


def main() -> None:
    from pathlib import Path

    api_key = os.environ["CH10_API_KEY"]
    client = ElasticClient(api_key)
    source_path = Path("data") / "ch09_r10.log"
    for row in log_data_iter(source_path):
        client.load_eventlog(row)
    history = client.query_eventlog()
    pprint(history["results"])

def query() -> None:
    api_key = os.environ["CH10_API_KEY"]
    client = ElasticClient(api_key)
    history = client.query_eventlog()
    for item in history["results"]:
        print(item["value"])

if __name__ == "__main__":
    main()
    query()
